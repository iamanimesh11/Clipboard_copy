.py"""
lg_kb_rag.py

Single-file pipeline:
- Load docs (PDF/txt)
- Chunk using LangChain text splitters
- Create embeddings (OpenAI or local sentence-transformers)
- Build FAISS vectorstore
- Expose FastAPI endpoint /ask for retrieval + LLM summarization

Adapt paths and provider choices to your infra.
"""
import os
import typing as t
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- Choose embedding provider ---
# Option A: OpenAI embeddings (recommended for quality)
USE_OPENAI_EMBEDDINGS = True

# Option B: Local sentence-transformer (no external API cost)
USE_LOCAL_EMBEDDINGS = False

# --- LangChain & vectorstore imports ---
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

if USE_OPENAI_EMBEDDINGS:
    from langchain.embeddings import OpenAIEmbeddings
else:
    from sentence_transformers import SentenceTransformer
    from langchain.embeddings import HuggingFaceEmbeddings

from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# ---------- Config ----------
DOCS_DIR = Path("./docs")        # put your PDFs/texts here
VECTORSTORE_PATH = Path("./faiss_index")
CHUNK_SIZE = 800                 # characters ~ adjust: 500-1200 typical
CHUNK_OVERLAP = 150
TOP_K = 4                        # number of chunks to retrieve
OPENAI_TEMPERATURE = 0.0

# ---------- FastAPI app ----------
app = FastAPI(title="LG Internal KB RAG")

class AskRequest(BaseModel):
    user_id: t.Optional[str] = None
    question: str

class AskResponse(BaseModel):
    answer: str
    source_chunks: t.List[str]

# ---------- Utility: Load documents ----------
def load_documents_from_dir(docs_dir: Path) -> t.List[Document]:
    documents: t.List[Document] = []
    for path in docs_dir.iterdir():
        if path.suffix.lower() in [".pdf"]:
            loader = PyPDFLoader(str(path))
            docs = loader.load()
            documents.extend(docs)
        elif path.suffix.lower() in [".txt", ".md"]:
            loader = TextLoader(str(path), encoding="utf-8")
            docs = loader.load()
            documents.extend(docs)
        else:
            # skip other types or add custom loaders (Word, HTML, Confluence export, etc.)
            continue
    return documents

# ---------- Utility: Chunk documents ----------
def chunk_documents(documents: t.List[Document],
                    chunk_size: int = CHUNK_SIZE,
                    chunk_overlap: int = CHUNK_OVERLAP) -> t.List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = splitter.split_documents(documents)
    return chunks

# ---------- Build or load vectorstore ----------
def build_vectorstore(chunks: t.List[Document], persist_path: Path) -> FAISS:
    # choose embeddings
    if USE_OPENAI_EMBEDDINGS:
        emb = OpenAIEmbeddings()
    else:
        hf_model = SentenceTransformer("all-MiniLM-L6-v2")
        emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", embedding=hf_model)

    # create FAISS index
    db = FAISS.from_documents(chunks, emb)
    # persist locally
    persist_path.mkdir(parents=True, exist_ok=True)
    db.save_local(str(persist_path))
    return db

def load_vectorstore(persist_path: Path) -> FAISS:
    if not persist_path.exists():
        raise FileNotFoundError("Vectorstore not found. Run indexing step first.")
    if USE_OPENAI_EMBEDDINGS:
        emb = OpenAIEmbeddings()
    else:
        hf_model = SentenceTransformer("all-MiniLM-L6-v2")
        emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", embedding=hf_model)
    db = FAISS.load_local(str(persist_path), embedding=emb)
    return db

# ---------- Create the QA chain ----------
def create_qa_chain(vectorstore: FAISS) -> RetrievalQA:
    retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})
    llm = OpenAI(temperature=OPENAI_TEMPERATURE)
    # Custom prompt to enforce grounding and short answers
    template = """
You are LG Assist — an internal knowledge assistant for LG employees.
Answer the user's question using ONLY the provided documents (do not invent facts).
If the answer is not present, say: "I could not find the information in the documents. Please check with the team."
Give a concise, step-by-step answer and include helpful links if present in the sources.

Question: {question}

Documents:
{context}

Answer in up to 300 words:
"""
    prompt = PromptTemplate(input_variables=["context", "question"], template=template)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",          # simple: stuffs retrieved docs into the prompt
        chain_type_kwargs={"prompt": prompt}
    )
    return qa_chain

# ---------- Indexing endpoint (run once to index docs) ----------
@app.post("/index")
def index_docs():
    docs = load_documents_from_dir(DOCS_DIR)
    if not docs:
        raise HTTPException(status_code=400, detail="No documents found in docs/ directory.")
    print(f"Loaded {len(docs)} source documents.")
    chunks = chunk_documents(docs)
    print(f"Created {len(chunks)} chunks.")
    db = build_vectorstore(chunks, VECTORSTORE_PATH)
    return {"status": "indexed", "chunks": len(chunks)}

# ---------- Ask endpoint (used by Angular frontend) ----------
@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question is empty")

    try:
        db = load_vectorstore(VECTORSTORE_PATH)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Knowledge base not indexed. Call /index first.")

    qa = create_qa_chain(db)
    # Run the chain
    answer = qa.run(question)

    # Also return the raw top-k chunk texts (sources) for transparency (optional)
    retriever = db.as_retriever(search_kwargs={"k": TOP_K})
    docs = retriever.get_relevant_documents(question)
    source_chunks = [d.page_content for d in docs]

    return AskResponse(answer=answer, source_chunks=source_chunks)

# ---------- Simple health endpoint ----------
@app.get("/health")
def health():
    return {"status": "ok"}

# ---------- CLI support ----------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", action="store_true", help="Index documents into vectorstore")
    parser.add_argument("--run", action="store_true", help="Run FastAPI server")
    args = parser.parse_args()

    if args.index:
        docs = load_documents_from_dir(DOCS_DIR)
        print(f"Loaded {len(docs)} docs")
        chunks = chunk_documents(docs)
        print(f"Chunks: {len(chunks)}")
        build_vectorstore(chunks, VECTORSTORE_PATH)
        print("Indexing complete.")
    if args.run:
        import uvicorn
        uvicorn.run("lg_kb_rag:app", host="0.0.0.0", port=8000, reload=False)
