# Импортирование библиотеки для работы с базами данных MySQL
import pymysql.cursors

# Импортирование библиотеки для отрисовки графического дизайна
from tkinter import *

# Импортирование настроек соединения с базой данных из файла config
from config import host, user, password, db_name
        

# Функции для создания и выполнения запросов в базу данных
# Функция для поиска слова и его перевода в базе данных
def search_translating() -> dict:
    word = word_input.get()
    query = f"SELECT * FROM french_rus WHERE french = '{word}' or russian = '{word}';"
    lang = "french"

    for l in word:
        if l in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя":
            lang = "russian"
    
    try:
        with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                print(result)

                # Очистка полей перед следующим переводом
                translating_word['text'] = ""
                translating_sex['text'] = ""
                translating_sound['text'] = ""

                # Изменение текста в полях с характеристиками слова
                if lang == "russian":
                    translating_word['text'] = result[0]['french']
                else:
                    translating_word['text'] = result[0]['russian']
                translating_sex['text'] = result[0]['sex']
                translating_sound['text'] = result[0]['sound']

    # Отлавливатель слов, которых нет в базе данных
    except IndexError:
        translating_word["text"] = "Данного слова нет в базе данных"


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


try:
    # Создание соединения с базой данных
    connection = pymysql.connect (
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )

    print("Successfully connected")
    print("#" * 70, end="\n\n")
    
    
    # Отрисовка графического дизайна
    root = Tk()
    root['bg'] = "white"
    root.title("Французско-русский переводчик")
    root.wm_attributes('-alpha', 1)
    root.geometry("800x600")
    root.resizable(width=False, height=False)

    # Оболочка графического дизайна
    frame = Frame(root, bg='white', padx=10, pady=5)
    frame.place(relwidth=1, relheight=1)

    # Заголовок "Введите слово"
    enter_word_label = Label(frame, text="Введите слово: ", bg='white', font=100)
    enter_word_label.place(x=0, y=0)

    # Поле ввода слова
    word_input = Entry(frame, bg="white", font=100, border=1)
    word_input.place(x=160, y=0)

    # Кнопка перевода
    translate_btn = Button(frame, text="Перевести", bg="green", font=100, command=search_translating)
    translate_btn.place(x=0, y=50)

    # Характеристики слова
    # Заголовок "Перевод: "
    translating_label = Label(frame, font=100, bg="white", text="Перевод: ")
    translating_label.place(x=0, y=100)
    # Заголовок с переводом слова
    translating_word = Label(frame, bg="white", font=100, text="")
    translating_word.place(x=150, y=100)

    # Заголовок "Род: "
    translating_label = Label(frame, font=100, bg="white", text="Род: ")
    translating_label.place(x=0, y=130)
    # Заголовок с родом слова
    translating_sex = Label(frame, bg="white", font=100, text="")
    translating_sex.place(x=150, y=130)

    # Заголовок "Произношение: "
    translating_label = Label(frame, font=100, bg="white", text="Произношение: ")
    translating_label.place(x=0, y=160)
    # Заголовок с произношением слова
    translating_sound = Label(frame, bg="white", font=100, text="")
    translating_sound.place(x=150, y=160)

    root.mainloop()


except Exception as ex:
    print(ex)
    print("Connection refused")

# Закрытие соединения с базой данных
finally:
    connection.close()
    print("#" * 70)
    print("Соединение закрыто")