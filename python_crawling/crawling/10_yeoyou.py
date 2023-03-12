import csv
import re
import time

from selenium import webdriver


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
    if s == '기본' or '기본제공' in s:
        return "-1"

    if '링' in s:
        return int(float(getNumFlat(s)) / 2.5 / 60)
    return getNumFlat(s.replace("건", "").replace("분", ""))


def getDataPerMonth(dataText):
    # 불안쓰
    if '매일' in dataText:
        return 0
    if str(dataText) == '0':
        return 0
    if '+' in dataText:
        return toMB(dataText.split('+')[0])
    elif '(' in dataText:
        return toMB(dataText.split('(')[0])
    else:
        return toMB(dataText)


def getDataPerDay(dataText):
    if '일' not in dataText:
        return 0
    else:
        startIndex = dataText.index('일')
        endIndex = min(dataText.rfind('+'), len(dataText))
        return toMB(dataText[startIndex + 1: endIndex])


def getDataExhaustionSpeed(dataText):
    if 'Mbps' not in dataText and 'kbps' not in dataText and 'Kbps' not in dataText:
        return ''
    else:
        endIndex = max(dataText.find('Mbps'), dataText.find('kbps'), dataText.find('Kbps')) + 4

        startIndex = 0
        if dataText.rfind('+') >= 0:
            startIndex = dataText.rfind('+') + 1
        if dataText.rfind('소진후') >= 0:
            startIndex = max(startIndex, dataText.rfind('소진후') + 3)
        if dataText.rfind('소진 후') >= 0:
            startIndex = max(startIndex, dataText.rfind('소진 후') + 4)
        if dataText.rfind('소진후 속도제한') >= 0:
            startIndex = max(startIndex, dataText.rfind('소진후 속도제한') + 8)

        rawDataExhaustionSpeed = dataText[startIndex: endIndex].replace('기본제공', '')

        if 'kbps' in rawDataExhaustionSpeed or 'Kbps' in rawDataExhaustionSpeed:
            return rawDataExhaustionSpeed.replace("kbps", "").replace("Kbps", "").replace(" ", "")
        elif 'Mbps' in rawDataExhaustionSpeed:
            return int(float(rawDataExhaustionSpeed.replace("Mbps", "")) * 1000)
        else:
            print("hey  :" + rawDataExhaustionSpeed)
            return ''


def getPrice(price):
    return getNumFlat(price.replace('월', '').replace('원', ''))


driver = webdriver.Chrome("/opt/homebrew/bin/chromedriver")
driver.get("https://www.yytelecom.co.kr/TelePaymentCtrls/RateListAll/telecom_type:lg")

with open("../csv/10_yeoyou.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "data_per_month", "data_per_day", "data_exhaustion_speed", "call_minutes", "text_messages",
                     "price_initial", "mobile_carrier_id", "cta_url"])

    for i in range(2, 8):
        driver.find_element("xpath", '//*[@id="rate_wrap"]/div/ul/li[' + str(i) + ']/a').click()

        time.sleep(1)

        plans = driver.find_element("xpath", '//*[@id="lg' + str(i) + '"]/div/table/tbody') \
            .find_elements("xpath", '//*[@id="lg' + str(i) + '"]/div/table/tbody/tr')

        for plan in plans:
            name = plan.find_element("xpath", 'td[1]').text
            print(name)
            call_minutes = getCallText(plan.find_element("xpath", 'td[2]').text)
            text_messages = getCallText(plan.find_element("xpath", 'td[3]').text)

            data = plan.find_element("xpath", 'td[4]').text
            data_per_month = getDataPerMonth(data)
            data_per_day = getDataPerDay(data)
            data_exhaustion_speed = getDataExhaustionSpeed(data)

            price_initial = getPrice(plan.find_element("xpath", 'td[5]').text)

            mobile_carrier_id = 10
            cta_url = "https://www.yytelecom.co.kr/TelePaymentCtrls/RateListAll/telecom_type:lg"

            writer.writerow(
                [name, data_per_month, data_per_day, data_exhaustion_speed, call_minutes, text_messages, price_initial,
                 mobile_carrier_id, cta_url])
