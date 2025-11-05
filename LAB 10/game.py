import json
import os
from typing import List, Dict, Any


def input_games() -> List[Dict[str, Any]]:
    """Ввод данных об играх с обработкой ошибок"""
    games = []
    while True:
        try:
            n = int(input("Введите количество игр (не менее 1): "))
            if n < 1:
                print("Количество игр должно быть не менее 1")
                continue
            break
        except ValueError:
            print("Ошибка: введите целое число")

    for i in range(n):
        print(f"\nИгра {i + 1}:")
        while True:
            title = input("Название игры: ").strip()
            if title:
                break
            print("Название не может быть пустым")

        genre = input("Жанр: ").strip() or "Не указан"

        while True:
            try:
                rating = float(input("Рейтинг (0-10): "))
                if 0 <= rating <= 10:
                    break
                print("Рейтинг должен быть от 0 до 10")
            except ValueError:
                print("Ошибка: введите число")

        games.append({"title": title, "genre": genre, "rating": rating})

    return games


def save_to_txt(games: List[Dict[str, Any]], filename: str = "games.txt") -> None:
    """Сохранение данных в текстовый файл"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for game in games:
                f.write(f"{game['title']} | {game['genre']} | {game['rating']:.1f}\n")
        print(f"Данные сохранены в {filename}")
    except IOError as e:
        print(f"Ошибка при сохранении в файл {filename}: {e}")


def load_from_txt(filename: str = "games.txt") -> List[Dict[str, Any]]:
    """Загрузка данных из текстового файла"""
    games = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if '|' in line:
                    parts = [p.strip() for p in line.strip().split('|')]
                    if len(parts) >= 3:
                        try:
                            games.append({
                                "title": parts[0],
                                "genre": parts[1],
                                "rating": float(parts[2])
                            })
                        except (ValueError, IndexError):
                            continue
        print(f"Загружено {len(games)} игр из {filename}")
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
    except IOError as e:
        print(f"Ошибка при чтении файла {filename}: {e}")


def save_to_json(games: List[Dict[str, Any]], filename: str = "games.json") -> None:
    """Сохранение данных в JSON файл"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(games, f, ensure_ascii=False, indent=4)
        print(f"Данные сохранены в {filename}")
    except IOError as e:
        print(f"Ошибка при сохранении в JSON файл: {e}")


def show_games(games: List[Dict[str, Any]], sort_by_rating: bool = False) -> None:
    """Вывод списка игр с возможностью сортировки по рейтингу"""
    if not games:
        print("Список игр пуст")
        return

    if sort_by_rating:
        games = sorted(games, key=lambda x: x['rating'], reverse=True)

    print("\n" + "=" * 60)
    print(f"{'Название':<30} | {'Жанр':<20} | {'Рейтинг':>7}")
    print("-" * 60)
    for game in games:
        print(f"{game['title']:<30} | {game['genre']:<20} | {game['rating']:>7.1f}")
    print("=" * 60 + "\n")


def filter_by_rating(games: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрация игр по минимальному рейтингу"""
    if not games:
        print("Нет данных для фильтрации")
        return []

    while True:
        try:
            threshold = float(input("\nВведите минимальный рейтинг для фильтрации (0-10): "))
            if 0 <= threshold <= 10:
                break
            print("Рейтинг должен быть от 0 до 10")
        except ValueError:
            print("Ошибка: введите число")

    filtered = [g for g in games if g["rating"] >= threshold]
    print(f"\nНайдено {len(filtered)} игр с рейтингом ≥ {threshold:.1f}")
    return filtered


def main():
    games = []
    current_data = []

    while True:
        print("\n" + "=" * 50)
        print("1. Добавить игры")
        print("2. Показать все игры")
        print("3. Сохранить в текстовый файл")
        print("4. Загрузить из текстового файла")
        print("5. Сохранить в JSON")
        print("6. Отфильтровать по рейтингу")
        print("7. Выход")

        choice = input("\nВыберите действие (1-7): ")

        if choice == "1":
            games = input_games()
            current_data = games.copy()

        elif choice == "2":
            sort_choice = input("Отсортировать по рейтингу? (д/н): ").lower()
            show_games(games, sort_by_rating=(sort_choice == 'д'))

        elif choice == "3":
            if games:
                filename = input("Введите имя файла (по умолчанию games.txt): ") or "games.txt"
                save_to_txt(games, filename)
            else:
                print("Нет данных для сохранения")

        elif choice == "4":
            filename = input("Введите имя файла (по умолчанию games.txt): ") or "games.txt"
            games = load_from_txt(filename)
            if games:
                current_data = games.copy()

        elif choice == "5":
            if games:
                filename = input("Введите имя файла (по умолчанию games.json): ") or "games.json"
                save_to_json(games, filename)
            else:
                print("Нет данных для сохранения")

        elif choice == "6":
            if games:
                filtered = filter_by_rating(games)
                if filtered:
                    show_choice = input("Показать отфильтрованный список? (д/н): ").lower()
                    if show_choice == 'д':
                        show_games(filtered, sort_by_rating=True)
            else:
                print("Нет данных для фильтрации")

        elif choice == "7":
            print("Выход из программы")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите от 1 до 7")
if __name__ == "__main__":
    main()