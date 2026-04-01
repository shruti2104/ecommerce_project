from database.db import get_connection
from datetime import datetime

def create_order(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.product_id, c.quantity, p.price
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    """, (user_id,))

    cart_items = cursor.fetchall()

    if not cart_items:
        return None

    total = sum(item['price'] * item['quantity'] for item in cart_items)

    cursor.execute(
        "INSERT INTO orders (user_id, total_amount, created_at) VALUES (?, ?, ?)",
        (user_id, total, datetime.utcnow().isoformat())
    )

    order_id = cursor.lastrowid

    for item in cart_items:
        cursor.execute(
            """
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (?, ?, ?, ?)
            """,
            (order_id, item['product_id'], item['quantity'], item['price'])
        )

    cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()

    return order_id

def get_order_details(order_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM orders WHERE id = ? AND user_id = ?",
        (order_id, user_id)
    )
    order = cursor.fetchone()
    products = []
    total = 0

    if order:
        cursor.execute("""
            SELECT p.name, p.price, oi.quantity, oi.price as order_price
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        """, (order_id,))

        items = cursor.fetchall()
        conn.close()


        for item in items:
            item = dict(item)
            item['subtotal'] = item['order_price'] * item['quantity']
            total += item['subtotal']
            products.append(item)

    return {'order': order, 'products': products, 'total': total}