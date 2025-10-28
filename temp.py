def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        # 1️⃣ Recursively sort both halves
        merge_sort(left_half)
        merge_sort(right_half)
        # 2️⃣ Merge them back
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
        # 3️⃣ Copy remaining elements
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
    return arr
    
my_array = [5,1,4,2,8]
sorted_array = merge_sort(my_array)
print(f"Original array: {my_array}")
print(f"Sorted array: {sorted_array}")
print("HURRAY!!!!")
