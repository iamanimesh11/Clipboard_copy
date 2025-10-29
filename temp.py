def quick_sort(arr):
    if len(arr)<=1:
        return arr
    
    pivot = arr[len(arr) // 2]  # Choosing the middle element as pivot
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left)+middle+quick_sort(right)
my_array = [5,1,2,8,4]
sorted_array = quick_sort(my_array)
print(f"Original array: {my_array}")
print(f"Sorted array: {sorted_array}")
print("HURRAY!!!!")
