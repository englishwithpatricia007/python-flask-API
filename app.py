from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

app = Flask(__name__)
##RuntimeError: The session is unavailable because no secret key was set.  Set the secret_key on the application to something unique and secret.
app.config['SECRET_KEY'] = 'minha chave_secreta'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

#Autenticação
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
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
    
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200   


@app.route('/api/products', methods=['GET'])
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

@app.route('/api/products/<int:product_id>', methods=['GET'])
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

@app.route('/api/products/add', methods=['POST'])
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

@app.route('/api/products/update/<int:product_id>', methods=['PUT'])
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

@app.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully"}), 200




@app.route('/teste')
def hello_world():  
  return 'Hello, World!'




if __name__ == '__main__': app.run(debug=True)