import re
import urllib.request
import urllib
from collections import deque

# from urllib.request import Request, urlopen

import ssl


url_queue = deque()
url_visited = set()

initial_url = 'http://news.dbanotes.net'    # 初始 url
cnt = 0

# url_visited.add(initial_url)
url_queue.append(initial_url)

# while len(url_queue) > 0:
while url_queue:
    current_url = url_queue.popleft() # 弹出一个 url 进行处理
    print('已经抓取: ' + str(cnt) + '   正在抓取 <---  ' + current_url)
    # url_visited.add(current_url) # 标记已访问的 url
    url_visited |= {current_url} # 标记已访问的 url
    cnt += 1

    context = ssl._create_unverified_context()

    # httpresponse = urllib.request.urlopen(current_url) # 直接打开url
    req = urllib.request.Request(current_url, headers={'User-Agent': 'Mozilla/5.0'}) # 构造reques对像
    try:
        httpresponse = urllib.request.urlopen(req, context=context, timeout=2)
    except:
        continue
    # 浏览器就是依靠 Content-Type 来判断响应的内容是网页还是图片，是视频还是音乐
    if 'html' not in httpresponse.getheader('Content-Type'):
        continue

    try:
        webpage = httpresponse.read().decode('utf-8')
    except:
        continue

    # 正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列  
    linkre = re.compile(r'href="(.+?)"')
    for x in linkre.findall(webpage):
        if 'http' in x and x not in url_visited:
            url_queue.append(x)
            print('新的 url 加入队列-->' + x)

