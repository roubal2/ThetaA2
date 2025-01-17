import csv
import json
import mysql.connector
from src.models.user import User
from src.models.category import Category
from src.models.product import Product
from src.models.order import Order
from src.models.orderItem import OrderItem
from src.database_connection import get_connection

def import_categories_csv(csv_path):
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                cat_name = row[0]
                c = Category(category_name=cat_name)
                c.create()
        print("Import kategorií z CSV úspěšně dokončen.")
    except FileNotFoundError:
        print(f"Chyba: Soubor {csv_path} nebyl nalezen.")
    except IndexError:
        print("Chyba: CSV soubor nemá očekávaný formát (nedostatek sloupců).")
    except Exception as e:
        print(f"Chyba při importu kategorií: {e}")


# src/services/import_service.py

def import_products_json(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            products_data = json.load(file)

        conn = get_connection()
        cursor = conn.cursor()

        for product in products_data:
            is_available = product.get('is_available', 1)
            new_product = Product(
                category_id=product.get('category_id'),
                product_name=product.get('product_name'),
                price=product.get('price'),
                is_available=is_available
            )
            print(f"Importuji produkt: Název={new_product.product_name}")
            new_product.create_with_connection(conn)

        conn.commit()
        print(f"Úspěšně importováno {len(products_data)} produktů.")
    except Exception as e:
        print(f"Chyba při importu produktů: {e}")
        if conn:
            conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


def import_users_csv(csv_path):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                if not row or len(row) < 4:
                    print("Varování: řádek je prázdný nebo neúplný, přeskočen.")
                    continue
                username = row[0]
                email = row[1]
                balance = float(row[2])
                is_active = bool(int(row[3]))
                u = User(username=username, email=email, balance=balance, is_active=is_active)
                u.create_with_connection(conn)
        conn.commit()
        print("Import uživatelů z CSV úspěšně dokončen.")
    except FileNotFoundError:
        print(f"Chyba: Soubor {csv_path} nebyl nalezen.")
    except IndexError:
        print("Chyba: CSV nemá dostatek sloupců.")
    except ValueError:
        print("Chyba: Špatný formát čísla (balance nebo is_active).")
    except Exception as e:
        print(f"Chyba při importu uživatelů: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def import_orders_csv(csv_path):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                user_id = int(row[0])
                order_total = float(row[1])
                order_status = row[2]
                order_date = row[3]
                o = Order(
                    user_id=user_id,
                    order_total=order_total,
                    order_status=order_status,
                    order_date=order_date
                )
                o.create_with_connection(conn)
        conn.commit()
        print("Import objednávek z CSV úspěšně dokončen.")
    except FileNotFoundError:
        print(f"Chyba: Soubor {csv_path} nebyl nalezen.")
    except IndexError:
        print("Chyba: CSV nemá dostatek sloupců.")
    except ValueError:
        print("Chyba: Špatný formát čísla (user_id nebo order_total).")
    except Exception as e:
        print(f"Chyba při importu objednávek: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


# src/services/import_service.py

def import_order_items_json(json_path):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            order_items_data = json.load(file)

        for item in order_items_data:
            order_id = item.get('order_id')
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)

            cursor.execute("SELECT 1 FROM products WHERE product_id = %s AND is_available = 1", (product_id,))
            if not cursor.fetchone():
                print(f"Varování: Produkt s ID {product_id} neexistuje nebo není dostupný. Přeskakuji položku.")
                continue

            new_order_item = OrderItem(
                order_id=order_id,
                product_id=product_id,
                quantity=quantity
            )
            print(f"Importuji položku objednávky: order_id={order_id}, product_id={product_id}")
            new_order_item.create_with_connection(conn)

        conn.commit()
        print(f"Úspěšně importováno {len(order_items_data)} položek objednávek.")
    except FileNotFoundError:
        print(f"Chyba: Soubor {json_path} nebyl nalezen.")
    except json.JSONDecodeError:
        print("Chyba: Nesprávný formát JSON souboru.")
    except mysql.connector.Error as db_err:
        print(f"DB Error při importu order_items: {db_err}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"Obecná chyba při importu order_items: {e}")
        if conn:
            conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()
            print("Databázové spojení bylo uzavřeno.")
