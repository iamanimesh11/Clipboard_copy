def bubble_sort_optimized(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # 🚀 If no swaps happened, stop early
        if not swapped:
            print(f"✅ Stopped early at i = {i}, array already sorted!")
            break
    return arr