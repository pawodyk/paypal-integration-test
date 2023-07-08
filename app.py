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
  # print(payload)
  # print(payload["nonce"], payload["type"])
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
      # return redirect(url_for(payment_success))
    else:
      print("this: ", result)
    return {"status": "success", "transactionID": result.transaction.id}, 201

  except Exception as ex:
    print(ex)
    return "exception", 500 
  


@app.get("/refund")
def refund_page():
  return render_template("refund.html")

@app.post("/refund")
def refund_payment():
  transactionID = request.form.get("transactionID")
  data = {}
  try:
    result = gateway.transaction.refund(transactionID)

    if result.is_success:
      print(result.transaction.status)
      print(result.transaction.processor_response_code)
      print(result.transaction.processor_response_text)
      data["status"] = "success"

    else:
      '''
      result.is_success
      # false                             |   # false

      result.transaction.status
      # "processor_declined"              |   # "settlement_declined"

      result.transaction.processor_response_code
      # e.g. "2005"                       |  # e.g. "4001"

      result.transaction.processor_response_text
      # e.g. "Invalid Credit Card Number" |  # e.g. "Settlement Declined"
      '''
      pass
  except Exception as ex:
    data["status"] = "fail"
    data['Error'] = ex
    
  return render_template("refund.html", data = data)