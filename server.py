from config import WATCH_DIR
from urlparse import urlparse, parse_qs

from flask import Flask, request

from order_coffee import order_coffee

app = Flask(__name__)

@app.route("/order")
def order():
    order_coffee()

if __name__ == "__main__":
    app.run()
