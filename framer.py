import Queue

initial_page = 'http://www.renminribo.com'

url_queue = Queue.Queue() # 未读的 url
seen = set() # 已经看过的 url 集合

see.insert(initial_page)
url_queue.put(initial_page)

while(True):
    if url_queue.size() > 0:    # 还有未爬的 url
        current_url = url_queue.pop()   # 从队列中取出一个 url
        store(current_url)  # 处理当前 url 页面
        for next_url in extract_urls(current_url): # 提取当前 url 页面链向的其他页面
            if next_url not in seen:
                seen.add(next_url) # ？？？也可以放在store处理后吧
                url_queue.push(next_url)