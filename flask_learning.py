from flask import Flask, request, render_template

app = Flask(__name__)
orders = []

@app.route('/')
def index():
    return render_template('order_form.html')

@app.route('/submit', methods=['POST'])
def submit_order():
