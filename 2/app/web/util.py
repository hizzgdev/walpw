#! /usr/bin/env python
# -*- coding:utf-8 -*-
from bottle import request,response

def get_cookie(key):
    secret = get_clientip()
    return request.get_cookie(key,secret=secret)

def set_cookie(key, value):
    secret = get_clientip()
    response.set_cookie(key,value,secret=secret)

def del_cookie(key):
    response.delete_cookie(key)

def get_clientip():
    return request.environ.get('REMOTE_ADDR')

def set_username_cookie(username):
    set_cookie('walpw',username)

def get_username_cookie():
    return get_cookie('walpw')

def clear_username_cookie():
    del_cookie('walpw')

