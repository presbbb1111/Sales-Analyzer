sales-analyzer

I work as a cashier at a grocery store, so for my first database project I wanted to build something I already understand from the other side of the register. This is a small Python program that stores a month of grocery sales in MySQL and pulls a few reports out of it:

top 10 best sellers
revenue per day
items that are low on stock and need to be reordered

It also saves a line chart of daily revenue.

revenue chart

The sales data is fake. generate_sales.py makes 1,000 random sales over the last 30 days, and some items (bananas, milk, eggs, tortillas) are weighted to sell more, like they would in a real store.

How it's set up

There are two tables, products and sales. Every sale has a product_id that points back to a product (a foreign key), so you can't record a sale for something that doesn't exist. The reports use JOIN and GROUP BY to combine the two tables. The schema is in sql/schema.sql.

MySQL runs in a Docker container so I didn't have to install it directly on my laptop.

src/generate_sales.py   makes data/sales.csv
src/load_data.py        creates the tables and loads both CSVs
src/reports.py          runs the reports and saves the chart
src/db.py               database connection (reads settings from .env)
Running it

You need Python 3 and Docker Desktop.

Start MySQL:

docker run --name sales-db -e MYSQL_ROOT_PASSWORD=devpassword -e MYSQL_DATABASE=sales -p 3306:3306 -d mysql:8

Give it about 20 seconds to start, then:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python src/generate_sales.py
python src/load_data.py
python src/reports.py

Part of the output:

Top 10 Best Sellers

 1. Bananas (1 lb)                365 sold
 2. Whole Milk (1 gal)            336 sold
 3. Flour Tortillas (10 ct)       261 sold

Low Stock - Reorder Soon

Trash Bags (40 ct)             7 left (reorder at 8)
Granola Bars (6 ct)            9 left (reorder at 12)
Stuff I want to add
lower the stock count when something sells (right now it stays the same)
revenue by category
connect it to the POS web app I'm working on so checkouts show up here