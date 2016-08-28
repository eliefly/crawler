import urllib.request
import http.cookiejar

def saveFile(data):
	with open('E:/Local_Code/crawler/temp.out', mode='wb') as f:
		f.write(data)


def makeMyOpener(head ={
    'Connection': 'Keep-Alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
}):
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

oper = makeMyOpener()
uop = oper.open('http://www.baidu.com/', timeout=1000)
data = uop.read()
print(data.decode())

saveFile(data)


# import urllib.request
# opener = urllib.request.build_opener()
# opener.addheaders = [('User-agent', 'Mozilla/5.0')]
# opener.open('http://www.example.com/')



# GET / HTTP/1.1
# Accept-Encoding: identity
# Accept: text/html, application/xhtml+xml, */*
# Connection: close
# Host: www.baidu.com
# User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko
# Accept-Language: en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3
