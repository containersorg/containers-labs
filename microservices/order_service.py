"""service for orders with value retention"""
from flask import Flask, json, request

app = Flask(__name__)

orders = []

# Endpoint to place orders
@app.route('/place_order', methods=['POST'])
def place_order():
    """Receives orders"""
    order_details = request.json
    medicine_name = order_details['medicine']
    requested_quantity = order_details['quantity']

    # Prepare order details
    order = {
        'customer_id': order_details['customer_id'],
        'medicine': medicine_name,
        'quantity': requested_quantity,
        'status': 'Pending'
    }

    orders.append(order)

    return json.dumps({'message': 'Order placed successfully'}, indent=4)

# Endpoint to view orders
@app.route('/view_orders', methods=['GET'])
def view_orders():
    """Print existing orders"""
    return json.dumps({'orders': orders}, indent=4)

if __name__ == '__main__':
    app.run(port=5002)
