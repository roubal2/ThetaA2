import mysql.connector
from src.database_connection import get_connection

class User:
    def __init__(self, user_id=None, username=None, email=None, balance=0.0, is_active=False, created_at=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.balance = balance
        self.is_active = is_active
        self.created_at = created_at

    def create_with_connection(self, existing_conn):
        cursor = existing_conn.cursor()
        try:
            sql = """
                INSERT INTO users (username, email, balance, is_active, created_at)
                VALUES (%s, %s, %s, %s, NOW())
            """
            values = (self.username, self.email, self.balance, self.is_active)
            print(f"Inserting User: username={self.username}, email={self.email}, balance={self.balance}, is_active={self.is_active}")
            cursor.execute(sql, values)
            self.user_id = cursor.lastrowid
        except mysql.connector.Error as db_err:
            print(f"DB Error (User.create_with_connection): {db_err}")
            existing_conn.rollback()
            raise
        except Exception as e:
            print(f"Obecná chyba (User.create_with_connection): {e}")
            existing_conn.rollback()
            raise
        finally:
            cursor.close()

    @classmethod
    def read(cls, user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM users WHERE user_id=%s"
            cursor.execute(sql, (user_id,))
            row = cursor.fetchone()
            if row:
                return cls(
                    user_id=row["user_id"],
                    username=row["username"],
                    email=row["email"],
                    balance=row["balance"],
                    is_active=row["is_active"],
                    created_at=row["created_at"]
                )
            return None
        except mysql.connector.Error as db_err:
            print(f"DB Error (User.read): {db_err}")
            return None
        except Exception as e:
            print(f"Obecná chyba (User.read): {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def update_balance_with_connection(self, existing_conn):
        cursor = existing_conn.cursor()
        try:
            sql = "UPDATE users SET balance = %s WHERE user_id = %s"
            print(f"Updating User Balance: new_balance={self.balance}, user_id={self.user_id}")
            cursor.execute(sql, (self.balance, self.user_id))
        except mysql.connector.Error as db_err:
            print(f"DB Error (User.update_balance_with_connection): {db_err}")
            existing_conn.rollback()
            raise
        except Exception as e:
            print(f"Obecná chyba (User.update_balance_with_connection): {e}")
            existing_conn.rollback()
            raise
        finally:
            cursor.close()