import urllib.request
import urllib

data = {}
data['word'] = 'eliefly'
url_values = urllib.parse.urlencode(data)
url = 'http://www.baidu.com/s?'
full_url = url + url_values
f = urllib.request.urlopen(full_url)
data = f.read()
data = data.decode('utf-8')
print(data)