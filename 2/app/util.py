#! /usr/bin/env python
# -*- coding:utf-8 -*-

import urllib
def fetch_url(url):
    resp = urllib.urlopen(url)
    resp_text = resp.read()
    resp_type = resp.info().getheader('content-type')
    return (resp_type,resp_text)

if __name__ == '__main__':
    #s = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
    #print(fetch_url(s))
    pass
