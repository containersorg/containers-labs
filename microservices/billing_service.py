"""service for billing"""
from flask import Flask, jsonify

app = Flask(__name__)

# Additional billing functionality can be added here

if __name__ == '__main__':
    app.run(port=5004)
