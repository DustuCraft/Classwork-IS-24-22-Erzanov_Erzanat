# Classwork-IS-24-22-Erzanov_Erzanat
LAB 2
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
