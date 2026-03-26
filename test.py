a = [1,5,2,6,3,7,4]
n = len(a)
#bubble sort
def bubble_sort(arr):
     for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
     return arr

# insertion sort
def insertion_sort(arr):
    for i in range(1, n):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

#merge sort
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

#timsort
def tim_sort(arr):
    arr.sort()
    return arr

#time complexity
# Bubble Sort: O(n^2)
# Insertion Sort: O(n^2)
# Merge Sort: O(n log n)
# Timsort: O(n log n) in the worst case, O(n) in the best case (when the array is already sorted)
def two_sum(nums, target):
    d = {}
    for i, num in enumerate(nums):
        print(f"Current number: {num}, Index: {i}")
        if target - num in d:
            print(f"Found a pair: {num} and {target - num} at indices {i} and {d[target - num]}")
            return [d[target - num], i]
        d[num] = i
        print(f"Dictionary state: {d}")
    print("No pair found that sums to the target.")

from collections import Counter
def count_words(words):
    return Counter(words)

def remove_duplicates(arr):
    return list(dict.fromkeys(arr))

if __name__ == "__main__": 
    # print("Sorting algorithms implemented successfully.")
    # print("Sorted array using bubble sort:", bubble_sort(a))
    # print("Sorted array using insertion sort:", insertion_sort(a))
    # print("Sorted array using merge sort:", merge_sort(a))
    # print("Sorted array using timsort:", tim_sort(a))
    # print("Two sum result:", two_sum(a, 5))
    # words = ["apple", "banana", "apple", "orange", "banana", "apple"]
    # print("Word count:", count_words(words))
    arr_with_duplicates = ["apple", "banana", "apple", "orange", "banana", "apple"]
    print("Array with duplicates removed:", remove_duplicates(arr_with_duplicates))