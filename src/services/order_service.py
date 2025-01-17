from src.database_connection import get_connection
from src.models.order import Order
from src.models.orderItem import OrderItem
import mysql.connector

def create_order_with_items(user_id, items):
    """
    Vytvoří novou objednávku pro daného uživatele (user_id).
    'items' je list tuple (product_id, quantity).
    Vše probíhá v jedné transakci.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        conn.start_transaction()
        # 1) Vytvořit záznam v `orders`
        sql_order = """INSERT INTO orders (user_id, order_date) VALUES (%s, NOW())"""
        cursor.execute(sql_order, (user_id,))
        new_order_id = cursor.lastrowid

        # 2) Vložit řádky do `orderItems`
        for (p_id, qty) in items:
            sql_item = """INSERT INTO orderItems (order_id, product_id, quantity)
                          VALUES (%s, %s, %s)"""
            cursor.execute(sql_item, (new_order_id, p_id, qty))

        # 3) Přepočítat `order_total` (join s products)
        sql_update_total = """
            UPDATE orders
            SET order_total = (
                SELECT SUM(p.price * oi.quantity)
                FROM orderItems oi
                JOIN products p ON oi.product_id = p.product_id
                WHERE oi.order_id = %s
            )
            WHERE order_id = %s
        """
        cursor.execute(sql_update_total, (new_order_id, new_order_id))

        conn.commit()
        return new_order_id
    except mysql.connector.Error as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
