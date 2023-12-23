from unittest import result
from flask import Flask, jsonify, request
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# PostgreSQL database configuration
db_config = {
    'dbname': 'Python',
    'user': 'postgres',
    'password': 'Reset@321',
    'host': 'localhost',
    'port': '5432'
}

# Define the connection string
conn_string = "dbname={dbname} user={user} password={password} host={host} port={port}".format(**db_config)

# Function to connect to the database and execute a query
def query_database(query, params=None):
    with psycopg2.connect(conn_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
    return result

# API endpoint to get product data based on product name
@app.route('/get_product', methods=['GET'])
def get_product():
    product_name = request.args.get('product_name')

    # Use SQL parameters to prevent SQL injection
    query = sql.SQL("SELECT * FROM product WHERE product_name = {}").format(sql.Literal(product_name))

    result = query_database(query)

    if result:
        # Convert the result to a dictionary for JSON serialization
        product_data = {
            'product_id': result[0][0],
            'product_name': result[0][1],
            'price': float(result[0][2]),
            'quantity': result[0][3],
            'created_at': str(result[0][4])
        }
        return jsonify(product_data)
    else:
        return jsonify({'message': 'No matching product found'}), 404
    
@app.route('/insert_product', methods=['POST'])
def insert_product():
    data = request.get_json()

    product_name = data.get('product_name')
    price = data.get('price')
    quantity = data.get('quantity')

    # Use SQL parameters to prevent SQL injection
    query = sql.SQL("INSERT INTO product (product_name, price, quantity) VALUES ({}, {}, {}) RETURNING *").format(
        sql.Literal(product_name),
        sql.Literal(price),
        sql.Literal(quantity)
    )
    result = query_database(query)
    return jsonify({'message': 'Product inserted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
