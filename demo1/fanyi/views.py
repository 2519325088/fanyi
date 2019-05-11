from django.shortcuts import render,redirect,reverse
from django.http import HttpResponseRedirect,HttpResponse
from urllib import request
import requests
import urllib
import re
import time

# Create your views here.

def index(request):
    return render(request, 'fanyi/index.html')


def fanyia(request):
    try:
        if request.method=="POST":
            key = request.POST['keya']
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
            return render(request,'fanyi/fanyi.html',{'result': result})
        elif request.method=="GET":
            return render(request,'fanyi/fanyi.html')
    except:
        return render(request, 'fanyi/fanyi.html')

def xiazai(request):
    songID = []
    songName = []
    for i in range(2):
        url = 'http://www.htqyy.com/top/musicList/hot?pageIndex=' + str(i) + '&pageSize=20'
        # print(url)
        # 获取音乐榜单的网页信息
        html = requests.get(url)
        strr = html.text
        # < span class ="title" > < a href="/play/108" target="play" title="牧羊曲" sid="108" > 牧羊曲 < / a > < / span >
        pat = r'title="(.*?)" sid' #匹配名字
        pat1 = r'sid="(.*?)"'  #匹配id
        idlist = re.findall(pat1, strr)
        titlelist = re.findall(pat, strr)
        songID.extend(idlist)
        songName.extend(titlelist)
    les=len(songName)
    les1=[]
    for i in range(les):
        les1.append(i)
    if request.method == "POST":
        gname= request.POST['sid']
        print(gname,'==========================')
        sid=songName.index(gname)
        print(sid,'=============================================')
        songurl = 'http://f2.htqyy.com/play7/' + str(sid) + '/mp3/5'
        songname = songName[sid]

        data = requests.get(songurl).content
        print('正在下载第', songname)

        with open('F:\\muc\\{}mp3'.format(songname), 'wb') as f:
            f.write(data)
        time.sleep(5)
        return render(request, 'fanyi/xiazai.html', {'songname': songName, 'songid': songID, 'les1': les})
    elif request.method == "GET":

        print(songName)
        print(songID)
        return render(request, 'fanyi/xiazai.html',{'songname':songName,'songid':songID,'les1':les})
    # for i in range(len(songID)):
    #     songurl = 'http://f2.htqyy.com/play7/' + str(i) + '/mp3/5'
    #     songname = songName[i]
    #
    #     data = requests.get(songurl).content
    #     print('正在下载第', i, '首----', songname)
    #
    #     with open('F:\\muc\\{}mp3'.format(songname), 'wb') as f:
    #         f.write(data)
    #     time.sleep(5)
