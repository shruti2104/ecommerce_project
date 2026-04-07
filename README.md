# 🛒 Flask E-commerce Project

A full-featured e-commerce backend built using Python and Flask.
This project demonstrates real-world backend concepts including authentication, cart management, orders, admin panel, and clean architecture.

---

## 🚀 Features

* 🔐 User Authentication (Register, Login, Logout)
* 📧 Email Verification
* 🔑 Forgot Password / Reset Password
* 🛒 Cart System

  * Guest cart (session-based)
  * User cart (database-based)
  * Auto merge on login
* 📦 Orders & Checkout
* 📄 Order Details Page
* 🛠️ Admin Panel

  * Add products
  * View products
  * View all orders
* 🧱 Clean Architecture (Services Layer)
* 🗄️ SQLite Database
* ⚙️ SQLAlchemy (ORM - partial integration)

---

## 🧰 Tech Stack

* Python 3.8+
* Flask
* Flask-SQLAlchemy
* SQLite
* Jinja2

---

## 📁 Project Structure

```
ecommerce_project/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── services/
│   ├── models/
│   └── decorators.py
│
├── database/
│   ├── db.py
│   ├── init_db.py
│   └── store.db
│
├── templates/
├── static/
├── main.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```
git clone <your-repo-url>
cd ecommerce_project
```

---

### 2️⃣ Create Virtual Environment

```
python3 -m venv venv
```

(If needed)

```
python3.8 -m venv venv
```

---

### 3️⃣ Activate Virtual Environment

**Linux / Mac:**

```
source venv/bin/activate
```

**Windows:**

```
venv\Scripts\activate
```

---

### 4️⃣ Install Dependencies

```
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

---

### 5️⃣ Setup Database

```
python database/init_db.py
```

---

### 6️⃣ Run the Application

```
python main.py
```

---

### 7️⃣ Open in Browser

```
http://127.0.0.1:5000
```

---

## 🔐 Admin Setup

To make a user admin:

```
sqlite3 database/store.db
```

Run:

```
UPDATE users SET is_admin = 1 WHERE email = 'your_email';
```

---

## ⚠️ Important Notes

* Do NOT commit `venv/`
* Do NOT commit `database/store.db`
* Always recreate virtual environment after cloning

---

## 📄 .gitignore Example

```
venv/
__pycache__/
*.pyc
database/store.db
.env
```

---

## 🧠 Architecture Overview

This project follows a layered approach:

* **Routes (Controllers)** → Handle HTTP requests
* **Services** → Business logic
* **Database Layer** → Data access
* **Templates** → UI rendering

---

## 🔮 Future Improvements

* JWT Authentication (API-based)
* Payment Integration
* Product Image Upload
* REST API (for frontend frameworks)
* Docker Setup
* Unit Testing

---

## 🤝 Contributing

Feel free to fork the repo and improve it.

---

## 📌 Author

Developed as a learning project for mastering Python backend development.

---
