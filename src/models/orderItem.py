from src.database_connection import get_connection
import mysql.connector

class OrderItem:
    def __init__(self, order_id=None, product_id=None, quantity=1):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity

    def create(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = """INSERT INTO orderItems (order_id, product_id, quantity) VALUES (%s, %s, %s)"""
            cursor.execute(sql, (self.order_id, self.product_id, self.quantity))
            conn.commit()
        except mysql.connector.Error as db_err:
            print(f"DB Error (orderItem.create): {db_err}")
            conn.rollback()
        except Exception as e:
            print(f"Obecná chyba (orderItem.create): {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()