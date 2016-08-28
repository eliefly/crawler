# -*- coding:utf-8 -*- 

import urllib.request
import http.cookiejar
import gzip
import re
import time

import PIL.Image


url_douban = 'https://www.douban.com'
url_login = url_douban + '/accounts/login'
url_cpatcha_prefix = url_douban + '/misc/captcha?id='


head = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Host': 'www.douban.com'
}

def ungzip(data):
    try:        # 尝试解压
        print('正在解压.....')
        data = gzip.decompress(data)
        print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data


def get_captcha_id(data):
	cer = re.compile(r'name="captcha-id" value="(.*)"', flags=0)
	strlist = cer.findall(data)
	return strlist[0]


def savefile(data):
	with open('login_douban.html', mode='wb') as f:
		f.write(data)



def makeMyOpener(head):
    cj = http.cookiejar.CookieJar() # 定义一个 CookieJar 实例，存储http cookies
    handle = urllib.request.HTTPCookieProcessor(cj) # 处理 http cookies 的handle
    # 返回一个 OpenerDirector实例，以给定的顺序链接handlers 。OpenerDirector类通过把BaseHandlers链接在一起打开URLs
    opener = urllib.request.build_opener(handle)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header # OpenerDirector 实例增加请求头部(header)
    return opener

opener = makeMyOpener(head)

response = opener.open(url_douban)
data = response.read()
data = ungzip(data)
captcha_id = get_captcha_id(data.decode())
print(captcha_id)

url_captcha = url_cpatcha_prefix + captcha_id
print(url_captcha)
# 获取验证码
cap_content = urllib.request.urlopen(url_captcha).read()
with open('captcha.gif', 'wb') as cap_file:
    cap_file.write(cap_content)


im = PIL.Image.open('captcha.gif')
im.show()
im.close()
captcha = input('captcha:')


id = input('id:')
password = input('password:')

dict_post = {
	'source': 'index_nav',
	'captcha-id': captcha_id,
	'captcha-solution': captcha,
	'form_email': id,
	'form_password': password,
}

postdata = urllib.parse.urlencode(dict_post)
postdata = postdata.encode() # POST data should be bytes or an iterable of bytes. It cannot be of type str.
response = opener.open(url_login, postdata)
data = response.read()
data = ungzip(data)
# print(data.decode())
savefile(data)



