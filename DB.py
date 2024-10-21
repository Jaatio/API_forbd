#pyuic5 .\QtDesign\Rating_edit.ui -o .\Gui_win\Rating_edit.py
import pymysql.cursors
import pymysql
import sys

class BdApi:

    def __init__(self):
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
                cursor.execute("SELECT * FROM 4question.information;")
                results = cursor.fetchall()
                return results
        except pymysql.MySQLError as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

    def fetch_filtered_orders(self, client_name):
        try:
            with self.connection.cursor() as cursor:
                sql_query = """
                SELECT client_name,order_name, order_data, order_status
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
                sql_query = "SELECT client_name FROM information"
                cursor.execute(sql_query)
                result = cursor.fetchall()

                return [row['client_name'] for row in result]
        except pymysql.MySQLError as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None


    def sort_data(self, field=None):
        # Определение порядка сортировки (по возрастанию или по убыванию)
        sort_order = "ASC" if self.ui.radioButton_ascending.isChecked() else "DESC"

        # Если поле не указано, выходим
        if not field:
            return

        # Выполнение SQL-запроса для сортировки данных по выбранному полю
        try:
            with self.DB.connection.cursor() as cursor:
                sql_query = f"SELECT * FROM information ORDER BY {field} {sort_order};"
                cursor.execute(sql_query)
                sorted_data = cursor.fetchall()

                # Обновление таблицы с отсортированными данными
                self.update_table(sorted_data)
        except pymysql.MySQLError as e:
            print(f"Ошибка при выполнении запроса: {e}")

    def fetch_sorted_data(self, field_name, sort_order):
        try:
            with self.connection.cursor() as cursor:
                sql_query = f"SELECT * FROM information ORDER BY {field_name} {sort_order};"
                cursor.execute(sql_query)
                results = cursor.fetchall()
                return results
        except pymysql.MySQLError as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None


DB = BdApi()

