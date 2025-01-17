from src.database_connection import get_connection
import mysql.connector

def generate_report():
    """
    Vygeneruje souhrnné statistiky z min. 3 tabulek.
    Pro ukázku: počet uživatelů, počet objednávek, celkový obrat.
    Můžete přidat libovolné agregace.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    result = {}
    try:
        # Počet aktivních uživatelů
        cursor.execute("SELECT COUNT(*) AS cnt FROM users WHERE is_active=1")
        row = cursor.fetchone()
        result["active_users"] = row["cnt"] if row else 0

        # Počet objednávek
        cursor.execute("SELECT COUNT(*) AS cnt FROM orders")
        row = cursor.fetchone()
        result["orders_count"] = row["cnt"] if row else 0

        # Součet order_total (obrat)
        cursor.execute("SELECT SUM(order_total) AS sum_total FROM orders")
        row = cursor.fetchone()
        result["total_revenue"] = row["sum_total"] if row["sum_total"] else 0

    except mysql.connector.Error as e:
        print("DB Error:", e)
    finally:
        cursor.close()
        conn.close()

    return result
