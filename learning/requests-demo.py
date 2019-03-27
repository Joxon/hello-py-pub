from requests_html import HTMLSession

browser = HTMLSession()
data_login = {'account': '838415369@qq.com',
              'password': 'ilhb8384'}
url_login_api = 'https://api.mtdhb.org/user/login'
r = browser.post(url_login_api, data=data_login)
print(r.json()['code'])
