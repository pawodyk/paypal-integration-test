from flask import Flask, render_template, request, url_for, redirect
import braintree
import os


gateway = braintree.BraintreeGateway(
  braintree.Configuration(
    environment=braintree.Environment.Sandbox,
    merchant_id=os.getenv("MERCHANT_ID"),
    public_key=os.getenv("PUBLIC_KEY"),
    private_key=os.getenv("PRIVATE_KEY")
  )
)



app = Flask(__name__)

@app.route("/")
def home():
  return render_template('index.html')

@app.get("/checkout")
def render_checkout():
  return render_template("checkout.html")

@app.post("/payment")
def process_payment():
  payload = request.get_json()
  print(payload)
  print(payload["nonce"], payload["type"])
  try:
    result = gateway.transaction.sale({
        "amount": "10.00",
        "payment_method_nonce": payload["nonce"],
        "options": {
          "submit_for_settlement": True
        }
    })
    if result.is_success:
      print("successful payment", result.transaction.id)
    else:
      print(result)

  except Exception as ex:
    print(ex)

  return render_template("checkout.html") # redirect(url_for("render_checkout"))

@app.route("/refund")
def refund_payment():
  return redirect(url_for("home"))