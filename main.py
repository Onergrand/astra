import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QFormLayout
from PyQt5.QtCore import Qt

class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить запись")
        self.layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.lat_input = QLineEdit()
        self.lon_input = QLineEdit()
        self.type_input = QLineEdit()
        
        self.layout.addRow("Название:", self.name_input)
        self.layout.addRow("Широта:", self.lat_input)
        self.layout.addRow("Долгота:", self.lon_input)
        self.layout.addRow("Тип:", self.type_input)
        
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.accept)
        self.layout.addWidget(self.add_button)
        
        self.setLayout(self.layout)

    def get_values(self):
        return self.name_input.text(), self.lat_input.text(), self.lon_input.text(), self.type_input.text()

class TableApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Table App")
        self.setGeometry(100, 100, 600, 400)
        
        self.layout = QVBoxLayout()
        
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Широта", "Долгота", "Тип"])
        self.table.setSortingEnabled(False)
        
        self.layout.addWidget(self.table)
        
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.open_add_dialog)
        self.layout.addWidget(self.add_button)
        
        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.clear_table)
        self.layout.addWidget(self.clear_button)
        
        self.table.horizontalHeader().sectionClicked.connect(self.sort_by_column)
        
        self.setLayout(self.layout)
        self.row_id = 1
        
        self.add_mock_data()

    def add_mock_data(self):
        mock_data = [
            ("Парк", "55.751244", "37.618423", "место"),
            ("Кафе", "55.752023", "37.615310", "пункт")
        ]
        for name, lat, lon, type_ in mock_data:
            self.add_row(name, lat, lon, type_)

    def open_add_dialog(self):
        dialog = AddDialog(self)
        if dialog.exec_():
            name, lat, lon, type_ = dialog.get_values()
            self.add_row(name, lat, lon, type_)

    def add_row(self, name="", lat="0.0", lon="0.0", type_="пункт"):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(str(self.row_id)))
        self.table.item(row_position, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table.setItem(row_position, 1, QTableWidgetItem(name))
        self.table.setItem(row_position, 2, QTableWidgetItem(lat))
        self.table.item(row_position, 2).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table.setItem(row_position, 3, QTableWidgetItem(lon))
        self.table.item(row_position, 3).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table.setItem(row_position, 4, QTableWidgetItem(type_))
        self.row_id += 1

    def clear_table(self):
        self.table.setRowCount(0)
        self.row_id = 1

    def sort_by_column(self, column):
        if column in [0, 2, 3]:  # ID, Широта, Долгота - сортировка по числам
            self.table.sortItems(column, Qt.AscendingOrder)
        else:  # Название, Тип - сортировка по алфавиту
            self.table.sortItems(column, Qt.AscendingOrder)

    def validate_edit(self, row, column):
        if column in [0, 2, 3]:  # Запрет на изменение ID, Широты, Долготы
            self.table.item(row, column).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

if __name__ == "__main__":  
    app = QApplication(sys.argv)
    window = TableApp()
    window.show()
    sys.exit(app.exec_())
