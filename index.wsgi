# coding: UTF-8
import sys
import os
app_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(app_root, 'site-packages'))

import sae
import web
from sae.ext.shell import ShellMiddleware
from weixinInterface import WeixinInterface
from weatherInterface import WeatherInterface
from youdaoInterface import YoudaoInterface



urls = (
    '/', 'Hello',
    #'/weixin','WeixinInterface'
    #'/weixin','WeatherInterface'
    '/weixin','YoudaoInterface'  
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

class Hello:
	def GET(self):
		return render.hello("sae服务器正常")

    
app = web.application(urls, globals()).wsgifunc()

application = sae.create_wsgi_app(app)