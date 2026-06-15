import os, requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

api_key = os.getenv("API_KEY")
account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
from_number = os.getenv("FROM_NUM")
to_number = os.getenv("TO_NUM")

client = Client(account_sid, auth_token)

if not account_sid:
    raise ValueError("ACCOUNT_SID not found in .env file")
if not auth_token:
    raise ValueError("AUTH_TOKEN not found in .env file")
if not api_key:
    raise ValueError("API KEY not found in .env file")

longitude = 51.517845
latitude = 0.007740

url = "https://api.openweathermap.org/data/2.5/forecast"


params = {
    "lat": latitude,
    "lon": longitude,
    "cnt": 4,
    "units": "metric",
    "appid": api_key
}

r = requests.get(url,params)
data = r.json()
# print(data)
r.raise_for_status()
if r.status_code != 200:
    print("Error", data.get("message"))
else:
    weather_list = []
    for idx in range (4):
        print(data['list'][0]['weather'])
        weather_list.append(data['list'][idx]['weather'][0]['id'])
        data0 = data['list'][0]['weather']
        print(data0[0]['id'])
    print(weather_list)

    will_rain = False

    will_rain = any(200 < idx < 700 for idx in weather_list)
    if will_rain:
        print("Bring an umbrela! ☔")
        message = client.messages.create(
            from_=from_number,
            body='Bring an umbrela! ☔',
            to=to_number
        )
        print(message.status)

    else:
        print("Should be fine without an umbrela 🌞")
        message = client.messages.create(
            from_=from_number,
            body='Should be fine without an umbrela 🌞',
            to=to_number
        )
        print(message.status)
