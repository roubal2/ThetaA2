from src.database_connection import get_connection
from src.models.order import Order
from src.models.orderItem import OrderItem
from src.models.user import User
from src.models.product import Product
import mysql.connector

def create_order_interactive(user_id, product_ids):
    conn = get_connection()
    try:
        conn.start_transaction()
        cursor = conn.cursor()

        user = User.read(user_id)
        if not user:
            print(f"Uživatel s ID {user_id} neexistuje.")
            conn.rollback()
            return None

        total_price = 0.0
        for prod_id in product_ids:
            product = Product.read(prod_id)
            if not product:
                print(f"Produkt s ID {prod_id} neexistuje. Přeskakuji.")
                continue
            total_price += product.price

        if total_price == 0:
            print("Žádné platné produkty, objednávka nebude vytvořena.")
            conn.rollback()
            return None

        if user.balance < total_price:
            print(f"Nedostatek peněz. Potřebujeme {total_price}, ale user má {user.balance}.")
            conn.rollback()
            return None

        new_order = Order(user_id=user.user_id, order_total=0.0)
        new_order.create_with_connection(conn)
        order_id = new_order.order_id

        for prod_id in product_ids:
            product = Product.read(prod_id)
            if not product:
                continue
            order_item = OrderItem(order_id=order_id, product_id=prod_id, quantity=1)
            order_item.create_with_connection(conn)

        sql_sum = """
                UPDATE orders
                SET order_total = (
                    SELECT SUM(p.price * oi.quantity)
                    FROM orderItems oi
                    JOIN products p ON oi.product_id = p.product_id
                    WHERE oi.order_id = %s
                )
                WHERE order_id = %s
            """
        cursor.execute(sql_sum, (order_id, order_id))

        new_balance = user.balance - total_price
        sql_user_update = "UPDATE users SET balance=%s WHERE user_id=%s"
        cursor.execute(sql_user_update, (new_balance, user.user_id))

        conn.commit()
        return order_id

    except mysql.connector.Error as db_err:
        print(f"DB Error (create_order_interactive): {db_err}")
        conn.rollback()
        return None
    except Exception as e:
        print(f"Obecná chyba (create_order_interactive): {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()
