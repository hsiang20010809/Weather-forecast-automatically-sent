import requests as req
import smtplib
import email.message
import schedule
import time
from datetime import datetime

my_email = "your_email_address"
target_email = ["your_target_email_address"]
password = "your_api_key"

def send_email():
    now = datetime.now().strftime("%Y-%m-%d")
    msg = email.message.EmailMessage()
    msg["From"] = my_email
    msg["To"] = target_email
    msg["Subject"] = f"今日天氣預報{now}"
    msg.set_content(get_weather())

    connection = smtplib.SMTP_SSL("smtp.gmail.com")
    connection.login(my_email, password)
    connection.send_message(msg)
    connection.close()
    print(f"{now} 天氣預報信件發送成功")


def get_weather():
    location = "新竹市" #根據需求自行更改
    params = {
    "Authorization":"你的中央氣象局api授權碼",
    "locationName":location
    }
    # 中央氣象局已更改主機網址為https://opendata.cwa.gov.tw
    res = req.get("https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001", params=params)

    data_list = [] 
    for i in range(0, 5):
        name = res.json()["records"]["location"][0]["weatherElement"][i]["elementName"]
        value = res.json()["records"]["location"][0]["weatherElement"][i]["time"][0]["parameter"]["parameterName"]
        data = f"{name}:{value}"
        data_list.append(data)
    
    all_data = "\n".join(data_list)
    illustrate = f"變數說明:Wx(天氣現象)、MaxT(最高溫度)、MinT(最低溫度)、CI(舒適度)、PoP(降雨機率)\n------------今日天氣預報({location})------------\n{all_data}"
    return illustrate

schedule.every().day.at("06:30:00").do(send_email) #每早6:30寄信

while True:
    schedule.run_pending() 
    time.sleep(1)

