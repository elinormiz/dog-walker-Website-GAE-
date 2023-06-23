# import webapp2  - Python web framework compatible with Google App Engine
import webapp2
# import logging so we can write messages to the log
import logging
# import the class DbHandler to interact with the database
import db_handler
#import users library
from google.appengine.api import users
#import date library
from datetime import date
#create an object- walker
class walker():
	def __init__(self):
		self.m_DbHandler=db_handler.DbHandler()
		# create data members of the class walker
		self.Price_per_day=None
		self.Max_dog_number_per_day= None
		self.W_Email = ""
		self.W_City = ""
		self.W_Phone_Number= ""
		self.W_First_name = ""
		self.W_Last_name = ""
		self.work_days=[]
		self.work_dogs=[]
		self.choose_day=""#the day the owner chose to get a walk

    #This method inserts the walker's info into a database
	def insertToDb(self):
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		#insert to Dog_walker table the walker details
		sql ="""INSERT INTO Dog_walker(Price_per_day,Max_dog_number_per_day,W_Email,W_City,W_Phone_Number,W_First_name,W_Last_name) 
		VALUES(%s,%s,%s,%s,%s,%s,%s)
		"""
		#execute the info
		cursor.execute( sql,(self.Price_per_day,self.Max_dog_number_per_day,self.W_Email,self.W_City,self.W_Phone_Number,self.W_First_name,self.W_Last_name))
		self.m_DbHandler.commit()
		#insert working days
		for day in self.work_days:
			cursor=self.m_DbHandler.getCursor()
			sql="""INSERT INTO work_days(work_day,W_Email)
				VALUES(%s,%s)
				"""
			cursor.execute( sql,(day,self.W_Email))
			self.m_DbHandler.commit()
		#insert dogs the walker works with
		for dog in self.work_dogs:
			cursor=self.m_DbHandler.getCursor()
			sql="""INSERT INTO work_with(Dog_type_name,W_Email)
			VALUES(%s,%s)
			"""
			cursor.execute( sql,(dog,self.W_Email))
			self.m_DbHandler.commit()
		self.m_DbHandler.disconnectFromDb()
		return

