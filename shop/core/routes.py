from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from flask_login import login_required
from shop.models import Product, Brands, Category

core = Blueprint('core', __name__)


def brands():
    brands = Brands.query.join(Product, (Brands.id == Product.brand_id)).all()
    return brands


def categories():
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()
    return categories


@core.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    allproducts = Product.query.filter(Product.stock > 0).order_by(Product.id.desc()).paginate(page=page, per_page=8)
    return render_template("products/index.html", allproducts=allproducts, brands=brands(), categories=categories())


@core.route('/product/<int:id>')
def single_page(id):
    product = Product.query.get_or_404(id)
    brands = Brands.query.join(Product, (Brands.id == Product.brand_id)).all()
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()
    return render_template('products/single_page.html', product=product, brands=brands(), categories=categories())


@core.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    brand_by_id = Brands.query.filter_by(id=id).first_or_404()
    brandproducts = Product.query.filter_by(brand=brand_by_id).paginate(page=page, per_page=8)
    return render_template("products/index.html", brandproducts=brandproducts, brands=brands(), categories=categories(),
                           brand_by_id=brand_by_id)


@core.route('/category/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    category_by_id = Category.query.filter_by(id=id).first_or_404()
    categoryproducts = Product.query.filter_by(category=category_by_id).paginate(page=page, per_page=8)
    return render_template("products/index.html", categoryproducts=categoryproducts, categories=categories(),
                           brands=brands(), category_by_id=category_by_id)
