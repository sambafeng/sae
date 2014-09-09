# -*- coding:utf-8 -*-
__author__ = 'I308972'
__date__ = '8/4/14 11:53 AM'
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#weatherInferface
def getPostId(content):
    postId=''
    with open('./properties/chineseCity.txt','r') as f:
        for line in f.readlines():
            lr=line.strip().split('=')[1].decode('utf-8')
            ll=line.strip().split('=')[0].decode('utf-8')
            if lr == (unicode(content)):
                postId=ll
                break
    return postId