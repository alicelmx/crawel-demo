import urllib2
import re
import time

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Hosts': 'hm.baidu.com',
    'Referer': 'http://www.xicidaili.com/nn',
    'Connection': 'keep-alive'
}


url = 'http://www.xicidaili.com/nn/' + '1'
req = urllib2.Request(url=url, headers=headers)
res = urllib2.urlopen(req).read()

ip_list = re.findall(
    "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{2,6})", res, re.S)

f = open("ip.txt", "a+")
for li in ip_list:
    ip = li[0] + ':' + li[1] + '\n'
    print ip
    f.write(ip)

time.sleep(2)

import urllib
import socket
socket.setdefaulttimeout(3)

inf = open("ip.txt")
lines = inf.readlines()
proxys = []
for i in range(0, len(lines)):
    proxy_host = "http://" + lines[i]
    proxy_temp = {"http": proxy_host}
    proxys.append(proxy_temp)

url = "http://ip.chinaz.com/getip.aspx"
ouf = open("valid_ip.txt", "a+")

for proxy in proxys:
    try:
        res = urllib.urlopen(url, proxies=proxy).read()
        valid_ip = proxy['http'][7:]
        print 'valid_ip: ' + valid_ip
        ouf.write(valid_ip)
    except Exception, e:
        print proxy
        print e
        continue
