-- tables for the sales analyzer
-- load_data.py runs this, it drops the tables and recreates them

DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS products;

CREATE TABLE products (
  product_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  category VARCHAR(50),
  price DECIMAL(6,2) NOT NULL,
  stock INT NOT NULL,
  reorder_level INT NOT NULL
);

CREATE TABLE sales (
  sale_id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  sale_date DATE NOT NULL,
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);