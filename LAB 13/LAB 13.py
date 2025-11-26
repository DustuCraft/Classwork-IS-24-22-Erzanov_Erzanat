import re
import json
import os

# ===== Безопасные функции ввода ===== #

def safe_choice(prompt, choices):
    while True:
        value = input(prompt).strip()
        if value in choices:
            return value
        print(f"Ошибка! Введите один из вариантов: {', '.join(choices)}")

def safe_text(prompt, allow_empty=False):
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("Ошибка! Строка не может быть пустой.")

def safe_number(prompt, allow_float=False):
    while True:
        raw = input(prompt).strip()
        if raw == "0":
            return 0  # вернуть 0 для выхода из подменю
        match = re.search(r"\d+(\.\d+)?", raw)
        if match:
            number = match.group()
            if "." in number and allow_float:
                return float(number)
            return int(float(number))
        print("Ошибка! Введите число (например: 20, 20 лет, 3.5 gpa).")


# ===== Классы ===== #

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_info(self):
        return f"Имя: {self.name}, Возраст: {self.age}"

    def to_dict(self):
        return {"type": "Person", "name": self.name, "age": self.age}

    @staticmethod
    def from_dict(data):
        return Person(data["name"], data["age"])

class Student(Person):
    def __init__(self, name, age, group, gpa):
        super().__init__(name, age)
        self.group = group
        self.gpa = gpa

    def display_info(self):
        return f"Студент: {self.name}, Возраст: {self.age}, Группа: {self.group}, GPA: {self.gpa}"

    def to_dict(self):
        return {"type": "Student", "name": self.name, "age": self.age,
                "group": self.group, "gpa": self.gpa}

    @staticmethod
    def from_dict(data):
        return Student(data["name"], data["age"], data["group"], data["gpa"])

class Teacher(Person):
    def __init__(self, name, age, subject, experience):
        super().__init__(name, age)
        self.subject = subject
        self.experience = experience

    def display_info(self):
        return f"Преподаватель: {self.name}, Возраст: {self.age}, Предмет: {self.subject}, Стаж: {self.experience} лет"

    def to_dict(self):
        return {"type": "Teacher", "name": self.name, "age": self.age,
                "subject": self.subject, "experience": self.experience}

    @staticmethod
    def from_dict(data):
        return Teacher(data["name"], data["age"], data["subject"], data["experience"])

class AdminStaff(Person):
    def __init__(self, name, age, position, department):
        super().__init__(name, age)
        self.position = position
        self.department = department

    def display_info(self):
        return f"Админ-персонал: {self.name}, Возраст: {self.age}, Должность: {self.position}, Отдел: {self.department}"

    def to_dict(self):
        return {"type": "AdminStaff", "name": self.name, "age": self.age,
                "position": self.position, "department": self.department}

    @staticmethod
    def from_dict(data):
        return AdminStaff(data["name"], data["age"], data["position"], data["department"])


# ===== Работа с файлом ===== #

FILENAME = "people.json"

def save_to_file(people):
    data = [p.to_dict() for p in people]
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_from_file():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r", encoding="utf-8") as f:
        data = json.load(f)
    people = []
    for item in data:
        t = item.get("type")
        if t == "Student":
            people.append(Student.from_dict(item))
        elif t == "Teacher":
            people.append(Teacher.from_dict(item))
        elif t == "AdminStaff":
            people.append(AdminStaff.from_dict(item))
        else:
            people.append(Person.from_dict(item))
    return people


# ===== Главное меню ===== #

people = load_from_file()
print(f"Загружено {len(people)} человек из файла.")

while True:
    print("\nМеню:")
    print("1 — Добавить человека")
    print("2 — Редактировать человека")
    print("3 — Удалить человека")
    print("4 — Показать всех людей")
    print("5 — Поиск")
    print("0 — Выход")

    choice = safe_choice("Выберите пункт: ", ["0","1","2","3","4","5"])

    if choice == "0":
        save_to_file(people)
        print("Данные сохранены. Выход.")
        break

    elif choice == "1":  # Добавление
        while True:
            print("\nКого хотите добавить? (0 — Назад)")
            print("1 — Студент")
            print("2 — Преподаватель")
            print("3 — Админперсонал")
            type_choice = safe_choice("Введите номер: ", ["0","1","2","3"])
            if type_choice == "0":
                break
            name = safe_text("Имя: ")
            age = safe_number("Возраст: ")
            if type_choice == "1":
                group = safe_text("Группа: ")
                gpa = safe_number("GPA: ", allow_float=True)
                people.append(Student(name, age, group, gpa))
            elif type_choice == "2":
                subject = safe_text("Предмет: ")
                experience = safe_number("Стаж: ")
                people.append(Teacher(name, age, subject, experience))
            elif type_choice == "3":
                position = safe_text("Должность: ")
                department = safe_text("Отдел: ")
                people.append(AdminStaff(name, age, position, department))
            print("Человек добавлен!")
            save_to_file(people)

    elif choice == "2":  # Редактирование
        while True:
            if not people:
                print("Список пуст!")
                break
            print("\nСписок людей (0 — Назад):")
            for idx,p in enumerate(people,1):
                print(f"{idx}. {p.display_info()}")
            idx_choice = safe_number("Введите номер человека для редактирования: ")
            if idx_choice == 0:
                break
            if 1 <= idx_choice <= len(people):
                person = people[idx_choice-1]
                print(f"Редактируем: {person.display_info()}")
                person.name = safe_text("Новое имя: ")
                person.age = safe_number("Новый возраст: ")
                if isinstance(person, Student):
                    person.group = safe_text("Новая группа: ")
                    person.gpa = safe_number("Новый GPA: ", allow_float=True)
                elif isinstance(person, Teacher):
                    person.subject = safe_text("Новый предмет: ")
                    person.experience = safe_number("Новый стаж: ")
                elif isinstance(person, AdminStaff):
                    person.position = safe_text("Новая должность: ")
                    person.department = safe_text("Новый отдел: ")
                print("Данные обновлены!")
                save_to_file(people)
            else:
                print("Некорректный номер!")

    elif choice == "3":  # Удаление
        while True:
            if not people:
                print("Список пуст!")
                break
            print("\nСписок людей (0 — Назад):")
            for idx,p in enumerate(people,1):
                print(f"{idx}. {p.display_info()}")
            idx_choice = safe_number("Введите номер человека для удаления: ")
            if idx_choice == 0:
                break
            if 1 <= idx_choice <= len(people):
                removed = people.pop(idx_choice-1)
                print(f"Удалён: {removed.display_info()}")
                save_to_file(people)
            else:
                print("Некорректный номер!")

    elif choice == "4":  # Показать всех
        if not people:
            print("Список пуст!")
        else:
            print("\n=== Все люди ===")
            for p in people:
                print(p.display_info())

    elif choice == "5":  # Поиск
        while True:
            if not people:
                print("Список пуст!")
                break
            term = safe_text("Введите текст для поиска (0 — Назад): ", allow_empty=True)
            if term == "0":
                break
            term = term.lower()
            results = [p for p in people if term in p.display_info().lower()]
            if results:
                print(f"\nНайдено {len(results)} человек:")
                for p in results:
                    print(p.display_info())
            else:
                print("Ничего не найдено.")