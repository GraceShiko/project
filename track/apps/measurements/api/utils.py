from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
import base64
import africastalking
import time


class Payment(object):
    def __init__(self):
        self.endpoint = "https://gwt-water.herokuapp.com"
        self.Consumer_Key = "6Gv6nSOgc5KTbWF7IYUoWQqeHAUWvTh5"
        self.Consumer_Secret = "x8OAeOHvbeM2GUWl"
        self.Lipa_Na_Mpesa_Online_Shortcode = "174379"
        self.Lipa_Na_Mpesa_Online_PassKey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        self.AccountReference = "GWT water track"
        self.TransactionDesc = "GWT water track"
        self.Timestamp = (datetime.now()).strftime("%Y%m%d%H%M%S%z")

        password = self.Lipa_Na_Mpesa_Online_Shortcode + self.Lipa_Na_Mpesa_Online_PassKey + self.Timestamp
        password_bytes = password.encode('ascii')
        base64_bytes = base64.b64encode(password_bytes)
        self.password = base64_bytes.decode('ascii')
        print(self.password)

    def access_token(self):
        mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        data = (requests.get(mpesa_auth_url, auth=HTTPBasicAuth(self.Consumer_Key, self.Consumer_Secret)))
        print(data)
        data = data.json()
        print(data)
        return (data['access_token'])

    def stk_push(self, phone_number, price):
        self.phone_number = phone_number[-12:]
        token = (self.access_token())
        access_token = token 
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": self.Lipa_Na_Mpesa_Online_Shortcode,
            "Password": self.password,
            "Timestamp": self.Timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(price),
            "PartyA": self.phone_number,
            "PartyB": self.Lipa_Na_Mpesa_Online_Shortcode,
            "PhoneNumber": self.phone_number,
            "CallBackURL": self.endpoint+"/api/mpesa_stk_push",
            "AccountReference": self.AccountReference,
            "TransactionDesc": self.TransactionDesc
        }
        print(self.endpoint+"/api/mpesa_stk_push")
        response = requests.post(api_url, json=request, headers=headers)
        print(response.json())
        return (response.json())

    def send_sms(self, phone_number, message):
        username = "watertap"
        api_key = "f68451185b34fec9b4b2202447d5c2e238c68b0c60dd8c72e49e16ec2266a6ef"

        africastalking.initialize(username, api_key)
        sms = africastalking.SMS

        try:
            response = sms.send(message, [ phone_number])  # Enter your phone number here
            print(response)
        except Exception as e:
            print(f"Something went wrong {e}")
