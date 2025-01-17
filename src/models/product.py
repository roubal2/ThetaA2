from src.database_connection import get_connection
import mysql.connector

class Product:
    def __init__(self, product_id=None, category_id=None, product_name=None, price=0.0, created_at=None, is_available=1):
        self.product_id = product_id
        self.category_id = category_id
        self.product_name = product_name
        self.price = price
        self.created_at = created_at
        self.is_available = is_available

    def create_with_connection(self, existing_conn):
        cursor = existing_conn.cursor()
        try:
            sql = """
                INSERT INTO products (category_id, product_name, price, created_at, is_available)
                VALUES (%s, %s, %s, NOW(), %s)
            """
            values = (self.category_id, self.product_name, self.price, self.is_available)
            print(f"Vkládám produkt: category_id={self.category_id}, product_name={self.product_name}, price={self.price}, is_active={self.is_available}")
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

    def update_with_connection(self, existing_conn):
        cursor = existing_conn.cursor()
        try:
            sql = """
                UPDATE products
                SET price=%s
                WHERE product_id=%s
            """
            values = (self.price, self.product_id)
            print(
                f"Upravuji produkt s ID {self.product_id}: , nová cena={self.price}")
            cursor.execute(sql, values)
        except mysql.connector.Error as db_err:
            print(f"DB Error (Product.update_with_connection): {db_err}")
            existing_conn.rollback()
            raise
        except Exception as e:
            print(f"Obecná chyba (Product.update_with_connection): {e}")
            existing_conn.rollback()
            raise
        finally:
            cursor.close()

    @classmethod
    def toggle_availability_with_connection(cls, existing_conn, product_id):
        cursor = existing_conn.cursor()
        try:
            cursor.execute("SELECT is_available FROM products WHERE product_id = %s", (product_id,))
            result = cursor.fetchone()
            if not result:
                print(f"Produkt ID {product_id} nebyl nalezen.")
                return

            current_status = result[0]
            new_status = 0 if current_status == 1 else 1

            sql = "UPDATE products SET is_available = %s WHERE product_id = %s"
            cursor.execute(sql, (new_status, product_id))
            status_text = "deaktivován" if new_status == 0 else "aktivován"
            print(f"Produkt ID {product_id} byl úspěšně {status_text}.")
        except mysql.connector.Error as db_err:
            print(f"DB Error (Product.toggle_availability_with_connection): {db_err}")
            existing_conn.rollback()
            raise
        except Exception as e:
            print(f"Obecná chyba (Product.toggle_availability_with_connection): {e}")
            existing_conn.rollback()
            raise
        finally:
            cursor.close()

    @classmethod
    def read(cls, product_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM products WHERE product_id=%s AND is_available = TRUE"
            cursor.execute(sql, (product_id,))
            row = cursor.fetchone()
            if row:
                return cls(
                    product_id=row["product_id"],
                    category_id=row["category_id"],
                    product_name=row["product_name"],
                    price=row["price"],
                    created_at=row["created_at"],
                    is_available=row["is_available"]
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

    @classmethod
    def read_all(cls, include_inactive=False):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            if include_inactive:
                cursor.execute("SELECT * FROM products")
            else:
                cursor.execute("SELECT * FROM products WHERE is_available = TRUE")
            rows = cursor.fetchall()
            products = [cls(
                product_id=row["product_id"],
                category_id=row["category_id"],
                product_name=row["product_name"],
                price=row["price"],
                created_at=row["created_at"],
                is_available=row["is_available"]
            ) for row in rows]
            return products
        except mysql.connector.Error as db_err:
            print(f"DB Error (Product.read_all): {db_err}")
            return []
        except Exception as e:
            print(f"Obecná chyba (Product.read_all): {e}")
            return []
        finally:
            cursor.close()
            conn.close()
