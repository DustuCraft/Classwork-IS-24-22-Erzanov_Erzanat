def binary_search(arr, left, right, x):
    if right >= left:
        mid = left + (right - left) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return binary_search(arr, left, mid - 1, x)
        else:
            return binary_search(arr, mid + 1, right, x)
    else:
        return -1

arr = [1, 3, 5, 7, 9, 11]
x = 7
result = binary_search(arr, 0, len(arr)-1, x)
if result != -1:
    print("Элемент найден на позиции:", result)
else:
    print("Элемент не найден в массиве")
