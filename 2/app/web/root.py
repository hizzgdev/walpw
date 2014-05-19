#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
from bottle import Bottle,view,static_file,redirect,request,response

from app.util import fetch_url
from app.web.diary import diary

static_path = 'static'

root = Bottle()
root.mount(diary,'/diary')

def get_background():
    #s = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
    #resp = fetch_url(s)
    #d = json.loads(resp[1])
    #bg_url=d['images'][0]['url']
    bg_url = 'http://s.cn.bing.net/az/hprichbg/rb/HerzliyaIsrael_ZH-CN12724786713_1366x768.jpg'
    return bg_url

@root.get('/')
@view('index')
def root_index():
#	redirect('/static/index.html')
#	redirect('http://'+os.environ['APP_NAME']+'.sinaapp.com/static/welcome.html')
    bgurl = get_background()
    return dict(background=bgurl)

@root.get('/static/:path#.*#')
def static_route(path):
    return static_file(path,root=static_path)

@root.get('/favicon.ico')
def favicon_route():
    #return static_file('favicon.ico','static')
    return ''

@root.post('/login')
def login():
    request.forms['walpw_username']
    redirect('/diary/')

@root.get('/bing_desktop')
def bing_desktop():
    s = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
    resp = fetch_url(s)
    response.set_content_type(resp[0])
    return resp[1]
