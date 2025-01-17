from src.database_connection import get_connection
import mysql.connector

class OrderItem:
    def __init__(self, order_id=None, product_id=None, quantity=1):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity

    def create_with_connection(self, existing_conn):
        cursor = existing_conn.cursor()
        try:
            sql = """INSERT INTO orderItems (order_id, product_id, quantity) VALUES (%s, %s, %s)"""
            print(f"Vkládám položku objednávky: order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity}")
            cursor.execute(sql, (self.order_id, self.product_id, self.quantity))
            self.order_item_id = cursor.lastrowid
        except mysql.connector.Error as db_err:
            print(f"DB Error (orderItem.create_with_connection): {db_err}")
            existing_conn.rollback()
            raise
        except Exception as e:
            print(f"Obecná chyba (orderItem.create_with_connection): {e}")
            existing_conn.rollback()
            raise
        finally:
            cursor.close()
