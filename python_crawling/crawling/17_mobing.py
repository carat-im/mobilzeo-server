import csv
import re
import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.request import urlopen

carrierId = 17


def toMB(s):
    if 'MB' in s:
        return s.replace("MB", "").replace(" ", "")
    elif 'GB' in s or 'G' in s:
        return int(float(s.replace("GB", "").replace("G", "")) * 1000)
    else:
        print('hey : toMB : ' + s)
        return ''


def GBtoMB(s):
    return int(float(s.replace("GB", "")) * 1000)


def getNums(s):
    return re.findall(r'\d+', s)


def getNumFlat(s):
    return "".join(getNums(s))


def getCallText(s):
    s = s.strip("음성\n").strip("문자\n")

    if s == '기본' or '기본제공' in s or '집/이동전화 무제한' in s:
        return "-1"

    result = getNumFlat(s.replace("건", "").replace("분", ""))
    if result == '':
        print('hey : ' + s)

    return result


def getDataPerMonth(dataText):
    dataText = dataText.replace("데이터\n", "").strip('월').replace("\n", "")

    # 불안쓰
    if '매일' in dataText:
        return 0
    if str(dataText) == '0':
        return 0
    if dataText[0:1] == '일':
        return 0
    if dataText == '-':
        return 0

    endIndex = len(dataText)
    if '+' in dataText:
        endIndex = min(endIndex, dataText.find('+'))
    if '(' in dataText:
        endIndex = min(endIndex, dataText.find('('))
    if '/' in dataText:
        endIndex = min(endIndex, dataText.find('/'))

    result = toMB(dataText[:endIndex])
    if result == '':
        print('hey : datapermonth : ' + dataText)
        return 0

    return result


def getDataPerDay(dataText):
    if '일' not in dataText:
        return ''
    else:
        dataText = dataText.replace("추가사용", "")

        startIndex = dataText.index('일')
        endIndex = min(dataText.rfind('+'), len(dataText))
        return toMB(dataText[startIndex + 1: endIndex])


def getDataExhaustionSpeed(dataText):
    if 'Mbps' not in dataText and 'kbps' not in dataText and 'Kbps' not in dataText:
        return ''
    else:
        dataText = dataText.replace("최대", "")
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
            rawDataExhaustionSpeed = rawDataExhaustionSpeed.strip("최대")
            return int(float(rawDataExhaustionSpeed.replace("Mbps", "")) * 1000)
        else:
            print("hey  :" + rawDataExhaustionSpeed)
            return ''


def getPrice(price):
    return getNumFlat(price.replace('월', '').replace('원', ''))


# driver = webdriver.Chrome("/opt/homebrew/bin/chromedriver")
# driver.get("https://www.mobing.co.kr/product/plan/price")

with open("../csv/" + str(carrierId) + "_moving.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "data_per_month", "data_per_day", "data_exhaustion_speed", "call_minutes", "text_messages",
                     "price_initial", "mobile_carrier_id", "cta_url"])

    plans = []
    for i in range(1, 6):
        response = urlopen(
            'https://www.mobing.co.kr/api/product/getPlanList?page=1&limit=100&type=3&searchAmount=' + str(
                i) + '&serviceType=2')
        plans += json.loads(response.read())["entity"]["list"]

    print(len(plans))
    print(plans[0])

    for plan in plans:
        try:
            name = plan['planNM']
            call_minutes = 0
            if plan['basicVoice'] == 99999:
                call_minutes = -1
            else:
                call_minutes = plan['basicVoice']

            text_messages = 0
            if (plan['basicSms'] == 99999):
                text_messages = -1
            else:
                text_messages = plan['basicSms']

            if call_minutes == '' or text_messages == '':
                continue

            data_per_month = 0
            if plan['basicDataMon'] is not None:
                data_per_month = toMB(plan['basicDataMon'] + plan['basicDataMonUnit'])

            data_per_day = 0
            if plan['basicDataDay'] is not None:
                data_per_day = toMB(plan['basicDataDay'] + plan['basicDataDayUnit'])

            data_exhaustion_speed = ''
            if plan['basicQos'] is not None:
                data_exhaustion_speed = getDataExhaustionSpeed(plan['basicQos'] + plan['basicQosUnit'])

            price_initial = plan['totalAmountMon']

            mobile_carrier_id = carrierId
            cta_url = "https://www.mobing.co.kr/product/plan/view?planID=" + plan['planID']

            writer.writerow(
                [name, data_per_month, data_per_day, data_exhaustion_speed, call_minutes, text_messages,
                 price_initial,
                 mobile_carrier_id, cta_url])
        except:
            print('e')
            continue
