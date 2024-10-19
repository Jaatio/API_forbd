#pyuic5 .\QtDesign\Rating_edit.ui -o .\Gui_win\Rating_edit.py
import pymysql.cursors
import pymysql
import sys

class BdApi:

    def __init__(self):
        # Создание соединения с базой данных
        try:
            self.connection = pymysql.connect(host='localhost',
                                              user='root',
                                              password='',
                                              database='4question',
                                              cursorclass = pymysql.cursors.DictCursor)

            print("Соединение с базой данных установлено")
        except pymysql.MySQLError as e:
            print(f"Ошибка при подключении к базе данных: {e}")
            sys.exit()

    def fetch_data(self):
        try:
            with self.connection.cursor() as cursor:
                # Выполнение SQL-запроса
                cursor.execute("SELECT * FROM 4question.information;")
                results = cursor.fetchall()  # Получаем все данные
                return results
        except pymysql.MySQLError as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

    def fetch_filtered_orders(self, client_name):
        try:
            with self.connection.cursor() as cursor:
                # Выполняем SQL-запрос с фильтрацией по имени клиента
                sql_query = """
                SELECT client_name, order_data, order_status
                FROM information
                WHERE client_name = %s
                """
                cursor.execute(sql_query, (client_name,))
                result = cursor.fetchall()
                return result
        except pymysql.MySQLError as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

    def fetch_usernames(self):
        try:
            with self.connection.cursor() as cursor:
                # Выполнение SQL-запроса для получения имён клиентов
                sql_query = "SELECT client_name FROM information"
                cursor.execute(sql_query)
                # Получаем все имена клиентов
                result = cursor.fetchall()

                # Возвращаем список имён
                return [row['client_name'] for row in result]
        except pymysql.MySQLError as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

DB = BdApi()

