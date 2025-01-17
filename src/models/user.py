# -*- coding: utf-8 -*-
from ..database_connection import get_connection
import mysql.connector

class User:
    def __init__(self, user_id=None, username=None, email=None, balance=0.0, is_active=False, created_at=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.balance = balance
        self.is_active = is_active
        self.created_at = created_at

    def create(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = """
                INSERT INTO users (username, email, balance, is_active, created_at)
                VALUES (%s, %s, %s, %s, NOW())
            """
            values = (self.username, self.email, self.balance, self.is_active)
            cursor.execute(sql, values)
            conn.commit()
            self.user_id = cursor.lastrowid
        except mysql.connector.Error as db_err:
            print(f"DB Error (User.create): {db_err}")
            conn.rollback()
        except Exception as e:
            print(f"Obecná chyba (User.create): {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def read(cls, user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM users WHERE user_id = %s"
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
        except mysql.connector.Error as e:
            print("DB Error:", e)
            return None
        finally:
            cursor.close()
            conn.close()

    def update(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = """
                UPDATE users
                SET username=%s, email=%s, balance=%s, is_active=%s
                WHERE user_id=%s
            """
            values = (self.username, self.email, self.balance, self.is_active, self.user_id)
            cursor.execute(sql, values)
            conn.commit()
        except mysql.connector.Error as e:
            print("DB Error:", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def delete(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = "DELETE FROM users WHERE user_id=%s"
            cursor.execute(sql, (self.user_id,))
            conn.commit()
        except mysql.connector.Error as e:
            print("DB Error:", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
