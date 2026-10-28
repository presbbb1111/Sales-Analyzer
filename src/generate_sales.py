import csv
import random
from datetime import date, timedelta
from pathlib import Path

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
PRODUCTS_FILE = PROJECT_FOLDER / "data" / "products.csv"
SALES_FILE = PROJECT_FOLDER / "data" / "sales.csv"

# product_id: how much more often it sells (everything else is 1)
popular = {1: 8, 7: 7, 8: 6, 12: 5, 13: 5, 16: 4, 20: 4, 30: 4}


def main():
    random.seed(42)  # same data every time

    with open(PRODUCTS_FILE) as f:
        num_products = len(list(csv.DictReader(f)))

    product_ids = list(range(1, num_products + 1))
    weights = [popular.get(pid, 1) for pid in product_ids]

    rows = []
    for i in range(1000):
        product_id = random.choices(product_ids, weights=weights)[0]
        quantity = random.randint(1, 5)
        sale_date = date.today() - timedelta(days=random.randint(0, 29))
        rows.append([product_id, quantity, sale_date])

    rows.sort(key=lambda row: row[2])

    with open(SALES_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["product_id", "quantity", "sale_date"])
        writer.writerows(rows)

    print(f"Created {len(rows)} sales across {num_products} products")


if __name__ == "__main__":
    main()