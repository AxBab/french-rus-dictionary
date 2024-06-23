# Функция для поиска слова и его перевода в базе данных
def search_translating() -> dict:
    print("Укажите слово на французском или его перевод на русский")
    word = input("Ожидание ввода слова:    ")

    # Определение языка введенного слова
    for l in word:
        if l in "abcdefghijklmnopqrstuvwxyz":
            lang = "french"
        elif l in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя":
            lang = "russian"

    return {'query': f"SELECT * FROM french_rus WHERE french = '{word}' or russian = '{word}';", 'lang': lang}

# Функция для вывода всех слов и их перевода из базы данных
def show_all_words() -> str:
    print("Весь список слов с их переводом на русский в алфавитном порядке:")
    return "SELECT french, russian, sex, sound FROM french_rus ORDER BY french"

# Функция для добавления нового слов его перевода в базу данных 
def add_new_translating() -> str:
    print("Укажите слово на французском его перевод на русский")

    french = input("Слово на французском:   ")
    # Проверка на правильность ввода слова на французском
    for fr_l in french:
        if fr_l in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя":
            print("Введите слово полностью на французском!")
            french = input("Слово на французском:   ")

    russian = input("Перевод слова на русский:   ")
    # Проверка на правильность ввода на русском
    for ru_l in russian:
        if ru_l in "abcdefghijklmnopqrstuvwxyz":
            print("Введите слово полностью на русском!")
            russian = input("Слово на русском:   ")

    sex = input("Введите род слова (если имеется):     ").upper()
    sound = input("Произношение слова:   ")

    return f"INSERT INTO french_rus (french, russian, sex, sound) VALUES ('{french}', '{russian}', '{sex}', '{sound}');"

# Функция для изменения параметров слова
def fix_word_translating() -> str:
    print("Укажите слово на французском или его перевод на русский для его изменения")
    word = input("Ожидание ввода слова: ")

    print("Что вы хотите сделалать со словом?")
    print("Изменить перевод: 1")
    print("Изменить звучание: 2")
    print("Удалить слово: 3")
    way = int(input("Ожидание выбора действия:   "))

    if way == 1:
        new_french = input("Введите новый перевод этого слова на французском:   ")
        new_russian = input("Введите новый перевод этого слова на русском:  ")
        new_sex = input("Род слова (если имеется):  ")[:1] # Выбор 1 буквы чтобы не выдавало ошибки из-за длины слова
        new_sound = input("Введите новое звучание этого слова:  ")
    
        return f"UPDATE french_rus SET french = '{new_french}', russian = '{new_russian}, sex = '{new_sex}', sound = '{new_sound}' WHERE french = '{word}' or russian = '{word}';"
    elif way == 2:
        new_sound = input("Введите новое звучание:  ")

        return f"UPDATE french_rus SET sound = '{new_sound}' WHERE french = '{word}' or russian = '{word}';"

    elif way == 3:
        return f"DELETE FROM french_rus WHERE french = '{word}' or russian = '{word}';"