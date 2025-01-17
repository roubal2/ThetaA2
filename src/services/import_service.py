import csv
import json
from src.models.user import User
from src.models.category import Category
from src.models.product import Product
from src.models.order import Order
from src.models.orderItem import OrderItem

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


def import_products_json(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                p = Product(
                    category_id=item["category_id"],
                    product_name=item["product_name"],
                    price=item["price"]
                )
                p.create()
        print("Import produktů z JSON úspěšně dokončen.")
    except FileNotFoundError:
        print(f"Chyba: Soubor {json_path} nebyl nalezen.")
    except KeyError as e:
        print(f"Chyba: V JSON chybí klíč {e}")
    except json.JSONDecodeError:
        print("Chyba: Soubor není validní JSON.")
    except Exception as e:
        print(f"Chyba při importu produktů: {e}")

def import_users_csv(csv_path):
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
                u.create()
        print("Import uživatelů z CSV úspěšně dokončen.")
    except FileNotFoundError:
        print(f"Chyba: Soubor {csv_path} nebyl nalezen.")
    except IndexError:
        print("Chyba: CSV nemá dostatek sloupců.")
    except ValueError:
        print("Chyba: Špatný formát čísla (balance nebo is_active).")
    except Exception as e:
        print(f"Chyba při importu uživatelů: {e}")

def import_orders_csv(csv_path):
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
                o.create_with_connection()
        print("Import objednávek z CSV úspěšně dokončen.")
    except FileNotFoundError:
        print(f"Chyba: Soubor {csv_path} nebyl nalezen.")
    except IndexError:
        print("Chyba: CSV nemá dostatek sloupců.")
    except ValueError:
        print("Chyba: Špatný formát čísla (user_id nebo order_total).")
    except Exception as e:
        print(f"Chyba při importu objednávek: {e}")

def import_order_items_json(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                oi = OrderItem(
                    order_id=item["order_id"],
                    product_id=item["product_id"],
                    quantity=item["quantity"]
                )
                oi.create_with_connection()
        print("Import orderItems z JSON úspěšně dokončen.")
    except FileNotFoundError:
        print(f"Chyba: Soubor {json_path} nebyl nalezen.")
    except KeyError as e:
        print(f"Chyba: V JSON chybí klíč {e}")
    except json.JSONDecodeError:
        print("Chyba: Soubor není validní JSON.")
    except Exception as e:
        print(f"Chyba při importu order_items: {e}")