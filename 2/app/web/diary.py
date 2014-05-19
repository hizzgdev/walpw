#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
from bottle import Bottle,view,static_file

diary = Bottle()

@diary.get('/')
@diary.get('')
@view('diary_index')
def root_index():
#	redirect('/static/index.html')
#	redirect('http://'+os.environ['APP_NAME']+'.sinaapp.com/static/welcome.html')
	return dict(title='root')

