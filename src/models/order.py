import mysql.connector
from src.database_connection import get_connection
class Order:
    def __init__(self, order_id=None, user_id=None, order_total=0.0,
                 order_status="Confirmed", order_date=None):
        self.order_id = order_id
        self.user_id = user_id
        self.order_total = order_total
        self.order_status = order_status
        self.order_date = order_date

    def create_with_connection(self, existing_conn):
        cursor = existing_conn.cursor()
        try:
            sql = """INSERT INTO orders (user_id, order_total, order_status, order_date)
                         VALUES (%s, %s, %s, NOW())"""
            print(f"Vkládám uživatele: user_id={self.user_id}, order_total={self.order_total}, order_status={self.order_status}")
            cursor.execute(sql, (self.user_id, self.order_total, self.order_status))
            self.order_id = cursor.lastrowid
        except mysql.connector.Error as db_err:
            print(f"DB Error (Order.create_with_connection): {db_err}")
            existing_conn.rollback()
            raise
        except Exception as e:
            print(f"Obecná chyba (Order.create_with_connection): {e}")
            existing_conn.rollback()
            raise
        finally:
            cursor.close()