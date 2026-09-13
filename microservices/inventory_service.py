"""service for inventories"""
from flask import Flask, json
import os

app = Flask(__name__)

inventory = {
    'medicine_A': {'stock': 100, 'price': 10},
    'medicine_B': {'stock': 50, 'price': 15},
    # ... other medicines
}

@app.route('/view_inventory', methods=['GET'])
def view_inventory():
    """Prints the inventory"""
    return json.dumps({'inventory': inventory}, indent=4)

if __name__ == '__main__':
    # app.run(port=5001)
    app.run(port=int(os.environ.get("INVENTORY_PORT", 5001)))
