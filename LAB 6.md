LAB 6
import random

# === Задание 1 ===
# Создаем массив A(50) из случайных целых чисел (-20 ... 20)
A = [random.randint(-20, 20) for _ in range(50)]
print("Исходный массив A:")
print(A)

for i in range(len(A)):
    if A[i] > 0:           # если элемент положительный
        A[i] = i           # заменить его на индекс
    if A[i] > 10:          # если элемент больше 10
        A[i] -= 2          # уменьшить на 2

print("\nПреобразованный массив A:")
print(A)


# === Задание 2 ===
# Создаем двумерный массив A(4,4)
B = [[random.randint(-20, 20) for _ in range(4)] for _ in range(4)]
print("\nДвумерный массив B:")
for row in B:
    print(row)

# Главная диагональ — элементы B[i][i]
diagonal = [B[i][i] for i in range(4)]
min_elem = min(diagonal)

print("\nЭлементы главной диагонали:", diagonal)
print("Наименьший элемент диагонали:", min_elem)
