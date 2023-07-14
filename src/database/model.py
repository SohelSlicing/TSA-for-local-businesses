import sqlite3

class database:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("db.sqlite3")
        self.c = self.conn.cursor()

    def create_user(self):
        self.c.execute("""CREATE TABLE user(
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name VARCHAR(50),
                    user_password TEXT,
                    user_phoneno TEXT   
        );""")
    
    def create_product(self):
        self.c.execute("""CREATE TABLE product(
                    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_name VARCHAR(30),
                    product_type VARCHAR(25),
                    product_price REAL,
                    product_stock INTEGER,
                    FOREIGN KEY(product_type) REFERENCES productTypes(type_id)
        );""")

    def create_transactions(self):
        self.c.execute("""CREATE TABLE transactions(
                       transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       customer_name VARCHAR(50),
                       transaction_date date,
                       total_amount REAL
        );""")

    def create_sales(self):
        self.c.execute("""CREATE TABLE sales(
                       sale_id INTEGER,
                       sales_date date,
                       sold_product_id INTEGER,
                       quantity INTEGER,
                       FOREIGN KEY(sale_id) REFERENCES transactions(transaction_id),
                       FOREIGN KEY(sold_product_id) REFERENCES product(product_id)
        );""")

    def create_product_type(self):
         self.c.execute("""CREATE TABLE productTypes(
                        type_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type_label VARCHAR(30)
         );""")

if __name__ == "__main__":
    db = database()
    db.create_product_type()
    db.create_product()
    #db.create_transactions()
    #db.create_sales()
    db.conn.close()