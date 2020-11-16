from flask import render_template, session, request, redirect, url_for, flash, Blueprint, make_response
from flask_login import login_user, current_user, logout_user, login_required
from shop import db, app, photos
from shop.models import CustomerDB, CustomerOrder
import secrets
import pdfkit
import stripe

customers = Blueprint('customers', __name__)

publishable_key = "pk_test_51Hnqe3HoHssRdbtSkTqloImAeUdqHgVpdlELSRMoUXUtjiSEM5dvMT0kIIRtLdGkpCf0E1naWiNwYtUnnFJM0ciP006fuQPSAQ"
stripe.api_key = "sk_test_51Hnqe3HoHssRdbtSKCDuQcXItViDubzDWpRvadelevim3G9eS4CL0XdSyfN8yq8XSgBzPbKvVRLXbFJiEAc0Crsq00sMaUqm6l "


@customers.route('/payment', methods=['GET', 'POST'])
def payment(data=None):
    invoice = request.form.get('invoice')
    paisaamount = request.form.get('paisaamount')
    customer = stripe.Customer.create(
        email = request.form['stripeEmail'],
        source= request.form['stripeToken']
    )

    charge= stripe.Charge.create(
        customer = customer.id,
        description = 'E-commerce shop',
        amount = paisaamount,
        currency = 'inr'
    )
    orders = CustomerOrder.query.filter_by(customer_id=current_user.id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
    orders.status = "Paid"
    db.session.commit()
    return redirect(url_for('customers.thanks'))


@customers.route('/thanks')
def thanks():
    return render_template('customer/thanks.html')


@customers.route('/customer/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        from shop.customers.forms import RegistrationForm
        customerRegister = RegistrationForm()
        if customerRegister.check_username(RegistrationForm.username):
            flash("'{}' username already taken".format(RegistrationForm.username), "error")
            return render_template('customer/customer_register.html')
        if customerRegister.check_email(RegistrationForm.email):
            flash("'{}' email already taken".format(RegistrationForm.email), "error")
        image_1 = photos.save(request.files.get('image1'), name=secrets.token_hex(10) + ".")
        if customerRegister.password == customerRegister.confirm_password:
            customerDetails = CustomerDB(username=customerRegister.username, email=customerRegister.email,
                                         password=customerRegister.password,
                                         country=customerRegister.country,
                                         state=customerRegister.state,
                                         city=customerRegister.city,
                                         contact=customerRegister.contact,
                                         address=customerRegister.address,
                                         zipcode=customerRegister.zipcode,
                                         image=image_1)
            db.session.add(customerDetails)
            db.session.commit()
            flash('Thanks for registering')
            return redirect(url_for("customers.customerlogin"))
        else:
            return render_template('customer/customer_register.html')
    return render_template('customer/customer_register.html', title="register")


@customers.route('/customer/login', methods=['GET', 'POST'])
def customerlogin():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        loggedUser = CustomerDB.query.filter_by(email=email).first()
        if loggedUser:
            if loggedUser.checkPasswordforCustomer(password):
                login_user(loggedUser)
                session['email'] = email
                flash(f'Welcome  {email} ! You have succesfully logged in')
                next = request.args.get('next')
                if next is None or not next[0] == '/':
                    next = url_for("core.home")
                return redirect(next)
            else:
                flash(f'Wrong Password', 'danger')
                return render_template("customer/login.html", title="login")
        else:
            flash(f'Hi  {email} ! Please register, as this email not registered', 'danger')
            return render_template("customer/login.html", title="login")
    else:
        return render_template("customer/login.html", title="login")


@customers.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('customers.customerlogin'))


@customers.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['ShoppingCart'])
            db.session.add(order)
            db.session.commit()
            flash('Your order has been sent successfully', 'success')
            session.pop('ShoppingCart')
            return redirect(url_for('customers.orders', invoice=invoice))
        except Exception as e:
            print(e)
            flash("Something failed in getting order", 'danger')
            return redirect(url_for('carts.getCart'))


@customers.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandtotal = 0
        total = 0
        subtotal = 0
        customer_id = current_user.id
        customer = CustomerDB.query.filter_by(id=customer_id).first()
        customer_order = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(
            CustomerOrder.id.desc()).first()
        for _key, products in customer_order.orders.items():
            discount = (products['discount'] / 100) * float(products['price'])
            total = float(products['price']) * int(products['quantity'])
            total = total - discount
            subtotal = subtotal + total
            tax = ("%.2f" % (.06 * float(subtotal)))
            grandtotal = subtotal + float(tax)
            paisaamount = str(grandtotal * 10).replace(".", "")



    else:
        return redirect(url_for('customers.customerlogin'))
    return render_template('customer/order.html', invoice=invoice, tax=tax, subtotal=subtotal, grandtotal=grandtotal,
                           customer=customer, paisaamount=paisaamount, customer_order=customer_order)


@customers.route('/get_pdf/<invoice>', methods=['POST'])
def get_pdf(invoice):
    if current_user.is_authenticated:
        subtotal = 0
        customer_id = current_user.id
        if request.method == "POST":
            customer = CustomerDB.query.filter_by(id=customer_id).first()
            customer_order = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(
                CustomerOrder.id.desc()).first()
            for _key, products in customer_order.orders.items():
                discount = (products['discount'] / 100) * float(products['price'])
                total = float(products['price']) * int(products['quantity'])
                total = total - discount
                subtotal = subtotal + total
                tax = ("%.2f" % (.06 * float(subtotal)))
                grandtotal = subtotal + float(tax)

                rendered = render_template('customer/pdf.html', invoice=invoice, tax=tax, subtotal=subtotal,
                                           grandtotal=grandtotal,
                                           customer=customer, customer_order=customer_order)
                pdf = pdfkit.from_string(rendered, False)
                response = make_response(pdf)
                response.headers['content-Type'] = 'application/pdf'
                response.headers['content-Disposition'] = 'atteched; filename' + invoice + '.pdf'
                return response
    return request(url_for('customers.orders'))
