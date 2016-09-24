#! /usr/bin/env python
# -*- coding:utf-8 -*-

import json
import datetime
from bottle import Bottle,view,static_file,redirect
from sae.storage import Bucket

import app.web.util as webtools

diary = Bottle()

diary_bucket = Bucket('diary')

@diary.get('/')
@view('diary_list')
def root_index():
    username = webtools.get_username_cookie()
    if username == None:
        redirect('/login')
    userinfo = get_user_info(username)
    if userinfo == None:
        redirect('/login')

    boy = userinfo['boy']
    girl = userinfo['girl']
    diarys = get_diarys_list(userinfo['diaryId'])
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

