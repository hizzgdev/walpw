#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
from bottle import Bottle,view,static_file

#from app.web.bbs import bbs

root = Bottle()

#root.mount(bbs,'/bbs')


#curr_path = os.path.split(os.path.realpath(__file__))[0]
#static_path = curr_path+'/static'
static_path = 'static'

@root.get('/')
@view('index')
def root_index():
#	redirect('/static/index.html')
#	redirect('http://'+os.environ['APP_NAME']+'.sinaapp.com/static/welcome.html')
	return dict(title='root')

@root.get('/static/:path#.*#')
def static_route(path):
    return static_file(path,root=static_path)

@root.get('/favicon.ico')
def favicon_route():
	#return static_file('favicon.ico','static')
	return ''


