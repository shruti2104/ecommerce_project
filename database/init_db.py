import sqlite3

connection = sqlite3.connect("store.db")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT,
    image_url TEXT
)
""")
# cursor.execute("INSERT INTO products (name, price, description) VALUES ('Laptop', 800, 'Powerful laptop')")
# cursor.execute("INSERT INTO products (name, price, description) VALUES ('Headphones', 150, 'Noise cancelling')")
# cursor.execute("INSERT INTO products (name, price, description) VALUES ('Phone', 600, 'Latest smartphone')")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
# cursor.execute("""
#     ALTER TABLE users ADD COLUMN is_verified INTEGER DEFAULT 0;
# """)
# cursor.execute("""
#     ALTER TABLE users ADD COLUMN verification_token TEXT;
# """)

# cursor.execute("""
#     ALTER TABLE users ADD COLUMN reset_token TEXT;
# """)
# cursor.execute("""
#     ALTER TABLE users ADD COLUMN reset_token_created_at TEXT;
# """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    UNIQUE(user_id, product_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    total_amount REAL,
    created_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price REAL
)
""")

connection.commit()
connection.close()

print("Tables updated.")
