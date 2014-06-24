from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2


app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()

    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    user = session.get('user', None)
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""
    purchased_melon_list = {}
    total_price = 0
    for melon_id in session['cart']:
        m = model.get_melon_by_id(melon_id)
        purchased_melon_list[melon_id] = purchased_melon_list.get(melon_id, [None, None, 0])
        
        if purchased_melon_list[m.id] == [None, None, 0]:
            purchased_melon_list[m.id] = [m.common_name, m.price, 1]
        else:
            purchased_melon_list[m.id][2] += 1
        total_price += (purchased_melon_list[m.id][1])

    print purchased_melon_list
    print total_price



    return render_template("cart.html", melon_list=purchased_melon_list, total_price=total_price)
    
@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    session['cart'] = session.get('cart', [])
    session['cart'].append(id)
    print session
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.
    
    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """
    flash("Successfully added to cart")
    return redirect("/cart")
    # return "Oops! This needs to be implemented!"


@app.route("/login", methods=["GET"])
def show_login():

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    email = request.form["email"]
    password = request.form["password"]

    print email
    print password

    customer = model.get_customer_by_email(email)
    session['user'] = customer.givenname

    print session['user']

    if not customer:

        flash("Sorry! Login Error.")
        return redirect("/login")


    return redirect("/melons")


@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

@app.route("/logout")
def logout(): 
    session['user'] = None
    flash("User has logged out.")
    return redirect("/melons")  

if __name__ == "__main__":
    app.run(debug=True)
