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
        valid_product_ids = []
        for prod_id in product_ids:
            product = Product.read(prod_id)
            if not product:
                print(f"Produkt s ID {prod_id} neexistuje. Přeskakuji.")
                continue
            total_price += product.price
            valid_product_ids.append(prod_id)

        if total_price == 0:
            print("Žádné platné produkty, objednávka nebude vytvořena.")
            conn.rollback()
            return None

        if user.balance >= total_price:
            order_status = 'In-Transit'
            new_balance = user.balance - total_price
        else:
            order_status = 'Refunded'
            new_balance = user.balance

        print(f"Tvořím objednávku, status: {order_status}, total_price: {total_price}, user_balance: {user.balance}")

        new_order = Order(user_id=user.user_id, order_total=total_price, order_status=order_status)
        new_order.create_with_connection(conn)
        order_id = new_order.order_id

        if order_status == 'In-Transit':
            for prod_id in valid_product_ids:
                order_item = OrderItem(order_id=order_id, product_id=prod_id, quantity=1)
                order_item.create_with_connection(conn)
            user.balance = new_balance
            user.update_balance_with_connection(conn)

        conn.commit()
        print("Objednávka byla úspěšně vytvořena a už je na cestě.")
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
