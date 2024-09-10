- Let's build a **shopping cart system** that allows users to add items, apply discounts, calculate total cost, and filter items based on price. 
- This simple project will allow us to demonstrate the use of **normal functions, higher-order functions, decorators, currying, map, filter and reduce**

In this project: 
- **Normal function** will handle basic operations like calculating totals and applying discounts 
- **Higher-order functions** will pass functions as argument(  e.g. to apply discount)
- **Decorators** will modify functions to log user actions
- **Currying** will be used to create specialized discount functions
- **Map, filter and reduce** will manipulate the cart data 



```python
from functools import reduce

# List of items in the cart (name, price, quantity)
shopping_cart = [
    {"name": "Laptop", "price": 1000, "quantity": 1},
    {"name": "Smartphone", "price": 500, "quantity": 2},
    {"name": "Headphones", "price": 100, "quantity": 3},
    {"name": "Mouse", "price": 50, "quantity": 2},
    {"name": "Keyboard", "price": 70, "quantity": 1}
]

# 1. Normal function to calculate total price of items in the cart
def calculate_total(cart):
    return sum(item['price'] * item['quantity'] for item in cart)

# 2. Higher-order function to apply a discount
def apply_discount(cart, discount_func):
    return [
        {**item, "price": discount_func(item['price'])} for item in cart
    ]

# 3. Currying function to create a specific discount function
def discount_percentage(percentage):
    def apply(price):
        return price * (1 - percentage / 100)
    return apply

# 4. Decorator to log actions
def log_action(action_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print(f"Action: {action_name} completed successfully.")
            return result
        return wrapper
    return decorator

# 5. Use a decorator to log the total calculation
@log_action("Calculate Total")
def get_total(cart):
    return calculate_total(cart)

# 6. Map function to add tax to each item's price (10% tax)
def add_tax(cart):
    return list(map(lambda item: {**item, "price": item['price'] * 1.10}, cart))

# 7. Filter items based on price threshold (e.g., items above $100)
def filter_expensive_items(cart, threshold):
    return list(filter(lambda item: item['price'] > threshold, cart))

# 8. Reduce to get total quantity of items
def total_quantity(cart):
    return reduce(lambda acc, item: acc + item['quantity'], cart, 0)

# Main flow of the shopping cart system
def main():
    print("Initial Shopping Cart:", shopping_cart)

    # Step 1: Calculate the total price of items before any discount or tax
    original_total = get_total(shopping_cart)
    print(f"Original Total: ${original_total:.2f}")
    
    # Step 2: Apply a 10% discount on all items using a higher-order function and currying
    ten_percent_discount = discount_percentage(10)
    discounted_cart = apply_discount(shopping_cart, ten_percent_discount)
    discounted_total = get_total(discounted_cart)
    print(f"Total after 10% Discount: ${discounted_total:.2f}")
    
    # Step 3: Add 10% tax to each item using map
    cart_with_tax = add_tax(discounted_cart)
    total_with_tax = get_total(cart_with_tax)
    print(f"Total after 10% Discount and 10% Tax: ${total_with_tax:.2f}")

    # Step 4: Filter out items costing more than $100
    expensive_items = filter_expensive_items(cart_with_tax, 100)
    print("Expensive Items (>$100):", expensive_items)

    # Step 5: Calculate the total quantity of items using reduce
    total_items_quantity = total_quantity(shopping_cart)
    print(f"Total Quantity of Items: {total_items_quantity}")

# Run the shopping cart system
main()

```

    Initial Shopping Cart: [{'name': 'Laptop', 'price': 1000, 'quantity': 1}, {'name': 'Smartphone', 'price': 500, 'quantity': 2}, {'name': 'Headphones', 'price': 100, 'quantity': 3}, {'name': 'Mouse', 'price': 50, 'quantity': 2}, {'name': 'Keyboard', 'price': 70, 'quantity': 1}]
    Action: Calculate Total completed successfully.
    Original Total: $2470.00
    Action: Calculate Total completed successfully.
    Total after 10% Discount: $2223.00
    Action: Calculate Total completed successfully.
    Total after 10% Discount and 10% Tax: $2445.30
    Expensive Items (>$100): [{'name': 'Laptop', 'price': 990.0000000000001, 'quantity': 1}, {'name': 'Smartphone', 'price': 495.00000000000006, 'quantity': 2}]
    Total Quantity of Items: 9

