from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from src.database.cashregister import cashRegister
from src.logger import logging

conn = sqlite3.connect("db.sqlite3", check_same_thread=False)
c = conn.cursor()

app = Flask(__name__)
app.secret_key = "KVLKCL"

class customerTransaction:
    def __init__(self, custname: str) -> None:
        self.customerName = custname
        self.sales_id = []
        self.qty = []

    def complete_transaction(self):
    # get customer name, product IDs, their quantities 
    # calculate final price fp = product unit costs * qty
        finalPrice = 0
        salesdict = {}
        for i in range(len(self.sales_id)):
            salesdict[self.sales_id[i]] = self.qty[i]

            unitprice = c.execute("SELECT product_price FROM product WHERE product_id = :id", {"id" : self.sales_id[i]}).fetchall()
            finalPrice += unitprice[0][0] * self.qty[i]

    # create transaction and get the 
        cr = cashRegister()
        lastID = cr.recordTransaction(self.customerName, finalPrice)

    # create sales for all products in the list
        cr.recordSales(salesdict, lastID)
        self.sales_id.clear()
        self.qty.clear()



@app.route("/", methods = ["GET", "POST"])
def index():   
    return render_template("index.html")

@app.route("/Register", methods = ["GET", "POST"])
def Register():
    if request.method == "POST":

        session["user"] = request.form.get("name")

        if not request.form.get("name") or not request.form.get("phone") or not request.form.get("password") or not request.form.get("confirm"):
            return "Please fill out all the fields"
        
        if request.form.get("password") != request.form.get("confirm"):
            return "Password Confirmation doesn't match your password"
        
        exist = c.execute("SELECT * FROM user WHERE user_phoneno =:phone", {"phone": request.form.get("phone")}).fetchall()

        if len(exist) != 0:
            return "user already exists"
        
        pwhash = generate_password_hash(request.form.get("password"), method = "pbkdf2:sha256", salt_length = 8)

        c.execute("INSERT INTO user(user_name, user_password, user_phoneno) VALUES(:name, :password, :phone)", {"name" : request.form.get("name"), "password" : pwhash  , "phone" : request.form.get("phone")})
        conn.commit()

        return "Registration Complete "
        
    return render_template("Register.html")

@app.route("/Login", methods = ["GET", "POST"])
def Login():
    if request.method == "POST":

        if not request.form.get("phone") or not request.form.get("password"):
            return "Please fill out all the fields"
        
        user = c.execute("SELECT * FROM user WHERE user_phoneno = :phone", {"phone": request.form.get("phone")}).fetchall()

        if len(user) == 0:
            return "You're not Registered"
        
        pwhash = user[0][2]
        if check_password_hash(pwhash, request.form.get("password")) == False:
            return "wrong password"
        
        session["user"] = user[0][1]

        return redirect(url_for('admin_panel'))
    else:
        if "user" in session:
            return redirect(url_for('admin_panel'))
        return render_template("Login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return render_template("index.html")

    
@app.route("/admin_panel", methods = ["POST", "GET"])
def admin_panel():
    if "user" in session:
        user = session["user"]
        
        cashregister = cashRegister()
        prodlist = cashregister.get_product_types()

        if request.method == "POST": 

            if request.form.get("newType"):
                cashregister.enterProductType(request.form.get("newType"))

            if request.form.get("productname"):
                prodname = request.form.get("productname")
                prodtype = request.form.get("typeprod")
                price = request.form.get("price")
                stock = request.form.get("stock")

                prodtypeID = cashregister.get_product_id(prodtype)

                cashregister.enterProduct(prodname, prodtypeID, price, stock)
                
        
        return render_template("admin_panel.html", listoftypes = prodlist)
    
    else:
        return render_template("login.html")
    
custtrans = customerTransaction("")
    
@app.route("/admin_panel/transactionpage", methods = ["POST", "GET"])
def cashregister():
    if "user" in session:
        user = session["user"]

        cashregister = cashRegister()

        if request.method == "POST":
            if not request.form.get("customerName"):
                pass
            else:
                custtrans.customerName = request.form.get("customerName")

            return redirect(url_for("testtransaction", typeselected = request.form.get("prod_type_selector")))

        return render_template("cashregister.html", prod_type_nameid = cashregister.get_prodtypes_idname())

    else:
        return redirect(url_for('Login'))
    
@app.route("/admin_panel/transactionpage/<typeselected>", methods = ["POST", "GET"])
def testtransaction(typeselected):
    if "user" in session:

        user = session["user"]
        cashr = cashRegister()
        list_of_products = cashr.get_product_idname(typeselected)

        if request.method == "POST":

            custtrans.sales_id.append(request.form.get("products"))
            custtrans.qty.append(int(request.form.get("quantity")))
        
        return render_template("additems.html", param1 = typeselected, products_list = list_of_products)
    else:
        return redirect(url_for('Login'))
    
@app.route("/completeTransaction")
def rundb():
    custtrans.complete_transaction()
    return redirect(url_for("admin_panel"))
    

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)