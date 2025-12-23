Perfect topic — advanced S3 bucket policy conditions are very exam-heavy.
I’ll give you only the conditions that actually matter, with when to use them.


---

🔐 Advanced S3 Bucket Policy Conditions (Exam-Focused)

Bucket policies = JSON + conditions
Conditions answer WHEN access is allowed or denied.


---

1️⃣ Enforce HTTPS only (🔥 MOST COMMON)

Condition

"Condition": {
  "Bool": {
    "aws:SecureTransport": "false"
  }
}

Meaning

❌ Deny all HTTP
✅ Allow only HTTPS

Exam clue

> “Ensure data is accessed securely”



👉 THIS CONDITION


---

2️⃣ Restrict by IP Address

Condition

"Condition": {
  "IpAddress": {
    "aws:SourceIp": "203.0.113.0/24"
  }
}

Meaning

Only allow requests from a specific IP range


Exam clue

> “Only allow access from corporate network”




---

3️⃣ Enforce SSE-KMS encryption on upload

Condition

"Condition": {
  "StringEquals": {
    "s3:x-amz-server-side-encryption": "aws:kms"
  }
}

Meaning

Users must use SSE-KMS

Rejects:

Unencrypted uploads

SSE-S3 uploads



Exam clue

> “Ensure all uploaded objects are encrypted with KMS”




---

4️⃣ Enforce specific KMS key

Condition

"Condition": {
  "StringEquals": {
    "s3:x-amz-server-side-encryption-aws-kms-key-id":
    "arn:aws:kms:region:account-id:key/key-id"
  }
}

Meaning

Forces usage of one specific CMK


Exam clue

> “Use only customer-managed KMS key”




---

5️⃣ Deny public access

Condition

"Condition": {
  "StringEquals": {
    "aws:PrincipalType": "Anonymous"
  }
}

(Usually paired with Effect: Deny)

Meaning

Blocks anonymous/public users


Exam clue

> “Prevent public access to bucket”




---

6️⃣ Restrict access to a specific VPC Endpoint

Condition

"Condition": {
  "StringEquals": {
    "aws:sourceVpce": "vpce-123456"
  }
}

Meaning

Access allowed only via VPC endpoint

No internet access


Exam clue

> “Private access from VPC only”




---

7️⃣ Restrict by AWS account or organization

Condition

"Condition": {
  "StringEquals": {
    "aws:PrincipalAccount": "123456789012"
  }
}

OR

"Condition": {
  "StringEquals": {
    "aws:PrincipalOrgID": "o-abc123xyz"
  }
}

Meaning

Only trusted accounts / org can access


Exam clue

> “Allow access only from same AWS Organization”




---

8️⃣ MFA-protected access (rare but exam-valid)

Condition

"Condition": {
  "Bool": {
    "aws:MultiFactorAuthPresent": "true"
  }
}

Meaning

Requires MFA to access S3


Exam clue

> “Sensitive data, MFA required”




---

🆚 QUICK EXAM CHEAT TABLE

Requirement in Question	Condition Key

HTTPS only	aws:SecureTransport
Corporate IP	aws:SourceIp
Enforce SSE-KMS	s3:x-amz-server-side-encryption
Enforce CMK	s3:x-amz-server-side-encryption-aws-kms-key-id
VPC-only access	aws:sourceVpce
Org-only access	aws:PrincipalOrgID
MFA required	aws:MultiFactorAuthPresent



---

🧠 Exam Golden Rule (VERY IMPORTANT)

> Security enforcement = DENY with conditions



Most strong bucket policies:

Use Effect: Deny

Then apply conditions


Why?
👉 Explicit deny always wins


---

🧠 One-Line Exam Answer

> Advanced S3 bucket policy conditions control when access is allowed, such as enforcing HTTPS, IP restrictions, KMS encryption, VPC endpoints, and MFA.




---

If you want next:

Full bucket policy with 3 conditions combined

Tricky exam MCQ

Bucket policy vs IAM policy confusion cleared