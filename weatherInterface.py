# -*- coding: utf-8 -*-
import hashlib
import web
#import lxml
import time
import os,sys
import urllib2,json
#from lxml import etree
import xml.etree.ElementTree as ET
from util.tools import getPostId

class WeatherInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
        #self.properties_root = os.path.join(self.app_root, 'properties')
    
    def GET(self):
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        token="sambafeng"
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        if hashcode == signature:
            return echostr

    def POST(self):
        str_xml = web.data()
        #xml = etree.fromstring(str_xml)
        xml = ET.fromstring(str_xml)
        content=xml.find("Content").text
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text

        # with open('properties/chineseCity.txt','r') as f:
        #     for line in f.readlines():
        #         lr=line.strip().split('=')[1].decode('utf-8')
        #         ll=line.strip().split('=')[0].decode('utf-8')
        #         if lr!=(unicode(content)):
        #             postId=''
        #         else:
        #             postId=ll
        #             break
        postId=getPostId(content)
        if postId!='':
            weatherHtml = urllib2.urlopen('http://www.weather.com.cn/data/cityinfo/' + postId + '.html').read()
            weatherJSON = json.JSONDecoder().decode(weatherHtml)
            weatherInfo = weatherJSON['weatherinfo']
            city = weatherInfo['city']
            h_temp=weatherInfo['temp1']
            l_temp=weatherInfo['temp2']
            weather=weatherInfo['weather']
            detail=h_temp+'~'+l_temp+'\n'+weather
            return self.render.reply_text(fromUser,toUser,int(time.time()),u"今天"+city+u"天气情况如下:\n"+detail)
        else:
            return self.render.reply_text(fromUser,toUser,int(time.time()),u"中国没有"+unicode(content)+u"这个城市的天气")