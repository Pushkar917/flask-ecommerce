from flask import render_template, session, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from shop import db, app
from shop.models import Users, Product, Brands, Category

admin = Blueprint('admin', __name__)


# this route is for admin home page, will be moved to admin later
@admin.route('/adminhome')
def adminhome():
    if 'email' not in session:
        flash(f'Please log in first', 'danger')
        return redirect(url_for('admin.login'))
    products = Product.query.all()
    return render_template("admin/index.html", products=products)


@admin.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        from shop.admin.forms import RegistrationForm
        userRegister = RegistrationForm()
        if userRegister.password == userRegister.confirm_password:
            userDetails = Users(username=userRegister.username, email=userRegister.email,
                                password=userRegister.password)
            db.session.add(userDetails)
            db.session.commit()
            flash('Thanks for registering')
            return redirect(url_for("admin.login"))
        else:
            return render_template('admin/register.html')
    return render_template('admin/register.html', title="register")


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        loggedUser = Users.query.filter_by(email=email).first()
        if loggedUser:
            if loggedUser.checkPassword(password):
                login_user(loggedUser)
                session['email'] = email
                flash(f'Welcome  {email} ! You have succesfully logged in')
                next = request.args.get('next')
                if next is None or not next[0] == '/':
                    next = url_for("admin.adminhome")
                return redirect(next)
            else:
                flash(f'Wrong Password')
                return render_template("admin/login.html", title="login")
        else:
            flash(f'Hi  {email} ! Please register, as this email not registered')
            return render_template("admin/login.html", title="login")
    else:
        return render_template("admin/login.html", title="login")


# Logout
@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash("logged out succesfully")
    return redirect(url_for("admin.login"))


@admin.route('/brands')
def brands():
    if 'email' not in session:
        flash(f'Please log in first', 'danger')
        return redirect(url_for('admin.login'))
    brands = Brands.query.order_by(Brands.id.desc()).all()
    return render_template('/admin/brands.html', title='brandpage', brands=brands)


@admin.route('/category')
def category():
    if 'email' not in session:
        flash(f'Please log in first', 'danger')
        return redirect(url_for('admin.login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('/admin/brands.html', title='brandpage', categories=categories)
