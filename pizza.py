

def take_order():
    ticket = []
    name = input("What is your first name? ")
    while True:
        order = input("What pizza would you like? ")
        toppings = input("What toppings would you like? ")
        ticket.append({"name": name, "order": order, "toppings": toppings})
        confirm = input("Would you like to make another order? (yes/no) ").strip().lower()
        if confirm == "no":
            print(f"Order summary:{ticket}")
            return ticket



take_order()