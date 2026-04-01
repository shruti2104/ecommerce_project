from flask import Blueprint, render_template, request, redirect, url_for, session #, g
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta
from app.services.cart_service import add_to_cart_db, remove_cart_item
from app.services.order_service import create_order, get_order_details
from app.services.account_service import verify_email_db
from app.decorators import admin_required

import sqlite3
import uuid
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# @app.before_request
# def load_user():
#     g.user_id = session.get('user_id')

main = Blueprint('main', __name__)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return wrapper

@main.route('/')
def home():
    return render_template("home.html")

@main.route('/products')
def products():
    from database.db import get_connection
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    connection.close()

    return render_template("products.html", products=products)
    #return "Products page coming soon"

@main.route('/admin/add-product', methods=['GET', 'POST'])
@admin_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        if name != '' and price != '' and int(price) > 0 and description != '':
            from database.db import get_connection
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                "INSERT INTO products (name, price, description) VALUES (?, ?, ?)",
                (name, price, description)
            )

            connection.commit()
            connection.close()
            return redirect(url_for('main.products'))
    return render_template("add_product.html")

@main.route('/delete-product/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    if id > 0:
        from database.db import get_connection
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (id,))
        connection.commit()
        connection.close()

    return redirect(url_for('main.products'))

@main.route('/edit-product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    from database.db import get_connection
    connection = get_connection()
    cursor = connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        if name != '' and price != '' and description != '':
            cursor.execute(
                "UPDATE products SET name = ?, price = ?, description = ? WHERE id = ?",
                (name, price, description, id)
            )

            connection.commit()
            connection.close()

            return redirect(url_for('main.products'))

    if id > 0:
        cursor.execute("SELECT * FROM products WHERE id = ?", (id,))
        product = cursor.fetchone()
        connection.close()
        return render_template("edit_product.html",product=product)
    return redirect(url_for('main.products'))

@main.route('/product/<int:id>')
def product_detail(id):
    from database.db import get_connection
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products WHERE id = ?", (id,))
    product = cursor.fetchone()

    connection.close()

    return render_template("product_detail.html", product=product)

@main.route('/add-to-cart/<int:id>', methods=['POST'])
def add_to_cart(id):
    if 'user_id' in session:
        add_to_cart_db(session['user_id'], id)
    else:
        if 'cart' not in session:
            session['cart'] = []

        found = False
        for product in session['cart']:
            if product['product_id'] == id:
                product['qty'] += 1
                found = True
                break

        if not found:
            session['cart'].append({'product_id': id, 'qty': 1})

        session.modified = True

    return redirect(url_for('main.view_cart'))

@main.route('/cart')
def view_cart():
    if 'user_id' in session:
        from database.db import get_connection

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.*, c.quantity
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = ?
        """, (session['user_id'],))

        items = cursor.fetchall()
        conn.close()

    # ✅ Guest → session
    else:
        items = []

        if 'cart' in session:
            from database.db import get_connection
            conn = get_connection()
            cursor = conn.cursor()

            for item in session['cart']:
                cursor.execute(
                    "SELECT * FROM products WHERE id = ?",
                    (item['product_id'],)
                )
                product = cursor.fetchone()

                if product:
                    product = dict(product)
                    product['quantity'] = item['qty']
                    items.append(product)

            conn.close()

    # Common processing
    products = []
    final_total = 0

    for item in items:
        item = dict(item)
        item['subtotal'] = item['price'] * item['quantity']
        final_total += item['subtotal']
        products.append(item)
    return render_template("cart.html", products=products, final_total=final_total)

@main.route('/remove-from-cart/<int:id>', methods=['POST'])
def remove_from_cart(id):
    if 'user_id' in session:
        user_id = session['user_id']
        remove_cart_item(user_id, id)
    else:
        if 'cart' in session:
            session['cart'] = [item for item in session['cart'] if item['product_id'] != id]
            session.modified = True
            print(session['cart'])
    return redirect(url_for('main.view_cart'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        from database.db import get_connection
        connection = get_connection()
        cursor = connection.cursor()

        if name != "" and email != '' and password != "":
            hashed_password = generate_password_hash(password)
            token = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO users (name, email, password, verification_token) VALUES (?, ?, ?, ?)",
                (name, email, hashed_password, token)
            )
            verification_link = f"http://127.0.0.1:5000/verify/{token}"
            print("VERIFY LINK:", verification_link)
            connection.commit()
        connection.close()

        return "User registered successfully."#redirect(url_for('main.home'))
    else:
        return render_template('register.html')
def merge_cart(user_id):
    if 'cart' not in session:
        return

    from database.db import get_connection

    conn = get_connection()
    cursor = conn.cursor()

    for item in session['cart']:
        product_id = item['product_id']
        qty = item['qty']

        cursor.execute(
            "SELECT * FROM cart WHERE user_id = ? AND product_id = ?",
            (user_id, product_id)
        )
        existing = cursor.fetchone()

        if existing:
            cursor.execute(
                "UPDATE cart SET quantity = quantity + ? WHERE user_id = ? AND product_id = ?",
                (qty, user_id, product_id)
            )
        else:
            cursor.execute(
                "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
                (user_id, product_id, qty)
            )

    conn.commit()
    conn.close()

    session.pop('cart', None)
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        from database.db import get_connection
        connection = get_connection()
        cursor = connection.cursor()

        if email != "":
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()

        connection.close()

        if user and check_password_hash(user['password'], password):
            if not user['is_verified']:
                return "Please verify your email first"
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['is_admin'] = user['is_admin']
            merge_cart(user['id'])
            if session['is_admin']:
                return redirect(url_for('main.admin'))
            else:
                return redirect(url_for('main.home'))
        else:
            return "Invalid credentials"

    return render_template('login.html')

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))

@main.route('/verify/<token>')
def verify_email(token):
    if token:
        return verify_email_db(token)
    else:
        return "No token"

@main.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        from database.db import get_connection
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        reset_link = ""
        if user:
            token = str(uuid.uuid4())
            now = datetime.utcnow().isoformat()

            cursor.execute(
                "UPDATE users SET reset_token = ?, reset_token_created_at = ? WHERE email = ?",
                (token, now, email)
            )

            connection.commit()

            reset_link = f"http://127.0.0.1:5000/reset-password/{token}"

        connection.close()

        return reset_link

    return render_template('forgot_password.html')

@main.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    from database.db import get_connection
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE reset_token = ?", (token,))
    user = cursor.fetchone()

    if not user:
        return "Invalid or expired token"

    # Optional: expiry check (24 hours)
    created_at = datetime.fromisoformat(user['reset_token_created_at'])
    if datetime.utcnow() - created_at > timedelta(hours=24):
        return "Token expired"

    if request.method == 'POST':
        new_password = request.form['password']
        hashed_password = generate_password_hash(new_password)

        cursor.execute(
            "UPDATE users SET password = ?, reset_token = NULL, reset_token_created_at = NULL WHERE id = ?",
            (hashed_password, user['id'])
        )

        connection.commit()
        connection.close()

        return redirect(url_for('main.login'))

    connection.close()
    return render_template('reset_password.html', token=token)

@main.route('/checkout', methods=['POST'])
@login_required
def checkout():
    order_id = create_order(session['user_id'])

    if not order_id:
        return "Cart is empty"

    return redirect(url_for('main.orders'))

@main.route('/orders')
@login_required
def orders():
    from database.db import get_connection

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC",
        (session['user_id'],)
    )

    orders = cursor.fetchall()
    conn.close()

    return render_template("orders.html", orders=orders)

@main.route('/order/<int:order_id>')
@login_required
def order_details(order_id):
    user_id = session['user_id']
    response = get_order_details(order_id, user_id)

    if not response['order']:
        return "Order not found or unauthorized"
    return render_template(
        "order_details.html",
        order=response['order'],
        products=response['products'],
        total=response['total']
    )

@main.route('/admin')
@admin_required
def admin():
    return render_template('admin/dashboard.html')

@main.route('/admin/orders')
@admin_required
def admin_orders():
    from database.db import get_connection

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT o.*, u.email
        FROM orders o
        JOIN users u ON o.user_id = u.id
        ORDER BY o.id DESC
    """)

    orders = cursor.fetchall()
    conn.close()

    return render_template('admin/orders.html', orders=orders)

@main.route('/admin/products')
@admin_required
def admin_products():
    from database.db import get_connection

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    return render_template('admin/products.html', products=products)