from flask import Flask, request, render_template, redirect
from datetime import datetime

app = Flask(__name__)

orders = []
HOUSE_PIZZAS = {
    'Margherita': {'toppings': ['Mozzarella', 'Basil', 'Tomato'], 'price': 10.00},
    'Meatlovers': {'toppings': ['Pepperoni', 'Sausage', 'Bacon'], 'price': 14.00},
    'Hawaiian': {'toppings': ['Ham', 'Pineapple', 'Cheese'], 'price': 12.00},
    'BBQ Chicken': {'toppings': ['Chicken', 'BBQ Sauce', 'Red Onions', 'Cheese'], 'price': 13.50},
    'Veggie Deluxe': {'toppings': ['Bell Peppers', 'Onions', 'Mushrooms', 'Olives', 'Cheese'], 'price': 11.50},
    'Four Cheese': {'toppings': ['Mozzarella', 'Cheddar', 'Parmesan', 'Gorgonzola'], 'price': 13.00},
    'Spicy Pepperoni': {'toppings': ['Pepperoni', 'Jalapeños', 'Chili Flakes', 'Cheese'], 'price': 12.50},
    'Mediterranean': {'toppings': ['Feta', 'Olives', 'Spinach', 'Sun-dried Tomatoes'], 'price': 14.00},
    'Truffle Mushroom': {'toppings': ['Mushrooms', 'Truffle Oil', 'Parmesan', 'Arugula'], 'price': 16.00},
    'Seafood Special': {'toppings': ['Shrimp', 'Clams', 'Garlic', 'Cheese'], 'price': 17.00}
}

def calculate_custom_price(toppings, base=8.00):
    return base + len(toppings) * 1.50

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/handle_login', methods=['POST'])
def handle_login():
    role = request.form.get('role')
    if role == 'admin':
        return redirect('/orders')
    elif role == 'customer':
        return redirect('/order_form')
    else:
        return redirect('/login')

@app.route('/order_form')
def order_form():
    house_choices = list(HOUSE_PIZZAS.keys())
    return render_template('order_form.html', house_choices=house_choices)

@app.route('/submit', methods=['POST'])
def submit_order():
    name = request.form['name']
    pizza = request.form['pizza']

    if pizza in HOUSE_PIZZAS:
        toppings = HOUSE_PIZZAS[pizza]['toppings']
        price = HOUSE_PIZZAS[pizza]['price']
    else:
        toppings = request.form.getlist('toppings')
        price = calculate_custom_price(toppings)

    order = {
        'name': name,
        'pizza': pizza,
        'toppings': toppings,
        'price': price,
        'id': len(orders),
        'status': 'Order Placed',
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    orders.append(order)
    return render_template('order_confirm.html', order=order)

@app.route('/orders')
def show_orders():
    return render_template('order_list.html', orders=orders)

@app.route('/update_status', methods=['POST'])
def update_status():
    order_id = request.form.get('order_id')
    new_status = request.form.get('new_status')

    if not order_id or not new_status:
        return "Missing order_id or new_status", 400

    try:
        order_id = int(order_id)
    except ValueError:
        return "Invalid order_id", 400

    for order in orders:
        if order['id'] == order_id:
            order['status'] = new_status
            break

    return redirect('/orders')


if __name__ == '__main__':
    app.run(debug=True)
