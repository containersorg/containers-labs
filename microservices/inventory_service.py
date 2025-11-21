"""service for inventories"""
from flask import Flask, json

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
    app.run(host='0.0.0.0', port=5001)
