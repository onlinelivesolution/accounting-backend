import requests


def send_sms(phone: str, message: str):

    payload = {
        "api_token": "YOUR_API_KEY",
        "sid": "YOUR_SID",
        "msisdn": phone,
        "sms": message,
        "csms_id": "123456"
    }

    response = requests.post(
        "https://smsplus.sslwireless.com/api/v3/send-sms",
        data=payload
    )

    return response.json()