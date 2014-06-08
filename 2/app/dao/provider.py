#! /usr/bin/env python
# -*- coding:utf-8 -*-

import traceback
import sae.const
import MySQLdb as mdb

class mysql(object):

	def __init__(self):
		self.host	= sae.const.MYSQL_HOST
		self.port	= int(sae.const.MYSQL_PORT)
		self.user	= sae.const.MYSQL_USER
		self.pwd	= sae.const.MYSQL_PASS
		self.db		= sae.const.MYSQL_DB
		#self.host='localhost'
		#self.user='walpw'
		#self.pwd='walpw'
		#self.db='app_walpw'

	def _conn(self):
		return mdb.connect(self.host,self.user,self.pwd,self.db,port=self.port)

	def _close(self,conn):
		if conn != None:
			conn.close()

	def query(self,sql,parameters=None):
		conn = None
		try:
			conn = self._conn()
			cur = conn.cursor(mdb.cursors.DictCursor)
			cur.execute('set names utf8')
			cur.execute(sql,parameters)
			rows = cur.fetchall()
			cur.close()
			return rows
		except mdb.Error,e:
			traceback.print_exc()
		finally:
			self._close(conn)

	def execute(self,sql,parameters=None):
		conn = None
		try:
			conn = self._conn()
			cur = conn.cursor()
			cur.execute('set names utf8')
			cur.execute(sql,parameters)
			conn.commit()
		except mdb.Error,e:
			traceback.print_exc()
			conn.rollback()
		finally:
			self._close(conn)


DbProvider = mysql
