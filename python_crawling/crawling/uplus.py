import requests
import csv
from bs4 import BeautifulSoup

# send a request to the URL
url = "https://www.uplusumobile.com/product/pric/usim/pricList"
response = requests.get(url)

# parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# find the table with plan information
table = soup.findAll(class_="acc-conts-wrap")
print(len(table))

for row in table:
    a = row.find(class_="discount-pay").text.replace(",", "").replace("원", "")
    # print(a)

with open("../csv/uplusmobile.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "data_per_month", "data_per_day", "call_minutes", "text_messages", "price_initial",
                     "mobile_carrier_id", "carrier_url"])
    for row in table:
        data = row.find(class_="vol").text

        data_per_month = 0
        data_per_day = 0
        if data[0] == "일":
            data_per_month = 0
            data_per_day = data[1:-2] + "000"
        elif "+" in data:
            month = data.split("+일")[0]
            day = data.split("+일")[1]
            if "GB" in month:
                data_per_month = int(float(month[:-2]) * 1000)
            else:
                data_per_month = month[:-2]
            data_per_day = day[:-2]
        else:
            if "GB" in data:
                print(data)
                data_per_month = int(float(data.replace("GB", "").replace(" ", "")) * 1000)
            else:
                data_per_month = data[:-2]
        print(data_per_month)

        name = row.find(class_="title").text
        call_minutes = row.find(class_="limit").text.replace("분", "").replace("무제한", "-1").replace("미제공", "0")
        text_messages = row.find(class_="supply").text.replace("건", "").replace("기본제공", "-1").replace("미제공", "0")
        price_initial = row.find(class_="discount-pay").text.replace(",", "").replace("원", "")
        mobile_carrier_id = 2

        carrier_url_data = row.find('a', href=True)
        base_url = "https://www.uplusumobile.com/product/pric/pricDetail?seq="
        base_url2 = "&upPpnCd="
        base_url3 = "&devKdCd="
        carrier_url = base_url + carrier_url_data['seq'] + base_url2 + carrier_url_data['upppncd'] + base_url3 + \
                      carrier_url_data['ctgrid']

        writer.writerow(
            [name, data_per_month, data_per_day, call_minutes, text_messages, price_initial, mobile_carrier_id,
             carrier_url])
