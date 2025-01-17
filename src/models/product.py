from src.database_connection import get_connection
import mysql.connector

class Product:
    def __init__(self, product_id=None, category_id=None, product_name=None, price=0.0, created_at=None):
        self.product_id = product_id
        self.category_id = category_id
        self.product_name = product_name
        self.price = price
        self.created_at = created_at

    def create_with_connection(self, existing_conn):
        cursor = existing_conn.cursor()
        try:
            sql = """
                INSERT INTO products (category_id, product_name, price, created_at)
                VALUES (%s, %s, %s, NOW())
            """
            values = (self.category_id, self.product_name, self.price)
            print(f"Inserting Product: category_id={self.category_id}, product_name={self.product_name}, price={self.price}")
            cursor.execute(sql, values)
            self.product_id = cursor.lastrowid
        except mysql.connector.Error as db_err:
            print(f"DB Error (Product.create): {db_err}")
            existing_conn.rollback()
            raise
        except Exception as e:
            print(f"Obecná chyba (Product.create): {e}")
            existing_conn.rollback()
            raise
        finally:
            cursor.close()

    @classmethod
    def read(cls, product_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM products WHERE product_id=%s"
            cursor.execute(sql, (product_id,))
            row = cursor.fetchone()
            if row:
                return cls(
                    product_id=row["product_id"],
                    category_id=row["category_id"],
                    product_name=row["product_name"],
                    price=row["price"],
                    created_at=row["created_at"]
                )
            return None
        except mysql.connector.Error as db_err:
            print(f"DB Error (Product.read): {db_err}")
            return None
        except Exception as e:
            print(f"Obecná chyba (Product.read): {e}")
            return None
        finally:
            cursor.close()
            conn.close()