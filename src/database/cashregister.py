import sqlite3
from datetime import date

class cashRegister:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("db.sqlite3")
        self.c = self.conn.cursor()
        self.todays_date = date.today()


    def enterProduct(self, name: str, type: int, price: float, stock: int):
        data = [(name, type, price, stock)]

        self.c.executemany("""INSERT INTO product(product_name, product_type, product_price, product_stock)
                       VALUES(?, ?, ?, ?);""", data)
        self.conn.commit()

    def recordTransaction(self, customer_name: str, total_amount: float):
        # Returns the transaction ID of the current transaction. Make sure to pass it to recordSales method
        
        data = [(customer_name, self.todays_date, total_amount)]

        self.c.executemany("""INSERT INTO transactions(customer_name, transaction_date, total_amount) 
                           VALUES(?, ?, ?);""", data)
        self.conn.commit()

        transactions = self.c.execute("SELECT transaction_id FROM transactions").fetchall()
        return transactions[-1][0]

    def enterProductType(self, productName: str):
        data = [(productName)]

        self.c.executemany("""INSERT INTO productTypes(type_label)
                           VALUES(?);""", (data,))
        self.conn.commit()

    def recordSales(self, soldproduct: dict, transactionId: int):
        # Always call this function along with the recordTransaction method only

        data = []
        for key in soldproduct:
            data.append((transactionId, self.todays_date, key, soldproduct[key]))
        
        self.c.executemany("""INSERT INTO sales(sale_id, sales_date, sold_product_id, quantity) 
                           VALUES(?, ?, ?, ?);""", data)
        self.conn.commit()
    
    def get_product_types(self):
        labels = self.c.execute("""SELECT type_label FROM productTypes""").fetchall()
        return labels
    
    def get_product_id(self, product: str):
        productid = self.c.execute("""SELECT type_id FROM productTypes WHERE type_label = :productid""", {"productid": product}).fetchall()
        return productid[0][0]
    
    def get_prodtypes_idname(self):
        types = self.c.execute("""SELECT type_id, type_label FROM productTypes""").fetchall()
        return types
    
    def get_product_idname(self, typeofprod: int):
        prods = self.c.execute("SELECT product_id, product_name FROM product WHERE product_type = :type", {"type" : typeofprod}).fetchall()
        return prods

if __name__ == "__main__":
    cr = cashRegister()
    
    prod = cr.get_product_idname(3)
    print(prod)
    cr.conn.close()


        