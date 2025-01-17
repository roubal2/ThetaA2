# -*- coding: utf-8 -*-
import sys
from src.models.user import User
from src.models.order import Order
from src.services.order_service import create_order_with_items
from src.services.import_service import (
    import_categories_csv, import_orders_csv,
    import_users_csv, import_order_items_json, import_products_json
)
from src.utils.report import generate_report

def main():
    while True:
        print("\n--- Hlavní menu ---")
        print("1) Přidat uživatele")
        print("2) Vytvořit objednávku (transakce)")
        print("3) Generovat report")
        print("4) Import dat (CSV/JSON)")
        print("5) Konec")

        choice = input("Vyberte akci (1-5): ").strip()

        if choice == "1":
            handle_create_user()
        elif choice == "2":
            handle_create_order_trans()
        elif choice == "3":
            handle_generate_report()
        elif choice == "4":
            handle_import_menu()
        elif choice == "5":
            print("Ukončuji aplikaci.")
            sys.exit(0)
        else:
            print("Neplatná volba, zkus to znovu.")

def handle_create_user():
    try:
        username = input("Zadej uživatelské jméno: ").strip()
        email = input("Zadej email: ").strip()
        balance_str = input("Zadej počáteční zůstatek (balance): ").strip()
        is_active_str = input("Uživatel aktivní? (1 = ano, 0 = ne): ").strip()

        # Ověření a konverze
        balance = float(balance_str)  # pokud je to neplatné, vyhodí ValueError
        if balance < 0:
            print("Chyba: Zůstatek nesmí být záporný.")
            return

        is_active_int = int(is_active_str)
        if is_active_int not in (0,1):
            print("Chyba: Zadej 0 nebo 1 pro is_active.")
            return
        is_active = bool(is_active_int)

        user = User(username=username, email=email, balance=balance, is_active=is_active)
        user.create()
        print(f"Uživatel {user.username} (ID {user.user_id}) vytvořen.")
    except ValueError:
        print("Chyba: Špatný formát čísla (balance nebo is_active).")
    except Exception as e:
        print(f"Chyba při vytváření uživatele: {e}")

def handle_create_order_trans():
    user_id_str = input("Zadej ID uživatele: ").strip()
    try:
        user_id = int(user_id_str)
        order_id = create_order_with_items(user_id, [(1,2), (2,1)])
        print(f"Objednávka (ID: {order_id}) byla úspěšně vytvořena.")
    except ValueError:
        print("Chyba: Zadej číselné user_id.")
    except Exception as e:
        print(f"Chyba při vytváření objednávky: {e}")

def handle_generate_report():
    try:
        data = generate_report()
        print("Souhrnný report:", data)
    except Exception as e:
        print(f"Chyba při generování reportu: {e}")

def handle_import_menu():
    print("\n--- Import dat ---")
    print("1) Import kategorií (CSV)")
    print("2) Import produktů (JSON)")
    print("3) Import uživatelů (CSV)")
    print("4) Import objednávek (CSV)")
    print("5) Import položek objednávek (JSON)")
    print("6) Import všeho (hromadně)")
    print("0) Zpět do hlavního menu")

    imp_choice = input("Vyberte akci (0-6): ").strip()

    if imp_choice == "1":
        csv_path = input("Cesta k CSV souboru kategorií: ").strip()
        import_categories_csv(csv_path)
    elif imp_choice == "2":
        json_path = input("Cesta k JSON souboru produktů: ").strip()
        import_products_json(json_path)
    elif imp_choice == "3":
        csv_path = input("Cesta k CSV souboru uživatelů: ").strip()
        import_users_csv(csv_path)
    elif imp_choice == "4":
        csv_path = input("Cesta k CSV souboru objednávek: ").strip()
        import_orders_csv(csv_path)
    elif imp_choice == "5":
        json_path = input("Cesta k JSON souboru položek objednávek (orderItems): ").strip()
        import_order_items_json(json_path)
    elif imp_choice == "6":
        print("Importuji vše (kategorie, produkty, uživatele, objednávky, orderItems)...")
        try:
            import_categories_csv("test_data/categories.csv")
            import_products_json("test_data/products.json")
            import_users_csv("test_data/users.csv")
            import_orders_csv("test_data/orders.csv")
            import_order_items_json("test_data/order_items.json")
            print("Všechny tabulky naplněny testovacími daty.")
        except Exception as e:
            print(f"Chyba při hromadném importu: {e}")
    elif imp_choice == "0":
        print("Návrat do hlavního menu.")
    else:
        print("Neplatná volba importu.")


if __name__ == "__main__":
    main()
