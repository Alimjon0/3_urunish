import json
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QHeaderView
)

# ====== Yordamchi funksiyalar ======
def load_data(filename):
    path = Path(filename)
    return json.load(open(path, "r")) if path.exists() else []

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ====== Kontaktlar ======
class ContactsTab(QWidget):
    FILE = "contacts.json"

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Ism", "Familiya", "Telefon"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        form = QHBoxLayout()
        self.name = QLineEdit(); self.name.setPlaceholderText("Ism")
        self.surname = QLineEdit(); self.surname.setPlaceholderText("Familiya")
        self.phone = QLineEdit(); self.phone.setPlaceholderText("Telefon")
        form.addWidget(self.name); form.addWidget(self.surname); form.addWidget(self.phone)
        self.layout.addLayout(form)

        btns = QHBoxLayout()
        self.add_btn = QPushButton("➕ Qo‘shish")
        self.edit_btn = QPushButton("✏️ Tahrirlash")
        self.del_btn = QPushButton("🗑 O‘chirish")
        btns.addWidget(self.add_btn); btns.addWidget(self.edit_btn); btns.addWidget(self.del_btn)
        self.layout.addLayout(btns)

        self.add_btn.clicked.connect(self.add_contact)
        self.edit_btn.clicked.connect(self.edit_contact)
        self.del_btn.clicked.connect(self.del_contact)
        self.load_table()

    def load_table(self):
        data = load_data(self.FILE)
        self.table.setRowCount(0)
        for row, c in enumerate(data):
            self.table.insertRow(row)
            self.table.setItem(row,0,QTableWidgetItem(c["name"]))
            self.table.setItem(row,1,QTableWidgetItem(c["surname"]))
            self.table.setItem(row,2,QTableWidgetItem(c["phone"]))

    def add_contact(self):
        if self.name.text() and self.surname.text() and self.phone.text():
            data = load_data(self.FILE)
            data.append({"name": self.name.text(),
                         "surname": self.surname.text(),
                         "phone": self.phone.text()})
            save_data(self.FILE, data)
            self.name.clear(); self.surname.clear(); self.phone.clear()
            self.load_table()

    def edit_contact(self):
        row = self.table.currentRow()
        if row >= 0:
            data = load_data(self.FILE)
            data[row]["name"] = self.name.text() or data[row]["name"]
            data[row]["surname"] = self.surname.text() or data[row]["surname"]
            data[row]["phone"] = self.phone.text() or data[row]["phone"]
            save_data(self.FILE, data)
            self.load_table()

    def del_contact(self):
        row = self.table.currentRow()
        if row >= 0:
            data = load_data(self.FILE)
            data.pop(row)
            save_data(self.FILE, data)
            self.load_table()


# ====== ToDo List ======
class TodoTab(QWidget):
    FILE = "todo.json"

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.table = QTableWidget(0,3)
        self.table.setHorizontalHeaderLabels(["Vazifa", "Tugash", "Holat"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        form = QHBoxLayout()
        self.title = QLineEdit(); self.title.setPlaceholderText("Vazifa nomi")
        self.due = QLineEdit(); self.due.setPlaceholderText("YYYY-MM-DD")
        form.addWidget(self.title); form.addWidget(self.due)
        self.layout.addLayout(form)

        btns = QHBoxLayout()
        self.add_btn = QPushButton("➕ Qo‘shish")
        self.done_btn = QPushButton("✅ Bajarildi")
        self.del_btn = QPushButton("🗑 O‘chirish")
        btns.addWidget(self.add_btn); btns.addWidget(self.done_btn); btns.addWidget(self.del_btn)
        self.layout.addLayout(btns)

        self.add_btn.clicked.connect(self.add_task)
        self.done_btn.clicked.connect(self.toggle_done)
        self.del_btn.clicked.connect(self.del_task)
        self.load_table()

    def load_table(self):
        data = load_data(self.FILE)
        self.table.setRowCount(0)
        for r,t in enumerate(data):
            self.table.insertRow(r)
            self.table.setItem(r,0,QTableWidgetItem(t["title"]))
            self.table.setItem(r,1,QTableWidgetItem(t["due"]))
            self.table.setItem(r,2,QTableWidgetItem("✅" if t["done"] else "❌"))

    def add_task(self):
        if self.title.text():
            data = load_data(self.FILE)
            data.append({"title": self.title.text(), "due": self.due.text(), "done": False})
            save_data(self.FILE, data)
            self.title.clear(); self.due.clear()
            self.load_table()

    def toggle_done(self):
        row = self.table.currentRow()
        if row >= 0:
            data = load_data(self.FILE)
            data[row]["done"] = not data[row]["done"]
            save_data(self.FILE, data)
            self.load_table()

    def del_task(self):
        row = self.table.currentRow()
        if row >= 0:
            data = load_data(self.FILE)
            data.pop(row)
            save_data(self.FILE, data)
            self.load_table()


# ====== Kitoblar ======
class BooksTab(QWidget):
    FILE = "books.json"

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.table = QTableWidget(0,3)
        self.table.setHorizontalHeaderLabels(["Nom", "Muallif", "Yil"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        form = QHBoxLayout()
        self.title = QLineEdit(); self.title.setPlaceholderText("Kitob nomi")
        self.author = QLineEdit(); self.author.setPlaceholderText("Muallif")
        self.year = QLineEdit(); self.year.setPlaceholderText("Yil")
        form.addWidget(self.title); form.addWidget(self.author); form.addWidget(self.year)
        self.layout.addLayout(form)

        btns = QHBoxLayout()
        self.add_btn = QPushButton("➕ Qo‘shish")
        self.edit_btn = QPushButton("✏️ Tahrirlash")
        self.del_btn = QPushButton("🗑 O‘chirish")
        btns.addWidget(self.add_btn); btns.addWidget(self.edit_btn); btns.addWidget(self.del_btn)
        self.layout.addLayout(btns)

        self.add_btn.clicked.connect(self.add_book)
        self.edit_btn.clicked.connect(self.edit_book)
        self.del_btn.clicked.connect(self.del_book)
        self.load_table()

    def load_table(self):
        data = load_data(self.FILE)
        self.table.setRowCount(0)
        for r,b in enumerate(data):
            self.table.insertRow(r)
            self.table.setItem(r,0,QTableWidgetItem(b["title"]))
            self.table.setItem(r,1,QTableWidgetItem(b["author"]))
            self.table.setItem(r,2,QTableWidgetItem(b["year"]))

    def add_book(self):
        if self.title.text():
            data = load_data(self.FILE)
            data.append({"title": self.title.text(), "author": self.author.text(), "year": self.year.text()})
            save_data(self.FILE, data)
            self.title.clear(); self.author.clear(); self.year.clear()
            self.load_table()

    def edit_book(self):
        row = self.table.currentRow()
        if row >= 0:
            data = load_data(self.FILE)
            if self.title.text(): data[row]["title"] = self.title.text()
            if self.author.text(): data[row]["author"] = self.author.text()
            if self.year.text(): data[row]["year"] = self.year.text()
            save_data(self.FILE, data)
            self.load_table()

    def del_book(self):
        row = self.table.currentRow()
        if row >= 0:
            data = load_data(self.FILE)
            data.pop(row)
            save_data(self.FILE, data)
            self.load_table()


# ====== Asosiy oynani yaratish ======
class MainApp(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🟢 Oson loyihalar")
        self.resize(700, 400)
        self.addTab(ContactsTab(), "Kontaktlar")
        self.addTab(TodoTab(), "ToDo List")
        self.addTab(BooksTab(), "Kitoblar")



app = QApplication([])
win = MainApp()
win.show()
app.exec_()