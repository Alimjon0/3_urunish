# 📦 Mahsulotlar Bazasini Boshqarish (PyQt + MySQL)

Bu loyiha **PyQt5** va **MySQL** asosida yozilgan bo‘lib, foydalanuvchilarga mahsulotlar bazasini boshqarish imkoniyatini beradi.  

## ✨ Imkoniyatlar

- 🔍 Mahsulotlarni qidirish  
- 📂 Kategoriya bo‘yicha filterlash  
- ➕ Yangi mahsulot qo‘shish  
- ✏️ Ma’lumotlarni tahrirlash  
- 🗑️ Mahsulotni o‘chirish  
- 📄 Sahifalab ko‘rish (pagination)  

---

## 🖼️ Interfeys ko‘rinishi
![Search](images/img.png)

### 🔎 Qidirish va filterlash
![Search](./images/search.png)

### 📋 Mahsulotlar ro‘yxati
![Table](./images/table.png)

### ➕ Qo‘shish, ✏️ Tahrirlash va 🗑️ O‘chirish
![CRUD](./images/crud.png)

---

## ⚙️ O‘rnatish va Ishga Tushirish

### 1. Repository-ni klonlash
```bash
git clone https://github.com/username/mahsulotlar-bazasi.git
cd mahsulotlar-bazasi
```

### 2. Virtual environment yaratish va kutubxonalarni o‘rnatish

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

### 3. MySQL bazasini sozlash

* `database.sql` faylini MySQL-ga import qiling.
* `config.py` faylida **username**, **password** va **database** nomini moslang.

### 4. Dastur ishga tushirish

```bash
python main.py
```

---

## 🛠️ Texnologiyalar

* [Python 3.x](https://www.python.org/)
* [PyQt5](https://pypi.org/project/PyQt5/)
* [MySQL](https://www.mysql.com/)

---

## 📌 Kelajak rejalar

* 📑 Mahsulotlar bo‘yicha Excel/PDF export
* 👥 User login/register tizimi
* 🌐 Django/Flask orqali web versiya

---

## 👨‍💻 Muallif

* Alimjon
* ✉️ alimjonegamberdiyev0@gmail.com
* 🌍 [GitHub Profilingiz](https://github.com/username)

# temp_crud
