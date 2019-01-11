# coding = utf-8

import datetime
import sched
import time

import openpyxl
import requests

headers_str = '''Host: app.bupt.edu.cn
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0
Accept: */*
Accept-Language: en-US,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate, br
Referer: https://app.bupt.edu.cn/buptys/wap/default/index
X-Requested-With: XMLHttpRequest
DNT: 1
Connection: keep-alive
Cookie: eai-sess=3uu1645bp6augqduiq7kt5q1m6; UUkey=9f75a3463d03ace811734ee0c6494238
Pragma: no-cache
Cache-Control: no-cache
Content-Length: 0'''
headers = dict([line.split(": ", 1) for line in headers_str.split("\n")])
url = 'https://app.bupt.edu.cn/buptys/wap/default/get-data'
sch = sched.scheduler()
delay_sec = 60


def post_and_write():
    print(datetime.datetime.now().isoformat() + ' 开始执行...')
    res = requests.post(url, headers=headers)
    if res.status_code == 200:
        xlsx_name = 'bupt-bathroom.xlsx'
        try:
            wb = openpyxl.load_workbook(xlsx_name)
        except FileNotFoundError:
            wb = openpyxl.Workbook()
        ws = wb.active
        data = res.json()['d']['data']
        content = [
            datetime.datetime.now().isoformat(),
            data['total']['male_shower'],
            data['now']['male_shower'],
            data['now']['male'],
            data['total']['female_shower'],
            data['now']['female_shower'],
            data['now']['female'],
        ]
        ws.append(content)
        wb.save(xlsx_name)
        print(' '.join(str(s) for s in content) + ' 写入成功')
    else:
        print('HTTP Status ' + res.status_code)
    sch.enter(delay_sec, 1, post_and_write)


if __name__ == '__main__':
    sch.enter(delay_sec, 1, post_and_write)
    try:
        sch.run()
    except KeyboardInterrupt:
        pass
