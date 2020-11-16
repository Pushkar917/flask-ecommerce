from flask import render_template, session, request, redirect, url_for, flash, Blueprint, current_app
from shop import db, app, photos
from shop.models import Brands, Category, Product
from shop.products.forms import AddProductForm
import secrets
import os

products = Blueprint('products', __name__)




@products.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if request.method == "POST":
        brand = request.form.get('brand')
        objBrand = Brands(brand)
        db.session.add(objBrand)
        db.session.commit()
        flash(f'{brand} added to database, success')
        return redirect(url_for('products.addbrand'))
    return render_template('products/addbrand.html', brands='brands')


@products.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash("Please login first", 'danger')
    updatebrand = Brands.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == 'POST':
        updatebrand.name = brand
        db.session.commit()
        flash(f'Your brand has been updated with this name {brand}', 'success')
    return render_template('products/updatebrand.html', updatebrand=updatebrand)


@products.route('/updatecategory/<int:id>', methods=['GET', 'POST'])
def updatecategory(id):
    if 'email' not in session:
        flash("Please login first", 'danger')
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == 'POST':
        updatecategory.name = category
        db.session.commit()
        flash(f'Your Category has been updated with this name {category}', 'success')
    return render_template('products/updatebrand.html', updatecategory=updatecategory)


@products.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if request.method == "POST":
        category = request.form.get('category')
        objcategory = Category(category)
        db.session.add(objcategory)
        db.session.commit()
        flash(f'{category} added to database, success')
        return redirect(url_for('products.addcategory'))
    return render_template('products/addbrand.html', category='category')


@products.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    form = AddProductForm()
    brands = Brands.query.all()
    categories = Category.query.all()
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.description.data
        category = request.form.get('category')
        brand = request.form.get('brand')
        image_1 = photos.save(request.files.get('image1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image3'), name=secrets.token_hex(10) + ".")
        prod = Product(name=name, price=price, discount=discount, stock=stock, colors=colors, desc=desc,
                       category_id=category,
                       brand_id=brand, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(prod)
        db.session.commit()
        flash(f'Item/Product {name} added into database, success')
        return redirect(url_for('admin.adminhome'))
    return render_template('products/addProduct.html', form=form, brands=brands, categories=categories)


@products.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    form = AddProductForm()
    brands = Brands.query.all()
    categories = Category.query.all()
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        brand = request.form.get('brand')
        category = request.form.get('category')
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.colors = form.colors.data
        product.desc = form.description.data
        if request.files.get('image1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images", product.image_1))
                product.image_1 = photos.save(request.files.get('image1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image1'), name=secrets.token_hex(10) + ".")
        if request.files.get('image2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images", product.image_2))
                product.image_1 = photos.save(request.files.get('image2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image2'), name=secrets.token_hex(10) + ".")

        if request.files.get('image3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images", product.image_3))
                product.image_1 = photos.save(request.files.get('image3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image3'), name=secrets.token_hex(10) + ".")

        db.session.commit()
        flash(f'Your product has been updated', 'success')
        return redirect(url_for('admin.adminhome'))
    form.name.data = product.name
    form.price.data = product.price
    form.description.data = product.desc
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.description.data = product.desc

    return render_template('products/updateproduct.html', form=form, brands=brands, categories=categories,
                           product=product)


@products.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    brand = Brands.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f"The Brand {brand.name} was deleted from your database", 'success')
        return redirect(url_for("admin.brands"))
    flash(f"The Brand {brand.name} can't be deleted from your database", 'warning')
    return redirect(url_for("admin.brands"))


@products.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash(f"The Brand {category.name} was deleted from your database", 'success')
        return redirect(url_for("admin.category"))
    flash(f"The Brand {category.name} can't be deleted from your database", 'warning')
    return redirect(url_for("admin.category"))


@products.route('/deleteproducts/<int:id>', methods=['POST'])
def deleteproducts(id):
    theproduct = Product.query.get_or_404(id)
    if request.method == 'POST':
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images", theproduct.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images", theproduct.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images", theproduct.image_1))
        except Exception as e:
            print(e)
        db.session.delete(theproduct)
        db.session.commit()
        flash(f"The Brand {theproduct.name} was deleted from your database", 'success')
        return redirect(url_for("admin.adminhome"))
    flash(f"The Brand {theproduct.name} can't be deleted from your database", 'warning')
    return redirect(url_for("admin.adminhome"))
