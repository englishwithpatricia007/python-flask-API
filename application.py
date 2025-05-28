from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

application = Flask(__name__)
##RuntimeError: The session is unavailable because no secret key was set.  Set the secret_key on the application to something unique and secret.
application.config['SECRET_KEY'] = 'minha chave_secreta'

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(application)
login_manager.init_app(application)
login_manager.login_view = 'login'
CORS(application)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    cart = db.relationship('CartItem', backref='user', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#Autenticação
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@application.route('/')
def index():
    return jsonify({"message": "Welcome to the E-commerce API"}), 200

# USER MANAGEMENT
@application.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        login_user(user)
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
    
@application.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200   

#PRODUCT MANAGEMENT
@application.route('/api/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    product_list = []

    for product in products:
        product_list.append({
        "id": product.id,
        "name": product.name,
        "price": product.price
    })

    if not product_list:
        return jsonify({"message": "No products found"}), 404 
    return jsonify(product_list), 200

@application.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description
    }), 200

@application.route('/api/products/add', methods=['POST'])
@login_required
def add_product():
   data = request.json
   if not data or 'name' not in data or 'price' not in data:
       return jsonify({"error": "Invalid input"}), 400
   
   new_product = Product(
        name=data['name'],
        price=data['price'],
        description=data.get('description', '')
    )
   db.session.add(new_product)
   db.session.commit()

   return jsonify({"message": "Product added successfully"}), 201

@application.route('/api/products/update/<int:product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    data = request.json
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'description' in data:
        product.description = data['description']
  
    db.session.commit()
    return jsonify({"message": "Product updated successfully"}), 200

@application.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully"}), 200

# CART MANAGEMENT

@application.route('/api/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    user = User.query.get(int(current_user.id))
    if not user:
        return jsonify({"error": "User not found"}), 404;
    
    new_cart_item = CartItem(product_id=product_id, user_id=current_user.id)
    db.session.add(new_cart_item)
    db.session.commit()

    return jsonify({"message": "Product added to cart"}), 201


@application.route('/api/cart/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_cart(product_id):
    cart_item = CartItem.query.filter_by(product_id=product_id, user_id=current_user.id).first()
    if not cart_item:
        return jsonify({"error": "Cart item not found"}), 404
    
    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({"message": "Product removed from cart"}), 200

@application.route('/api/cart', methods=['GET'])
@login_required
def view_cart():
    #cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    user = User.query.get(int(current_user.id))
    cart_items = user.cart

    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 200
    
    cart_list = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product:
            cart_list.append({
                "product_id": product.id,
                "name": product.name,
                "price": product.price
            })
    
    return jsonify(cart_list), 200


@application.route('/api/cart/checkout', methods=['POST'])
@login_required
def checkout_cart():
    user = User.query.get(int(current_user.id))
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    return jsonify({"message": "Checkout successful."}), 200

if __name__ == '__main__': application.run(debug=True)