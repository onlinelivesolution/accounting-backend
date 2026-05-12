from twilio.rest import Client

ACCOUNT_SID = "your_sid"
AUTH_TOKEN = "your_token"
FROM_NUMBER = "+1234567890"


def send_sms(phone: str, otp: str):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    client.messages.create(body=f"Your ERP OTP is {otp}", from_=FROM_NUMBER, to=phone)
