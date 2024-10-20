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
        self.load_data()
        self.load_usernames()

        self.all_users = []
        self.load_data()
        self.load_usernames()

        # Подключаем кнопки к слотам
        self.ui.pushButton_filter.clicked.connect(self.filter_data)
        self.ui.pushButton_show_all.clicked.connect(self.load_data)
        self.ui.pushButton_search.clicked.connect(self.search_data)
        self.ui.pushButton_search.clicked.connect(self.search_data)
        #self.ui.radioButton_ascending.clicked.connect(self.)
        #self.ui.radioButton_descending.clicked.connect(self.)

    #Вкид в таблицу
    def load_data(self):

        all_users = self.DB.fetch_data()

        if all_users:
            model = QStandardItemModel()

            headers = list(all_users[0].keys()) if all_users else []
            model.setHorizontalHeaderLabels(headers)

            for row in all_users:
                items = [QStandardItem(str(data)) for data in
                         row.values()]
                model.appendRow(items)

            self.ui.tableView_information.setModel(model)
        else:
            print("Нет данных для отображения.")

    #Фильтрация
    def filter_fun(self):
        all_users = self.DB.fetch_data()

        if all_users:
            model = QStandardItemModel()

            headers = list(all_users[0].keys()) if all_users else []
            model.setHorizontalHeaderLabels(headers)

            for row in all_users:
                items = [QStandardItem(str(data)) for data in
                         row.values()]
                model.appendRow(items)

            self.ui.tableView_information.setModel(model)
        else:
            print("Нет данных для отображения.")

    #Фильтрация обновление
    def update_table(self, data):
        model = QStandardItemModel()
        headers = ["Имя клиента", "Дата заказа", "Статус заказа"]
        model.setHorizontalHeaderLabels(headers)

        for row in data:
            items = [QStandardItem(str(row['client_name'])),
                     QStandardItem(str(row['order_data'])),
                     QStandardItem(str(row['order_status']))]
            model.appendRow(items)

        self.ui.tableView_information.setModel(model)

    def filter_data(self):
        selected_username = self.ui.comboBox_clients.currentText()
        filtered_data = self.DB.fetch_filtered_orders(selected_username)

        if filtered_data:
            self.update_table(filtered_data)
        else:
            print(f"Нет заказов для клиента {selected_username}")

    #Вкид в комбобокс имен
    def load_usernames(self):
        usernames = self.DB.fetch_usernames()

        for username in usernames:
            self.ui.comboBox_clients.addItem(username)

    #Поиск по совпадениям
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

