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
import get_information
#create a function that will return a list of distinct walkers in our system
def show():
	#use get_walkers func from get_information to get all walkers
	info=get_information.information()
	all_walkers=info.get_walkers(None,None,None,None)
	lst=[]
	mail_lst=[]
	#making a list of walkers that the work_days will be a day list
	for walker in all_walkers:
		if walker.W_Email not in mail_lst:
			mail_lst.append(walker.W_Email)
			walker.work_days=[walker.work_days]
			lst.append(walker)
		else:#walker is in the new list
			for second_walker in lst:#find the walker in our new list and append to his work days the new day
				if second_walker.W_Email==walker.W_Email:
					second_walker.work_days.append(walker.work_days)
	return lst

