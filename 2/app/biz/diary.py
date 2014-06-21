#! /usr/bin/env python
# -*- coding:utf-8 -*-

import uuid
import datetime
#from app.lib.relativedelta import relativedelta
from app.dao.diary import DiaryDao
class DiaryService(object):

    def __init__(self):
        self.dda = DiaryDao()

    def save_diary(self, username, diary):
        nowtime = datetime.datetime.now()
        userInfoService = UserInfoService()
        diary['edittime'] = nowtime
        diary['mosttop'] = 0
        if diary['id'] == None or len(diary['id']) == 0 :
            uid = uuid.uuid5(uuid.NAMESPACE_DNS,uuid.uuid1().get_hex()).get_urn()
            uid = uid[9:]
            diary['id'] = uid
            diary['username'] = username
            diary['lover'] = userInfoService.get_lover_name(username)
            self.dda.add_diary(diary)
        else :
            is_diary_owner = self.is_diary_owner(diary['id'],username)
            if not is_diary_owner:
                return '-1'
            append_content = '\r\n[以上内容由{0}修改于{1:%Y年%m月%d日 %H:%M:%S}]'.format(username,nowtime)
            diary['content'] = diary['content']+append_content
            self.dda.update_diary(diary)
        return 0

    def append_diary(self, diaryid, username, content):
        is_diary_owner = self.is_diary_owner(diaryid,username)
        if not is_diary_owner:
            return '-1'
        nowtime = datetime.datetime.now()
        append_content = '\r\n[以上内容由{0}修改于{1:%Y年%m月%d日 %H:%M:%S}]'.format(username,nowtime)
        self.dda.append_diary(diaryid, '\r\n'+content+append_content)
        return '0'

    def delete_diary(self, diaryid, username):
        is_diary_owner = self.is_diary_owner(diaryid,username)
        if not is_diary_owner:
            return '-1'
        self.dda.delete_diary(diaryid)
        return '0'

    def comment_count_up(self, diaryid):
        self.dda.comment_count_add(diaryid, 1)
    
    def comment_count_down(self, diaryid):
        self.dda.comment_count_add(diaryid, -1)

    def get_recent_diarys(self, username, limit):
        since = datetime.datetime.now() - datetime.timedelta(days=30000)
        return self.dda.get_diarys_by_user_since_date(username, since, limit);

    def get_diary_by_id_xml(self, username, diaryid):
        if username == None:
            return None
        diarys = self.dda.get_diary_by_id(diaryid)
        if len(diarys) > 0:
            diary = diarys[0]
            if diary['FDUName'] == username or diary['FDULoverName'] == username or diary['FDOpenLevel'] == 0:
                self.dda.hit_diary(diaryid)
            else:
                diarys = None
        return self.strf_diarys('data',diarys)

    def get_diary_by_id_dict(self, username, diaryid):
        if username == None:
            return None
        diarys = self.dda.get_diary_by_id(diaryid)
        diary = None
        if len(diarys) > 0:
            diary = diarys[0]
            if diary['FDUName'] == username or diary['FDULoverName'] == username or diary['FDOpenLevel'] == 0:
                self.dda.hit_diary(diaryid)
            else:
                diary = None
        return diary

    def get_diarys_by_date(self, username, year, month, day):
        if username == None:
            return None
        date = datetime.date(year, month, day)
        diarys = self.dda.get_diarys_by_user_date(username,date)
        for diary in diarys :
            self.dda.hit_diary(diary['FDID'])
        diarys_str = self.strf_diarys('data',diarys)
        return diarys_str

    def _get_diarys_by_month(self, username, year, month):
        date_start = datetime.date(year, month, 1)
        date_end = date_start + relativedelta(months=1)
        diarys = self.dda.get_diarysdate_by_user_datescope(username, date_start, date_end)
        return diarys

    def get_diarysdate_by_month(self, username, year, month):
        strArray = []
        diarys = self._get_diarys_by_month(username, year, month)
        if diarys != None :
            for diary in diarys:
                strArray.append(diary['FDTime'].strftime('%d'))
        return ','.join(strArray)

    def get_diarysdate_by_scope(self,year,month):
        dateformat = '{:0>4d}'
        if year == None:
            date_group_count = self.dda.year_group_count()
        elif month == None:
            date_s = datetime.datetime(year,1,1,0,0,0)
            date_e = date_s + relativedelta(years=1)
            dateformat = '{:0>2d}'
            date_group_count = self.dda.month_group_count(date_s,date_e)
        else:
            date_s = datetime.datetime(year,month,1,0,0,0)
            date_e = date_s + relativedelta(months=1)
            dateformat = '{:0>2d}'
            date_group_count = self.dda.date_group_count(date_s,date_e)
        strdate = []
        strcount = []
        if date_group_count == None or len(date_group_count) == 0:
            return '|'

        for row in date_group_count:
            strdate.append(dateformat.format(row['d']))
            strcount.append(str(row['c']))
        return ','.join(strdate)+'|'+','.join(strcount)

    def get_diarysdate_by_user_scope(self,username,year,month):
        if username == None or len(username) == 0:
            return '|'
        dateformat = '{:0>4d}'

        if year == None:
            date_group_count = self.dda.year_group_count(username=username)
        elif month == None:
            date_s = datetime.datetime(year,1,1,0,0,0)
            date_e = date_s + relativedelta(years=1)
            dateformat = '{:0>2d}'
            date_group_count = self.dda.month_group_count(date_s,date_e,username=username)
        else:
            date_s = datetime.datetime(year,month,1,0,0,0)
            date_e = date_s + relativedelta(months=1)
            dateformat = '{:0>2d}'
            date_group_count = self.dda.date_group_count(date_s,date_e,username=username)
        strdate = []
        strcount = []

        if date_group_count == None or len(date_group_count) == 0:
            return '|'

        for row in date_group_count:
            strdate.append(dateformat.format(row['d']))
            strcount.append(str(row['c']))
        return ','.join(strdate)+'|'+','.join(strcount)

    def get_diarys_by_user_scope(self,username,year,month):
        if year == None:
            date_s = None
            date_e = None
        elif month == None:
            date_s = datetime.datetime(year,1,1,0,0,0)
            date_e = date_s + relativedelta(years=1)
        else:
            date_s = datetime.datetime(year,month,1,0,0,0)
            date_e = date_s + relativedelta(months=1)
        diarys = self.dda.get_diarys_by_user_datescope(date_s,date_e,username)
        return self.strf_diarys('info',diarys)
        

    def strf_diarys(self, outputtype, diarys):
        strArray = []
        if diarys != None :
            if outputtype == 'data' :
                for diary in diarys :
                    strArray.append(self.strf_diary_data(diary))
            else :
                for diary in diarys :
                    strArray.append(self.strf_diary_info(diary))
        formatter = '''<?xml version=\"1.0\" encoding=\"utf-8\"?>
<diarys>
{0}
</diarys>'''
        return formatter.format(''.join(strArray))

    
    def strf_diary_info(self, diary):
        if diary == None :
            return None
        formatter = '''<diary>
<id>{0[FDID]}</id>
<title><![CDATA[{0[FDTitle]}]]></title>
<date>{0[FDTime]:%Y-%m-%d}</date>
<author>{0[FDUName]}</author>
<visit>{0[FDVisitCount]}</visit>
<comment>{0[FDCommCount]}</comment>
</diary>'''
        return formatter.format(diary)


    def strf_diary_data(self, diary):
        if diary == None :
            return None

        formatter = '''<diary>
<id>{0[FDID]}</id>
<title><![CDATA[{0[FDTitle]}]]></title>
<date>{0[FDTime]:%Y-%m-%d}</date>
<weather>{0[FDWeather]}</weather>
<author>{0[FDUName]}</author>
<visit>{0[FDVisitCount]}</visit>
<comment>{0[FDCommCount]}</comment>
<content><![CDATA[{0[FDContent]}]]></content>
<openlevel>{0[FDOpenLevel]}</openlevel>
<allowcomment>{0[FDAllowComment]}</allowcomment>
</diary>'''
        return formatter.format(diary)

    def is_diary_owner(self, diaryid, username):
        owners = self.dda.get_diary_owners(diaryid)
        if owners == None:
            return False

        if username == owners[0] or username == owners[1]:
            return True
        else:
            return False

    def can_comment(self, diaryid):
        diary_info = self.dda.get_diary_fields(['FDAllowComment'], diaryid)
        if diary_info == None or len(diary_info) == 0:
            return False
        if diary_info[0]['FDAllowComment']:
            return True
        else:
            return False

if __name__ == '__main__':
    print('use app.service.diary.Diary for diary service')
