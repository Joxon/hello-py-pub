# coding: utf-8

import sqlite3
import time
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler

from wxpy import *

from requests_html import HTMLSession

HOST = '0.0.0.0'
PORT = 9000

httpd = None
qrcode_viewed = False
img_tag = ''

MTDHB_ACCOUNT = ''
MTDHB_PASSWORD = ''


class QRCodeServerHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        paths = {
            '/': {
                'status': 200
            },
        }

        if self.path in paths:
            self.respond(paths[self.path])
        else:
            self.respond({'status': 500})

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        html = '''<html><head><title>WX-QRCode</title></head>
        <body style="background:dimgray;text-align:center;">
        <p style="color:white;font-size:xx-large;">QRCode generated at: %s</p>
        %s</body></html>''' % (time.asctime(), img_tag)

        return bytes(html, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)
        global qrcode_viewed
        qrcode_viewed = True


def on_qrcode_downloaded(uuid, status, qrcode):
    # uuid 4aPVGQ9cEA==
    # status 0
    # qrcode b'...'

    if qrcode == b'':
        print('qr_callback triggered with empty qrcode.')
        return

    global img_tag, httpd, qrcode_viewed
    img_tag = "<img src='data:image/png;base64,%s'/>" % str(
        base64.b64encode(qrcode)).split("'")[1]

    if httpd == None:
        httpd = HTTPServer((HOST, PORT), QRCodeServerHandler)
        if HOST == '0.0.0.0':
            print('HTTP server created on http://127.0.0.1:%s at %s' %
                  (PORT, time.asctime()))
        else:
            print('HTTP server created on http://%s:%s at %s' %
                  (HOST, PORT, time.asctime()))

    qrcode_viewed = False
    print('QRCode downloaded. HTTP server is running...')
    try:
        while not qrcode_viewed:
            httpd.handle_request()
        print('QRCode viewed. HTTP server frozen. Sleep for 5 seconds...')
        time.sleep(5)
    except Exception as e:
        print(str(e))


def on_user_logined():
    global httpd
    if isinstance(httpd, HTTPServer):
        httpd.server_close()
        print('User logged in. HTTP Server stopped at %s' % time.asctime())
    else:
        print('User logged in from cache...')


class HongBaoBot(object):
    table = 'hb'

    def __init__(self, msg, text):
        self.msg = msg
        self.text = str(text)
        try:
            self.con = sqlite3.connect('hb.sqlite')
            self.cur = self.con.cursor()
            self.cur.execute(
                'CREATE TABLE IF NOT EXISTS %s (url TEXT PRIMARY KEY, used INTEGER DEFAULT 0)'
                % self.table)
        except Exception as e:
            msg.reply('打开数据库时发生了异常：' + str(e))

    @staticmethod
    def is_hongbao(text):
        return (bool)(
            text.startswith('https://url.cn/') and
            len(text) == 22) or text.startswith('https://h5.ele.me/hongbao/')

    def save_hongbao_to_db(self):
        msg = self.msg
        con = self.con
        cur = self.cur
        table = self.table
        text = self.text

        msg.reply('收到红包链接，处理中...')
        try:
            cur.execute('insert into %s values("%s", 0)' % (table, text))
            msg.reply('添加成功！')
            con.commit()

        except Exception as e:
            stre = str(e)
            if 'Duplicate' or 'UNIQUE' in stre:
                msg.reply('添加失败！这个红包已经有了！异常：' + stre)
            else:
                msg.reply('添加失败！异常：' + stre)
            con.rollback()

    def dian_yi_shou(self):
        msg = self.msg
        con = self.con
        cur = self.cur
        table = self.table

        msg.reply('查询中...')
        cur.execute('SELECT url FROM %s WHERE used=0' % table)
        data = cur.fetchone()

        if data == None:
            msg.reply('红包已经耗尽了！')
        else:
            url = data[0]

            url_login = 'https://mtdhb.org/login'
            headers = \
                {'Host': 'api.mtdhb.org',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en-US;q=0.7,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'text-Type': 'application/x-www-form-urlencoded',
                'DNT': '1',
                'Connection': 'keep-alive'}
            browser = HTMLSession()
            browser.get(url_login, headers=headers)

            data_login = {'account': MTDHB_ACCOUNT, 'password': MTDHB_PASSWORD}
            url_login_api = 'https://api.mtdhb.org/user/login'
            r = browser.post(url_login_api, data=data_login)
            if r.json()['code'] == 0:
                msg.reply('登录成功...')

                url_receive_api = 'https://api.mtdhb.org/user/receiving'
                data_receive = {'phone': '', 'url': url, 'force': 0}
                headers['X-User-Token'] = r.json()['data']['token']

                r = browser.post(
                    url_receive_api, data=data_receive, headers=headers)
                if r.json()['code'] == 0:
                    sec = 5
                    msg.reply('垫一手请求已经提交，服务器正在处理...等待%d秒' % sec)
                    time.sleep(sec)

                    url_number_api = 'https://api.mtdhb.org/user/number'

                    r = browser.get(url_number_api, headers=headers)
                    if r.json()['code'] == 0:
                        avail = r.json()['data']['ele']['available']
                        total = r.json()['data']['ele']['total']
                        msg.reply('查询次数成功。\n剩余次数：%d\n总共次数：%d' % (avail, total))
                    else:
                        msg.reply('获取次数失败！JSON = %s' % r.json())

                    msg.reply('最佳手气红包链接如下，可以直接领取：\n' + url)
                    print('dian_yi_shou(): %s used!' % url)

                    try:
                        cur.execute('UPDATE %s SET used=1 WHERE url = "%s"' %
                                    (table, url))
                        con.commit()
                    except Exception as e:
                        msg.reply('更新标记失败！\n' + str(e))
                        con.rollback()

                    try:
                        cur.execute(
                            'SELECT count(*) FROM %s WHERE used=0' % table)
                        msg.reply('未使用红包：%d个' % cur.fetchone()[0])
                    except Exception as e:
                        msg.reply('查询未使用红包失败！\n' + str(e))
                        con.rollback()

                else:
                    msg.reply('垫一手失败！JSON = %s' % r.json())
            else:
                msg.reply('登录失败！JSON = %s' % r.json())

    def mark_used_and_reply(self):
        msg = self.msg
        con = self.con
        cur = self.cur
        table = self.table

        msg.reply('查询中...')
        cur.execute('SELECT url FROM %s WHERE used=0' % table)
        data = cur.fetchone()

        if data == None:
            msg.reply('红包已经耗尽了！')
        else:
            url = data[0]
            msg.reply('红包链接如下：')
            msg.reply(url)

            try:
                cur.execute(
                    'UPDATE %s SET used=1 WHERE url = "%s"' % (table, url))
                con.commit()

                cur.execute('SELECT count(*) FROM %s WHERE used=0' % table)
                msg.reply('未使用红包：%d个' % cur.fetchone()[0])

            except Exception as e:
                msg.reply('更新标记失败！\n' + str(e))
                con.rollback()

    def get_hongbao_count(self):
        msg = self.msg
        con = self.con
        cur = self.cur
        table = self.table

        try:
            cur.execute('SELECT count(*) FROM %s WHERE used=0' % table)
            msg.reply('未使用红包：%d个' % cur.fetchone()[0])
            # cur.fetchone() => Row
            # cur.fetchone()[0] => Row[Col=0]

            cur.execute('SELECT count(*) FROM %s' % table)
            msg.reply('总红包数量：%d个' % cur.fetchone()[0])

        except Exception as e:
            msg.reply('查询失败！异常：' + str(e))

    def mark_used(self):
        msg = self.msg
        con = self.con
        cur = self.cur
        table = self.table
        text = self.text

        url = text.split(' ')[1]
        if self.is_hongbao(url):
            try:
                cur.execute(
                    'UPDATE %s SET used=1 WHERE url="%s"' % (table, url))
                con.commit()
                msg.reply('成功标记 %s 为【已使用】' % url)
            except Exception as e:
                con.rollback()
                msg.reply('标记异常：' + str(e))
        else:
            msg.reply('链接不正确！')

    def mark_unused(self):
        msg = self.msg
        con = self.con
        cur = self.cur
        table = self.table
        text = self.text

        url = text.split(' ')[1]
        if self.is_hongbao(url):
            try:
                cur.execute(
                    'UPDATE %s SET used=0 WHERE url="%s"' % (table, url))
                con.commit()
                msg.reply('成功标记 %s 为【未使用】' % url)
            except Exception as e:
                con.rollback()
                msg.reply('标记异常：' + str(e))
        else:
            msg.reply('链接不正确！')

    def close_db(self):
        self.cur.close()
        self.con.close()


def run_hongbao_bot(msg):
    text = ''
    if msg.type == SHARING:
        text = msg.url
        msg.reply('收到一个分享链接...')
        msg.reply(text)
    elif msg.type == TEXT:
        text = msg.text

    if HongBaoBot.is_hongbao(text) or text.startswith('.'):
        hbbot = HongBaoBot(msg, text)

        if HongBaoBot.is_hongbao(text):
            hbbot.save_hongbao_to_db()

        elif text == '.1':
            hbbot.dian_yi_shou()

        elif text == '.11':
            hbbot.mark_used_and_reply()

        elif text == '.2':
            hbbot.get_hongbao_count()

        elif text.startswith('.u1 '):
            hbbot.mark_used()

        elif text.startswith('.u0 '):
            hbbot.mark_unused()

        else:
            msg.reply('转发【链接】添加红包\n' + '输入【.1】获取红包并垫一手\n' +
                      '输入【.11】获取红包但不垫\n' + '输入【.2】查询剩余个数\n' +
                      '输入【.u1 链接】将链接标记为已使用\n' + '输入【.u0 链接】将链接标记为未使用\n')

        hbbot.close_db()
        del hbbot


if __name__ == '__main__':
    bot = Bot(
        cache_path=True,
        console_qr=False,
        qr_path='wx-qrcode.png',
        qr_callback=on_qrcode_downloaded,
        login_callback=on_user_logined)

    print('Loading hongbao bot...')
    driver_group = bot.groups().search('542外卖车队')[0]
    my_group = bot.groups().search('自己的群')[0]
    # chats 可以是Group的list，也可以是单个Group，留空会监听所有群
    # msg_types 是str的常量，留空会监听所有msg类型
    @bot.register(
        chats=[driver_group, my_group], msg_types='', except_self=False)
    def hongbao_bot(msg):
        run_hongbao_bot(msg)

    # embed(banner='wxpy is running!')
    print('wxpy is running!')
    bot.join()