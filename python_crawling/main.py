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

# print(table)

for t in table:
    title = t.find(class_="vol")
    title.text
    print(title.text)

# create a CSV file and write the plan information to it
with open("csv/uplusmobile.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "data_per_month", "call_minutes", "text_messages", "price_initial", "mobile_carrier_id",
                     "carrier_url"])
    for row in table:
        name = row.find(class_="title").text
        data_per_month = row.find(class_="vol").text
        call_minutes = row.find(class_="limit").text
        text_messages = row.find(class_="supply").text
        price_initial = row.find(class_="discount-pay").text
        mobile_carrier_id = 2

        carrier_url_data = row.find('a', href=True)
        base_url = "https://www.uplusumobile.com/product/pric/pricDetail?seq="
        base_url2 = "&upPpnCd="
        base_url3 = "&devKdCd="
        carrier_url = base_url + carrier_url_data['seq'] + base_url2 + carrier_url_data['upppncd'] + base_url3 + \
                      carrier_url_data['ctgrid']

        writer.writerow(
            [name, data_per_month, call_minutes, text_messages, price_initial, mobile_carrier_id, carrier_url])
