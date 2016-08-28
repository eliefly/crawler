# import login_douban
from login_douban import DouBanClient
from bs4 import BeautifulSoup
from collections import deque
import json
from datetime import datetime

'''
运用 login_douban.py 的登录豆瓣得到的 sessioin 访问豆瓣其他 url.

爬取豆瓣中标记看过的电影，记录片名及类型。
保存数据格式如下：
    卢旺达饭店                剧情 历史 战争
    碧海蓝天                  剧情 爱情
    爆裂鼓手                  剧情 音乐
    雨中曲                    喜剧 爱情 歌舞
    大鱼                      剧情 家庭 奇幻 冒险
    辩护人                    剧情
    黑客帝国3：矩阵革命       动作 科幻
'''


def getAllPage(fist_page):
    '''
    从我看的电影第1页开始获取所有页的url，返回一个deque
    '''
    page_deque = deque()
    next_page_url = fist_page
    while next_page_url:
        page_deque.append(next_page_url)
        req = session.get(next_page_url, verify=False)
        soup = BeautifulSoup(req.text, 'lxml')
        result = soup.find(rel="next")  # 下一页的url在 rel="next" 处
        if result:
            next_page_url = result['href']
        else:
            next_page_url = ''
    return page_deque    


def getMovieInPage(first_page):
    '''
    获取每一页中的电影
    '''
    req = session.get(first_page, verify=False)
    client.saveHtmlPage(req, 'movie_seen.html')

    soup = BeautifulSoup(req.text, 'lxml')
    result = soup.find_all('a', {'class': 'nbg'}) # 单个电影的url在 class="nbg" 处
    page_deque = deque()
    for movie in result:
        page_deque.append(movie['href'])
    return page_deque


def getMovieInfo(movie_url):
    '''
    获取影片信息
    '''
    print('影片链接：', movie_url)
    req = session.get(movie_url, verify=False)
    if req.status_code != 200:
        url_error = movie_url + ':影片链接失效----'
        return url_error
    soup = BeautifulSoup(req.text, 'lxml')
    result = soup.find('meta', {'name': 'keywords'})['content']
    movie_name = result.split(',')[0]

    # 获取电影类型
    result = soup.find_all(property="v:genre")
    type_list = list()
    for type_blank in result:
        type_list.append(type_blank.get_text()) 

    m_dict = dict()
    m_dict[movie_name] = type_list
    # print(m_dict)

    # 保存数据
    # with open('movie_mine_seen.json', 'a') as f:
    #     json.dump(m_dict, f)

    return m_dict


def saveMovieInfo(movie_info):
    '''
    保存获取的影片信息
    '''
    # m_dict = {'碧海蓝天': ['剧情', '爱情']}
    # m_str = '碧海蓝天 剧情 爱情'
    if isinstance(movie_info, dict):
        m_dict = movie_info
        # 将dict数据转为字符串数据
        name = str(list(m_dict.keys())[0])
        # m_str = '{0:10}'.format(name) # 同m_str = '%-10s' % (name)，但中文对齐有问题

        [num1, num2] = calDoubleNum(name)
        m_str = name + ' '*(25-2*num1 - num2) # 在片名增加特定的空格数，以对其中文

        for value in list(m_dict.values())[0]:
            m_str = m_str + ' ' + str(value)

        print('saving-----> ' + m_str + '-------')
        with open('movie_mine_seen.txt', 'a', encoding='utf-8') as f:
            f.write(m_str + '\n')
    else: # m_dict = '影片链接失效'
        url_error = movie_info
        # with open('movie_mine_seen.txt', 'a', encoding='utf-8') as f:
        #     f.write(url_error + '\n')


def calDoubleNum(str):
    '''
    计算字符串中文和非中文的个数
    '''
    num1, num2 = 0, 0
    for char in str:
        inside_code=ord(char)
        if inside_code < 0x0020 or inside_code > 0x7e: # 如果全角字符
            num1 = num1 + 1
        else:
            num2 = num2 + 1
    print(num1, num2)
    return [num1, num2]


if __name__ == '__main__':

    global session

    client = DouBanClient()
    # client = login_douban.DouBanClient()
    client.login()  
    session = client.getSession()
    # header = {
    #     'Host': 'movie.douban.com'
    # }
    header = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Host': 'movie.douban.com'
    }

    session.headers.update(header)
    url_movie ='https://movie.douban.com/mine' # 从我的电影主页开始
    req = session.get(url_movie, verify=False)
    client.saveHtmlPage(req, 'movie_mine.html')
    print(req.url)

    soup = BeautifulSoup(req.text, 'lxml')
    first_page = soup.find('a', target="_self")['href'] # 获取 我看过的电影第1页
    # print(first_page)

    page_deque = getAllPage(first_page) # 获取我看电影的所有页的url

    while page_deque:
        page = page_deque.popleft() # 取出一个电影页url
        movie_deque = getMovieInPage(page)  # 获取电影所有影片url
        while movie_deque:
            movie_url = movie_deque.popleft() # 取出单部影片的url
            movie_info = getMovieInfo(movie_url) # 有可能返回str:url_error = '影片链接失效'
            print(movie_info)
            saveMovieInfo(movie_info)  

    # 保存截至时间
    # time = datetime.now().strftime('%a, %Y %b %d %H:%M')
    # with open('movie_mine_seen.txt', 'a', encoding='utf-8') as f:
    #     f.write('update time:   ' + time + '\n')
