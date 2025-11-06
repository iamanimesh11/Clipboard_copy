def count_Even(arr,count):
    print(f"arr,calling {arr}")
    if not arr:
        return 
    if len(arr)==1 and arr[0]%2==0:
        count+=1
        return
    print(arr)
    print(count)
    if arr[0]%2==0:
        count+=1
    return count_Even(arr[1:],count)
arr=[2,4,3,5,8]
count=0
x=count_Even(arr,count)
print(x)
