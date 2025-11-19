import json
from datetime import datetime

class Student:
    def __init__(self, name, group, gpa):
        self.__name = name
        self.__group = group
        self.__gpa = gpa

    # --- Getters ---
    def get_name(self):
        return self.__name

    def get_group(self):
        return self.__group

    def get_gpa(self):
        return self.__gpa

    # --- Setters with update logging ---
    def set_name(self, new_name):
        old = self.__name
        if new_name != old:
            self.__name = new_name
            self.save_update(field="name", old_value=old, new_value=new_name)
            print("✔ Имя изменено.")
        else:
            print("ℹ Имя не изменилось.")

    def set_group(self, new_group):
        old = self.__group
        if new_group != old:
            self.__group = new_group
            self.save_update(field="group", old_value=old, new_value=new_group)
            print("✔ Группа изменена.")
        else:
            print("ℹ Группа не изменилась.")

    def update_gpa(self, new_gpa):
        try:
            new_gpa = float(new_gpa)
        except (ValueError, TypeError):
            print("❌ Неверный формат GPA.")
            return

        if 0 <= new_gpa <= 4:
            old = self.__gpa
            if new_gpa != old:
                self.__gpa = new_gpa
                self.save_update(field="gpa", old_value=old, new_value=new_gpa)
                print(f"✔ GPA обновлён: {old} → {new_gpa}")
            else:
                print("ℹ GPA не изменился.")
        else:
            print("❌ Ошибка: GPA должен быть в диапазоне 0 — 4.0")

    # --- Display ---
    def display_info(self):
        print(f"▶ Имя: {self.__name} | Группа: {self.__group} | GPA: {self.__gpa}")

    # --- Save single update entry to studentsUpdate.json (append to list) ---
    def save_update(self, field, old_value, new_value, filename="studentsUpdate.json"):
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "student_name": self.__name,
            "field": field,
            "old_value": old_value,
            "new_value": new_value
        }

        try:
            with open(filename, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []

        history.append(entry)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

        print(f"💾 Изменение зафиксировано в {filename}")


class Group:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)
        print(f"✔ Студент '{student.get_name()}' добавлен.")

    def show_all(self):
        if not self.students:
            print("⚠ Список студентов пуст.")
            return

        print("\n📋 Текущий список студентов:")
        for i, s in enumerate(self.students, start=1):
            print(f"{i}. {s.get_name()} | {s.get_group()} | GPA: {s.get_gpa()}")

    def edit_student(self):
        if not self.students:
            print("⚠ Нет студентов для редактирования.")
            return

        self.show_all()
        try:
            idx = int(input("\nВведите номер студента для редактирования: "))
            if not (1 <= idx <= len(self.students)):
                raise IndexError
            student = self.students[idx - 1]
        except (ValueError, IndexError):
            print("❌ Некорректный выбор.")
            return

        # Show current values numbered 1-3
        print("\nТекущее состояние:")
        print(f"1. Студент: {student.get_name()}")
        print(f"2. Группа: {student.get_group()}")
        print(f"3. GPA: {student.get_gpa()}")

        try:
            field = int(input("Что хотите изменить? Выберите 1–3: "))
        except ValueError:
            print("❌ Введите число 1, 2 или 3.")
            return

        if field == 1:
            new_name = input("Введите новое имя: ").strip()
            if new_name:
                student.set_name(new_name)
            else:
                print("❌ Имя не должно быть пустым.")
        elif field == 2:
            new_group = input("Введите новую группу: ").strip()
            if new_group:
                student.set_group(new_group)
            else:
                print("❌ Группа не должна быть пустой.")
        elif field == 3:
            try:
                new_gpa = float(input("Введите новый GPA (0–4): "))
                student.update_gpa(new_gpa)
            except ValueError:
                print("❌ GPA должен быть числом.")
        else:
            print("❌ Неверный пункт (нужно 1, 2 или 3).")

    def remove_student(self):
        if not self.students:
            print("⚠ Нет студентов для удаления.")
            return

        self.show_all()
        try:
            idx = int(input("\nВведите номер студента для удаления: "))
            if not (1 <= idx <= len(self.students)):
                raise IndexError
            s = self.students.pop(idx - 1)
            # Log deletion in studentsUpdate.json
            try:
                with open("studentsUpdate.json", "r", encoding="utf-8") as f:
                    history = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                history = []
            history.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "student_name": s.get_name(),
                "field": "deleted",
                "old_value": {"group": s.get_group(), "gpa": s.get_gpa()},
                "new_value": None
            })
            with open("studentsUpdate.json", "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=4)
            print(f"✔ Студент '{s.get_name()}' удалён и запись добавлена в studentsUpdate.json.")
        except (ValueError, IndexError):
            print("❌ Некорректный выбор.")

    def save_to_file(self, filename="students.json"):
        data = [
            {"name": s.get_name(), "group": s.get_group(), "gpa": s.get_gpa()}
            for s in self.students
        ]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"💾 Основной список сохранён в {filename}")

    def load_from_file(self, filename="students.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.students = [Student(d["name"], d["group"], d["gpa"]) for d in data]
            print(f"🔄 Загружено {len(self.students)} студентов из {filename}")
        except FileNotFoundError:
            print(f"⚠ Файл {filename} не найден — начнём с пустого списка.")
        except (json.JSONDecodeError, KeyError):
            print(f"⚠ Ошибка в формате {filename}. Начинаем с пустого списка.")


# ---------------- Main Program ----------------
def main():
    group = Group()
    # Попробуем загрузить существующий основной файл при старте (если он есть)
    group.load_from_file()

    while True:
        print("\n=====================================")
        print("   🧑‍🎓 СИСТЕМА УЧЁТА СТУДЕНТОВ (Меню)")
        print("=====================================")
        print("1 — Добавить студента")
        print("2 — Показать всех студентов")
        print("3 — Редактировать студента (1-Имя, 2-Группа, 3-GPA)")
        print("4 — Удалить студента")
        print("5 — Сохранить основной список")
        print("6 — Показать историю изменений (studentsUpdate.json)")
        print("7 — Выйти (с сохранением)")
        print("=====================================")

        choice = input("Выберите действие (1–7): ").strip()

        if choice == "1":
            name = input("🔹 Имя студента: ").strip()
            if not name:
                print("❌ Имя не должно быть пустым.")
                continue
            group_name = input("🔹 Группа (например IS-23-1): ").strip()
            if not group_name:
                print("❌ Группа не должна быть пустой.")
                continue
            while True:
                try:
                    gpa = float(input("🔹 GPA (0–4): "))
                    if 0 <= gpa <= 4:
                        break
                    print("⚠ GPA должен быть от 0 до 4.")
                except ValueError:
                    print("⚠ Введите числовое значение для GPA.")
            group.add_student(Student(name, group_name, gpa))

        elif choice == "2":
            group.show_all()

        elif choice == "3":
            group.edit_student()

        elif choice == "4":
            group.remove_student()

        elif choice == "5":
            group.save_to_file()

        elif choice == "6":
            try:
                with open("studentsUpdate.json", "r", encoding="utf-8") as f:
                    history = json.load(f)
                if not history:
                    print("ℹ История пустая.")
                else:
                    print("\n📜 История изменений:")
                    for i, e in enumerate(history, start=1):
                        print(f"{i}. [{e['timestamp']}] {e['student_name']} — {e['field']}: {e['old_value']} → {e['new_value']}")
            except (FileNotFoundError, json.JSONDecodeError):
                print("⚠ Файл studentsUpdate.json не найден или повреждён.")

        elif choice == "7":
            group.save_to_file()
            print("👋 Выход. Данные сохранены.")
            break

        else:
            print("❌ Неверный выбор. Введите число от 1 до 7.")


if __name__ == "__main__":
    main()