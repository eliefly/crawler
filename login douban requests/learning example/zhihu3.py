作者：7sDream
链接：https://www.zhihu.com/question/29755376/answer/45496745
来源：知乎
著作权归作者所有，转载请联系作者获得授权。

_Zhihu_URL = 'http://www.zhihu.com'
_Login_URL = _Zhihu_URL + '/login'
_Captcha_URL_Prefix = _Zhihu_URL + '/captcha.gif?r='
_Cookies_File_Name = 'cookies.json'

_session = None
_header = {'X-Requested-With': 'XMLHttpRequest',
           'Referer': 'http://www.zhihu.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; '
                         'Trident/7.0; Touch; LCJB; rv:11.0)'
                         ' like Gecko',
           'Host': 'www.zhihu.com'}

def get_captcha_url():
    """获取验证码网址

    :return: 验证码网址
    :rtype: str
    """
    return _Captcha_URL_Prefix + str(int(time.time() * 1000))

def _save_captcha(url):
    global _session
    r = _session.get(url)
    with open('code.gif', 'wb') as f:
        f.write(r.content)

def login(email='', password='', captcha='', savecookies=True):
    """不使用cookies.json，手动登陆知乎

    :param str email: 邮箱
    :param str password: 密码
    :param str captcha: 验证码
    :param bool savecookies: 是否要储存cookies文件
    :return: 一个二元素元祖 , 第一个元素代表是否成功（0表示成功），
        如果未成功则第二个元素表示失败原因
    :rtype: (int, dict)
    """
    global _session
    global _header
    data = {'email': email, 'password': password,
            'rememberme': 'y', 'captcha': captcha}
    r = _session.post(_Login_URL, data=data)
    j = r.json()
    c = int(j['r'])
    m = j['msg']
    if c == 0 and savecookies is True:
        with open(_Cookies_File_Name, 'w') as f:
            json.dump(_session.cookies.get_dict(), f)
    return c, m

def create_cookies():
    """创建cookies文件, 请跟随提示操作

    :return: None
    :rtype: None
    """
    if os.path.isfile(_Cookies_File_Name) is False:
        email = input('email: ')
        password = input('password: ')
        url = get_captcha_url()
        _save_captcha(url)
        print('please check code.gif for captcha')
        captcha = input('captcha: ')
        code, msg = login(email, password, captcha)

        if code == 0:
            print('cookies file created!')
        else:
            print(msg)
        os.remove('code.gif')
    else:
        print('Please delete [' + _Cookies_File_Name + '] first.')

def _init():
    global _session
    if _session is None:
        _session = requests.session()
        _session.headers.update(_header)
        if os.path.isfile(_Cookies_File_Name):
            with open(_Cookies_File_Name, 'r') as f:
                cookies_dict = json.load(f)
                _session.cookies.update(cookies_dict)
        else:
            print('no cookies file, this may make something wrong.')
            print('if you will run create_cookies or login next, '
                  'please ignore me.')
            _session.post(_Login_URL, data={})
    else:
        raise Exception('call init func two times')

_init()