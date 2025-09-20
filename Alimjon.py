import sys
import pymysql
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QLabel, QComboBox, QTableWidget,
    QPushButton, QTableWidgetItem, QMessageBox
)

PAGE_SIZE = 5


class Mahsulotlar(QWidget):
    def __init__(self, connection, cursor):
        super().__init__()
        self.connection = connection
        self.cursor = cursor
        self.CURRENT_PAGE = 0

        self.setWindowTitle("Mahsulotlar bazasi (CRUD + Qidirish)")
        self.resize(750, 500)

        # 🔍 Qidirish va filter
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Mahsulot nomi...")

        self.category_box = QComboBox()
        self.load_category()

        self.btn_search = QPushButton("Qidirish")
        self.btn_refresh = QPushButton("Yangilash")
        self.btn_add = QPushButton("Qo‘shish")
        self.btn_edit = QPushButton("Tahrirlash")
        self.btn_delete = QPushButton("O‘chirish")

        # Jadval
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nomi", "Narxi", "Kategoriya"])
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 220)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 200)

        # Layout
        top = QHBoxLayout()
        top.addWidget(QLabel("Kategoriya:"))
        top.addWidget(self.category_box)
        top.addWidget(self.search_box)
        top.addWidget(self.btn_search)
        top.addWidget(self.btn_refresh)

        bottom = QHBoxLayout()
        bottom.addWidget(self.btn_add)
        bottom.addWidget(self.btn_edit)
        bottom.addWidget(self.btn_delete)

        layout = QVBoxLayout()
        layout.addLayout(top)
        layout.addWidget(self.table)
        layout.addLayout(bottom)
        self.setLayout(layout)

        # Button eventlar
        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_search.clicked.connect(self.search)
        self.btn_add.clicked.connect(self.add_item)
        self.btn_edit.clicked.connect(self.edit_item)
        self.btn_delete.clicked.connect(self.remove_item)

        self.load_data()

    # --------- Bazadan kategoriyalarni olish
    def load_category(self):
        try:
            self.cursor.execute("SELECT name FROM categories ORDER BY id")
            rows = self.cursor.fetchall()
            self.categories_box.clear()
            self.categories_box.addItem("Barchasi")
            for row in rows:
                self.categories_box.addItem(row[0])
        except Exception as e:
            QMessageBox.critical(self, "Xato", f"Kategoriyalarni yuklashda xato:\n{e}")

    # --------- Mahsulotlarni yuklash
    def load_data(self):
        sql = """
            SELECT p.id, p.name, p.price, c.name
            FROM products p
            LEFT JOIN categories c ON p.category_id=c.id
            ORDER BY p.id DESC
        """
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.table.setRowCount(0)
        for r, row in enumerate(data):
            self.table.insertRow(r)
            for c, value in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(value) if value is not None else ""))

    # --------- Qidirish
    def search(self):
        name = self.search_box.text().strip()
        cat = self.category_box.currentText()

        sql = """
            SELECT p.id, p.name, p.price, c.name
            FROM products p
            LEFT JOIN categories c ON p.category_id=c.id
            WHERE 1=1
        """
        params = []

        if name:
            sql += " AND p.name LIKE %s"
            params.append(f"%{name}%")
        if cat and cat != "Barchasi":
            sql += " AND c.name=%s"
            params.append(cat)

        sql += " ORDER BY p.id DESC"

        self.cursor.execute(sql, tuple(params))
        data = self.cursor.fetchall()

        self.table.setRowCount(0)
        for r, row in enumerate(data):
            self.table.insertRow(r)
            for c, value in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(value) if value else ""))

    # --------- Qo‘shish
    def add_item(self):
        name = self.search_box.text().strip()
        cat = self.category_box.currentText()
        if not name:
            QMessageBox.warning(self, "Ogohlantirish", "Mahsulot nomini kiriting!")
            return

        cat_id = None
        if cat and cat != "Barchasi":
            self.cursor.execute("SELECT id FROM categories WHERE name=%s", (cat,))
            r = self.cursor.fetchone()
            cat_id = r[0] if r else None

        self.cursor.execute(
            "INSERT INTO products(name, price, category_id) VALUES(%s, %s, %s)",
            (name, 0, cat_id)
        )
        self.connection.commit()
        self.load_data()
        self.search_box.clear()

    # --------- Tahrirlash
    def edit_item(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ogohlantirish", "Tahrirlash uchun yozuvni tanlang!")
            return

        id_ = int(self.table.item(row, 0).text())
        new_name = self.search_box.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Ogohlantirish", "Yangi nomni kiriting!")
            return

        self.cursor.execute("UPDATE products SET name=%s WHERE id=%s", (new_name, id_))
        self.connection.commit()
        self.load_data()
        self.search_box.clear()

    # --------- O‘chirish
    def remove_item(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ogohlantirish", "O‘chirish uchun yozuvni tanlang!")
            return

        id_ = int(self.table.item(row, 0).text())
        self.cursor.execute("DELETE FROM products WHERE id=%s", (id_,))
        self.connection.commit()
        self.load_data()


if __name__ == "__main__":
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="admin",
            database="organization_db"
        )
        cursor = connection.cursor()
        print("✅ Baza ulandi")
    except Exception as e:
        print("❌ Baza bilan ulanishda xato:", e)
        sys.exit()

    app = QApplication(sys.argv)
    oyna = Mahsulotlar(connection, cursor)
    oyna.show()
    sys.exit(app.exec_())
