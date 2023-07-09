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
        "currency": 'EUR',
        "payment_method_nonce": payload["nonce"],
        "options": {
          "submit_for_settlement": True
        }
    })
    if result.is_success:
      # print("successful payment", result.transaction.id)
      # return redirect(url_for(payment_success))
      return {"status": "success", "transactionID": result.transaction.id}, 201
    else:
      # print("this: ", result.transaction.__dict__.keys())
      # print("result.transaction.__dict__")
      errortxt = ""
      match result.transaction.status: 
        case "processor_declined":
          errortxt = "%s (%s)" % (result.transaction.processor_response_text, result.transaction.processor_response_code) 
        case "settlement_declined":
          errortxt = "%s (%s)" % (result.transaction.processor_settlement_response_text, result.transaction.processor_settlement_response_code) 
        case "gateway_rejected":
          errortxt = "Gateway rejected the payment"
        case _:
          errortxt = "Unknown Error"
      
      return {"status": result.transaction.status, "error_text": errortxt}, 403

  except Exception as ex:
    # print(ex)
    return "exception", 500 
  


@app.get("/refund")
def refund_page():
  return render_template("refund.html")

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
@app.post("/refund")
def refund_payment():
  transactionID = request.form.get("transactionID")
  data = {}

  try:
    result = gateway.transaction.refund(transactionID)
    if(result.transaction):
      if result.is_success:
        # print(result.transaction.status)
        # print(result.transaction.processor_response_code)
        # print(result.transaction.processor_response_text)
        data["status"] = "success"
      
      else:
        data["status"] = "fail"
        data['Error'] = result.transaction.processor_response_text
    else:
      raise Exception("Transaction could not be found")
  except Exception as ex:
    data["status"] = "exception"
    data['Error'] = str(ex)
    
  # print(data)  
  return render_template("refund.html", data = data)

if __name__ == "__main__":
  app.run(host=os.environ.get('IP', '127.0.0.1'), port=int(os.environ.get('PORT', 5000)), debug=False)