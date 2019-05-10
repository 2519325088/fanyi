from django.shortcuts import render,redirect,reverse
from django.http import HttpResponseRedirect,HttpResponse
from urllib import request
import urllib
import re

# Create your views here.


def index(requset):
    try:
        if requset.method=="POST":
            key = requset.POST['keya']
            head = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                              'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                              'Chrome/74.0.3729.131 Safari/537.36'
            }
            url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rul'
            formdate = {
                'i': key,
                'from': 'AUTO',
                'to': 'AUTO',
                'smartresult': 'dict',
                'client': 'fanyideskweb',
                'salt': '15573878832616',
                'sign': '5b2b7e8734c62ea56aafcae7a3c2a5fc',
                'ts': '1557387883261',
                'bv': '316dd52438d41a1d675c1d848edf4877',
                'doctype': 'json',
                'version': '2.1',
                'keyfrom': 'fanyi.web',
                'action': 'FY_BY_REALTlME'
            }

            date = urllib.parse.urlencode(formdate).encode(encoding='utf-8')

            # 有 date 就是post请求
            # 没有就是get请求
            req = request.Request(url, data=date, headers=head)

            resp = request.urlopen(req).read().decode()

            # 正则表达式，提取 "tgt":" 和 "} 中间的任意内容
            pat = r'"tgt":"(.*?)"}'

            result = re.findall(pat, resp)[0]
            print(result)
            return render(requset,'fanyi/fanyi.html',{'result': result})
        elif requset.method=="GET":
            return render(requset,'fanyi/fanyi.html')
    except:
        return render(requset, 'fanyi/fanyi.html')