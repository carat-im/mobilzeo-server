import requests
import csv
from bs4 import BeautifulSoup

url = "https://www.snowman.co.kr/portal/chageAdtnsvc/ppdChage/list"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

table = soup.findAll(class_="service-pay-item")
print(len(table))

for row in table:
    a = row.find(class_="promotion").findAll(class_="item")
    # print(a[0])

with open("../csv/snowman.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "data_per_month", "call_minutes", "text_messages", "price_initial",
                     "mobile_carrier_id", "carrier_url"])
    for row in table:
        promotion = row.find(class_="promotion").findAll(class_="item")
        data = promotion[0]
        call = promotion[1]
        text = promotion[2]

        data_per_month = 0
        if '무제한' in data.text:
            data_per_month = -1
        elif data.findAll('em')[1] == 'MB':
            data_per_month = data.findAll('em')[0].text
        else:
            data_per_month = int(float(data.findAll('em')[0].text) * 1000)

        call_minutes = 0
        if call.text == '음성 무제한':
            call_minutes = -1
        else:
            print(call.text)
            call_minutes = call.text.replace("음성", "").replace(" ", "").replace("분", "")

        text_messages = 0
        if text.text == '문자 무제한':
            text_messages = -1
        else:
            print(text.text)
            text_messages = text.text.replace("문자", "").replace(" ", "").replace("건", "")

        name = row.find(class_="name").text
        price_initial = row.find(class_="price").find(class_="num").text.replace(",", "").replace("원", "")
        mobile_carrier_id = 3

        carrier_url = "https://www.snowman.co.kr/portal/chageAdtnsvc/ppdChage/list"

        writer.writerow(
            [name, data_per_month, call_minutes, text_messages, price_initial, mobile_carrier_id,
             carrier_url])
