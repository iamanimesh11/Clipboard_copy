def insertAtBottom(stack, item):
    # Base case: if stack is empty, push item
    if not stack:
        stack.append(item)
        return
    # Otherwise, pop top and recurse
    top = stack.pop()
    insertAtBottom(stack, item)
    # Push top back
    stack.append(top)

def reverseStack(stack):
    # Base case
    if not stack:
        return
    # Pop top element
    top = stack.pop()
    # Reverse remaining stack
    reverseStack(stack)
    # Insert popped element at the bottom
    insertAtBottom(stack, top)

# Example usage
stack = [1, 2, 3, 4]
print("Original stack:", stack)
reverseStack(stack)
print("Reversed stack:", stack)