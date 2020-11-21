import os
import os.path
import time
import json
import random
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

payload = {}
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvd3d3Lml0anV6aS5jb21cL2FwaVwvdXNlcnNcL3VzZXJfaGVhZGVyX2luZm8iLCJpYXQiOjE2MDU5MjA2NDMsImV4cCI6MTYwNTkzMDk4NSwibmJmIjoxNjA1OTI3Mzg1LCJqdGkiOiJRajBxelRsRnUzcHJ4MVlTIiwic3ViIjo4ODU2NTksInBydiI6IjIzYmQ1Yzg5NDlmNjAwYWRiMzllNzAxYzQwMDg3MmRiN2E1OTc2ZjciLCJ1dWlkIjoiY2twcHJvIn0.MAOpiwmlKGORrpizvCeaABQCL3RC6E7MqkmwXF2vQb8',
    'cookie': '_ga=GA1.2.1749298967.1601431547; MEIQIA_TRACK_ID=1iDALK8NzJJkpzQiJ3gGsFJsLOE; gr_user_id=1d00fc76-037f-4acc-aff6-20a0a2408e68; MEIQIA_VISIT_ID=1kJaAkxr52RaxYZkjSnF9h7N4nX; _gid=GA1.2.828805624.1605920588; juzi_user=885659; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1605405847,1605420428,1605920588,1605927478; juzi_token=Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvd3d3Lml0anV6aS5jb21cL2FwaVwvdXNlcnNcL3VzZXJfaGVhZGVyX2luZm8iLCJpYXQiOjE2MDU5MjA2NDMsImV4cCI6MTYwNTk1MzY3NywibmJmIjoxNjA1OTUwMDc3LCJqdGkiOiJpSnVkblhMeDdhTlZCS3BpIiwic3ViIjo4ODU2NTksInBydiI6IjIzYmQ1Yzg5NDlmNjAwYWRiMzllNzAxYzQwMDg3MmRiN2E1OTc2ZjciLCJ1dWlkIjoiY2twcHJvIn0.FEQhjExsmKCYNdHDghfQZ8oSZjuAVbAAsC106PdI_94; _gat_gtag_UA_59006131_1=1; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1605950170',
    'curlopt_followlocation': 'true',
    'referer': 'https://www.itjuzi.com/deathCompany',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin'
}


def save_to_file(info, pid):
    filename = str(pid) + '.json'
    with open(filename, 'w') as file_obj:
        json.dump(info, file_obj)


def check_existed_file(pid):
    fname = str(pid) + '.json'
    if os.path.isfile(fname):
        return True
    else:
        return False


# BlockingScheduler
scheduler = BlockingScheduler()


# 输出时间
def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# 输出时间
def get_company_info():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for i in range(6, 1442):
        if check_existed_file(i):
            print("第{}页已存在".format(str(i)))
            continue

        url = "https://www.itjuzi.com/api/closure?com_prov=&sort=&page={}&keyword=&cat_id=".format(i)
        print(url)
        print("开始延时")
        ti = random.randint(3, 7)
        print(ti)
        time.sleep(ti)
        print("延时结束")
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            tt = response.text.encode('utf8')
            tt = json.loads(tt)
            print(tt)
            save_to_file(tt, i)
            print("第{}页下载成功".format(str(i)))
        except Exception as e:
            print(e)


# scheduler.add_job(get_company_info, 'interval', minutes=1)
# scheduler.start()
get_company_info()


