# -*- coding: utf-8 -*-
import sys
from src.models.user import User
from src.models.order import Order
from src.services.order_service import create_order_with_items
from src.services.import_service import import_categories_csv, import_orders_csv,import_users_csv,import_order_items_json,import_products_json
from src.utils.report import generate_report

def main():
    while True:
        print("\n--- Hlavní menu ---")
        print("1) Přidat uživatele")
        print("2) Vytvořit objednávku (transakce)")
        print("3) Generovat report")
        print("4) Import dat (CSV/JSON)")
        print("5) Konec")

        choice = input("Vyberte akci: ")

        if choice == "1":
            username = input("Zadej uživatelské jméno: ")
            email = input("Zadej email: ")
            user = User(username=username, email=email)
            user.create()
            print(f"Uživatel {user.username} (ID {user.user_id}) vytvořen.")

        elif choice == "2":
            user_id = input("Zadej ID uživatele: ")
            try:
                order_id = create_order_with_items(user_id, [ (1,2), (2,1) ])
                print(f"Objednávka (ID: {order_id}) byla úspěšně vytvořena.")
            except Exception as e:
                print("Chyba při vytváření objednávky:", e)

        elif choice == "3":
            try:
                report_data = generate_report()
                print("Souhrnný report:", report_data)
            except Exception as e:
                print("Chyba při generování reportu:", e)
        elif choice == "4":
            print("\n--- Import dat ---")
            print("1) Import kategorií (CSV)")
            print("2) Import produktů (JSON)")
            print("3) Import uživatelů (CSV)")
            print("4) Import objednávek (CSV)")
            print("5) Import položek objednávek (JSON)")
            print("6) Import všeho (hromadně)")
            print("0) Zpět do hlavního menu")

            imp_choice = input("Vyberte akci: ")

            if imp_choice == "1":
                csv_path = input("Cesta k CSV souboru kategorií: ")
                import_categories_csv(csv_path)
            elif imp_choice == "2":
                json_path = input("Cesta k JSON souboru produktů: ")
                import_products_json(json_path)
            elif imp_choice == "3":
                csv_path = input("Cesta k CSV souboru uživatelů: ")
                import_users_csv(csv_path)
            elif imp_choice == "4":
                csv_path = input("Cesta k CSV souboru objednávek: ")
                import_orders_csv(csv_path)
            elif imp_choice == "5":
                json_path = input("Cesta k JSON souboru položek objednávek (orderItems): ")
                import_order_items_json(json_path)
            elif imp_choice == "6":
                print("Importuji vše (kategorie, produkty, uživatele, objednávky, orderItems)...")
                import_categories_csv("test_data/categories.csv")
                import_products_json("test_data/products.json")
                import_users_csv("test_data/users.csv")
                import_orders_csv("test_data/orders.csv")
                import_order_items_json("test_data/order_items.json")
                print("Všechny tabulky naplněny testovacími daty.")
            elif imp_choice == "0":
                print("Návrat do hlavního menu.")
            else:
                print("Neplatná volba importu.")
        elif choice == "5":
            print("Ukončuji aplikaci.")
            sys.exit(0)
        else:
            print("Neplatná volba.")

if __name__ == "__main__":
    main()
