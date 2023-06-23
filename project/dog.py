# import logging so we can write messages to the log
import logging
# import the class DbHandler to interact with the database
import db_handler
#import users library
from google.appengine.api import users
#import date library
from datetime import date
#create an object- dog
class dog():
	def __init__(self):
		self.m_DbHandler=db_handler.DbHandler()
		self.Dog_id=""
		# create data members of the class dog
		self.Dog_name= ""
		self.Gender = ""
		self.Age = ""
		self.Dog_type_name= ""
		self.OR_Email = ""
		self.activityday=None

    #This method inserts the dog's info into a database
	def insertToDb(self):
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		#this sql query inserts the dog's info immidiately when he signs up to the system into the Dog table
		sql ="""INSERT INTO Dog(Dog_name,Gender,Age,Dog_type_name,OR_Email) 
		VALUES(%s,%s,%s,%s,%s)
		"""
		#execute the info
		cursor.execute( sql,(self.Dog_name,self.Gender,self.Age,self.Dog_type_name,self.OR_Email))
		self.Dog_id=cursor.lastrowid
		self.m_DbHandler.commit()
		self.m_DbHandler.disconnectFromDb()
		return

