#! /usr/bin/env python
# -*- coding:utf-8 -*-

from provider import DbProvider

class UserDao(DbProvider):

    def __init__(self):
        DbProvider.__init__(self)

    def validate_user_encpwd(self,username,encpwd):
        rows = self.query('select FUName from T_User_M where FUName = %s and FUPassword = %s',(username,encpwd))
        validate_fail = (rows == None or len(rows) == 0)
        return not validate_fail

    def reset_password(self,username,pwd):
        sql = 'update T_User_M set FUPassword=%s where FUName=%s'
        param = (pwd, username)
        self.execute(sql,param)

    def reset_password_lover(self,username,pwd):
        sql = 'update T_User_M set FUPassword=%s where FULover=%s'
        param = (pwd, username)
        self.execute(sql,param)

    def save_user_info(self,username,bigarea,smallarea,birthday,email):
        sql = 'update T_User_M set FUAreaBig=%s,FUAreaSmall=%s,FUBirthday=%s,FUSafeEmail=%s where FUName=%s'
        param=(bigarea,smallarea,birthday,email,username)
        self.execute(sql,param)

    def get_user_info(self,username,field=None):
        rows = None
        if(field == None):
            rows = self.query('select FUID,FUName,FULover,FUStatus,FURegIP,FURegTime,FULoginIP,FULoginTime,FULoginCount,FUPassword,FUSafeEmail,FUBirthday,FUNickName,FUSex,FUAreaBig,FUAreaSmall,FUFaceImage from T_User_M where FUName = %s',(username))
        else:
            rows = self.query('select '+field+' from T_User_M where FUName = %s',(username))
        return rows

    def insert_user_info(self,userinfo):
        sql = 'insert into T_User_M(FUID,FUName,FULover,FUStatus,FURegIP,FURegTime,FUPassword,FUBirthday,FUNickName,FUSex,FUAreaBig,FUAreaSmall) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        param = (userinfo['id'],userinfo['username'],userinfo['lover'],0,userinfo['ip'],userinfo['time'],userinfo['password'],userinfo['birthday'],userinfo['nickname'],userinfo['sex'],userinfo['bigarea'],userinfo['smallarea'])
        self.execute(sql,param)

    def get_user_lover_name(self,username):
        rows = self.query('select FULover from T_User_M where FUName = %s',(username))
        if rows == None or len(rows) == 0 :
            return None
        else:
            return rows[0]['FULover']

    def update_user_logininfo(self,logininfo):
        sql = 'update T_User_M set FULoginIP = %s,FULoginTime = %s, FULoginCount = FUloginCount + 1 where FUName= %s'
        param = (logininfo['ip'],logininfo['time'],logininfo['username'])
        self.execute(sql,param)


if __name__ == '__main__':
    pass
