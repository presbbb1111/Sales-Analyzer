import matplotlib.pyplot as plt

from db import PROJECT_FOLDER, get_connection


def main():
    conn = get_connection()
    cursor = conn.cursor()

    # top 10 best sellers
    cursor.execute("""
        SELECT p.name, SUM(s.quantity) AS units_sold
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.name
        ORDER BY units_sold DESC
        LIMIT 10
    """)
    print("\nTop 10 Best Sellers")
    print("-------------------")
    rank = 1
    for name, units in cursor.fetchall():
        print(f"{rank:>2}. {name:<28} {units:>4} sold")
        rank += 1

    # revenue per day
    cursor.execute("""
        SELECT s.sale_date, SUM(s.quantity * p.price) AS revenue
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY s.sale_date
        ORDER BY s.sale_date
    """)
    days = cursor.fetchall()
    print("\nDaily Revenue")
    print("-------------")
    total = 0
    for day, revenue in days:
        print(f"{day}   ${revenue:.2f}")
        total += revenue
    print(f"\nTotal: ${total:.2f}")
    print(f"Average per day: ${total / len(days):.2f}")

    # items that need to be reordered
    cursor.execute("""
        SELECT name, stock, reorder_level
        FROM products
        WHERE stock <= reorder_level
        ORDER BY stock
    """)
    print("\nLow Stock - Reorder Soon")
    print("------------------------")
    for name, stock, reorder_level in cursor.fetchall():
        print(f"{name:<28} {stock:>3} left (reorder at {reorder_level})")

    cursor.close()
    conn.close()

    # line chart of revenue per day
    dates = [day for day, revenue in days]
    revenues = [float(revenue) for day, revenue in days]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, revenues, marker="o")
    plt.title("Daily Revenue")
    plt.xlabel("Date")
    plt.ylabel("Revenue ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(PROJECT_FOLDER / "revenue_chart.png")
    print("\nSaved chart to revenue_chart.png")


if __name__ == "__main__":
    main()