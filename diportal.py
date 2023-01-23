from io import BytesIO
import pycurl
import json
from pprint import pprint
from datetime import date
import calendar
import re

deliveryPointId1 = "XXXXXXXXXX"
deliveryPointId2 = "XXXXXXXXXX"
businessPartnerId = "XXXXXXXXXX"
businessRoleId = "KZ"
source = "KOC"
profileRole = "null"
loadProfileRoles = "true"
deviceSerialNumber = "000XXXXXXXXXXXXXXX"
deviceEquipmentNumber = "000XXXXXXXXXXXXXXX"
xcsrf = "sdfsdfsdSDFERWerwerfjkn34"

today = date.today()
from_date = "{0}-{1}-01".format(today.year,today.month)
maxdays = calendar.monthrange(today.year, today.month)[1]
to_date   = "{0}-{1}-{2}".format(today.year,today.month,maxdays)


#useragent = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0"
#useragent = "Mozilla/5.0 (Unknown; Linux x86_64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.0.0 Safari/E7FBAF"
useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/517.36 (KHTML, like Gecko) Chrome/55.0.0.0 Safari/517.36"
secchua = "\"Google Chrome\";v=\"55\", \"Chromium\";v=\"55\", \"Not=A?Brand\";v=\"21\""
secchuaplatform = "\"Linux\""

spotreba = "{\n  \"filter\": {\n    \"deliveryPointId\": \""+deliveryPointId1+"\",\n    \"from\": \""+from_date+"\",\n    \"to\": \""+to_date+"\",\n    \"profileRole\": "+profileRole+",\n    \"loadProfileRoles\": "+loadProfileRoles+"\n  },\n  \"businessPartnerId\": \""+businessPartnerId+"\",\n  \"businessRoleId\": \""+businessRoleId+"\",\n  \"source\": \""+source+"\"\n}"
prebytok = "{\n  \"filter\": {\n    \"deliveryPointId\": \""+deliveryPointId2+"\",\n    \"from\": \""+from_date+"\",\n    \"to\": \""+to_date+"\",\n    \"profileRole\": "+profileRole+",\n    \"loadProfileRoles\": "+loadProfileRoles+"\n  },\n  \"businessPartnerId\": \""+businessPartnerId+"\",\n  \"businessRoleId\": \""+businessRoleId+"\",\n  \"source\": \""+source+"\"\n}"
vyuct = "{\n  \"filter\": {\n    \"deliveryPointId\": \""+deliveryPointId1+"\",\n    \"dateFrom\": \"2022-12-31\",\n    \"dateTo\": \""+to_date+"\",\n    \"deviceSerialNumber\": \""+deviceSerialNumber+"\",\n    \"deviceEquipmentNumber\": \""+deviceEquipmentNumber+"\"\n  },\n  \"businessPartnerId\": \""+businessPartnerId+"\",\n  \"businessRoleId\": \""+businessRoleId+"\"\n}";

def firstUrl(url0, data0):
    b_obj = BytesIO()
    crl = pycurl.Curl()
    crl.setopt(crl.URL, url0)
    crl.setopt(crl.COOKIEFILE, 'cookie.txt')
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.setopt(crl.SSL_VERIFYPEER, 1)
    crl.setopt(crl.SSL_VERIFYHOST, False)
    crl.setopt(crl.POST, 1)
    crl.setopt(crl.POSTFIELDS, data0)
    crl.setopt(crl.HTTPHEADER, [
        "Accept: application/json, text/plain, */*",
        "Accept-Language: en-US,en;q=0.9,hu;q=0.8,sk;q=0.7,cs;q=0.6",
        "Cache-Control: no-cache",
        "Connection: keep-alive",
        "Origin: https://www.diportal.sk",
        "Pragma: no-cache",
        "Referer: https://www.diportal.sk/portal/",
        "Sec-Fetch-Dest: empty",
        "Sec-Fetch-Mode: cors",
        "Sec-Fetch-Site: same-origin",
        "User-Agent: "+useragent+"",
        "X-CSRF: {0}".format(xcsrf),
        "content-type: application/json",
        "sec-ch-ua: "+secchua+"",
        "sec-ch-ua-mobile: ?0",
        "sec-ch-ua-platform: "+secchuaplatform+""
    ])
    crl.perform()
    get_body = b_obj.getvalue()
    if re.search(b"Chybov", get_body.decode('latin-1').encode("utf-8")):
        print("Chyba, pravdepodobne cookie!")
        exit(0)
    elif re.search(b"Request Rejected", get_body.decode('latin-1').encode("utf-8")):
        print("Chyba, pravdepodobne cookie!")
        exit(0)
    return get_body

def first(data00, data01):
    data = json.loads(firstUrl('https://www.diportal.sk/portal/api/interval-data/getProfileData', data00))
    if "dailyIntervalData" in data["data"]["profileData"]:
            print("\n{0}:".format(data01))
            no = len(data["data"]["profileData"]["dailyIntervalData"])
            for xn in range(no):
                if data["data"]["profileData"]["dailyIntervalData"][xn]["dailyState"] == "ALL_VALID":
                    date = data["data"]["profileData"]["dailyIntervalData"][xn]["date"]
                    consumption = data["data"]["profileData"]["dailyIntervalData"][xn]["consumption"]
                    measuredValueUnit = data["data"]["profileData"]["measuredValueUnit"]
                    print("{0} - {1} {2}".format(date,consumption,measuredValueUnit))

def second():
    data = json.loads(firstUrl('https://www.diportal.sk/portal/api/register-data/getData', vyuct))
    if "deviceSerialNumber" in data["data"][0]:
            print("\nVyrovnanie:")
            no = len(data["data"])
            for xn in range(no):
                if data["data"][xn]["deviceSerialNumber"] == deviceSerialNumber:
                    settlementDate = data["data"][xn]["settlementDate"]
                    counterId = data["data"][xn]["counterId"]
                    settlementState = data["data"][xn]["settlementState"];
                    print("{0} - {1} {2} kWh".format(settlementDate,counterId,settlementState))

first(spotreba, "Spotreba")
first(prebytok, "Prebytok")
second()
