#import db_handler module
import db_handler
# import operating system library
import os
#import MYSQLdb library
import MySQLdb
# import logging so we can write messages to the log
import logging
#import users library
from google.appengine.api import users
#import modules
import walker
import dog
import check
#creating a class to get information from the database
class information():
	def __init__(self):#create a dbhandler object
		self.m_DbHandler=db_handler.DbHandler()
	#takes the owner's dogs
	def get_dogs_name(self):
		#take the email of the current user
		user = users.get_current_user()
		email=str(user.email())
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		#this sql query inserts the user's info immidiately when he signs up to the system into the UserDetails table
		sql ="""SELECT Dog.Dog_name FROM Dog WHERE Dog.OR_Email=%s 
		"""
		#execute the info
		cursor.execute( sql,(email,))
		self.m_DbHandler.commit()
		dog_lst=cursor.fetchall()
		#make it to a list that every index is a name of a dog
		new1=str(dog_lst).replace("(", "").replace("'", "").replace(")","").replace(",","")
		new1=new1.split(" ")
		new=[]
		for i in new1:
			new.append(i[1:])
		self.m_DbHandler.disconnectFromDb()
		return new
	#get all the cities that dog walkers sign up with
	def get_cities_name(self):
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		sql=("""SELECT DISTINCT Dog_walker.W_City FROM Dog_walker
		""")
		cursor.execute( sql)
		self.m_DbHandler.commit()
		cities_lst=cursor.fetchall()
		#create the output from the database to a good string
		new1=str(cities_lst).replace("(", "").replace("'", "").replace(")","").replace(",","")
		new1=new1.split(" ")
		new=[]
		#make it to a list that every index is a city
		for i in new1:
			new.append(i[1:])
		self.m_DbHandler.disconnectFromDb()
		return new
	#when the owner wants to pick a walker, he can make some filters, this will handle the filters
	def get_walkers(self,dog,city,day,max_price):
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		#if he want to filter cy the city
		if city:
			#and he want to filter cy the day
			if day:
				#and he want to filter cy the max price
				if max_price:#3 filters: price,walker city,work day
					sql=("""SELECT * FROM Dog_walker join work_days using(W_Email) 
						WHERE Dog_walker.Price_per_day<=%s and work_days.work_day=%s and Dog_walker.W_City=%s
						""")
					cursor.execute( sql,(max_price,day,city,))
				else:#2 filters: walker city,work day
					sql=("""SELECT * FROM Dog_walker join work_days using(W_Email)
						WHERE work_days.work_day=%s and Dog_walker.W_City=%s
						""")
					cursor.execute( sql,(day,city,))
			else:
				if max_price:#2 filters: price, walker city
					sql=("""SELECT * FROM Dog_walker join work_days using(W_Email) 
						WHERE Dog_walker.Price_per_day<=%s and Dog_walker.W_City=%s
						""")
					cursor.execute( sql,(max_price,city,))
				else:#1 filter: walker city
					sql=("""SELECT * FROM Dog_walker join work_days using(W_Email) 
						WHERE Dog_walker.W_City=%s
						""")
					cursor.execute( sql,(city,))
		else:
			if day:
				if max_price:#2 filters: price, work day
					sql=("""SELECT * FROM Dog_walker join work_days using(W_Email) 
						WHERE Dog_walker.Price_per_day<=%s and work_days.work_day=%s
						""")
					cursor.execute( sql,(max_price,day,))
				else:#1 filter: work day
					sql=("""SELECT * FROM Dog_walker join work_days using(W_Email)
						WHERE work_days.work_day=%s
						""")
					cursor.execute( sql,(day,))
			else:
				if max_price:#1 filter: price
					sql=("""SELECT * FROM Dog_walker join work_days using(W_Email) 
						WHERE Dog_walker.Price_per_day<=%s
						""")
					cursor.execute( sql,(max_price,))
				else:#no filters
					sql=("""SELECT * FROM Dog_walker join work_days using(W_Email) 
						""")
					cursor.execute( sql)
		self.m_DbHandler.commit()
		info=cursor.fetchall()
		
		#create a list
		lst=[]
		#organize the information to a list of lists, that every index will be a walker object
		for elem in info:
			#create the output from the database to a good string
			new1=str(elem).replace("(", "").replace("'", "").replace(")","").replace(",","")
			new1=new1.split(" ")
			lst.append(new1)
		new1=[]
		for j in lst:
			new=[]
			for i in j:
				if i[0]=='u':
					new.append(i[1:])
				if i[-1]=='L':
					new.append(i[:-1])
			new1.append(new)
		self.m_DbHandler.disconnectFromDb()
		#create a list
		new2=[]
		#append to the new list all the walkers we get from the data base as a walker object
		for object in new1:
			new_walker=walker.walker()
			new_walker.W_Email=object[0]
			new_walker.Price_per_day=object[1]
			new_walker.Max_dog_number_per_day=object[2]
			new_walker.W_City=object[3]
			new_walker.W_Phone_Number=object[4]
			new_walker.W_First_name=object[5]
			new_walker.W_Last_name=object[6]
			new_walker.work_days=(object[7])
			new2.append(new_walker)
		if len(new2)>0:#if there is a walker in the list
			#return a walker object
			return new2
		else:
			return None
	#when the owner wants to pick a walker, we will show him the walker he chose
	def show_walker(self,email,day=None):
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		#this sql query inserts the user's info immidiately when he signs up to the system into the UserDetails table
		sql=("""SELECT * FROM Dog_walker 
			WHERE Dog_walker.W_Email=%s
		""")
		#execute the info
		cursor.execute( sql,(email,))
		self.m_DbHandler.commit()
		details=cursor.fetchall()
		#convert the information to a list of information about the walker
		for elem in details:
			#create the output from the database to a good string
			new1=str(elem).replace("(", "").replace("'", "").replace(")","").replace(",","")
			new1=new1.split(" ")
		self.m_DbHandler.disconnectFromDb()
		new2=[]
		for i in new1:
			#create the output from the database to a good string
			i=i.replace('(',"").replace(',',"").replace('u',"").replace('L',"").replace("'","")
			new2.append(i)
		#create a walker objects with his attributes
		new_walker=walker.walker()
		new_walker.W_Email=new2[2]
		new_walker.Price_per_day=new2[0]
		new_walker.Max_dog_number_per_day=new2[1]
		new_walker.W_City=new2[3]
		new_walker.W_Phone_Number=new2[4]
		new_walker.W_First_name=new2[5]
		new_walker.W_Last_name=new2[6]
		new_walker.choose_day=str(day)
		return new_walker	
	#return the dog id
	def getdogid(self,o_email,dog_name):
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		#this sql query inserts the user's info immidiately when he signs up to the system into the UserDetails table
		sql=("""SELECT Dog_id FROM Dog 
			WHERE Dog.Dog_name=%s and Dog.OR_Email=%s
		""")
		#execute the info
		cursor.execute( sql,(dog_name,o_email,))
		self.m_DbHandler.commit()
		id=cursor.fetchall()
		#make the information to a string of the id
		id=str(id).replace('((',"").replace('L,),)',"")
		logging.info('the text is'+str(id))
		self.m_DbHandler.disconnectFromDb()
		return id
	#after an owner pick a walker, this function will insert the match to the database
	def insertToDb(self,Dog_id,work_day,W_Email):
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		#this sql query inserts the user's info immidiately when he signs up to the system into the UserDetails table
		sql ="""INSERT INTO walks_on(Dog_id,work_day,W_Email) 
		VALUES(%s,%s,%s)
		"""
		#execute the info
		cursor.execute( sql,(Dog_id,work_day,W_Email,))
		self.m_DbHandler.commit()
		self.m_DbHandler.disconnectFromDb()
		return
	#get the walker customers
	def get_customers(self,email):
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		sql=("""SELECT Dog.Dog_id, Dog.Dog_name,Dog.Gender,Dog.Age,Dog.Dog_type_name,Dog.OR_Email,work_day
			FROM Dog JOIN walks_on USING(Dog_id)
			WHERE walks_on.W_Email=%s
						""")
		cursor.execute( sql,(email,))
		self.m_DbHandler.commit()
		info=cursor.fetchall()
		#convert the information to a list of lists and every indext will be a dog object
		lst=[]
		for elem in info:
			#create the output from the database to a good string
			new1=str(elem).replace("(", "").replace("'", "").replace(")","").replace(",","")
			new1=new1.split(" ")
			lst.append(new1)
		new2=[]
		for j in lst:
			new=[]
			for i in j:
				if i[0]=='u':
					new.append(i[1:])
				if i[-1]=='L':
					new.append(i[:-1])
			new2.append(new)
		self.m_DbHandler.disconnectFromDb()
		#create new list
		new3=[]
		for object in new2:
			#convert to dog objects with his attributes ane append to the new list
			new_dog=dog.dog()
			new_dog.Dog_id=object[0]
			new_dog.Dog_name=object[1]
			new_dog.Gender=object[2]
			new_dog.Age=object[3]
			new_dog.Dog_type_name=object[4]
			new_dog.OR_Email=object[5]
			new_dog.activityday=object[6]
			new3.append(new_dog)

		if len(new3)>0:#if there is a dog
			return new3
		else:
			return 0
	#get the name of the current user
	def get_owner_walker_name(self,email):
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		check_who=check.check()#creating an check object
		if check_who.ownercheck(email):#check if he is a owner
			sql=("""SELECT DISTINCT Owner_regular.O_First_name FROM Owner_regular WHERE Owner_regular.OR_Email=%s
			""")
		elif check_who.walkercheck(email):#check if he is a walker
			sql=("""SELECT DISTINCT Dog_walker.W_First_name FROM Dog_walker WHERE Dog_walker.W_Email=%s
			""")
		cursor.execute(sql,(email,))
		self.m_DbHandler.commit()
		name=cursor.fetchall()
		#create the output from the database to a good string
		name=str(name).replace("(", "").replace("'", "").replace(")","").replace(",","")
		if name[0]=='u':
			name=name[1:]
		self.m_DbHandler.disconnectFromDb()
		return name
	#get the orders of the owner user
	def get_orders(self,email):
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		sql=("""SELECT Dog.Dog_id, Dog.Dog_name,Dog.Dog_type_name,work_day,W_Email
			FROM Dog JOIN walks_on USING(Dog_id)
			WHERE Dog.OR_Email=%s
						""")
		cursor.execute( sql,(email,))
		self.m_DbHandler.commit()
		info=cursor.fetchall()
		#convert the information to a list of lists 
		lst=[]
		for elem in info:
			#create the output from the database to a good string
			new1=str(elem).replace("(", "").replace("'", "").replace(")","").replace(",","")
			new1=new1.split(" ")
			lst.append(new1)
		new2=[]
		for j in lst:
			new=[]
			for i in j:
				if i[0]=='u':
					new.append(i[1:])
				if i[-1]=='L':
					new.append(i[:-1])
			new2.append(new)
		self.m_DbHandler.disconnectFromDb()
		#create new list
		new3=[]
		for object in new2:
			#convert to list of lists, in each list there will be the following parameters
			dogi=[]
			dogi.append(object[0])
			dogi.append(object[1])
			dogi.append(object[2])
			dogi.append(object[3])
			dogi.append(object[4])
			new3.append(dogi)
		#if there is one order at least
		if len(new3)>0:
			return new3
		else:
			return None
#get all the dogs for the current user
	def get_all_dogs(self,email):
	#take the email of the current user

		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		#this sql query inserts the user's info immidiately when he signs up to the system into the UserDetails table
		sql ="""SELECT * FROM Dog WHERE Dog.OR_Email=%s 
		"""
		#execute the info
		cursor.execute( sql,(email,))
		self.m_DbHandler.commit()
		dog_lst=cursor.fetchall()
	
		lst=[]
		#organize the information to a list of lists, that every index will be a walker object
		for elem in dog_lst:
			#create the output from the database to a good string
			new1=str(elem).replace("(", "").replace("'", "").replace(")","").replace(",","")
			new1=new1.split(" ")
			lst.append(new1)
		new1=[]
		for j in lst:
			new=[]
			for i in j:
				if i[0]=='u':
					new.append(i[1:])
				if i[-1]=='L':
					new.append(i[:-1])
			new1.append(new)
		self.m_DbHandler.disconnectFromDb()
		#create a list
		new2=[]
		#append to the new list all the walkers we get from the data base as a walker object
		for object in new1:
			new_dog=dog.dog()
			new_dog.Dog_id=object[0]
			new_dog.Dog_name=object[1]
			new_dog.Gender=object[2]
			new_dog.Age=object[3]
			new_dog.Dog_type_name=object[4]
			new_dog.Or_Email=object[5]
			new2.append(new_dog)
		return new2
