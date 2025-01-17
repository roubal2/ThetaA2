import csv
import json
from src.models.user import User
from src.models.category import Category
from src.models.product import Product
from src.models.order import Order
from src.models.orderItem import OrderItem

def import_categories_csv(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        # Očekávejme, že CSV má např. jen jeden sloupec s názvem kategorie
        for row in reader:
            cat_name = row[0]
            c = Category(category_name=cat_name)
            c.create()
    print("Import kategorií z CSV úspěšně dokončen.")

def import_products_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Očekávejme formát: [{"category_id":1,"product_name":"ABC","price":99.9, ...]
        for item in data:
            p = Product(
                category_id=item["category_id"],
                product_name=item["product_name"],
                price=item["price"],
            )
            p.create()
    print("Import produktů z JSON úspěšně dokončen.")

def import_users_csv(csv_path):
    """
    Načítá uživatele z CSV, očekávejme např. formát se 4 sloupci:
    username,email,balance,is_active

    Příklad .csv:
    johndoe,john@doe.com,100.0,1
    janedoe,jane@doe.com,50.0,0
    """
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            username = row[0]
            email = row[1]
            balance = float(row[2])
            is_active = bool(int(row[3]))
            u = User(username=username, email=email, balance=balance, is_active=is_active)
            u.create()
    print("Import uživatelů z CSV úspěšně dokončen.")

def import_orders_csv(csv_path):
    """
    Načítá objednávky z CSV, očekávejme např. formát se 2 sloupci:
    user_id,order_total

    Příklad .csv:
    1,150.0
    2,299.9

    Pozn.: order_date může být nastaveno default (NOW()) v DB,
    nebo sem lze přidat i datum, dle vaší tabulky a preference.
    """
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
            o.create()
    print("Import objednávek z CSV úspěšně dokončen.")

def import_order_items_json(json_path):
    """
    Příklad JSON formátu pro orderItems:
    [
      {"order_id":1, "product_id":2, "quantity":3},
      {"order_id":1, "product_id":5, "quantity":2},
      {"order_id":2, "product_id":2, "quantity":1}
    ]
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            oi = OrderItem(
                order_id=item["order_id"],
                product_id=item["product_id"],
                quantity=item["quantity"]
            )
            oi.create()
    print("Import orderItems z JSON úspěšně dokončen.")