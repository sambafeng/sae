# -*- coding: utf-8 -*-
import hashlib
import web
#import lxml
import time
import os
import urllib2,json
#from lxml import etree
import xml.etree.ElementTree as ET

class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
    
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
        return self.render.reply_text(fromUser,toUser,int(time.time()),u"(刚上线的APP，很多功能还没有，现在只能鹦鹉学舌)你刚才说的是:"+content)        