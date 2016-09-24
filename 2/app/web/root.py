#! /usr/bin/env python
# -*- coding:utf-8 -*-

import json
import datetime
import hashlib
from bottle import Bottle,debug,view,static_file,redirect,request,response
from app.util import fetch_url
from app.web.util import set_username_cookie,get_username_cookie,clear_username_cookie
from sae.storage import Bucket

debug(True)

static_path = 'static'
diary_bucket = Bucket('diary')

root = Bottle()

@root.get('/static/:path#.*#')
def static_route(path):
    return static_file(path,root=static_path)

@root.get('/favicon.ico')
def favicon_route():
    #return static_file('favicon.ico','static')
    return ''

@root.get('/bing_desktop')
def bing_desktop():
    s = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
    resp = fetch_url(s)
    response.set_content_type(resp[0])
    return resp[1]

@root.get('/')
@view('login')
def root_index():
    return login_get()

@root.get('/login')
@view('login')
def login_get():
    bgurl = get_background_cached()
    redirect_url = request.GET.get('go')
    if redirect_url == None:
        redirect_url = '/diary'
    return dict(background=bgurl,redirect_url = redirect_url)

@root.post('/login')
def login_post():
    f = request.forms#.decode('utf-8')
    username = f.get('walpw_username')
    password = f.get('walpw_password')
    redirect_url = f.get('go')
    if username != None:
        user_info = get_user_info(username)
        if user_info != None and user_info['password'] == hashlib.md5(password).hexdigest():
            set_username_cookie(username)
            redirect(redirect_url)
    redirect('/login')


@root.get('/logout')
def logout():
    clear_username_cookie()
    redirect('/login')


@root.get('/diary')
@view('diary_list')
def diary_list():
    #DiaryService().dump_users()
    username = get_username_cookie()
    if username == None:
        redirect('/login')
    userinfo = get_user_info(username)
    if userinfo == None:
        redirect('/login')

    boy = userinfo['boy']
    girl = userinfo['girl']
    diarys = get_diary_list(userinfo['diaryId'])
    return dict(boy=boy,girl=girl,diarys=diarys)

def get_user_info(username):
    obj_id = '/user/{0}.dat'.format(username)
    try:
        content = diary_bucket.get_object_contents(obj_id)
        if content != None:
            return json.loads(content)
    except:
        pass
    return None

def get_diary_list(diary_id):
    obj_id = '/diary/{0}.dat'.format(diary_id)
    try:
        content = diary_bucket.get_object_contents(obj_id)
        if content != None:
            return json.loads(content)
    except:
        pass
    return None

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


