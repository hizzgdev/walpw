#! /usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
from provider import DbProvider

class DiaryDao(DbProvider):

    def __init__(self):
        DbProvider.__init__(self)

    def get_users(self):
        rows = self.query('select FUName as girl, FULover as boy, FUPassword as password, FUNickName as diaryId from T_User_M where EXISTS (select 1 from T_Document where FDTags = FUNickName) and FUSex = 2 limit 1000')
        return rows

    def get_user_diarys(self, diaryId):
        sql = 'select FDID,FDUName,FDTitle,FDContent,DATE_FORMAT(FDTime, %s) as FDTime1,FDIP,DATE_FORMAT(FDEditTime,%s) as FDEditTime1,FDWeather from T_Document where FDTags = %s limit 1000'
        return self.query(sql, ('%Y-%m-%d %H:%i:%s', '%Y-%m-%d %H:%i:%s', diaryId))

    def get_diary_by_id(self, diaryid):
        condition = 'FDID=%s'
        param = (diaryid)
        return self.get_diarys(condition,param)

    def get_diarys_by_user_since_date(self, username, since, limit):
        condition = 'FDTime >= %s and (FDUName = %s or FDULoverName = %s)'
        params = (since,username,username)
        return self.get_diarys(condition, params, True, 'desc', limit)

    def get_diarys_by_user_date(self, username, date):
        condition = ' FDTime >= %s and FDTime < %s and (FDUName = %s or FDULoverName = %s)'
        date_e = date+datetime.timedelta(days=1)
        params = (date,date_e,username,username)
        return self.get_diarys(condition,params)

    def get_diarysdate_by_user_datescope(self, username, date_start, date_end):
        sql = 'select distinct FDTime from T_Document where FDTime >= %s and FDTime < %s and (FDUName = %s or FDULoverName = %s)'
        params = (date_start,date_end,username,username)
        rows = self.query(sql, params)
        return rows

    def get_diarys_by_user_datescope(self, date_start, date_end, username):
        if date_start != None and date_end != None:
            condition = ['FDTime >= %s and FDTime < %s']
            param = [date_start,date_end]
            order_type = 'asc'
        else:
            condition = []
            param = []
            order_type = 'desc'

        if username == None:
            condition.append('FDOpenLevel=0')
        else:
            condition.append('(FDUName = %s or FDULoverName = %s)')
            param.append(username)
            param.append(username)
        return self.get_diarys(' and '.join(condition),param,with_content=False,order_type=order_type)
            

    def year_group_count(self,username=None):
        if username == None:
            sql = 'select year(FDTime) as d,count(*) as c from T_Document where FDOpenLevel=0 group by d'
            param = ()
        else:
            sql = 'select year(FDTime) as d,count(*) as c from T_Document where FDUName=%s or FDULoverName=%s group by d'
            param = (username,username)
        rows = self.query(sql,param)
        return rows
        
    def month_group_count(self,date_s,date_e,username=None):
        if username == None:
            sql = 'select month(FDTime) as d,count(*) as c from T_Document where FDOpenLevel=0 and FDTime>=%s and FDTime<%s group by d'
            param = (date_s,date_e)
        else:
            sql = 'select month(FDTime) as d,count(*) as c from T_Document where FDTime>=%s and FDTime<%s and (FDUName=%s or FDULoverName=%s) group by d'
            param = (date_s,date_e,username,username)
        rows = self.query(sql,param)
        return rows

    def date_group_count(self,date_s,date_e,username=None):
        if username == None:
            sql = 'select day(FDTime) as d,count(*) as c from T_Document where FDOpenLevel=0 and FDTime>=%s and FDTime<%s group by d'
            param = (date_s,date_e)
        else:
            sql = 'select day(FDTime) as d,count(*) as c from T_Document where FDTime>=%s and FDTime<%s and (FDUName=%s or FDULoverName=%s) group by d'
            param = (date_s,date_e,username,username)
        rows = self.query(sql,param)
        return rows

    def get_diarys(self, condition, params, with_content=True, order_type='asc', limit=-1, offset=-1):
        sql = None
        if with_content :
            sql = 'select FDID,FDUName,FDULoverName,FDTitle,FDTags,FDContent,FDTime,FDIP,FDEditTime,FDOpenLevel,FDCommCount,FDVisitCount,FDMostTop,FDRemark,FDAllowComment,FDWeather from T_Document'
        else :
            sql = 'select FDID,FDUName,FDULoverName,FDTitle,FDTags,\'\' as FDContent,FDTime,FDIP,FDEditTime,FDOpenLevel,FDCommCount,FDVisitCount,FDMostTop,FDRemark,FDAllowComment,FDWeather from T_Document'

        if condition != None :
            sql = sql + ' where ' + condition
        if order_type == 'asc':
            sql = sql + ' order by FDTime'
        else:
            sql = sql + ' order by FDTime desc'

        if limit >= 0 :
            sql = sql + ' limit ' + str(limit)
        if offset >= 0 :
            sql = sql + ' offset ' + str(offset)

        rows = self.query(sql, params)

        return rows

    def hit_diary(self, diaryid):
        sql = 'update T_Document set FDVisitCount = FDVisitCount + 1 where FDID = %s'
        self.execute(sql,(diaryid))

    def add_diary(self, diary):
        sql = 'insert into T_Document(FDID,FDUName,FDULoverName,FDTitle,FDTags,FDContent,FDTime,FDIP,FDEditTime,FDOpenLevel,FDCommCount,FDVisitCount,FDMostTop,FDRemark,FDAllowComment,FDWeather) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        param = (diary['id'],diary['username'],diary['lover'],diary['title'],'',diary['content'],diary['date'],diary['ip'],diary['edittime'],diary['openlevel'],'0','0',diary['mosttop'],'',diary['allowcomment'],diary['weather'])
        self.execute(sql,param)

    def update_diary(self, diary):
        sql = 'update T_Document set FDTitle=%s,FDContent=%s,FDTime=%s,FDIP=%s,FDEditTime=%s,FDOpenLevel=%s,FDMostTop=%s,FDRemark=%s,FDAllowComment=%s,FDWeather=%s where FDID=%s'
        param = (diary['title'],diary['content'],diary['date'],diary['ip'],diary['edittime'],diary['openlevel'],diary['mosttop'],'',diary['allowcomment'],diary['weather'],diary['id'])
        self.execute(sql,param)

    def append_diary(self, diaryid, content):
        sql = 'update T_Document set FDContent = concat(FDContent,%s) where FDID=%s'
        param = (content,diaryid)
        self.execute(sql,param)

    def delete_diary(self, diaryid):
        self.execute('delete from T_Document where FDID=%s',(diaryid))

    def get_diary_owners(self, diaryid):
        rows = self.query('select FDUName,FDULoverName from T_Document where FDID=%s',(diaryid))
        if rows == None or len(rows) == 0:
            return None
        else:
            return [rows[0]['FDUName'],rows[0]['FDULoverName']]

    def get_diary_fields(self, fields, diaryid):
        rows = self.query('select '+','.join(fields)+' from T_Document where FDID=%s',(diaryid))
        return rows

    def comment_count_add(self, diaryid, increase):
        sql = 'update T_Document set FDCommCount = FDCommCount + %s where FDID = %s'
        self.execute(sql,(increase, diaryid))

if __name__ == '__main__':
    print('use app.dao.document.DocumentDataAccess for documents data access')
