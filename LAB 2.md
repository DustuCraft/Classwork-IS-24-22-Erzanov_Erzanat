<img width="1684" height="707" alt="image" src="https://github.com/user-attachments/assets/b46f26f8-4960-49ff-b8e5-b8a34ac165f4" />
#LAB 2

while True: 
    num1 = float(input("Первое число >")) 
    operator = input("Оператор >")
    num2 = float(input("Второе число >")) 
     
    # Вычитание 
    if operator == "-": 
        print("Ответ:", num1 - num2) 
    # Сложение 
    elif operator == "+": 
        print("Ответ:", num1 + num2) 
    # Умножение 
    elif operator == "*": 
        print("Ответ:", num1 * num2) 
    #Целочисленное деление
    elif operator == "//": 
        print("Ответ:", num1 // num2) 
    #Остаток от деления
    elif operator == "%": 
        print("Ответ:", num1 % num2)     
    # Деление 
    elif operator == "/": 
        if num2 != 0:  # Проверка деления на ноль 
            print("Ответ:", num1 / num2) 
        else: 
            print("Ошибка! Деление на ноль!") 
    else: 
        print("Ошибка") 

