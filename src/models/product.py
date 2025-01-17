from src.database_connection import get_connection
import mysql.connector

class Product:
    def __init__(self, product_id=None, category_id=None, product_name=None, price=0.0, product_status=None, created_at=None):
        self.product_id = product_id
        self.category_id = category_id
        self.product_name = product_name
        self.price = price
        self.product_status = product_status
        self.created_at = created_at

    def create(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = """
                INSERT INTO products (category_id, product_name, price, created_at)
                VALUES (%s, %s, %s, NOW())
            """
            values = (self.category_id, self.product_name, self.price)
            cursor.execute(sql, values)
            conn.commit()
            self.product_id = cursor.lastrowid
        except mysql.connector.Error as db_err:
            print(f"DB Error (Product.create): {db_err}")
            conn.rollback()
        except Exception as e:
            print(f"Obecná chyba (Product.create): {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
