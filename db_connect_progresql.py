from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtWidgets import QMessageBox
import sys

db = QSqlDatabase().addDatabase("QPSQL")
db.setDatabaseName("qt_progres_test")
db.setUserName("postgres")  # postgres is the default root username
db.setPassword("77894019")    # add your password here
print("Available drivers", db.drivers())
if not db.open():
    print("Unable to connect.")
    print('Last error', db.lastError().text())
else:
    print("Connection to the database successful")
db.open()
query = QSqlQuery(db)


def create_tables():
    db.transaction()
    query.exec("""  create type sexeEnum as enum('Garçon', 'Fille'); """)
    query.exec(""" CREATE TABLE IF NOT EXISTS patient (
                id serial PRIMARY KEY,
                lastname VARCHAR (50) NOT NULL,
                firstname VARCHAR (50) NOT NULL,
                birthday TIMESTAMP NOT NULL,
                sexe sexeEnum
    );
    """)
    db.commit()
    print("tables are created ! ")


def add(lastname, firstname, birthday, sexe):
    query.prepare("""INSERT INTO patient (
                    lastname,
                    firstname,
                    birthday,
                    sexe)
                    VALUES (?, ?, ?,?)""")
    query.addBindValue(lastname)
    query.addBindValue(firstname)
    query.addBindValue(birthday)
    query.addBindValue(sexe)

    if query.exec():
        db.commit()
    else:
        print(query.lastError())


def remove(id):
    print("delete")
    query.exec(f"DELETE FROM patient WHERE id = {id}")
