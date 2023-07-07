from flask import Flask, render_template, request, url_for, redirect
import braintree


gateway = braintree.BraintreeGateway(
  braintree.Configuration(
      braintree.Environment.Sandbox,
      merchant_id="use_your_merchant_id",
      public_key="use_your_public_key",
      private_key="use_your_private_key"
  )
)


app = Flask(__name__)

@app.route("/")
def home():
  return render_template('index.html')

@app.get("/checkout")
def render_checkout():
  return render_template("checkout.html")

@app.post("/checkout")
def process_checkout():
  return "<p> checkout completed"