from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
import sys
from DB import BdApi
from Forms.main_window import Ui_Dialog_api

class Main_window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Dialog_api()
        self.ui.setupUi(self)
        self.DB = BdApi()
        self.sort_order = 'ASC'  # Значение сортировки по умолчанию (возрастание)
        self.current_sort_field = None  # Для отслеживания текущего поля сортировки

        self.load_data()
        self.load_usernames()

        # Настройка динамического размера таблицы
        self.ui.tableView_information.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Подключаем кнопки для выбора полей
        self.ui.pushButton_sort_client.clicked.connect(lambda: self.sort_data("client_name"))
        self.ui.pushButton_sort_orderdata.clicked.connect(lambda: self.sort_data("order_data"))
        self.ui.pushButton_sort_telephone.clicked.connect(lambda: self.sort_data("telephone"))
        self.ui.pushButton_sort_email.clicked.connect(lambda: self.sort_data("email"))
        self.ui.pushButton_sort_orderstatus.clicked.connect(lambda: self.sort_data("order_status"))

        # Подключаем радиокнопки для сортировки
        self.ui.radioButton_ascending.clicked.connect(lambda: self.set_sort_order("ASC"))
        self.ui.radioButton_descending.clicked.connect(lambda: self.set_sort_order("DESC"))

    # Устанавливаем порядок сортировки
    def set_sort_order(self, order):
        self.sort_order = order
        print(f"Сортировка установлена: {order}")
        if self.current_sort_field:  # Если поле сортировки уже выбрано
            self.sort_data(self.current_sort_field)  # Повторная сортировка с новым порядком

    # Загружаем данные в таблицу
    def load_data(self):
        all_users = self.DB.fetch_data()

        if all_users:
            self.update_table(all_users)
        else:
            print("Нет данных для отображения.")

    # Обновляем таблицу
    def update_table(self, data):
        model = QStandardItemModel()
        headers = list(data[0].keys()) if data else []
        model.setHorizontalHeaderLabels(headers)

        for row in data:
            items = [QStandardItem(str(value)) for value in row.values()]
            model.appendRow(items)

        self.ui.tableView_information.setModel(model)

    # Сортировка данных
    def sort_data(self, field_name):
        self.current_sort_field = field_name  # Сохраняем текущее поле сортировки
        sorted_data = self.DB.fetch_sorted_data(field_name, self.sort_order)
        if sorted_data:
            self.update_table(sorted_data)  # Обновляем таблицу с отсортированными данными
        else:
            print(f"Ошибка при сортировке по полю: {field_name}")

    # Фильтрация данных
    def filter_data(self):
        selected_username = self.ui.comboBox_clients.currentText()
        filtered_data = self.DB.fetch_filtered_orders(selected_username)

        if filtered_data:
            self.update_table(filtered_data)
        else:
            print(f"Нет заказов для клиента {selected_username}")

    # Вкид в комбобокс имен
    def load_usernames(self):
        usernames = self.DB.fetch_usernames()

        for username in usernames:
            self.ui.comboBox_clients.addItem(username)

    # Поиск по совпадениям
    def search_data(self):
        search_string = self.ui.lineEdit_search_string.text().strip().lower()
        model = self.ui.tableView_information.model()

        for row in range(model.rowCount()):
            for column in range(model.columnCount()):
                item = model.item(row, column)
                if item and search_string in item.text().lower():
                    item.setBackground(QColor('yellow'))
                else:
                    item.setBackground(QColor(''))




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    start_app = Main_window()
    start_app.show()
    sys.exit(app.exec_())

