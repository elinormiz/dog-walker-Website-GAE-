import webapp2
#import jinja and os libraries
import jinja2
# import operating system library
import os
#import users library
from google.appengine.api import users
# import logging so we can write messages to the log
import logging
#import modules
import owner
import walker
import dog
import get_information
import db_handler
#import MYSQLdb library
import MySQLdb
# ---------------------------------------------------------------------------------
#creating a class to find errors that the user makes
# ---------------------------------------------------------------------------------
class check():
	def __init__(self):
		self.m_DbHandler=db_handler.DbHandler()
	#if the user already pick this walker to his dog at this day- return True if there is an error
	def errorcheck(self,dog_id,work_day,W_Email):
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		#this sql query inserts the user's info immidiately when he signs up to the system into the UserDetails table
		sql ="""SELECT * FROM walks_on
				WHERE Dog_id=%s and work_day=%s and W_Email=%s
		"""
		#execute the info
		rows_count=cursor.execute( sql,(dog_id,work_day,W_Email,))
		self.m_DbHandler.commit()
		if rows_count>0:#if there is a match
			info=cursor.fetchall()
			a=True#error
		else:
			a=False
		return a
	#will check if the user is a walker
	def walkercheck(self,W_Email):
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		#this sql query inserts the user's info immidiately when he signs up to the system into the UserDetails table
		#checking if there is already a walker with his google account
		sql ="""SELECT * FROM Dog_walker
				WHERE W_Email=%s
		"""
		#execute the info
		rows_count=cursor.execute( sql,(W_Email,))
		self.m_DbHandler.commit()
		if rows_count>0:
			info=cursor.fetchall()
			a=True#error
		else:
			a=False
		return a
	#will check if the user is an owner
	def ownercheck(self,OR_Email):
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		#this sql query inserts the user's info immidiately when he signs up to the system into the UserDetails table
		#checking if there is already a owner with his google account
		sql ="""SELECT * FROM Owner_regular
				WHERE OR_Email=%s
		"""
		#execute the info
		rows_count=cursor.execute( sql,(OR_Email,))
		self.m_DbHandler.commit()
		if rows_count>0:
			info=cursor.fetchall()
			a=True#error
		else:
			a=False
		return a
	#check how many customers the walker has at this day.
	def enough_place(self,work_day,W_email):
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		#this sql query inserts the user's info immidiately when he signs up to the system into the UserDetails table
		sql ="""SELECT COUNT(*) FROM walks_on
				WHERE work_day=%s
				GROUP BY W_Email
				HAVING W_Email=%s
			"""
		#execute the info
		cursor.execute( sql,(work_day,W_email,))
		self.m_DbHandler.commit()
		details=cursor.fetchall()
		#create the details as a good atring
		details=str(details).replace('((',"").replace('L,),)',"")
		if str(details)=='()':
			details=0
		return int(details)
		
	