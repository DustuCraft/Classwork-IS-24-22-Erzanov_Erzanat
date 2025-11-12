import math
import datetime

# Файлы для записи
RESULT_FILE = "result.txt"
ERROR_FILE = "errors.log"

def log_error(message):
    """Логирование ошибок в файл"""
    with open(ERROR_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} - ERROR - {message}\n")

def calculate_compound_interest(P, r, t, n=12):
    """Расчёт суммы по формуле сложных процентов"""
    if P <= 0 or r <= 0 or t <= 0 or n <= 0:
        raise ValueError("Все значения должны быть положительными.")
    S = P * (1 + r / n) ** (n * t)
    return S

def main():
    try:
        print("Практическое задание\n")

        # Ввод данных
        P = float(input("Введите сумму вклада: "))
        r = float(input("Введите годовую ставку (%): "))
        t = float(input("Введите срок вклада (в годах): "))

        # Проверка входных значений
        if P <= 0 or r <= 0 or t <= 0:
            raise ValueError("Все значения должны быть положительными.")

        # Перевод ставки в доли
        r = r / 100

        # Расчёт
        S = calculate_compound_interest(P, r, t)

        print(f"\nИтоговая сумма через {t:.0f} лет: {S:.2f} тенге")
        print("Работа программы завершена.")

        # Запись результата в файл
        with open(RESULT_FILE, "w", encoding="utf-8") as file:
            file.write(f"Вклад: {P} тг\n")
            file.write(f"Ставка: {r * 100:.1f}%\n")
            file.write(f"Срок: {t} лет\n")
            file.write(f"Итоговая сумма: {S:.2f} тг\n")

    except ValueError as e:
        print(f"Ошибка при расчете: {e}")
        log_error(f"Ошибка при расчете: {e}")

    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        log_error(f"Непредвиденная ошибка: {e}")

    finally:
        print("\nПрограмма завершена.\n")

if __name__ == "__main__":
    main()