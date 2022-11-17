import sys
from PySide6.QtWidgets import QApplication, QWidget, QAbstractItemView, QHeaderView, QPushButton, QMessageBox, QLineEdit, QTableView, QMainWindow, QDateEdit, QComboBox, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlTableModel
from db_connect_progresql import create_tables, db, add, remove


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Postgresql CRUD OPERATION")
        self.setMinimumSize(600, 400)
        create_tables()
        self.initializeUi()
        self.handle_btn_click()

    def initializeUi(self):
        """ Ui initialization """
        self.lastname_lineEdit = QLineEdit("")
        self.lastname_lineEdit.setMinimumHeight(30)
        self.lastname_lineEdit.setPlaceholderText('Nom')
        self.firstname_lineEdit = QLineEdit("")
        self.firstname_lineEdit.setMinimumHeight(30)
        self.firstname_lineEdit.setPlaceholderText('Prénom')
        self.birthday = QDateEdit()
        self.birthday.setCalendarPopup(True)
        self.birthday.setMinimumHeight(30)
        self.birthday.setMinimumWidth(150)
        self.sexe = QComboBox()
        self.sexe.setMinimumHeight(30)
        self.sexe.addItems(['Fille', 'Garçon'])
        self.add_btn = QPushButton("Add")
        self.add_btn.setMinimumHeight(30)
        self.remove_btn = QPushButton("Remove")
        self.remove_btn.setMinimumHeight(30)
        self.update_btn = QPushButton("Edit")
        self.update_btn.setCheckable(True)
        self.update_btn.setMinimumHeight(30)

        self.table_view = QTableView()
        self.model = QSqlTableModel(db=db)
        self.model.setTable("patient")
        self.table_view.setModel(self.model)
        # self.table_view.setSelectionMode()
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Nom")
        self.model.setHeaderData(2, Qt.Horizontal, "Prénom")
        self.model.setHeaderData(3, Qt.Horizontal, "DDN")
        self.model.setHeaderData(4, Qt.Horizontal, "Sexe")

        self.table_view.setEditTriggers(
            QAbstractItemView.NoEditTriggers)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.horizontalHeader(
        ).setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.setSelectionMode(
            QAbstractItemView.SingleSelection)
        self.table_view.setSelectionBehavior(
            QAbstractItemView.SelectRows)

        self.model.select()

        lineEditLayout = QHBoxLayout()
        lineEditLayout.addWidget(self.lastname_lineEdit)
        lineEditLayout.addWidget(self.firstname_lineEdit)
        lineEditLayout.addWidget(self.birthday)
        lineEditLayout.addWidget(self.sexe)

        btn_layout = QHBoxLayout()
        # btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.remove_btn)
        btn_layout.addWidget(self.add_btn)
        main_layout = QVBoxLayout()
        main_layout.addLayout(lineEditLayout)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.table_view)

        centralWidget = QWidget()
        centralWidget.setLayout(main_layout)
        self.setCentralWidget(centralWidget)

    def handle_btn_click(self):
        self.add_btn.clicked.connect(self.add_fn)
        # self.update_btn.clicked.connect(self.update_fn)
        self.remove_btn.clicked.connect(self.remove_fn)

    def getSelectedIndex(self):
        index = self.table_view.selectedIndexes()
        if index:
            return index[0].data()

    def add_fn(self):
        print('Add')
        lastname = self.lastname_lineEdit.text().strip()
        firstname = self.firstname_lineEdit.text().strip()
        birthday = self.birthday.text().strip()
        sexe = self.sexe.currentText().strip()
        if lastname and firstname:
            add(lastname, firstname, birthday, sexe)
            self.model.select()
            self.lastname_lineEdit.setText("")
            self.firstname_lineEdit.setText("")
        else:
            print("lastname & firstname doivent être renseignés")
            button = QMessageBox.critical(
                self,
                "Attention !",
                "Il faut renseigner tous les champs !",
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok)

    def remove_fn(self):
        id = self.getSelectedIndex()
        if not id:
            button = QMessageBox.critical(
                self,
                "Attention !",
                "Il faut selectionner une personne !",
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok)
        else:
            print(id)
            remove(id)
            print('Remove')
            self.model.select()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())
