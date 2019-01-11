# encoding=utf-8

import sqlite3
from requests_html import HTMLSession
import time

ACCOUNT = ''
PASSWORD = ''
DB_NAME = ''


def onQQMessage(bot, contact, member, content):

    if not bot.isMe(contact, member):

        if content == '.help' or '[@ME]' in content:
            bot.SendTo(
                contact, '转发【链接】添加红包\n' + '输入【.1】获取红包并垫一手\n' +
                '输入【.11】获取红包但不垫\n' + '输入【.2】查询剩余个数\n' + '输入【.u1 链接】将链接标记为已使用\n'
                + '输入【.u0 链接】将链接标记为未使用\n')

        elif content == '.stop':
            bot.SendTo(contact, '红包机器人好像关闭不了')
            # bot.Stop()

        else:
            con = sqlite3.connect(DB_NAME)  # 目录是qqbot的启动目录
            cur = con.cursor()
            table = 'hb'
            # SQLite does not have a separate Boolean storage class.
            # Instead, Boolean values are stored as integers 0 (false) and 1 (true).
            cur.execute(
                'CREATE TABLE IF NOT EXISTS %s (url TEXT PRIMARY KEY, used INTEGER DEFAULT 0)'
                % table)

            # if content == '.clrdb':
            #     try:
            #         cur.execute('DELETE FROM %s' % table)
            #         bot.SendTo(contact, '清库成功！')
            #     except Exception as e:
            #         bot.SendTo(contact, '清库失败！异常：' + str(e))

            if content.startswith('https://url.cn/') and len(content) == 22:
                bot.SendTo(contact, content)
                bot.SendTo(contact, '收到红包链接，处理中...')

                try:
                    cur.execute(
                        'insert into %s values("%s", 0)' % (table, content))
                    bot.SendTo(contact, '添加成功！')
                    con.commit()

                except Exception as e:
                    if 'Duplicate' or 'UNIQUE' in str(e):
                        bot.SendTo(contact, '添加失败！这个红包已经有了！')
                    else:
                        bot.SendTo(contact, '添加失败！异常：' + str(e))
                    con.rollback()

            elif content == '.1':
                bot.SendTo(contact, '查询中...')
                cur.execute('SELECT url FROM %s WHERE used=0' % table)
                data = cur.fetchone()

                if data == None:
                    bot.SendTo(contact, '红包已经耗尽了！')
                else:
                    url = data[0]

                    url_login = 'https://mtdhb.org/login'
                    headers = \
                        {'Host': 'api.mtdhb.org',
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
                         'Accept': 'application/json, text/plain, */*',
                         'Accept-Language': 'en-US,en-US;q=0.7,en;q=0.3',
                         'Accept-Encoding': 'gzip, deflate, br',
                         'Content-Type': 'application/x-www-form-urlencoded',
                         'DNT': '1',
                         'Connection': 'keep-alive'}
                    browser = HTMLSession()
                    browser.get(url_login, headers=headers)

                    data_login = {'account': ACCOUNT, 'password': PASSWORD}
                    url_login_api = 'https://api.mtdhb.org/user/login'
                    r = browser.post(url_login_api, data=data_login)
                    if r.json()['code'] == 0:
                        bot.SendTo(contact, '登录成功...')

                        url_receive_api = 'https://api.mtdhb.org/user/receiving'
                        data_receive = {'phone': '', 'url': url, 'force': 0}

                        headers['X-User-Token'] = r.json()['data']['token']

                        r = browser.post(
                            url_receive_api,
                            data=data_receive,
                            headers=headers)
                        if r.json()['code'] == 0:
                            sec = 3
                            bot.SendTo(contact, '正在垫一手...等待%d秒' % sec)
                            url_number_api = 'https://api.mtdhb.org/user/number'
                            time.sleep(sec)

                            r = browser.get(url_number_api, headers=headers)
                            if r.json()['code'] == 0:
                                bot.SendTo(
                                    contact, '剩余次数：%d' %
                                    r.json()['data']['ele']['available'])
                                bot.SendTo(
                                    contact, '总共次数：%d' %
                                    r.json()['data']['ele']['total'])
                            else:
                                bot.SendTo(contact,
                                           '获取次数失败！JSON = %s' % r.json())

                            bot.SendTo(contact, '最佳手气红包链接如下，可以直接领取：')
                            bot.SendTo(contact, url)

                            try:
                                cur.execute(
                                    'UPDATE %s SET used=1 WHERE url = "%s"' %
                                    (table, url))
                                con.commit()

                                cur.execute(
                                    'SELECT count(*) FROM %s WHERE used=0' %
                                    table)
                                bot.SendTo(contact,
                                           '未使用红包：%d个' % cur.fetchone()[0])

                            except Exception as e:
                                bot.SendTo(contact, '更新标记失败！\n' + str(e))
                                con.rollback()

                        else:
                            bot.SendTo(contact, '垫一手失败！JSON = %s' % r.json())
                    else:
                        bot.SendTo(contact, '登录失败！JSON = %s' % r.json())

            elif content == '.11':
                bot.SendTo(contact, '查询中...')
                cur.execute('SELECT url FROM %s WHERE used=0' % table)
                data = cur.fetchone()

                if data == None:
                    bot.SendTo(contact, '红包已经耗尽了！')
                else:
                    url = data[0]
                    bot.SendTo(contact, '红包链接如下：')
                    bot.SendTo(contact, url)

                    try:
                        cur.execute('UPDATE %s SET used=1 WHERE url = "%s"' %
                                    (table, url))
                        con.commit()

                        cur.execute(
                            'SELECT count(*) FROM %s WHERE used=0' % table)
                        bot.SendTo(contact, '未使用红包：%d个' % cur.fetchone()[0])

                    except Exception as e:
                        bot.SendTo(contact, '更新标记失败！\n' + str(e))
                        con.rollback()

            elif content == '.2':
                try:
                    cur.execute('SELECT count(*) FROM %s WHERE used=0' % table)
                    bot.SendTo(contact, '未使用红包：%d个' % cur.fetchone()[0])
                    # cur.fetchone() => Row
                    # cur.fetchone()[0] => Row[Col=0]

                    cur.execute('SELECT count(*) FROM %s' % table)
                    bot.SendTo(contact, '总红包数量：%d个' % cur.fetchone()[0])

                except Exception as e:
                    bot.SendTo(contact, '查询失败！异常：' + str(e))

            elif content.startswith('.u1 '):
                url = content.split(' ')[1]
                if url.startswith('https://url.cn/') and len(url) == 22:
                    try:
                        cur.execute('UPDATE %s SET used=1 WHERE url="%s"' %
                                    (table, url))
                        con.commit()
                        bot.SendTo(contact, '标记成功')
                    except Exception as e:
                        con.rollback()
                        bot.SendTo(contact, '标记异常：' + str(e))
                else:
                    bot.SendTo(contact, '链接不正确！')

            elif content.startswith('.u0 '):
                url = content.split(' ')[1]
                if url.startswith('https://url.cn/') and len(url) == 22:
                    try:
                        cur.execute('UPDATE %s SET used=0 WHERE url="%s"' %
                                    (table, url))
                        con.commit()
                        bot.SendTo(contact, '标记成功')
                    except Exception as e:
                        con.rollback()
                        bot.SendTo(contact, '标记异常：' + str(e))
                else:
                    bot.SendTo(contact, '链接不正确！')

            elif content.startswith('.'):
                bot.SendTo(contact, '未知指令，输入【.help】获取帮助')

            cur.close()
            con.close()
