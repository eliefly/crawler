# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import pickle




url_douban = 'https://www.douban.com'
url_login = url_douban + '/accounts/login'
url_cpatcha_prefix = url_douban + '/misc/captcha?id='

# 构造 Request headers
header = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Host': 'www.douban.com'
}

session_douban = requests.Session()
session_douban.headers.update(header)

# 豆瓣首页
rep = session_douban.get(url_douban, verify=True)

# with open('cookie1.pickle', 'wb') as f:
#     pickle.dump(session_douban.cookies, f)

# with open('cookie1.pickle', 'rb') as f:
#     cookie1 = pickle.load(f)

# print(cookie1)

print(session_douban.cookies)

# with open('douban.html', 'wb') as f:
#     f.write(rep.content)

# 获取
soup = BeautifulSoup(rep.text, 'lxml')
cap = soup.find('input', {'name': 'captcha-id'})
if cap != None: # 如果需要验证码
    captcha_id = cap['value']

    # 验证码图像 url
    url_captcha = url_cpatcha_prefix + captcha_id
    print(url_captcha)

    # 输入用户名，密码，验证码
    user_id = input('user_id:')
    user_password = input('user_password:')

    # 获取并打开图像
    r = requests.get(url_captcha)
    im = Image.open(io.BytesIO(bytearray(r.content)))
    im.show()
    captcha = input('captcha:')

    post_data = {
        'source': 'index_nav',
        'captcha-id': captcha_id,
        'captcha-solution': captcha,
        'form_email': user_id,
        'form_password': user_password,
    }
else: # 如果不需要验证码
    # 输入用户名，密码，验证码
    user_id = input('user_id:')
    user_password = input('user_password:')
    post_data = {
        'source': 'index_nav',
        'form_email': user_id,
        'form_password': user_password,
    }


# 豆瓣登录叶
rep = session_douban.post(url_login, post_data)
if rep.status_code == 200:
    print('登录成功!')

# 保存cookies
# with open('cookie2.pickle', 'wb') as f:
#     pickle.dump(session_douban.cookies, f)

# with open('cookie2.pickle', 'rb') as f:
#     cookie2 = pickle.load(f)

# print(cookie2)


# 保存登录成功页，验证登录是否成功
# with open('douban_login_page.html', 'wb') as f:
#     f.write(rep.content)

# 使用cookies再打开豆瓣首页
session_douban.cookies.update(session_douban.cookies)
rep = session_douban.get(url_douban)
with open('douban_home_page.html', 'wb') as f:
    f.write(rep.content)












