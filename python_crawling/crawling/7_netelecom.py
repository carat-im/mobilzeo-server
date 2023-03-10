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


url = "http://www.n-telecom.co.kr/products/KTdefer_lte.jsp"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

table = soup.findAll(class_="collapsed planT")

print(len(table))

for row in table:
    a = row.find(class_="row").findAll('div')[0].text
    print(a)

with open("../csv/7_ntelecom.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "data_per_month", "call_minutes", "text_messages", "price_initial",
                     "mobile_carrier_id", "carrier_url"])
    for row in table:
        name = row.find(class_="row").findAll('div')[0].text

        tr = row.find("tr").findAll("td")

        call_minutes = tr[1].text
        text_messages = tr[3].text
        data_per_month = tr[5].text

        price_initial = "".join(re.findall(r'\d+', row.find(class_="payT2").text))
        mobile_carrier_id = 7

        # carrier_url = "https://www.eyes.co.kr" + row.find("btn").find("a").get('href')
        carrier_url = "http://www.n-telecom.co.kr/products/KTdefer_lte.jsp"

        writer.writerow(
            [name, data_per_month, call_minutes, text_messages, price_initial, mobile_carrier_id,
             carrier_url])
