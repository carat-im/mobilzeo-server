import requests
import csv
from bs4 import BeautifulSoup
import re


def toMB(s):
    if 'MB' in s:
        return s.replace("MB", "").replace(" ", "")
    elif 'GB' in s:
        return int(float(s.replace("GB", "")) * 1000)
    else:
        print(s)
        return ''


def GBtoMB(s):
    return int(float(s.replace("GB", "")) * 1000)


def getNums(s):
    return re.findall(r'\d+', s)


url = "https://www.smartelmall.com/sub/charge/recom_new.asp"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

main_table = soup.findAll(class_="list_view")

table = []
for m in main_table:
    table += m.findAll("li")

print(len(table))

for row in table:
    a = row.find(class_="head").find("p").text

with open("../csv/4_smartelmall.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "data_per_month", "data_per_day", "call_minutes", "text_messages", "price_initial",
                     "mobile_carrier_id", "carrier_url"])
    for row in table:
        name = row.find(class_="head").find("p").text

        tds = row.find(class_="info").findAll("td")

        call = tds[0].text
        text = tds[1].text
        data = tds[2].text

        call_minutes = 0
        if '기본제공' in call or '무제한' in call:
            call_minutes = -1
        elif '-' in call:
            call_minutes = 0
        else:
            call_minutes = re.findall(r'\d+', call)[0]

        text_messages = 0
        if '기본제공' in text or '무제한' in text:
            text_messages = -1
        elif '-' in text:
            text_messages = 0
        else:
            text_messages = re.findall(r'\d+', text)[0]

        data_per_month = 0
        data_per_day = 0

        if "+" in data and '/일' in data:
            month = data.split("+")[0]
            day = data.split("+")[1]

            data_per_month = toMB(month)
            if '/일' in day:
                data_per_day = toMB(day.split("/일")[0])
        elif 'MB' in data:
            data_per_month = getNums(data)[0]
        else:
            data_per_month = GBtoMB(getNums(data)[0])

        price_initial = "".join(re.findall(r'\d+', row.find(class_="price").find("span").text))
        mobile_carrier_id = 4

        carrier_url = "https://www.smartelmall.com" + row.find("a").get('href')

        writer.writerow(
            [name, data_per_month, data_per_day, call_minutes, text_messages, price_initial, mobile_carrier_id,
             carrier_url])
