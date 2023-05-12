from flask import Flask, render_template, redirect, flash, request, session, url_for
import jinja2

import melons

app = Flask(__name__)
app.jinja_env.undefined = jinja2.StrictUndefined
app.secret_key = "super secret"

@app.route('/')
def homepage():
    return render_template('base.html')

@app.route("/melons")
def all_melons():
   """Return a page listing all the melons available for purchase."""
   melon_list = melons.get_all()
   return render_template("all_melons.html", melon_list=melon_list)

@app.route("/melon/<melon_id>")
def melon_details(melon_id):
   """Return a page showing all info about a melon. Also, provide a button to buy that melon."""
   melon = melons.get_by_id(melon_id)
   return render_template("melon_details.html", melon=melon)

@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
   """Add a melon to the shopping cart."""
   if 'cart' not in session:
      session['cart'] = {}

   cart = session['cart']
   cart[melon_id] = cart.get(melon_id, 0) + 1
   session.modified = True
   flash(f"Melon {melon_id} successfully added...")
   print(cart)
   return redirect(url_for('show_shopping_cart'))

@app.route("/cart")
def show_shopping_cart():
   """Display contents of shopping cart."""
   order_total = 0
   cart_melons = []

   cart = session.get('cart', {})

   for melon_id, quantity in cart.items():
      melon = melons.get_by_id(melon_id)

      total_cost = melon.price * quantity

      order_total += total_cost

      melon.quantity = quantity 
      melon.total_cost = total_cost 

      cart_melons.append(melon)

   return render_template("cart.html", cart_melons=cart_melons, order_total=order_total)

@app.route('/empty-cart')
def empty_cart():
   session['cart'] = {}

   return redirect(url_for('show_shopping_cart'))

if __name__ == "__main__":
    app.run(debug=True)