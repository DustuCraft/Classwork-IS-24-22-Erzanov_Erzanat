"""
Система расчёта итоговой оценки студента
"""
import logging
import json
import os
from typing import List, Union

# Настройка логирования
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)


class GradeCalculator:
    """Класс для расчёта и определения оценок студента"""

    MIN_GRADE = 0
    MAX_GRADE = 100

    GRADE_SCALE = {
        'A': 90,
        'B': 80,
        'C': 70,
        'D': 60,
        'F': 0
    }

    @staticmethod
    def validate_grades(grades: List[Union[int, float]]) -> None:
        """
        Валидирует список оценок

        Args:
            grades: Список оценок

        Raises:
            ValueError: Если список пуст или оценки вне допустимого диапазона
            TypeError: Если оценки не являются числами
        """
        if not grades:
            logging.error("Попытка обработать пустой список оценок")
            raise ValueError("Список оценок не может быть пустым")

        if not all(isinstance(grade, (int, float)) for grade in grades):
            logging.error(f"Некорректный тип данных в списке: {grades}")
            raise TypeError("Все оценки должны быть числами (int или float)")

        for grade in grades:
            if not (GradeCalculator.MIN_GRADE <= grade <= GradeCalculator.MAX_GRADE):
                logging.error(f"Оценка вне диапазона: {grade}")
                raise ValueError(
                    f"Оценка должна быть в диапазоне "
                    f"{GradeCalculator.MIN_GRADE}-{GradeCalculator.MAX_GRADE}"
                )

    @staticmethod
    def calculate_average(grades: List[Union[int, float]]) -> float:
        """
        Вычисляет средний балл

        Args:
            grades: Список оценок

        Returns:
            Средний балл, округлённый до 2 знаков
        """
        GradeCalculator.validate_grades(grades)
        avg = sum(grades) / len(grades)
        logging.info(f"Средний балл рассчитан: {avg:.2f} для оценок {grades}")
        return round(avg, 2)

    @staticmethod
    def determine_grade_letter(average: Union[int, float]) -> str:
        """
        Определяет буквенную оценку на основе среднего балла

        Args:
            average: Средний балл

        Returns:
            Буквенная оценка (A, B, C, D, F)

        Raises:
            ValueError: Если средний балл вне допустимого диапазона
        """
        if not isinstance(average, (int, float)):
            logging.error(f"Некорректный тип для среднего балла: {type(average)}")
            raise TypeError("Средний балл должен быть числом")

        if not (GradeCalculator.MIN_GRADE <= average <= GradeCalculator.MAX_GRADE):
            logging.error(f"Средний балл вне диапазона: {average}")
            raise ValueError(
                f"Средний балл должен быть в диапазоне "
                f"{GradeCalculator.MIN_GRADE}-{GradeCalculator.MAX_GRADE}"
            )

        for letter, threshold in GradeCalculator.GRADE_SCALE.items():
            if average >= threshold:
                logging.info(f"Определена оценка '{letter}' для среднего балла {average}")
                return letter

        return 'F'

    @staticmethod
    def generate_student_report(name: str, grades: List[Union[int, float]]) -> dict:
        """
        Формирует итоговый отчёт студента

        Args:
            name: Имя студента
            grades: Список оценок

        Returns:
            Словарь с информацией об успеваемости студента
        """
        if not name or not isinstance(name, str):
            logging.error(f"Некорректное имя студента: {name}")
            raise ValueError("Имя студента должно быть непустой строкой")

        avg = GradeCalculator.calculate_average(grades)
        letter = GradeCalculator.determine_grade_letter(avg)

        report = {
            'name': name.strip(),
            'grades': grades,
            'average': avg,
            'letter_grade': letter,
            'total_subjects': len(grades),
            'max_grade': max(grades),
            'min_grade': min(grades)
        }

        logging.info(f"Создан отчёт для студента '{name}': {letter} ({avg})")
        return report

    @staticmethod
    def format_report(report: dict) -> str:
        """
        Форматирует отчёт для вывода

        Args:
            report: Словарь с данными отчёта

        Returns:
            Отформатированная строка отчёта
        """
        return f"""
{'=' * 50}
ОТЧЁТ ОБ УСПЕВАЕМОСТИ
{'=' * 50}
Студент: {report['name']}
Количество предметов: {report['total_subjects']}
Оценки: {', '.join(map(str, report['grades']))}
{'=' * 50}
Средний балл: {report['average']}
Максимальная оценка: {report['max_grade']}
Минимальная оценка: {report['min_grade']}
{'=' * 50}
ИТОГОВАЯ ОЦЕНКА: {report['letter_grade']}
{'=' * 50}
"""


def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return []


def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def show_menu():
    print("\nМеню:")
    print("1. Добавить/изменить оценки студенту")
    print("2. Удалить студента")
    print("3. Редактировать студента")
    print("4. Удалить оценку")
    print("5. Сохранить изменения")
    print("6. Показать всех студентов")
    print("0. Выйти")
    return input("Выберите действие: ").strip()


def main():
    FILENAME = 'students_grades.json'
    data = load_data(FILENAME)
    while True:
        choice = show_menu()
        if choice == '1':
            name = input("Имя студента: ").strip()
            grades_input = input("Оценки через пробел: ").strip()
            grades = [float(x) for x in grades_input.split()]
            found = False
            for student in data:
                if student['name'] == name:
                    student['grades'] = grades
                    found = True
                    break
            if not found:
                data.append({'name': name, 'grades': grades})
            print(f"Оценки для {name} обновлены.")
        elif choice == '2':
            name = input("Имя студента для удаления: ").strip()
            data = [s for s in data if s['name'] != name]
            print(f"Студент {name} удалён.")
        elif choice == '3':
            name = input("Имя студента для редактирования: ").strip()
            for student in data:
                if student['name'] == name:
                    new_name = input("Новое имя: ").strip()
                    student['name'] = new_name
                    print(f"Имя изменено на {new_name}.")
                    break
            else:
                print("Студент не найден.")
        elif choice == '4':
            name = input("Имя студента: ").strip()
            for student in data:
                if student['name'] == name:
                    print(f"Текущие оценки: {student['grades']}")
                    idx = int(input("Номер оценки для удаления (начиная с 1): ")) - 1
                    if 0 <= idx < len(student['grades']):
                        del student['grades'][idx]
                        print("Оценка удалена.")
                    else:
                        print("Некорректный номер.")
                    break
            else:
                print("Студент не найден.")
        elif choice == '5':
            save_data(FILENAME, data)
            print("Изменения сохранены.")
        elif choice == '6':
            if not data:
                print("Нет студентов.")
            for student in data:
                print(f"{student['name']}: {student['grades']}")
        elif choice == '0':
            break
        else:
            print("Некорректный выбор.")

if __name__ == "__main__":
    main()