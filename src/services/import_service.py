import csv
import json
from src.models.category import Category
from src.models.product import Product

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
        # Očekávejme formát: [{"category_id":1,"product_name":"ABC","price":99.9,"product_status":"Confirmed"}, ...]
        for item in data:
            p = Product(
                category_id=item["category_id"],
                product_name=item["product_name"],
                price=item["price"],
                product_status=item["product_status"]
            )
            p.create()
    print("Import produktů z JSON úspěšně dokončen.")
