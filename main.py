# Импортирование библиотеки для работы с базами данных MySQL
import pymysql.cursors

# Импортирование настроек соединения с базой данных из файла config
from config import host, user, password, db_name

# Импортирование функций для создания запросов в базу данных
from queries import search_translating, show_all_words, add_new_translating, fix_word_translating



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
    
    while True:
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

            # Меню выбора действия
            print("Найти перевод слова: 1")
            print("Показать перевод всех слов: 2")
            print("Добавить перевод слова: 3")
            print("Изменить слово: 4")
            print()

            way = int(input("Ожидание выбора действия:   "))
            print()
            query = ""

            # Создание запроса
            if way == 1:
                query, lang = search_translating().values()
            elif way == 2:
                query = show_all_words()
            elif way == 3:
                query = add_new_translating()
            elif way == 4:
                query = fix_word_translating()

            # Выполнение запроса в базу данных
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    if way == 1:
                        print()
                        result = cursor.fetchall()
                        if lang == "french":
                            print(f"Перевод {result[0]['french']}: {result[0]['russian']}")
                            print(f"Род: {result[0]['sex']}")
                            print(f"Произношение: {result[0]['sound']}")
                        elif lang == "russian":
                            print(f"Перевод {result[0]['russian']}: {result[0]['french']}")
                            print(f"Род: {result[0]['sex']}")
                            print(f"Произношение: {result[0]['sound']}")
                        else:
                            print("Вы ввели слово не на французском и не на русском!")

                    if way == 2:
                        print()
                        result = cursor.fetchall()

                        print("#" * 70)
                        for i in result:
                            print(f"{i['french']}: {i['russian']}")
                            print(f"Род: {i['sex']}")
                            print(f"Произношение: {i['sound']}")
                            print()
                        print("#" * 70)
                    connection.commit()
                    print()

            # Отлавливатель слов, ненаходящихся в базе данных
            except IndexError:
                print("#" * 70)
                print("Error")
                print("Такого слова нет в базе данных")
                print("#" * 70)
                print()


        # Закрытие соединения с базой данных
        finally:
            connection.close()
            print("#" * 70)
            print("Соединение закрыто")

except Exception as ex:
    print(ex)
    print("Connection refused")