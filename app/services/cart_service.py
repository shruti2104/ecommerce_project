from database.db import get_connection

def add_to_cart_db(user_id, product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM cart WHERE user_id = ? AND product_id = ?",
        (user_id, product_id)
    )
    item = cursor.fetchone()

    if item:
        cursor.execute(
            "UPDATE cart SET quantity = quantity + 1 WHERE user_id = ? AND product_id = ?",
            (user_id, product_id)
        )
    else:
        cursor.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
            (user_id, product_id, 1)
        )

    conn.commit()
    conn.close()

def remove_cart_item(user_id, product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM cart WHERE user_id = ? AND product_id = ?",
        (user_id, product_id)
    )

    conn.commit()
    conn.close()

def get_cart_items(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.*, c.quantity
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    """, (user_id,))

    items = cursor.fetchall()
    conn.close()
    return items