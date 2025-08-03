from flask import Flask, request, redirect, render_template, jsonify


from kite_service import generate_login_url, generate_access_token,  place_gttorder, place_orders_from_sheet

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    url = generate_login_url()
    return render_template("login.html", login_url=url)

@app.route("/callback")
def callback():
    request_token = request.args.get("request_token")
    access_token = generate_access_token(request_token)
    return render_template("result.html", message=f"Access Token Generated: {access_token}")

# @app.route("/place-order", methods=["POST"])
# def place_order_route():
#     data = request.form
#     order_data = {
#         "symbol": data["symbol"],
#         "quantity": int(data["quantity"]),
#         "transaction_type": data["transaction_type"],
#         "exchange": data["exchange"],
#         "product": data["product"],
#         "order_type": data["order_type"],
#         "variety": data["variety"]
#     }
#     result = place_order(order_data)
#     return render_template("result.html", message=result)

# @app.route("/place-gtt", methods=["POST"])
# def place_gtt_route():
#     data = request.form
#     order_data = {
#         "symbol": data["symbol"],
#         "quantity": int(data["quantity"]),
#         "transaction_type": data["transaction_type"],
#         "exchange": data["exchange"],
#         "product": data["product"],
#         "order_type": data["order_type"],
#         "trigger_price": float(data["trigger_price"]),
#         "last_price": float(data["last_price"]),
#         "order_price": float(data["order_price"]),
#         "trigger_type": data["trigger_type"]
#     }
#     result = place_gtt_order(order_data)
#     return render_template("result.html", message=result)

@app.route("/trigger-sheet-orders")
def trigger_sheet_orders():

    place_orders_from_sheet();

    return render_template("result.html" , message = "✅ Orders placed from sheet (check sheet for status)")






@app.route("/trigger-gtt-orders")
def trigger_gtt_order():
    place_gttorder();

    return render_template("result.html",message = "✅ Orders placed from sheet (check sheet for status)")


if __name__ == "__main__":
    app.run(debug=True)
