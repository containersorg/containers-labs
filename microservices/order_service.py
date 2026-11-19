"""service for orders with value retention and inter-service communication"""
from flask import Flask, json, request
import json
import os
import requests

app = Flask(__name__)

# File to store orders
ORDERS_FILE = '/data/orders.json'
INVENTORY_API_URL = "http://inventory_service:5001"

# Create the orders file if it doesn't exist                                                   
if not os.path.exists(ORDERS_FILE):
   with open(ORDERS_FILE, 'w') as f:
      json.dump([], f)
 
def read_orders():
   """Read orders from file"""
   with open(ORDERS_FILE, 'r') as f:
      return json.load(f)
 
def write_orders(orders):
   """Write orders to file"""
   with open(ORDERS_FILE, 'w') as f:
      json.dump(orders, f, indent=2)
  
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

    allorders = read_orders()
    allorders.append(order)
    write_orders(allorders)

    return json.dumps({'message': 'Order placed successfully'}, indent=4)

# Endpoint to view orders
@app.route('/view_orders', methods=['GET'])
def view_orders():
    """Print existing orders"""
    allorders = read_orders()
    return json.dumps({'orders': allorders}, indent=4)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
