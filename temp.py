def examples(n):
    if n==0:
        print("base case reached")
        return
    print("before recursion:",n)
    examples(n-1)
    print("after recursion:",n)
    
examples(3)
