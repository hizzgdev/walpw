#! /usr/bin/env python
# -*- coding:utf-8 -*-
from bottle import request,response

def get_cookie(key):
    secret = get_clientip()
    return request.get_cookie(key,secret=secret)

def set_cookie(key, value):
    secret = get_clientip()
    response.set_cookie(key,value,secret=secret)

def get_clientip():
    return request.environ.get('REMOTE_ADDR')

def set_username_cookie(username):
    set_cookie('walpw',username)

def get_username_cookie():
    return get_cookie('walpw')

