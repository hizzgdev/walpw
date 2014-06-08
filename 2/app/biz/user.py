#! /usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import re,datetime,uuid
from app.dao.user import UserDao

class UserService(object):

#used
    def _md5(self,str):
        if str == None:
            return ''
        else:
            return hashlib.md5(str).hexdigest()

    def __init__(self):
        self.uda = UserDao()
        self.InvalidDateTime = datetime.datetime(1900,1,1,0,0,0)
        self.BadWords = ':;,\'"/\\*#!&^.%<>'

#used
    def check_user_identity(self,username,password):
        encpwd = self._md5(password)
        return self.uda.validate_user_encpwd(username,encpwd)

    def is_safe_username(self, username):
        ua = re.split('['+self.BadWords+']',username)
        if len(ua) > 1:
            return False
        else:
            return True

    def is_user_exist(self, username):
        rows = self.uda.get_user_info(username,field='FUID')
        if rows == None or len(rows) == 0:
            return False
        else:
            return True
        
    def register(self,boy,girl):
        encodeUtil = EncodeUtil()
        boyname = boy['username']
        girlname = girl['username']
        nowtime = datetime.datetime.now()
        boy['id'] = uuid.uuid5(uuid.NAMESPACE_DNS,uuid.uuid1().get_hex()).get_hex()
        boy['lover']    = girlname
        boy['time']    = nowtime
        boy['password'] = encodeUtil.md5hash(boy['password'])
        boy['birthday'] = self.InvalidDateTime
        boy['nickname'] = boyname
        boy['sex']    = '1'

        girl['id'] = uuid.uuid5(uuid.NAMESPACE_DNS,uuid.uuid1().get_hex()).get_hex()
        girl['lover']    = boyname
        girl['time']    = nowtime
        girl['password'] = encodeUtil.md5hash(girl['password'])
        girl['birthday'] = self.InvalidDateTime
        girl['nickname'] = girlname
        girl['sex']    = '2'

        if self.is_user_exist(boyname):
            return -1
        if self.is_user_exist(girlname):
            return -2
        self.uda.insert_user_info(boy)
        self.uda.insert_user_info(girl)
        return 0

    def get_user_face_path(self, username):
        rows = self.uda.get_user_info(username, field='FUFaceImage')
        if(rows == None or len(rows) == 0):
            return None
        else:
            return rows[0]['FUFaceImage']

    def get_lover_name(self, username):
        return self.uda.get_user_lover_name(username)
        #cache

    def update_user_logininfo(self, username,ip):
        logininfo = {
            'username':username,
            'ip':ip,
            'time':datetime.datetime.now()
            }
        self.uda.update_user_logininfo(logininfo)

    def update_password(self, username, old_pwd, pwd, pwd_lover):
        old_pwd_pass = self.check_user_identity(username, old_pwd)
        if not old_pwd_pass:
            return -1
        encodeUtil = EncodeUtil()
        if pwd != None and len(pwd) > 0 :
            self.uda.reset_password(username,encodeUtil.md5hash(pwd))
        if pwd_lover != None and len(pwd_lover) > 0:
            self.uda.reset_password_lover(username,encodeUtil.md5hash(pwd_lover))
        return 0

    def reset_password(self, username, enc_pwd, pwd):
        pwd_field = 'FUPassword'
        userinfo = self.uda.get_user_info(username,pwd_field)
        old_pwd = userinfo[pwd_field]
        encodeUtil = EncodeUtil()
        old_encpwd = encodeUtil.md5hash('walpw'+old_pwd+'walgw')
        if enc_pwd == old_encpwd:
            self.uda.reset_password(username,encodeUtil.md5hash(pwd))
            return 0
        else:
            return -1


    def save_userinfo(self,username,userinfo):
        strbirthday = userinfo['birthday']
        if strbirthday == None or len(strbirthday) == 0:
            birthday = self.InvalidDateTime
        else:
            birthday = datetime.datetime.strptime(strbirthday,'%Y_%m_%d')
        self.uda.save_user_info(username,userinfo['bigarea'],userinfo['smallarea'],birthday,userinfo['email'])


#used
    def get_userinfo(self, username):
        userinfo = None
        if username != None and len(username) > 0:
            userinfos = self.uda.get_user_info(username)
            if userinfos != None and len(userinfos) > 0:
                userinfo = userinfos[0]
        return userinfo














        strArray = []
        strArray.append('<?xml version=\"1.0\" encoding=\"utf-8\"?>')
        strArray.append('<userinfos>')
        strArray.append(self.strf_userinfo(userinfo))
        strArray.append('</userinfos>')
        return ''.join(strArray)

    def strf_userinfo(self, userinfo):
        if userinfo == None :
            return ''
        if userinfo['FUSex'] == 1:
            sex = 'male'
        else:
            sex = 'female'
        birthday = userinfo['FUBirthday']
        if birthday == self.InvalidDateTime:
            strbirthday = ''
        else:
            strbirthday = birthday.strftime('%m/%d/%Y')
        
        strArray = []
        strArray.append('<userinfo>')
        strArray.append('<username>{0}</username>'.format(userinfo['FUName']))
        strArray.append('<sex>{0}</sex>'.format(sex))
        strArray.append('<lover>{0}</lover>'.format(userinfo['FULover']))
        strArray.append('<email>{0}</email>'.format(userinfo['FUSafeEmail']))
        strArray.append('<birthday>{0}</birthday>'.format(strbirthday))
        strArray.append('<bigarea>{0}</bigarea>'.format(userinfo['FUAreaBig']))
        strArray.append('<smallarea>{0}</smallarea>'.format(userinfo['FUAreaSmall']))
        strArray.append('</userinfo>')
        return ''.join(strArray)

if __name__ == '__main__':
    print('this is user information service')
