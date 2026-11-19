"""Service for customers"""
from flask import Flask, json

app = Flask(__name__)

customers = {
    'customer_id_1': {'name': 'John Doe', 'address': '123 Main St'},
    'customer_id_2': {'name': 'Alice Smith', 'address': '456 Elm St'},
    # ... other customers
}

@app.route('/view_customer/<customer_id>', methods=['GET'])
def view_customer(customer_id):
    """Prints existing customers"""
    if customer_id not in customers:
        return json.dumps({'message': 'Customer not found'}, indent=4)

    return json.dumps({'customer_details': customers[customer_id]}, indent=4)

if __name__ == '__main__':
    app.run(port=5003)
