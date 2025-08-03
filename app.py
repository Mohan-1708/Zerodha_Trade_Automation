from flask import Flask, request, redirect, render_template, jsonify


from kite_service import set_kite_client , generate_login_url, generate_access_token,  place_gttorder, place_orders_from_sheet

app = Flask(__name__)

#default empty
session_store = {

}




@app.route("/")
def home():
    return render_template("index.html")

@app.route('/set_credentials', methods=['POST'])
def set_credentials():
    api_key = request.form['api_key']
    api_secret = request.form['api_secret']

    session_store['api_key'] = api_key
    session_store['api_secret'] = api_secret

    set_kite_client(api_key, api_secret)  # ✅ Pass both arguments
    return redirect('/login')


@app.route("/login")
def login():
    url = generate_login_url()
    return render_template("login.html", login_url=url)

@app.route("/callback")
def callback():
    request_token = request.args.get("request_token")

    access_token = generate_access_token(request_token)
    print(access_token)
    return render_template("result.html", message=f"Access Token Generated: {access_token}")


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
