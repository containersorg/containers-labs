"""service for orders"""
from flask import Flask, json

app = Flask(__name__)

orders = []

# Endpoint to place orders
@app.route('/place_order', methods=['POST'])
def place_order():
    """Receives orders"""
    # Process order logic
    # ...
    return json.dumps({'message': 'Order placed successfully'}, indent=4)

# Endpoint to view orders
@app.route('/view_orders', methods=['GET'])
def view_orders():
    """Print existing orders"""
    return json.dumps({'orders': orders}, indent=4)

if __name__ == '__main__':
    app.run(port=5002)
