from src.database_connection import get_connection
import mysql.connector

class Category:
    def __init__(self, category_id=None, category_name=None):
        self.category_id = category_id
        self.category_name = category_name

    def create(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = """INSERT INTO categories (category_name) VALUES (%s)"""
            cursor.execute(sql, (self.category_name,))
            conn.commit()
            self.category_id = cursor.lastrowid
        except mysql.connector.Error as e:
            print("DB Error:", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    # read/update/delete analogicky jako u User
