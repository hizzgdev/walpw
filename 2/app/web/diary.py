#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
from bottle import Bottle,view,static_file,redirect

from app.web.util import get_username_cookie
from app.biz.user import UserService
from app.biz.diary import DiaryService

diary = Bottle()

@diary.get('/')
@view('diary_list')
def root_index():
    ds = DiaryService()
    us = UserService()
    username = get_username_cookie()
    if username == None:
        redirect('/login')
    #userinfo = us.get_user_info(username)
    #diarys = ds.get_recent_diarys(username, 12)
    #return dict(userinfo=userinfo,diarys=diarys)

    return dict(userinfo=None,diarys=[])

