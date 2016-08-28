# -*- coding:utf-8 -*- 

import urllib.request
import http.cookiejar
import gzip
import re
import urllib.parse

import time
import PIL.Image


url_zhihu = 'http://www.zhihu.com'
url_login = url_zhihu + '/login/email'

url_captcha_prefix = url_zhihu + '/captcha.gif?r='
url_captcha = url_captcha_prefix + str(int(time.time() * 1000))

print(url_captcha)



def ungzip(data):
    try:        # 尝试解压
        print('正在解压.....')
        data = gzip.decompress(data)
        print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data


def getXSRF(data):
	cer = re.compile(r'name="_xsrf" value="(.*)"', flags=0)
	strlist = cer.findall(data)
	return strlist[0]

def savefile(data):
	with open('login_zhihu.html', mode='wb') as f:
		f.write(data)

# headers
head = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Host': 'www.zhihu.com'
}


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

oper = makeMyOpener(head)

op = oper.open(url_zhihu)
data = op.read()
data = ungzip(data)
# print(data.decode())

# 登录知乎

# 获取登录数据 xsrf
xsrf = getXSRF(data.decode())
print(xsrf)

# 获取验证码
cap_content = urllib.request.urlopen(url_captcha).read()
with open('captcha.gif', 'wb') as cap_file:
	cap_file.write(cap_content)

im = PIL.Image.open('captcha.gif')
im.show()
im.close()
captcha = input('capture:')


id = input('your id:')
password = input('your password:')

print(captcha)

dict_post = {
	'_xsrf': xsrf,
	'email': id,
	'password': password,
	'captcha': captcha,
	'remember_me': 'False'
}

postdata = urllib.parse.urlencode(dict_post).encode()
op = oper.open(url_login, postdata)
data = op.read()
data = ungzip(data)
print(data.decode())


op = oper.open(url_zhihu)
data = op.read()
data = ungzip(data)
print(data)
savefile(data)