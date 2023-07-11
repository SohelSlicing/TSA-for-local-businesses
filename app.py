from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

conn = sqlite3.connect("db.sqlite3", check_same_thread=False)
c = conn.cursor()

app = Flask(__name__)
app.secret_key = "KVLKCL"

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

        return render_template("forecast.html")
    else:
        if "user" in session:
            return render_template("forecast.html")
        return render_template("Login.html")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)