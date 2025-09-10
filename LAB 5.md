LAB 5

nums = list(map(int, input("Введи список чисел через пробел: ").split()))
print("Исходный список:", nums)

print("Обратный порядок:", nums[::-1])

print("Сортировка по abs:", sorted(nums, key=abs, reverse=True))

nums[0], nums[-1] = nums[-1], nums[0]
print("После обмена первым и последним:", nums)
