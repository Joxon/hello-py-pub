# coding=utf-8

import time
from _thread import start_new_thread

from requests_html import HTMLSession

ACCOUNT = ''
PASSWORD = ''

headers = \
    {'Host': 'jwxt.bupt.edu.cn',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
     'Accept-Language': 'en-US,en-US;q=0.7,en;q=0.3',
     'Accept-Encoding': 'gzip, deflate',
     'Referer': 'http://jwxt.bupt.edu.cn/jwLoginAction.do',
     'Content-Type': 'application/x-www-form-urlencoded',
     # 'Content-Length': '46',
     'DNT': '1',
     'Connection': 'keep-alive',
     'Upgrade-Insecure-Requests': '1'}

# cookies = {'JSESSIONID': 'abcuwulHj2s2h6PrkYSrw'}

browser = HTMLSession()

url_code = 'http://jwxt.bupt.edu.cn/validateCodeAction.do?random='
r = browser.request('GET', url_code, headers=headers)

# TODO 检验验证码是否下载成功，只判断200不够充分
if (r.status_code != 200):
    print('验证码下载失败')
    exit(-1)

img_name = 'bupt-jwxt-code.jpg'
img_code = open(img_name, 'wb')
img_code.write(r.content)
img_code.close()
print(img_name + '已保存')

account = ACCOUNT  # input('账号：')
password = PASSWORD  # input('密码：')
code = input('验证码：')
data = {
    'zjh': account,  # 证件号
    'mm': password,  # 密码
    'type': 'sso',  # 类型
    'v_yzm': code
}  # v验证码

url_login = 'http://jwxt.bupt.edu.cn/jwLoginAction.do'
r = browser.request('POST', url_login, data=data, headers=headers)

title_ok = '学分制综合教务'
title_bad = 'URP 综合教务系统 - 登录'
alert_gif = '/img/icon/alert.gif'

if alert_gif in r.html.html:
    print('账号信息错误或验证码错误，登录失败，请重试')
    exit(-1)

elif title_bad in r.html.html:
    print('未填写验证码或其他错误，登录失败，请重试')
    exit(-2)

elif title_ok in r.html.html:

    def view_scores_only(s_list):
        idx = 7
        col = 1
        while idx < len(s_list):
            if col != 7:
                if col == 3:
                    course = s_list[idx]
                    print(course, end='： ')
                col = col + 1
            else:
                if ((not s_list[idx].isdigit()) or int(s_list[idx]) > 100
                        or int(s_list[idx]) < 0):
                    print('')
                    idx = idx - 1
                else:
                    score = s_list[idx]
                    print(score)
                col = 1
            idx = idx + 1
        print('\n')

    def view_scores_all(s_list):
        # print(score_list)
        # [0]-[6] are titles
        idx = 0
        while idx < 7:
            print(s_list[idx], end=' ')
            idx = idx + 1
        print('')

        idx = 7
        col = 1
        while idx < len(s_list):
            if col != 7:
                print(s_list[idx], end=' ')
                col = col + 1
            else:
                if ((not s_list[idx].isdigit()) or int(s_list[idx]) > 100
                        or int(s_list[idx]) < 0):
                    print('')
                    idx = idx - 1
                else:
                    print(s_list[idx])
                col = 1
            idx = idx + 1
        print('\n')

    def input_func(p):
        input()
        p.append(True)
        return

    print('登录成功')
    prompt = '11.选课-单次\n' \
             '12.选课-监控\n' \
             '21.本学期查分-精简\n' \
             '22.本学期查分-完整\n' \
             '23.本学期查分-监控\n' \
             '3.毕设题目介绍\n' \
             'q.退出\n' \
             '请输入：'
    sel = input(prompt)

    while sel != 'q':
        if sel == '11':
            # TODO 选课失败，原因未知
            headers[
                'Referer'] = 'http://jwxt.bupt.edu.cn/xkAction.do?actionType=1'
            url_course_view = 'http://jwxt.bupt.edu.cn/xkAction.do?actionType=-1'
            browser.request('GET', url_course_view, headers=headers)

            course_id = input('请输入课程ID：')
            course_data = {
                'actionType': '9',
                'kcId': course_id,
                'preActionType': '1'
            }
            url_course_pick = 'http://jwxt.bupt.edu.cn/xkAction.do'
            r = browser.request(
                'POST', url_course_pick, data=course_data, headers=headers)

            msg_success = '选课成功'
            if msg_success in r.html.text:
                print(msg_success)
            else:
                print('选课失败')

        elif sel == '12':
            pressed = []
            input_thread = start_new_thread(input_func, (pressed, ))

            headers[
                'Referer'] = 'http://jwxt.bupt.edu.cn/xkAction.do?actionType=1'
            url_course_view = 'http://jwxt.bupt.edu.cn/xkAction.do?actionType=-1'
            r = browser.request('GET', url_course_view, headers=headers)

            # 操作ID
            # 'actionType': '9' 选课
            # POST: http://jwxt.bupt.edu.cn/xkAction.do
            # "postData": {
            #             "mimeType": "application/x-www-form-urlencoded",
            #             "params": [
            #               {
            #                 "name": "kcId",
            #                 "value": "3132121150_01"
            #               },
            #               {
            #                 "name": "kcId",
            #                 "value": "3132131010_02"
            #               },
            #               {
            #                 "name": "preActionType",
            #                 "value": "1"
            #               },
            #               {
            #                 "name": "actionType",
            #                 "value": "9"
            #               }
            #             ],
            #             "text": "kcId=3132121150_01&kcId=3132131010_02&preActionType=1&actionType=9"
            #           }
            # 'actionType': '10' 退课
            # GET: http://jwxt.bupt.edu.cn/xkAction.do?actionType=10&kcId=3132121150
            # 课程ID
            # 'kcId': '3132111080_02' Web开发技术
            # 'kcId': '3132112090_01' 软件工程综合设计与实验
            # 'kcId': '3132114080_01' 数字媒体内容综合设计与实验

            course_data = {
                'actionType': '9',
                'kcId': '3132111080_02',
                'preActionType': '1'
            }
            headers[
                'Referer'] = 'http://jwxt.bupt.edu.cn/xkAction.do?actionType=1'
            url_course_pick = 'http://jwxt.bupt.edu.cn/xkAction.do'

            interval = 1
            print('\n开始监控，回车停止，每' + str(interval) + 's刷新一次...')
            msg_success = '选课成功'
            while not pressed:
                r = browser.request(
                    'POST', url_course_pick, data=course_data, headers=headers)
                if msg_success in r.html.text:
                    print('[' + time.ctime() + ']')
                    print(msg_success)
                time.sleep(interval)

        elif sel == '21':
            headers['Referer'] = 'http://jwxt.bupt.edu.cn/menu/s_menu.jsp'
            url_scores = 'http://jwxt.bupt.edu.cn/bxqcjcxAction.do'
            r = browser.request('GET', url_scores, headers=headers)
            try:
                scores = r.html.find('#user', first=True).text
                print('\n本学期成绩：')
                view_scores_only(scores.split('\n'))
            except AttributeError:
                print('服务器返回了异常数据，请重试')

        elif sel == '22':
            headers['Referer'] = 'http://jwxt.bupt.edu.cn/menu/s_menu.jsp'
            url_scores = 'http://jwxt.bupt.edu.cn/bxqcjcxAction.do'
            r = browser.request('GET', url_scores, headers=headers)
            try:
                scores = r.html.find('#user', first=True).text
                print('\n本学期成绩：')
                view_scores_all(scores.split('\n'))
            except AttributeError:
                print('服务器返回了异常数据，请重试')

        elif sel == '23':
            pressed = []
            input_thread = start_new_thread(input_func, (pressed, ))

            headers['Referer'] = 'http://jwxt.bupt.edu.cn/menu/s_menu.jsp'
            url_scores = 'http://jwxt.bupt.edu.cn/bxqcjcxAction.do'
            r = browser.request('GET', url_scores, headers=headers)

            try:
                scores_old = r.html.find('#user', first=True).text
                interval = 1
                print('\n当前成绩：')
                view_scores_only(scores_old.split('\n'))
                print('开始监控，回车停止，每' + str(interval) + 's刷新一次...')
                time.sleep(interval)
                while not pressed:
                    r = browser.request('GET', url_scores, headers=headers)
                    scores_new = r.html.find('#user', first=True).text
                    if scores_old == scores_new:
                        pass
                        # print('无变化，等待' + str(interval) + 's...')
                    else:
                        print('[' + time.ctime() + ']')
                        print('检测到变化！新的成绩如下：')
                        view_scores_only(scores_new.split('\n'))
                        # break
                        # scores_old = scores_new
                    time.sleep(interval)
            except AttributeError:
                print('服务器返回了异常数据，请重试')

        elif sel == '3':
            # function m_view(zxjxjhh,tmbh){
            #     showModalDialog("shtmAction.do?actionType=5&zxjxjhh="+zxjxjhh+"&tmbh="+tmbh, window,
            #     "dialogWidth:800px;dialogHeight:640px;help:no;status:no");
            # } showModalDialog 已被废弃，仅IE支持
            # zxjxjhh
            # tmbh 题目标号
            tmbh_start = int(input('输入开始标号：'))
            tmbh_end = int(input('输入结束标号：'))

            txt = open(
                'bupt-designs-' + str(tmbh_start) + '-' + str(tmbh_end) +
                '.txt',
                'w',
                encoding='utf-8')
            zxjxjhh = '2018-2019-1-2'
            tmbh = tmbh_start
            url_shtm = 'http://jwxt.bupt.edu.cn/shtmAction.do?actionType=5&zxjxjhh=' + zxjxjhh + '&tmbh=' + str(
                tmbh)
            while tmbh < tmbh_end:
                r = browser.request('GET', url_shtm, headers=headers)
                txt.write('\n\n题目标号：' + str(tmbh) + '\n')
                txt.write(r.html.text)
                tmbh += 1
                url_shtm = 'http://jwxt.bupt.edu.cn/shtmAction.do?actionType=5&zxjxjhh=' + zxjxjhh + '&tmbh=' + str(
                    tmbh)
            txt.close()

        else:
            print('未知选项\n')

        sel = input(prompt)

else:
    print('未知状态')
