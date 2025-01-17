import mysql.connector
from src.database_connection import get_connection
class Order:
    def __init__(self, order_id=None, user_id=None, order_total=0.0, order_date=None):
        self.order_id = order_id
        self.user_id = user_id
        self.order_total = order_total
        self.order_date = order_date

    def create(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = """INSERT INTO orders (user_id, order_total, order_date) VALUES (%s, %s, NOW())"""
            cursor.execute(sql, (self.user_id, self.order_total))
            conn.commit()
            self.order_id = cursor.lastrowid
        except mysql.connector.Error as e:
            print("DB Error:", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    # read/update/delete analogicky
