from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/storeDB'
mongo = PyMongo(app)

@app.route('/addProduct', methods=['POST'])
def create_user():
    productName = request.json['productName']
    price = request.json['price']
    description = request.json['description']
    createAt = request.json['createAt']

    if productName and price and description and createAt:
        
        id = mongo.db.products.insert(
            {
                'productName' : productName,
                'price' : price,
                'description' : description,
                'createAt' : createAt
            }
        )
        
        response = {
            'id': str(id),
            'productName' : productName,
            'price' : price,
            'description' : description,
            'createAt' : createAt
        }
        return response
    else:
        return not_found()
    
    return {'message': 'received'}

@app.route('/getProducts', methods=['GET'])
def get_products():
    products = mongo.db.products.find()
    response = {"products": products}
    return Response(json_util.dumps(response),  mimetype='application/json')

@app.route('/getProductById/<id>', methods=['GET'])
def get_product(id):
    product = mongo.db.products.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(product)
    return Response(response, mimetype='application/json')

@app.route('/updateProduct/<id>', methods=['PUT'])
def update_product(id):
    productName = request.json['productName']
    price = request.json['price']
    description = request.json['description']
    createAt = request.json['createAt']

    if productName and price and description and createAt:
        mongo.db.products.update_one({'_id': ObjectId(id)}, {'$set': {
            'productName' : productName,
            'price' : price,
            'description' : description,
            'createAt' : createAt
        }})
        response = jsonify({
        'message': 'Product with id: ' + id + ' was updated successfully'
    })
    return response

@app.route('/deleteProduct/<id>', methods=['DELETE'])
def delete_product(id):
    mongo.db.products.delete_one({'_id': ObjectId(id)})
    response = jsonify({
        'message': 'Product with id: ' + id + ' was deleted successfully'
    })
    return response

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource not found: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True)

#TODOS LOS METODOS FUNCIONAN CORRECTAMENTE