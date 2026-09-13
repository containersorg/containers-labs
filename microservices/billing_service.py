"""service for billing"""
from flask import Flask, jsonify
import os

app = Flask(__name__)

# Additional billing functionality can be added here

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5004)
    app.run(host='0.0.0.0', port=int(os.environ.get("BILLING_PORT", 5004)))