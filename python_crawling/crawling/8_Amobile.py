import requests
import csv
from bs4 import BeautifulSoup
import re


def toMB(s):
    if 'MB' in s:
        return s.replace("MB", "").replace(" ", "")
    elif 'GB' in s or 'G' in s:
        return int(float(s.replace("GB", "").replace("G", "")) * 1000)
    else:
        print(s)
        return ''


def GBtoMB(s):
    return int(float(s.replace("GB", "")) * 1000)


def getNums(s):
    return re.findall(r'\d+', s)


def getNumFlat(s):
    return "".join(getNums(s))


def getCallText(s):
    if s == '기본':
        return "-1"
    return s.replace("건", "").replace("분", "")


url = "https://www.amobile.co.kr/plan"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

table = [x for x in soup.findAll('tr') if x.find(class_="plan_list_tit").text.replace("\n", "") != '요금제명']

print(len(table))

for row in table:
    a = row.find(class_="plan_list_tit").text.replace("\n", "")
    # print(a)

with open("../csv/8_amobile.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "data_per_month", "call_minutes", "text_messages", "price_initial",
                     "mobile_carrier_id", "carrier_url"])
    for row in table:
        name = row.find(class_="plan_list_tit").text.replace("\n", "")

        tr = row.findAll("td")
        data = tr[3].text.replace("+1Mbps", "").replace("+3Mbps", "").replace("+5Mbps", "").replace("+10Mbps", "")
        print(data)

        call_minutes = getCallText(tr[1].text)
        text_messages = getCallText(tr[2].text)
        data_per_month = data
        if '+' not in data and '(' not in data:
            data_per_month = toMB(data)

        price_initial = getNumFlat(tr[7].text.split("(")[0].replace("\n", ""))
        mobile_carrier_id = 8

        carrier_url = "https://www.amobile.co.kr" + row.find("a").get('href')

        writer.writerow(
            [name, data_per_month, call_minutes, text_messages, price_initial, mobile_carrier_id,
             carrier_url])
