import sqlite3

def init_db():
    conn = sqlite3.connect('pizza_orders.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            order_details TEXT,
            total_price INTEGER,
            address TEXT,
            user_name Text,
            status TEXT,
            courier_id INTEGER DEFAULT NULL
        )
    ''')
    conn.commit()
    conn.close()


def save_order(user_id, order_details, total_price, address, name):
    conn = sqlite3.connect('pizza_orders.db')
    c = conn.cursor()
    c.execute('INSERT INTO orders (user_id, order_details, total_price, address, user_name, status) VALUES (?, ?, ?, ?, ?, ?)',
              (user_id, order_details, total_price, address, name, "Замовлення оформлено"))
    conn.commit()
    conn.close()


def get_all_orders():
    conn = sqlite3.connect('pizza_orders.db')
    c = conn.cursor()
    # Fetch the order ID as well
    c.execute('SELECT id, user_id, order_details, total_price, address, user_name FROM orders WHERE status = "Замовлення оформлено"')
    orders = c.fetchall()
    conn.close()
    return orders


def get_order_status(order_id):
    conn = sqlite3.connect('pizza_orders.db')
    c = conn.cursor()
    c.execute('SELECT status FROM orders WHERE id=?', (order_id,))
    status = c.fetchone()
    conn.close()
    return status[0] if status else None


def update_order_status(order_id, courier_id, new_status):
    conn = sqlite3.connect('pizza_orders.db')
    c = conn.cursor()
    c.execute('UPDATE orders SET status=?, courier_id=? WHERE id=?', (new_status, courier_id, order_id))
    conn.commit()
    conn.close()



