#! /usr/bin/env python
# -*- coding=utf-8 -*-

import sys
sys.path.append('/home/zzg/projects/walpw.sae/2/sae')
from bottle import debug,run,request,response,redirect,static_file
from app.web.root import root

if __name__ == '__main__':
    debug(True)
    #run(server='gevent',app=_app)
    run(app=root,host='0.0.0.0',reloader=True)
    #run(server='gevent',app=_app,host='192.168.9.119',reloader=True)
    #run(app=_app,host='192.168.9.119',port='80')
