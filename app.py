from flask import Flask, render_template, session, redirect, url_for, request, flash
import json



app = Flask(__name__)
app.secret_key = "secret123"


# -----------------------------
# Încărcare produse din JSON
# -----------------------------
def load_products():
    with open("products.json", "r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------------
# Pagina principală
# -----------------------------
@app.route("/")
def index():
    products = load_products()
    return render_template("index.html", products=products)


# -----------------------------
# Pagina unui produs
# -----------------------------
@app.route("/product/<int:product_id>")
def product_page(product_id):
    products = load_products()
    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        return "Produs inexistent", 404

    return render_template("product.html", product=product)


# -----------------------------
# Adăugare în coș
# -----------------------------
@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    cart = session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session["cart"] = cart
    flash("Produs adăugat în coș")
    return redirect(url_for("cart"))


# -----------------------------
# Pagina coșului
# -----------------------------
@app.route("/cart")
def cart():
    products = load_products()
    cart = session.get("cart", {})
    items = []
    total = 0

    for pid, qty in cart.items():
        product = next((p for p in products if p["id"] == int(pid)), None)
        if product:
            line_total = product["price"] * qty
            total += line_total
            items.append({
                "product": product,
                "qty": qty,
                "line_total": line_total
            })

    return render_template("cart.html", items=items, total=total)


# -----------------------------
# Login
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        flash("Te-ai logat (simulat).")
        return redirect(url_for("index"))

    return render_template("login.html")


# -----------------------------
# Register
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        flash("Cont creat (simulat).")
        return redirect(url_for("login"))

    return render_template("register.html")


# -----------------------------
# Pornirea aplicației
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)