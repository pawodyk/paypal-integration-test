# Integration of PayPal Payment using braintree API

Step 1
Your front-end requests a client token from your server and initializes the client SDK.

Step 2
Your server generates and sends a client token back to your client using the server SDK.

Step 3
The customer submits payment information, the client SDK communicates that information to Braintree and returns a payment method nonce.

Step 4
Your front-end sends the payment method nonce to your server.

Step 5
Your server code receives the payment method nonce and then uses the server SDK to create a transaction.