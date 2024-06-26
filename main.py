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
                error_label['text'] = ""

                # Изменение текста в полях с характеристиками слова
                if lang == "russian":
                    translating_word['text'] = result[0]['french']
                else:
                    translating_word['text'] = result[0]['russian']
                translating_sex['text'] = result[0]['sex']
                translating_sound['text'] = result[0]['sound']

    # Отлавливатель слов, которых нет в базе данных
    except IndexError:
        error_label["text"] = "Слова нет в словаре"


# Функция для вывода всех слов и их перевода из базы данных
def show_all_words() -> str:
    def back():
        show_all_words_frame.destroy()
        scroll.destroy()

    query = "SELECT french, russian, sex, sound FROM french_rus ORDER BY french"

    # Отрисовка раздела для показа всех слов
    show_all_words_frame = Frame(root, bg='white', padx=10, pady=5)
    show_all_words_frame.place(relwidth=1, relheight=1)

    # Кнопка для возврата к основному разделу
    back_btn = Button(show_all_words_frame, bg="blue", font=100, text="Назад", command=lambda: back())
    back_btn.place(x=0, y=0)

    # Поле для отрисовки слов
    words_cointainer = Text(show_all_words_frame, bg="silver", font=200, wrap=WORD, border=2, relief="solid", padx=10, pady=5)
    words_cointainer.place(x=20, y=60, relwidth=0.95, relheight=0.85)

    # Отрисовка слов

    # Графический способ
    # for i in range(1, 1001):
    #     word = Label(text=f"{i}", bg="yellow", font=100, width=10, height=3)
    #     words_cointainer.window_create(INSERT, window=word)

    # Текстовый способ
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()[::-1]
        
        # Заполнение поля словами
        for i in result:
           word = f"{i['french']}: {i['russian']}\n\n"
           words_cointainer.insert(0.0, word)
        
        words_counter = Label(show_all_words_frame, bg="white", font=200, border=2, relief="solid", padx=8, pady=8, text=f"Количество слов: {len(result)}")
        words_counter.place(x=250, y=0)

    # Делает поле для слов неизменяемым
    words_cointainer["state"] = "disabled"

    scroll = Scrollbar(command=words_cointainer.yview)
    scroll.pack(side=RIGHT, fill=Y)
    words_cointainer.config(yscrollcommand = scroll.set)


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
    # Оболочка графического дизайна
    root = Tk()
    root['bg'] = "white"
    root.title("Французско-русский переводчик")
    root.wm_attributes('-alpha', 1)
    root.geometry("800x600")
    root.resizable(width=False, height=False)

    # Секция для виджетов для перевода
    translator_frame = Frame(root, bg='white', relief="solid", borderwidth=2, padx=10, pady=5)
    translator_frame.place(x=5, y=5, relwidth=0.5, relheight=0.4)

    # Заголовок "Введите слово"
    enter_word_label = Label(translator_frame, text="Введите слово: ", bg='white', font=100)
    enter_word_label.place(x=0, y=0)

    # Поле ввода слова
    word_input = Entry(translator_frame, bg="white", font=100, border=1, relief="solid")
    word_input.place(x=160, y=0)

    # Кнопка перевода
    translate_btn = Button(translator_frame, text="Перевести", bg="green", font=100, command=search_translating)
    translate_btn.place(x=0, y=50)

    # Характеристики слова
    # Заголовок "Перевод: "
    translating_label = Label(translator_frame, font=100, bg="white", text="Перевод: ")
    translating_label.place(x=0, y=100)
    # Заголовок с переводом слова
    translating_word = Label(translator_frame, bg="white", font=100, text="")
    translating_word.place(x=150, y=100)

    # Заголовок "Род: "
    translating_label = Label(translator_frame, font=100, bg="white", text="Род: ")
    translating_label.place(x=0, y=130)
    # Заголовок с родом слова
    translating_sex = Label(translator_frame, bg="white", font=100, text="")
    translating_sex.place(x=150, y=130)

    # Заголовок "Произношение: "
    translating_label = Label(translator_frame, font=100, bg="white", text="Произношение: ")
    translating_label.place(x=0, y=160)
    # Заголовок с произношением слова
    translating_sound = Label(translator_frame, bg="white", font=100, text="")
    translating_sound.place(x=150, y=160)

    # Сообщение об ошибках
    error_label = Label(translator_frame, bg="white", font=100, text="", fg="red")
    error_label.place(x=130, y=55)
    
    # Секция для виджетов для других фунцкий
    other_func_frame = Frame(root, bg='white', relief="solid", borderwidth=2, padx=10, pady=5)
    other_func_frame.place(x=420, y=5, relwidth=0.45, relheight=0.4)

    show_all_words_btn = Button(other_func_frame, text="Просмотреть весь словарь", bg="yellow", font=80, command=show_all_words)
    show_all_words_btn.place(x=0, y=0)

    root.mainloop()


except Exception as ex:
    print(ex)
    print("Connection refused")

# Закрытие соединения с базой данных
finally:
    connection.close()
    print("#" * 70)
    print("Соединение закрыто")