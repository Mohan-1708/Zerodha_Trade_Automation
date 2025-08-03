# from kiteconnect import KiteConnect
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
#
# # Zerodha credentials
# api_key = "lza9556095dg7wn2"
# api_secret = "8rhgrlk666b35vyuragzwqbiy6us4sme"
# kite = KiteConnect(api_key=api_key)
#
#
#
# # Google Sheet credentials
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name("wired-caldron-364108-aea19497bbd4.json", scope)
# client = gspread.authorize(creds)
# sheet = client.open("Multi Stock Signals").worksheet("Today Signal")
#
#
#
# kite = None  # Global instance
#
# def set_kite_client(api_key):
#     global kite
#     kite = KiteConnect(api_key=api_key)
#
# def generate_login_url():
#     return kite.login_url()
#
# def generate_access_token(request_token):
#     data = kite.generate_session(request_token, api_secret=api_secret)
#     kite.set_access_token(data["access_token"])
#     return data["access_token"]
#
# def place_gttorder():
#     rows = sheet.get_all_records()
#     for i, row in enumerate(rows, start=2):  # Start from row 2 in sheet
#         if row.get("Execute", "").strip().lower() == "yes":
#             try:
#                 tradingsymbol = row["Instrument"].strip().upper()
#                 Last_Traded_Price = int(row["Price"])
#                 exchange = row["Exchange"].strip().upper()
#                 txn_type_str = row["Transaction Type"].strip().upper()
#                 trigger_price = float(row["Trigger Price"])
#                 target_price = float(row["Target Price"])
#                 quantity = int(row["Quantity"])
#                 product = row["Product Type"].strip().upper()
#
#                 txn_type = kite.TRANSACTION_TYPE_BUY if txn_type_str == "BUY" else kite.TRANSACTION_TYPE_SELL
#
#                 # Set dummy last price for GTT (must differ from trigger by >0.25%)
#                 #dummy_last_price = trigger_price * 0.997 if txn_type == kite.TRANSACTION_TYPE_BUY else trigger_price * 1.003
#
#                 gtt_id = kite.place_gtt(
#                     trigger_type=kite.GTT_TYPE_SINGLE,
#                     tradingsymbol=tradingsymbol,
#                     exchange=exchange,
#                     trigger_values=[trigger_price],
#                     last_price=round(Last_Traded_Price, 2),
#                     orders=[
#                         {
#                             "transaction_type": txn_type,
#                             "quantity": quantity,
#                             "order_type": kite.ORDER_TYPE_LIMIT,
#                             "price": target_price,
#                             "product": product
#                         }
#                     ]
#                 )
#
#                 # Update Sheet
#                 sheet.update_cell(i, 17, f"✅ GTT ID: {gtt_id}")
#                 sheet.update_cell(i, 16, "")  # Clear Execute
#
#             except Exception as e:
#                 sheet.update_cell(i, 17, f"❌ {str(e)}")
#         else:
#             sheet.update_cell(i, 16, f"❌ Execute not marked as 'Yes'")
#
#
# def place_orders_from_sheet():
#     rows = sheet.get_all_records()
#     for i, row in enumerate(rows, start=2):
#         if row.get("Execute", "").strip().lower() == "yes":
#             try:
#                 symbol = row["Instrument"].strip().upper()
#                 quantity = int(row["Quantity"])
#                 txn_type = kite.TRANSACTION_TYPE_BUY if row["Transaction Type"].upper() == "BUY" else kite.TRANSACTION_TYPE_SELL
#                 exchange = row["Exchange"].strip().upper()
#                 product = row["Product Type"].strip().upper()
#                 order_type = row["Order Type"].strip().upper()
#                 variety = row["Variety"].strip().lower() or "regular"
#
#                 order_id = kite.place_order(
#                     variety=variety,
#                     exchange=exchange,
#                     tradingsymbol=symbol,
#                     transaction_type=txn_type,
#                     quantity=quantity,
#                     product=product,
#                     order_type=order_type
#                 )
#
#                 sheet.update_cell(i, 17, f"✅ Order placed: {order_id}")
#                 sheet.update_cell(i, 16, "")
#             except Exception as e:
#                 sheet.update_cell(i, 17, f"❌ {str(e)}")
#         else:
#             sheet.update_cell(i, 16, "❌ Not marked as 'Yes'")


from kiteconnect import KiteConnect
import gspread
from oauth2client.service_account import ServiceAccountCredentials

kite = None  # Global instance
api_secret = None  # Will be set at runtime

# ---------- Google Sheet credentials ----------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("wired-caldron-364108-aea19497bbd4.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Multi Stock Signals").worksheet("Today Signal")

# ---------- Kite Setup Functions ----------
def set_kite_client(api_key_val, api_secret_val):
    global kite, api_secret
    kite = KiteConnect(api_key=api_key_val)
    api_secret = api_secret_val


def generate_login_url():
    return kite.login_url()


def generate_access_token(request_token):
    data = kite.generate_session(request_token, api_secret=api_secret)
    kite.set_access_token(data["access_token"])
    return data["access_token"]


# ---------- Order Placement Functions ----------
def place_gttorder():
    rows = sheet.get_all_records()
    for i, row in enumerate(rows, start=2):
        if row.get("Execute", "").strip().lower() == "yes":
            try:
                tradingsymbol = row["Instrument"].strip().upper()
                last_price = float(row["Price"])
                exchange = row["Exchange"].strip().upper()
                txn_type_str = row["Transaction Type"].strip().upper()
                trigger_price = float(row["Trigger Price"])
                target_price = float(row["Target Price"])
                quantity = int(row["Quantity"])
                product = row["Product Type"].strip().upper()

                txn_type = kite.TRANSACTION_TYPE_BUY if txn_type_str == "BUY" else kite.TRANSACTION_TYPE_SELL

                gtt_id = kite.place_gtt(
                    trigger_type=kite.GTT_TYPE_SINGLE,
                    tradingsymbol=tradingsymbol,
                    exchange=exchange,
                    trigger_values=[trigger_price],
                    last_price=round(last_price, 2),
                    orders=[
                        {
                            "transaction_type": txn_type,
                            "quantity": quantity,
                            "order_type": kite.ORDER_TYPE_LIMIT,
                            "price": target_price,
                            "product": product
                        }
                    ]
                )

                sheet.update_cell(i, 17, f"✅ GTT ID: {gtt_id}")
                sheet.update_cell(i, 16, "")
            except Exception as e:
                sheet.update_cell(i, 17, f"❌ {str(e)}")
        else:
            sheet.update_cell(i, 16, f"❌ Execute not marked as 'Yes'")


def place_orders_from_sheet():
    rows = sheet.get_all_records()
    for i, row in enumerate(rows, start=2):
        if row.get("Execute", "").strip().lower() == "yes":
            try:
                symbol = row["Instrument"].strip().upper()
                quantity = int(row["Quantity"])
                txn_type = kite.TRANSACTION_TYPE_BUY if row["Transaction Type"].upper() == "BUY" else kite.TRANSACTION_TYPE_SELL
                exchange = row["Exchange"].strip().upper()
                product = row["Product Type"].strip().upper()
                order_type = row["Order Type"].strip().upper()
                variety = row.get("Variety", "regular").strip().lower() or "regular"

                order_id = kite.place_order(
                    variety=variety,
                    exchange=exchange,
                    tradingsymbol=symbol,
                    transaction_type=txn_type,
                    quantity=quantity,
                    product=product,
                    order_type=order_type
                )

                sheet.update_cell(i, 17, f"✅ Order placed: {order_id}")
                sheet.update_cell(i, 16, "")
            except Exception as e:
                sheet.update_cell(i, 17, f"❌ {str(e)}")
        else:
            sheet.update_cell(i, 16, "❌ Not marked as 'Yes'")
