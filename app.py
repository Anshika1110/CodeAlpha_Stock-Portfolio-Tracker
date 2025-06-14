from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

stock_prices = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOG": 2800,
    "MSFT": 320,
    "AMZN": 125
}

portfolio = {}

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        stock = request.form["stock"].upper()
        quantity = request.form["quantity"]

        if stock not in stock_prices:
            message = "❌ Stock not recognized."
        elif not quantity.isdigit():
            message = "❌ Please enter a valid quantity."
        else:
            quantity = int(quantity)
            portfolio[stock] = portfolio.get(stock, 0) + quantity
            message = f"✅ Added {quantity} shares of {stock}"

    total_value = sum(stock_prices[s] * q for s, q in portfolio.items())
    portfolio_details = [
        {"symbol": s, "quantity": q, "price": stock_prices[s], "value": stock_prices[s] * q}
        for s, q in portfolio.items()
    ]

    return render_template("index.html", portfolio=portfolio_details, total=total_value, message=message)

@app.route("/save")
def save():
    with open("portfolio_web.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Stock", "Quantity", "Price", "Value"])
        for stock, quantity in portfolio.items():
            price = stock_prices[stock]
            value = price * quantity
            writer.writerow([stock, quantity, price, value])
        total = sum(stock_prices[s] * q for s, q in portfolio.items())
        writer.writerow(["Total", "", "", total])
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
