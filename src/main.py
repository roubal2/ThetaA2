# -*- coding: utf-8 -*-
import sys
import mysql.connector
from src.models.user import User
from src.models.order import Order
from src.models.product import Product
from src.database_connection import get_connection
from src.services.order_service import create_order_interactive
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
        print("5) Zobrazení produktů")
        print("6) Odstranění produktu")
        print("7) Upravení ceny produktu")
        print("8) Konec")

        choice = input("Vyberte akci (1-8): ").strip()

        if choice == "1":
            handle_create_user()
        elif choice == "2":
            handle_create_order_trans()
        elif choice == "3":
            handle_generate_report()
        elif choice == "4":
            handle_import_menu()
        elif choice == "5":
            handle_view_products()
        elif choice == "6":
            handle_delete_product()
        elif choice == "7":
            handle_update_product()
        elif choice == "8":
            print("Ukončuji aplikaci.")
            sys.exit(0)
        else:
            print("Neplatná volba, zkus to znovu.")


def handle_create_user():
    conn = get_connection()
    try:
        username = input("Zadej uživatelské jméno: ").strip()
        email = input("Zadej email: ").strip()
        balance_str = input("Zadej počáteční zůstatek (balance): ").strip()
        is_active_str = input("Uživatel aktivní? (1 = ano, 0 = ne): ").strip()

        balance = float(balance_str)
        if balance < 0:
            print("Chyba: Zůstatek nesmí být záporný.")
            return

        is_active_int = int(is_active_str)
        if is_active_int not in (0, 1):
            print("Chyba: Zadej 0 nebo 1 pro is_active.")
            return
        is_active = bool(is_active_int)

        user = User(username=username, email=email, balance=balance, is_active=is_active)
        user.create_with_connection(conn)
        conn.commit()
        print(f"Uživatel {user.username} (ID {user.user_id}) vytvořen.")
    except ValueError:
        print("Chyba: Špatný formát čísla (balance nebo is_active).")
    except Exception as e:
        print(f"Chyba při vytváření uživatele: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()


def handle_create_order_trans():
    try:
        user_id_str = input("Zadej ID uživatele (customer_id): ").strip()
        user_id = int(user_id_str)

        items_input = input("Zadej položky objednávky ve formátu category_id:product_id;...: ").strip()
        if not items_input:
            print("Nebyla zadána žádná položka. Ruším objednávku.")
            return

        list_of_items = parse_category_product_input(items_input)
        if not list_of_items:
            print("Žádné platné položky byly zadány. Ruším objednávku.")
            return

        order_id = create_order_interactive(user_id, list_of_items)
        if order_id is not None:
            print(f"Objednávka (ID: {order_id}) byla úspěšně vytvořena.")
        else:
            print("Objednávka se nezaložila (uživatel nemá dostatek peněz nebo jiná chyba).")

    except ValueError:
        print("Chyba: Zadej platné číslo pro user_id.")
    except Exception as e:
        print(f"Chyba při vytváření objednávky: {e}")


def parse_category_product_input(items_input):
    result = []
    pairs = items_input.split(';')
    for pair in pairs:
        pair = pair.strip()
        if not pair:
            continue
        parts = pair.split(':')
        if len(parts) < 2:
            print(f"Varování: neplatný formát '{pair}'. Přeskakuji.")
            continue
        prod_id_str = parts[1]

        try:
            prod_id = int(prod_id_str)
            result.append(prod_id)
        except ValueError:
            print(f"Varování: product_id '{prod_id_str}' není platné číslo. Přeskakuji.")
    return result


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


def handle_view_products():
    try:
        products = Product.read_all(include_inactive=True)
        if not products:
            print("Žádné produkty nebyly nalezeny.")
            return
        print("\n--- Seznam Všech Produktů ---")
        for product in products:
            status = "Aktivní" if product.is_active else "Neaktivní"
            print(
                f"ID: {product.product_id}, Kategorie: {product.category_id}, Název: {product.product_name}, Cena: {product.price:.2f}, Stav: {status}")
    except Exception as e:
        print(f"Chyba při zobrazování produktů: {e}")


def handle_delete_product():
    conn = get_connection()
    try:
        product_id_str = input("Zadej ID produktu, který chceš smazat: ").strip()
        product_id = int(product_id_str)
        product = Product.read(product_id)
        if not product:
            print(f"Produkt s ID {product_id} neexistuje.")
            return

        confirmation = input(
            f"Jsi si jistý, že chceš smazat produkt '{product.product_name}' (ID {product.product_id})? (y/n): ").strip().lower()
        if confirmation != 'y':
            print("Smazání produktu bylo zrušeno.")
            return

        try:
            conn.start_transaction()

            Product.deactivate_with_connection(conn, product_id)

            conn.commit()
        except mysql.connector.Error as db_err:
            print(f"DB Error při deaktivaci produktu: {db_err}")
            conn.rollback()
        except Exception as e:
            print(f"Obecná chyba při deaktivaci produktu: {e}")
            conn.rollback()
        finally:
            conn.close()
            print("Databázové spojení bylo uzavřeno.")
    except ValueError:
        print("Chyba: Špatný formát čísla.")
    except mysql.connector.Error as db_err:
        print(f"DB Error při mazání produktu: {db_err}")
    except Exception as e:
        print(f"Obecná chyba při mazání produktu: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()


def handle_update_product():
    conn = get_connection()
    try:
        product_id_str = input("Zadej ID produktu, který chceš aktualizovat: ").strip()
        product_id = int(product_id_str)
        product = Product.read(product_id)
        if not product:
            print(f"Produkt s ID {product_id} neexistuje.")
            return

        print(f"Aktualizace Ceny Produktu ID {product.product_id}: {product.product_name}")
        new_price_str = input(f"Nová cena (aktuální: {product.price}): ").strip()

        if not new_price_str:
            print("Nebyla zadána žádná nová cena. Aktualizace byla zrušena.")
            return

        try:
            new_price = float(new_price_str)
            if new_price < 0:
                print("Chyba: Cena nemůže být záporná.")
                return
        except ValueError:
            print("Chyba: Špatný formát ceny. Zadej číslo (např. 29.99).")
            return

        product.price = new_price
        product.update_with_connection(conn)
        conn.commit()
        print(f"Cena Produktu ID {product.product_id} byl úspěšně aktualizován.")
    except ValueError:
        print("Chyba: Špatný formát čísla.")
    except mysql.connector.Error as db_err:
        print(f"DB Error při aktualizaci produktu: {db_err}")
    except Exception as e:
        print(f"Obecná chyba při aktualizaci produktu: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    main()
