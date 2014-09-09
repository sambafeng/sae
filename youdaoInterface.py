# -*- coding: utf-8 -*-
import hashlib
import web
#import lxml
import time
import os,sys
import urllib2,json,urllib
#from lxml import etree
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

class YoudaoInterface:

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

        word=unicode(content)

        youdaoHtml = 'http://dict.youdao.com/search'
        youdaoData = {'le': 'eng', 'q': word, 'keyfrom': 'dict'}

        youdaoRequest = urllib2.Request(youdaoHtml, urllib.urlencode(youdaoData))
        youdaoRequest.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)')
        wordHtml = urllib2.urlopen(youdaoRequest)
        wordSoup = BeautifulSoup(wordHtml.read().decode('utf-8'))
        keyword = wordSoup.find('span', {'class', 'keyword'}).string
        
        words=[]
        for word in wordSoup.find_all('span', {'class', 'def'}):
            words.append(word.string)        
        
        cmean=unicode('\n'.join(words))
        
        if cmean=='':
            return self.render.reply_text(fromUser,toUser,int(time.time()),u"OOO~没有翻译")
        else:
        	return self.render.reply_text(fromUser,toUser,int(time.time()),u"翻译结果:\n"+cmean)