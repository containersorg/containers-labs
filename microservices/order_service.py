"""service for orders with value retention and inter-service communication"""
from flask import Flask, json, request
import requests 

app = Flask(__name__)

orders = []
INVENTORY_API_URL = "http://127.0.0.1:5001" # URL for the inventory service

# Endpoint to place orders
@app.route('/place_order', methods=['POST'])
def place_order():
    """Receives orders and checks inventory via API call"""
    order_details = request.json
    medicine_name = order_details['medicine']
    requested_quantity = order_details['quantity']

    # --- API Call to Inventory Service ---
    try:
        inventory_response = requests.get(f"{INVENTORY_API_URL}/view_inventory")
        inventory_response.raise_for_status()  # Raise an exception for bad status codes
        inventory_data = inventory_response.json()['inventory']

        if medicine_name not in inventory_data or requested_quantity > inventory_data[medicine_name]['stock']:
            return json.dumps({'message': 'Insufficient stock or medicine not found'}, indent=4), 400
    except requests.exceptions.RequestException as e:
        return json.dumps({'message': 'Could not connect to inventory service', 'error': str(e)}, indent=4), 503

    # If stock is sufficient, proceed to create the order
    # (In a real app, you would also need to call the inventory service to *update* the stock)
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
