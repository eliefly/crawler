# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import pickle
import os
import json


class DouBanClient():

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

    def __init__(self):
        self.__session = requests.session()
        self.__session.headers.update(self.header)
        self.cookiename = 'cookie.json'
        self.__cookie = self.__loadCookie()


    def __saveCookie(self):
        # with open(self.cookiename, 'wb') as f:
            # pickle.dump(self.__session.cookies, f)
        with open(self.cookiename, 'w') as f:
            json.dump(self.__session.cookies.get_dict(), f, indent=2)


    def __loadCookie(self):
        if os.path.isfile(self.cookiename):
            # with open(self.cookiename, 'rb') as f:
            #     cookie = pickle.load(f)
            with open(self.cookiename, 'r') as f:
                cookie = json.load(f)            
            return cookie
        return None 


    def getCaptchaId(self):
        '''
        获取验证码
        '''
        html = self.__session.get(self.url_douban).text
        soup = BeautifulSoup(html, 'lxml')
        cap = soup.find('input', {'name': 'captcha-id'})
        if cap is None:
            return None
        else:
            return cap['value']


    def saveHtmlPage(self, response, pagename):
        with open(pagename, 'wb') as f:
            f.write(response.content)


    def manualLogin(self, postdata):
        '''
        手动输入登录
        '''
        rep = self.__session.post(self.url_login, postdata)
        print(self.__session.cookies)
        self.__saveCookie()
        self.saveHtmlPage(rep, 'douban_manual_login_page.html')
        accout = self.isLoginOk(rep)
        if accout is None:
            print('登录失败!')
        else:
            print(accout.getText() + '登录成功!!!')

    def isLoginOk(self, response):
        '''
        判断是否登录成功
        '''
        soup = BeautifulSoup(response.text, 'lxml')
        accout = soup.find('a', {'href': 'https://www.douban.com/accounts/', 'class':'bn-more'})
        return accout

    def getSession(self):
        return self.__session


    def login(self):
        if self.__cookie:
            print('检测到cookie文件，使用cookie登录')
            print(self.__cookie)
            self.__session.cookies.update(self.__cookie)
            rep = self.__session.get(self.url_douban) # cookie登录直接使用首页
            self.saveHtmlPage(rep, 'douban_cookie_login_page.html')
            accout = self.isLoginOk(rep)    # 判断登录是否成功
            if accout is None:
                print('登录失败，删除当前cookie')
                os.remove(self.cookiename)
            else:
                print(accout.getText() + '登录成功!!!')
        else:
            print('没有检测到cookie文件，手动登录...')
            captcha_id = self.getCaptchaId()

            if captcha_id is None:
                print('无需验证码登录...')
                user_id = input('user_id:')
                user_password = input('user_password:')
                post_data = {
                    'source': 'index_nav',
                    'form_email': user_id,
                    'form_password': user_password,
                }
                self.manualLogin(post_data)
            else:
                print('验证码登录...')
                url_captcha = self.url_cpatcha_prefix + captcha_id
                # print(url_captcha)

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
                self.manualLogin(post_data)   

if __name__ == '__main__':
    client = DouBanClient()
    client.login()  
    # 返回会话session，可用这个session进行其他网络操作，详见requests库
    session = client.getSession()                            


