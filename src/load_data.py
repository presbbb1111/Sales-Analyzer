import csv

from db import PROJECT_FOLDER, get_connection


def read_csv(filename):
    with open(PROJECT_FOLDER / "data" / filename) as f:
        return list(csv.DictReader(f))


def main():
    products = read_csv("products.csv")
    sales = read_csv("sales.csv")

    conn = get_connection()
    cursor = conn.cursor()

    # run schema.sql to recreate the tables
    schema = (PROJECT_FOLDER / "sql" / "schema.sql").read_text()
    for statement in schema.split(";"):
        if statement.strip():
            cursor.execute(statement)

    # products have to go in first since sales point to them
    for p in products:
        cursor.execute(
            "INSERT INTO products (name, category, price, stock, reorder_level) VALUES (%s, %s, %s, %s, %s)",
            (p["name"], p["category"], p["price"], p["stock"], p["reorder_level"])
        )

    for s in sales:
        cursor.execute(
            "INSERT INTO sales (product_id, quantity, sale_date) VALUES (%s, %s, %s)",
            (s["product_id"], s["quantity"], s["sale_date"])
        )

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Loaded {len(products)} products and {len(sales)} sales")


if __name__ == "__main__":
    main()