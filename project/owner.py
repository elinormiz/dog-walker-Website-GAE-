# import logging so we can write messages to the log
import logging
# import the class DbHandler to interact with the database
import db_handler
#import users library
from google.appengine.api import users
#import date library
from datetime import date
#create an object- owner
class owner():
	def __init__(self):
		self.m_DbHandler=db_handler.DbHandler()
		self.Monthly_commission=80#not relevent to the site
		# create data members of the class owner
		self.O_Date_of_registration= date.today()
		self.O_City = ""
		self.O_Phone_nubmer = ""
		self.O_Last_name= ""
		self.O_First_name = ""
		self.OR_Email = ""

    #This method inserts the owner's info into a database
	def insertToDb(self):
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		#this sql query inserts the owner's info immidiately when he signs up to the system into the UserDetails table
		sql ="""INSERT INTO Owner_regular(Monthly_commission,O_Date_of_registration,O_City,O_Phone_number,O_Last_name,O_First_name,OR_Email) 
		VALUES(80,sysdate(),%s,%s,%s,%s,%s)
		"""
		#execute the info
		cursor.execute( sql,(self.O_City,self.O_Phone_nubmer,self.O_Last_name,self.O_First_name,self.OR_Email))
		self.m_DbHandler.commit()
		self.m_DbHandler.disconnectFromDb()
		return

