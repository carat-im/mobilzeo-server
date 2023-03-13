import csv
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

carrierId = 15


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
    s = s.strip("음성\n").strip("문자\n")

    if s == '기본' or '기본제공' in s or '집/이동전화 무제한' in s:
        return "-1"

    result = getNumFlat(s.replace("건", "").replace("분", ""))
    if result == '':
        print('hey : ' + s)

    return result


def getDataPerMonth(dataText):
    dataText = dataText.replace("데이터\n", "").strip('월')

    # 불안쓰
    if '매일' in dataText:
        return 0
    if str(dataText) == '0':
        return 0
    if dataText[0:1] == '일':
        return 0

    endIndex = len(dataText)
    if '+' in dataText:
        endIndex = min(endIndex, dataText.find('+'))
    if '(' in dataText:
        endIndex = min(endIndex, dataText.find('('))
    if '/' in dataText:
        endIndex = min(endIndex, dataText.find('/'))

    return toMB(dataText[:endIndex])


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


driver = webdriver.Chrome("/opt/homebrew/bin/chromedriver")
driver.get("https://www.sk7mobile.com/prod/data/callingPlanList.do?refCode=USIM")

with open("../csv/" + str(carrierId) + "_sk7.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "data_per_month", "data_per_day", "data_exhaustion_speed", "call_minutes", "text_messages",
                     "price_initial", "mobile_carrier_id", "cta_url"])

    for i in range(1, 12):
        if i > 1:
            driver.find_element(By.XPATH, '//*[@id="frm"]/div/div[3]/dl[' + str(i) + ']').click()
        time.sleep(1)

        plans = driver.find_elements(By.XPATH, '//*[@id="frm"]/div/div[3]/dl/dd/div/a')

        for plan in plans:
            print(plan.text)
            try:
                name = plan.find_element(By.XPATH, 'div/div/strong/span[1]').text
                call_minutes = getCallText(plan.find_element(By.XPATH, 'div/div/div/ul/li[2]').text)
                text_messages = getCallText(plan.find_element(By.XPATH, 'div/div/div/ul/li[3]').text)

                if call_minutes == '' or text_messages == '':
                    continue
                data = plan.find_element(By.XPATH, 'div/div/div/ul/li[1]').text

                data_per_month = getDataPerMonth(data)
                data_per_day = getDataPerDay(data)
                data_exhaustion_speed = getDataExhaustionSpeed(data)
                price_initial = getPrice(plan.find_element(By.XPATH, 'div/div/div/div/div/div/strong').text)

                mobile_carrier_id = carrierId
                # cta_url = plan.find_element(By.XPATH, 'div[2]/a').get_attribute('href')
                cta_url = "https://www.sk7mobile.com/prod/data/callingPlanList.do?refCode=USIM"

                writer.writerow(
                    [name, data_per_month, data_per_day, data_exhaustion_speed, call_minutes, text_messages,
                     price_initial,
                     mobile_carrier_id, cta_url])
            except:
                continue
