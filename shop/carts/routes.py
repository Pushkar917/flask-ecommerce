from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from shop.models import Product, Brands, Category
from shop.core.routes import brands, categories

carts = Blueprint('carts', __name__)


def mergeDict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    else:
        return False


@carts.route('/addcart', methods=['POST'])
def Addcart():
    try:
        product_id = request.form.get("products_id")
        quantity = request.form.get("quantity")
        colors = request.form.get("colors")
        product = Product.query.filter_by(id=product_id).first()
        if product_id and quantity and colors and request.method == 'POST':
            dictItems = {product_id: {'name': product.name, 'price': float(product.price), 'discount': product.discount,
                                      'colors': colors, 'quantity': quantity, 'image': product.image_1}}

            if 'ShoppingCart' in session:
                print(session['ShoppingCart'])
                if product_id in session['ShoppingCart']:
                    for key, item in session['ShoppingCart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] = int(item['quantity']) + 1
                            print(item['quantity'])
                else:
                    session['ShoppingCart'] = mergeDict(session['ShoppingCart'], dictItems)
                    return redirect(request.referrer)
            else:
                session['ShoppingCart'] = dictItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@carts.route('/carts')
def getCart():
    if 'ShoppingCart' not in session or len(session['ShoppingCart']) <=0:
        return redirect(url_for('core.home'))
    subtotal = 0
    grandtotal = 0

    for key, product in session['ShoppingCart'].items():
        discount = (product['discount']/100) * float(product['price'])
        total =+ float(product['price']) * int(product['quantity'])
        total -= discount
        subtotal = subtotal + total
        tax = ("%.2f" %(.06 * float(subtotal)))
        grandtotal = subtotal + float(tax)
    return render_template('products/carts.html', tax=tax, grandtotal=str(grandtotal), brands=brands(), categories=categories())


@carts.route('/empty')
def emptycart():
    try:
        session.pop('ShoppingCart', None)
        return redirect(url_for('core.home'))
    except Exception as e:
        print(e)


@carts.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'ShoppingCart' not in session or len(session['ShoppingCart']) <=0:
        return redirect(url_for('core.home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['ShoppingCart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash("Item is updated", "success")
                    return redirect(url_for('carts.getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('cart.getCart'))
    return redirect(url_for('/'))


@carts.route('/deleteItem/<int:id>')
def deleteItem(id):
    if 'ShoppingCart' not in session or len(session['ShoppingCart']) <=0:
        return redirect(url_for('core.home'))
    try:
        session.modified= True
        for key, item in session['ShoppingCart'].items():
            if int(key) == id:
                session['ShoppingCart'].pop(key,None)
        return redirect(url_for('carts.getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('carts.getCart'))

