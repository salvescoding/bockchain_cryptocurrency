from flask import Flask
from flask_cors import CORS

from wallet import Wallet

app = Flask(__name__)
wallet = Wallet()
CORS(app)
