#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import datetime
from bottle import Bottle,view,static_file,redirect,request,response

from app.util import fetch_url
from app.web.util import set_username_cookie
from app.web.diary import diary

from app.biz.user import UserService

static_path = 'static'

root = Bottle()
root.mount(diary,'/diary')

def get_background():
    s = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
    resp = fetch_url(s)
    d = json.loads(resp[1])
    bg_url=d['images'][0]['url']
    #bg_url = 'http://s.cn.bing.net/az/hprichbg/rb/HerzliyaIsrael_ZH-CN12724786713_1366x768.jpg'
    return bg_url

def get_background_cached():
    return get_background_kvdb()

def get_background_kvdb():
    import sae.kvdb
    t = datetime.datetime.now().strftime('%Y%m%d')
    kv = sae.kvdb.KVClient()
    t_mc = kv.get('bg_time')
    bg_url = kv.get('bg_url')
    if bg_url == None or t != t_mc:
        bg_url = get_background()
        kv.set('bg_url',bg_url)
    if t != t_mc:
        kv.set('bg_time',t)
    return bg_url


def get_background_mc():
    import pylibmc as memcache
    t = datetime.datetime.now().strftime('%Y%m%d')
    mc = memcache.Client()
    t_mc = mc.get('bg_time')
    bg_url = mc.get('bg_url')
    if bg_url == None or t != t_mc:
        bg_url = get_background()
        mc.set('bg_url',bg_url)
    if t != t_mc:
        mc.set('bg_time',t)
    return bg_url

@root.get('/')
@view('login')
def root_index():
#   redirect('/static/index.html')
#   redirect('http://'+os.environ['APP_NAME']+'.sinaapp.com/static/welcome.html')
    return login_get()

@root.get('/static/:path#.*#')
def static_route(path):
    return static_file(path,root=static_path)

@root.get('/favicon.ico')
def favicon_route():
    #return static_file('favicon.ico','static')
    return ''

@root.get('/login')
@view('login')
def login_get():
    bgurl = get_background_cached()
    redirect_url = request.GET.get('go')
    if redirect_url == None:
        redirect_url = '/diary/'
    return dict(background=bgurl,redirect_url = redirect_url)


@root.post('/login')
def login_post():
    userService = UserService()
    f = request.forms#.decode('utf-8')
    username = f.get('walpw_username')
    password = f.get('walpw_password')
    redirect_url = f.get('go')
    if username != None:
        validate = userService.check_user_identity(username,password)
        if validate :
            set_username_cookie(username)
            redirect(redirect_url)
    redirect('/login')

@root.get('/bing_desktop')
def bing_desktop():
    s = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
    resp = fetch_url(s)
    response.set_content_type(resp[0])
    return resp[1]
