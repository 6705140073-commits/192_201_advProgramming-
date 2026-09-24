"""
Assignment 03 — Refactor the Messy Store System
192-201 Advanced Computer Programming with Generative AI
Week 5 — OOP Design & Refactoring

Student refactor based on the teacher-provided starter program.
The legacy section is kept as the behaviour reference.
"""

import io
import contextlib


# ==============================================================================
# LEGACY STORE SYSTEM — behaviour reference. DO NOT EDIT.
# ==============================================================================

PRODUCTS = [
    ("Laptop", 1200.0, "electronics"),
    ("Headphones", 200.0, "electronics"),
    ("Coffee Beans", 15.0, "food"),
    ("Notebook", 5.0, "stationery"),
    ("Water Bottle", 10.0, "food"),
    ("Monitor", 300.0, "electronics"),
    ("Pen", 2.0, "stationery"),
]

TAXRATE = 0.07
foodtax = 0.0

ORDERS = [
    ("Alice", "gold", [(0, 1), (1, 2), (2, 3)]),
    ("Bob", "none", [(3, 10), (6, 5)]),
    ("Charlie", "platinum", [(5, 2), (4, 6), (2, 2)]),
    ("Dana", "silver", [(1, 1), (3, 3), (6, 10)]),
]


def calc(o):
    global TAXRATE
    n = o[0]
    t = o[1]
    items = o[2]
    sub = 0.0
    tax = 0.0

    print("Receipt for " + n + " (" + t + ")")
    print("-" * 40)

    for it in items:
        pi = it[0]
        q = it[1]
        p = PRODUCTS[pi][1]
        nm = PRODUCTS[pi][0]
        cat = PRODUCTS[pi][2]
        line = p * q
        sub = sub + line

        if cat == "food":
            tax = tax + line * foodtax
        else:
            tax = tax + line * TAXRATE

        print(nm + " x" + str(q) + " = " + str(line))

    d = 0.0

    if t == "none":
        d = 0.0
    elif t == "silver":
        if sub > 100:
            d = sub * 0.05
        else:
            d = sub * 0.02
    elif t == "gold":
        if sub > 100:
            d = sub * 0.10
        else:
            d = sub * 0.05
    elif t == "platinum":
        if sub > 100:
            d = sub * 0.15
        else:
            d = sub * 0.10

    totalqty = 0
    for it in items:
        totalqty = totalqty + it[1]

    if totalqty >= 10:
        d = d + sub * 0.03

    total = sub - d + tax

    pts = 0
    if t == "none":
        pts = int(total // 10)
    elif t == "silver":
        pts = int(total // 10) * 2
    elif t == "gold":
        pts = int(total // 10) * 3
    elif t == "platinum":
        pts = int(total // 10) * 5

    print("-" * 40)
    print("Subtotal: " + str(round(sub, 2)))
    print("Discount: " + str(round(d, 2)))
    print("Tax: " + str(round(tax, 2)))
    print("Total: " + str(round(total, 2)))
    print("Points earned: " + str(pts))
    print("")

    return total


def legacy_main():
    grand = 0.0
    for order in ORDERS:
        grand = grand + calc(order)

    print("GRAND TOTAL (all orders): " + str(round(grand, 2)))


# ==============================================================================
# BEHAVIOUR LOCK
# ==============================================================================

def capture(function):
    """Run a function and return everything it printed."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        function()
    return buffer.getvalue()


GOLDEN_OUTPUT = capture(legacy_main)


# ==============================================================================
# REFACTORED SOLUTION
# ==============================================================================

# Named constants
TAX_RATE = 0.07
FOOD_TAX_RATE = 0.0
FOOD_CATEGORY = "food"
DISCOUNT_LIMIT = 100
BULK_LIMIT = 10
BULK_RATE = 0.03
POINTS_DIVISOR = 10
RECEIPT_LINE = "-" * 40


class Product:
    """Store the information and tax behaviour of one product."""

    def __init__(self, name, price, category):
        if price < 0:
            raise ValueError("Price cannot be negative")
        if not name:
            raise ValueError("Product name cannot be empty")

        self.name = name
        self.price = price
        self.category = category

    def line_total(self, quantity):
        return self.price * quantity

    def tax_for(self, quantity):
        """Calculate this product's tax."""
        if self.category == FOOD_CATEGORY:
            rate = FOOD_TAX_RATE
        else:
            rate = TAX_RATE

        return self.line_total(quantity) * rate


class OrderItem:
    """A product together with the quantity ordered."""

    def __init__(self, product, quantity):
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")

        self.product = product
        self.quantity = quantity

    def total(self):
        return self.product.line_total(self.quantity)

    def tax(self):
        return self.product.tax_for(self.quantity)


class Customer:
    """Base customer type. The base tier has no membership discount."""

    tier = "none"
    points_multiplier = 1

    def __init__(self, name):
        if not name:
            raise ValueError("Customer name cannot be empty")
        self.name = name

    def discount_rate(self, subtotal):
        return 0.0


class Silver(Customer):
    tier = "silver"
    points_multiplier = 2

    def discount_rate(self, subtotal):
        if subtotal > DISCOUNT_LIMIT:
            return 0.05
        return 0.02


class Gold(Customer):
    tier = "gold"
    points_multiplier = 3

    def discount_rate(self, subtotal):
        if subtotal > DISCOUNT_LIMIT:
            return 0.10
        return 0.05


class Platinum(Customer):
    tier = "platinum"
    points_multiplier = 5

    def discount_rate(self, subtotal):
        if subtotal > DISCOUNT_LIMIT:
            return 0.15
        return 0.10


class Order:
    """An order has one customer and a collection of order items."""

    def __init__(self, customer, items):
        self.customer = customer
        self.items = items

    def subtotal(self):
        return sum(item.total() for item in self.items)

    def discount(self):
        subtotal = self.subtotal()
        amount = subtotal * self.customer.discount_rate(subtotal)

        quantity = sum(item.quantity for item in self.items)
        if quantity >= BULK_LIMIT:
            amount += subtotal * BULK_RATE

        return amount

    def tax(self):
        return sum(item.tax() for item in self.items)

    def total(self):
        return self.subtotal() - self.discount() + self.tax()

    def points(self):
        return int(self.total() // POINTS_DIVISOR) * self.customer.points_multiplier

    def receipt(self):
        print("Receipt for " + self.customer.name + " (" + self.customer.tier + ")")
        print(RECEIPT_LINE)

        for item in self.items:
            print(
                item.product.name
                + " x"
                + str(item.quantity)
                + " = "
                + str(item.total())
            )

        print(RECEIPT_LINE)
        print("Subtotal: " + str(round(self.subtotal(), 2)))
        print("Discount: " + str(round(self.discount(), 2)))
        print("Tax: " + str(round(self.tax(), 2)))
        print("Total: " + str(round(self.total(), 2)))
        print("Points earned: " + str(self.points()))
        print("")


def refactored_main():
    products = [
        Product("Laptop", 1200.0, "electronics"),
        Product("Headphones", 200.0, "electronics"),
        Product("Coffee Beans", 15.0, "food"),
        Product("Notebook", 5.0, "stationery"),
        Product("Water Bottle", 10.0, "food"),
        Product("Monitor", 300.0, "electronics"),
        Product("Pen", 2.0, "stationery"),
    ]

    alice = Gold("Alice")
    bob = Customer("Bob")
    charlie = Platinum("Charlie")
    dana = Silver("Dana")

    orders = [
        Order(
            alice,
            [
                OrderItem(products[0], 1),
                OrderItem(products[1], 2),
                OrderItem(products[2], 3),
            ],
        ),
        Order(
            bob,
            [
                OrderItem(products[3], 10),
                OrderItem(products[6], 5),
            ],
        ),
        Order(
            charlie,
            [
                OrderItem(products[5], 2),
                OrderItem(products[4], 6),
                OrderItem(products[2], 2),
            ],
        ),
        Order(
            dana,
            [
                OrderItem(products[1], 1),
                OrderItem(products[3], 3),
                OrderItem(products[6], 10),
            ],
        ),
    ]

    grand_total = 0.0

    for order in orders:
        order.receipt()
        grand_total += order.total()

    print("GRAND TOTAL (all orders): " + str(round(grand_total, 2)))


# ==============================================================================
# SELF-TEST
# ==============================================================================

def _check():
    try:
        your_output = capture(refactored_main)
    except NotImplementedError:
        print("Solution not implemented yet.\n")
        print("Below is the TARGET output your refactor must reproduce exactly:\n")
        print(GOLDEN_OUTPUT)
        return

    if your_output == GOLDEN_OUTPUT:
        print("PASS - behaviour is unchanged. Your refactor is safe.\n")
    else:
        print("FAIL - the output changed, so this is not yet a valid refactor.\n")

        golden = GOLDEN_OUTPUT.splitlines()
        yours = your_output.splitlines()

        for i in range(max(len(golden), len(yours))):
            expected = golden[i] if i < len(golden) else "<no line>"
            actual = yours[i] if i < len(yours) else "<no line>"

            if expected != actual:
                print("First difference at line " + str(i + 1) + ":")
                print("  expected: " + repr(expected))
                print("  yours:    " + repr(actual))
                break


if __name__ == "__main__":
    _check()
