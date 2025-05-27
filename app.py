from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)
CORS(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

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