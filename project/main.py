# ------------------------------------------------------
# Dog Walkers-Project02
# ------------------------------------------------------
# Description:  This app will  create a site for dog walkers and dog owners.
# Authors:  Elinor Mizrahi, Tal Zohar, Matan Porcilan
# Last updated: 12.01.19
# ------------------------------------------------------

# import webapp2  - Python web framework compatible with Google App Engine
import webapp2
#import jinja and os libraries
import jinja2
# import operating system library
import os
#import users library
from google.appengine.api import users
# import logging so we can write messages to the log
import logging
#import our modules:
import owner
import walker
import dog
import get_information
import check
import func
#Load jinja
jinja_environment = jinja2.Environment(	loader=
										jinja2.FileSystemLoader(os.path.dirname(__file__)))
# ---------------------------------------------------------------------------------
# Main_login- user will see this page if he is not login to google account
# ---------------------------------------------------------------------------------
class Main_login(webapp2.RequestHandler):
	# When we receive an HTTP GET request - display the "home page" 
	def get(self):
		user = users.get_current_user()
		if user:#user is a member of our site
			self.redirect('/mainpage')
		else:#new user
        # Creat a template object
			template = jinja_environment.get_template('main_login.html')
		#Creating an HTML page and response
			self.response.write(template.render())
# ---------------------------------------------------------------------------------
# Main_page- user will see this page if he is not register to our site
# ---------------------------------------------------------------------------------
class Main_page(webapp2.RequestHandler):

    # When we receive an HTTP GET request - display the "home page" 
	def get(self):
		email = users.get_current_user().email()
		k=check.check()#creating an check object
		if k.walkercheck(email):#check if he is a walker
			self.redirect('/home_walker')
		elif k.ownercheck(email):#check if he is an owner
        # Creat a template object
			self.redirect('/home_owner')
		else:#not owner and not walker so he will sign up in the main_page
			template = jinja_environment.get_template('main_page.html')
		#Creating an HTML page and response
			self.response.write(template.render())
# ---------------------------------------------------------------------------------
# Walker- user will see this page if he want to register to our site as a dog walker
# ---------------------------------------------------------------------------------
class Walker(webapp2.RequestHandler):
 # When we receive an HTTP GET request - analyze and save parameters  and send them to the 'get_inputs_walker.html'
    def get(self):
	# Creat a template object
		template = jinja_environment.get_template('get_inputs_walker.html')
		#Creating an HTML page and response
		self.response.write(template.render())
# ---------------------------------------------------------------------------------
# home_walker- user will see this page if he register to our site as a dog walker
# ---------------------------------------------------------------------------------
class home_walker(webapp2.RequestHandler):
 # When we receive an HTTP GET request - analyze and save parameters  and send them to the 'walker.html'
    def get(self):
		#get the email of the user so we can know his name from the data base
		user = users.get_current_user()
		email=user.email()
		info=get_information.information()
		#use the function to get the walker's name
		walker=info.get_owner_walker_name(email)
		parameters_for_template={'name':walker}
		# Creat a template object
		template = jinja_environment.get_template('walker.html')
		#Creating an HTML page and response
		self.response.write(template.render(parameters_for_template))		
# ---------------------------------------------------------------------------------
# Owner- user will see this page if he want to register to our site as a dog owner
# ---------------------------------------------------------------------------------
class Owner(webapp2.RequestHandler):
 # When we receive an HTTP GET request - analyze and save parameters  and send them to the 'get_inputs_owner.html'
    def get(self):
# Creat a template object
		template = jinja_environment.get_template('get_inputs_owner.html')
		#Creating an HTML page and response
		self.response.write(template.render())
# ---------------------------------------------------------------------------------
# home_owner- user will see this page if he register to our site as a dog owner
# ---------------------------------------------------------------------------------
class home_owner(webapp2.RequestHandler):
 # When we receive an HTTP GET request - analyze and save parameters  and send them to the 'owner.html'
    def get(self):
		#get the email of the user so we can know his name from the data base
		user = users.get_current_user()
		email=user.email()
		info=get_information.information()
		#use the function to get the owner's name
		owner=info.get_owner_walker_name(email)
		parameters_for_template={'name':owner}
		# Creat a template object
		template = jinja_environment.get_template('owner.html')
		#Creating an HTML page and response
		self.response.write(template.render(parameters_for_template))
# ---------------------------------------------------------------------------------
# info_dog- this class will insert the dog of the current user to the data base
# ---------------------------------------------------------------------------------
class info_dog(webapp2.RequestHandler):
 # When we receive an HTTP GET request - analyze and save parameters  and send them to the 'owner.html'
    def post(self):
		#get the email of the user so we can know his email to the data base
		user = users.get_current_user()
		email=user.email()
		#creating a new dog object
		new_dog=dog.dog()
		new_dog.Dog_name=self.request.get('dogname')
		new_dog.Gender=self.request.get('gender')
		new_dog.Age=self.request.get('age')
		new_dog.Dog_type_name=self.request.get('Dogtype')
		new_dog.OR_Email=email
		#insert the dog to the data base
		new_dog.insertToDb()
		#show the owner his owner page after he finished
		# take the user back to his home page
		self.redirect('/home_owner')
# ---------------------------------------------------------------------------------
# info_owner- this class will insert the owner to the data base
# ---------------------------------------------------------------------------------		
class info_owner(webapp2.RequestHandler):
 # When we receive an HTTP GET request - analyze and save parameters  and send them to the 'owner.html'
    def post(self):
		#creating an owner object
		new_owner=owner.owner()
		new_owner.O_City=self.request.get('City')
		new_owner.O_Phone_nubmer=self.request.get('phonenumber')
		new_owner.O_Last_name=self.request.get('lname')
		new_owner.O_First_name=self.request.get('fname')
		new_owner.OR_Email=self.request.get('email')
		#insert the owner object to the database
		new_owner.insertToDb()
		#show the owner his owner page after he finished
		# Creat a template object
		template = jinja_environment.get_template('owner.html')
		#send to the html parameters in dictionary
		parameters_for_template={'name':new_owner.O_First_name}
		#Creating an HTML page and response
		self.response.write(template.render(parameters_for_template))		
# ---------------------------------------------------------------------------------
# info_walker- this class will insert the walker to the data base
# ---------------------------------------------------------------------------------	
class info_walker(webapp2.RequestHandler):
 # When we receive an HTTP GET request - analyze and save parameters  and send them to the 'walker.html'
    def post(self):
		#creating a walker object
		new_walker=walker.walker()
		new_walker.Price_per_day=self.request.get('price')
		new_walker.Max_dog_number_per_day= self.request.get('maxdogs')
		new_walker.W_Email = self.request.get('email')
		new_walker.W_City = self.request.get('city')
		new_walker.W_Phone_Number= self.request.get('phonenumber')
		new_walker.W_First_name = self.request.get('fname')
		new_walker.W_Last_name = self.request.get('lname')
		#checking the days the walker marked he works at
		day_lst=['day1','day2','day3','day4','day5','day6','day7']
		for day in day_lst:
			if self.request.get(day):
				new_walker.work_days.append(self.request.get(day))
		#checking the dogs the walker marked he works with
		dog_lst=['type1','type2','type3','type4','type5','type6','type7','type8']
		for dog in dog_lst:
			if self.request.get(dog):
				new_walker.work_dogs.append(self.request.get(dog))
		#if there is no days selected so he chose all the days
		if len(new_walker.work_days)==0:
			new_walker.work_days=["sunday","monday","tuesday","wednesday","thursday","friday","saturday"]
		#if there is no types selected so he chose all the types
		if len(new_walker.work_dogs)==0:
			new_walker.work_dogs=["labrador","french_Bulldog","pug","poodle","shih_tzu","golden_retriever","pomeranian","chihuahua"]
		#insert the new walker to the database
		new_walker.insertToDb()
		#send to the html parameters in dictionary
		parameters_for_template={'name':new_walker.W_First_name}
		# Creat a template object
		template = jinja_environment.get_template('walker.html')
		#Creating an HTML page and response
		self.response.write(template.render(parameters_for_template))
# ---------------------------------------------------------------------------------
# info_order- this class will show the choice of the selected walker
# ---------------------------------------------------------------------------------	
class info_order(webapp2.RequestHandler):
 # When we receive an HTTP GET request - analyze and save parameters  and send them to the right html
    def post(self):
		#get the dog id from the query
		dog_id=self.request.get('dog_id') 
		#get the walker's details from the query
		W_details=self.request.get('walker_details')
		W_details=W_details.split(',')
		W_email=W_details[0]
		work_day=W_details[1]
		#get the currtent user's email for checking errors
		o_email=users.get_current_user().email()
		k=check.check()
		if k.errorcheck(dog_id,work_day,W_email):#they chose this combination
			# Creat a template object
			template = jinja_environment.get_template('error.html')
			#Creating an HTML page and response
			self.response.write(template.render())
		else:
			info1=get_information.information()
			logging.info("hahaha"+str(W_details))
			k2=check.check()
			info=get_information.information()
			#get the max_dogs per day of the walker
			max_days=info.show_walker(W_email).Max_dog_number_per_day
			#take the number of trips the walker has for this day
			place=k2.enough_place(work_day,W_email)
			if int(place)<int(max_days):#there is a place for the dog
				info1.insertToDb(dog_id,work_day,W_email)
				#Creating an HTML page and response
				info2=get_information.information()
				walker=info2.show_walker(W_email,work_day)
				# Creat a template object
				template = jinja_environment.get_template('show_walker.html')
				#send to the html parameters in dictionary
				parameters_for_template={'walker':walker}
				#Creating an HTML page and response
				self.response.write(template.render(parameters_for_template))
			else:#there is no place for this day
				# Creat a template object
				template = jinja_environment.get_template('no_place_error.html')
				#Creating an HTML page and response
				self.response.write(template.render())
# ---------------------------------------------------------------------------------
# my_customers- this class will show to the walker who choose him
# ---------------------------------------------------------------------------------	
class my_customers(webapp2.RequestHandler):
 # When we receive an HTTP GET request - analyze and save parameters  and send them to the 'walker_customers.html'
    def get(self):
		#get the email of the user so we can know who to look for in the data base
		email=users.get_current_user().email()
		info=get_information.information()
		#use the function to get the walkers customers
		customers=info.get_customers(email)
		if customers==0:
			# Creat a template object
			template = jinja_environment.get_template('no_customers.html')
			#Creating an HTML page and response
			self.response.write(template.render())
		#send to the html parameters in dictionary
		else:
			parameters_for_template={'dogs':customers}
			# Creat a template object
			template = jinja_environment.get_template('walker_customers.html')
			#Creating an HTML page and response
			self.response.write(template.render(parameters_for_template))
# ---------------------------------------------------------------------------------
# my_customers- this class will show to the owner the walker he chose 
# ---------------------------------------------------------------------------------	
class my_orders(webapp2.RequestHandler):
 # When we receive an HTTP GET request - analyze and save parameters  and send them to the 'Owner_order.html'
    def get(self):
		#get the email of the user so we can know who to look for in the data base
		email=users.get_current_user().email()
		info=get_information.information()
		#use the function to get the walkers customers
		order=info.get_orders(email)
		#if there is at least one order
		if order:
			#send to the html parameters in dictionary
			parameters_for_template={'order':order}
			# Creat a template object
			template = jinja_environment.get_template('Owner_order.html')
			#Creating an HTML page and response
			self.response.write(template.render(parameters_for_template))
		#if there is no orders for this user
		else:
			# Creat a template object
			template = jinja_environment.get_template('no_order.html')
			#Creating an HTML page and response
			self.response.write(template.render())
# ---------------------------------------------------------------------------------
# add_dog- this class will show to the owner a form- where he can add a new dog to the database and to see his dogs
# ---------------------------------------------------------------------------------
class add_dog(webapp2.RequestHandler):
 # When we receive an HTTP GET request - analyze and save parameters  and send them to the 'add_dog.html'
    def get(self):
		#take the email of the current user for sql
		user = users.get_current_user()
		email=user.email()
		#create 1 object of information
		info1=get_information.information()
		dogs=info1.get_all_dogs(email)
		if dogs!=None:
			len_dogs=len(dogs)
		else:
			len_dogs=0
		#send to the html parameters in dictionary
		parameters_for_template={'dogs':dogs, 'leng':len_dogs}
		# Creat a template object
		template = jinja_environment.get_template('add_dog.html')
		#Creating an HTML page and response
		self.response.write(template.render(parameters_for_template))			
# ---------------------------------------------------------------------------------
# add_order- this class will show to the owner a form- where he can choose the dog that he want to order for him a trip
# ---------------------------------------------------------------------------------
class add_order(webapp2.RequestHandler):
 # When we receive an HTTP GET request - analyze and save parameters  and send them to the 'add_order.html'
    def get(self):
		#create 1 object of information
		info1=get_information.information()
		#takes the dog's name
		dog_name=info1.get_dogs_name()
		#if there is not a dog in the system for the current user
		if dog_name==['']:
			template = jinja_environment.get_template('dog_error.html')
			self.response.write(template.render())
		#if there is a dog in the system for the current user
		else:
			#send to the html parameters in dictionary
			parameters_for_template={'dogs':dog_name}
			# Creat a template object
			template = jinja_environment.get_template('add_order.html')
			#Creating an HTML page and response
			self.response.write(template.render(parameters_for_template))
			
# ---------------------------------------------------------------------------------
# add_order2- this class will show to the owner all of the walkers that he can choose
# ---------------------------------------------------------------------------------
class add_order2(webapp2.RequestHandler):
 # When we receive an HTTP GET request - analyze and save parameters  and send them to the right html
    def post(self):
		#get the current user's email for the "getdogid" function
		email=users.get_current_user().email()
		#take the dog name
		dog=self.request.get('Mydog')
		#if the owner chose a dog
		if dog:
			city=self.request.get('City')
			day= self.request.get('day')
			max_price = self.request.get('price')
			#create 2 objects of information
			info1=get_information.information()
			info2=get_information.information()
			#get the dor id
			dog_id=info2.getdogid(email,dog)
			#get the walkers after the filter
			para=info1.get_walkers(dog,city,day,max_price)
			#if there is no filtering that matches the requirements
			if para==None:
				# Creat a template object
				template = jinja_environment.get_template('cant_filter.html')
				#Creating an HTML page and response
				self.response.write(template.render())
			else:
				#send to the html parameters in dictionary
				parameters_for_template={'info':para, 'dog_id':dog_id,'owner_email':email,'dog_name':dog}
				# Creat a template object
				template = jinja_environment.get_template('walker_options.html')
				#Creating an HTML page and response
				self.response.write(template.render(parameters_for_template))
		else:#owner didn't pick a dog
			# Creat a template object
			template = jinja_environment.get_template('dog_error.html')
			#Creating an HTML page and response
			self.response.write(template.render())
# ---------------------------------------------------------------------------------
# AboutUs- user will see this page if he want to know more about us
# ---------------------------------------------------------------------------------
class AboutUs(webapp2.RequestHandler):
    # When we receive an HTTP GET request - display the "about us" 
    def get(self):
        # Creat a template object
		template = jinja_environment.get_template('about.html')
		#Creating an HTML page and response
		self.response.write(template.render())
# ---------------------------------------------------------------------------------
# ContactUs- user will see this page if he want to know how to contact with us
# ---------------------------------------------------------------------------------
class ContactUs(webapp2.RequestHandler):
    # When we receive an HTTP GET request - display the "Contuct us" 
    def get(self):
        # Creat a template object
		template = jinja_environment.get_template('contact.html')
		#Creating an HTML page and response
		self.response.write(template.render())
# ---------------------------------------------------------------------------------
# ContactUs- user could see all the walkers in our site
# ---------------------------------------------------------------------------------
class all_walkers(webapp2.RequestHandler):
 # When we receive an HTTP GET request - analyze and save parameters  and send them to the right html
    def get(self):
		#create all_walkers object
		para=func.show()
		#send to the html parameters in dictionary
		parameters_for_template={'info':para}
			# Creat a template object
		template = jinja_environment.get_template('all_walkers.html')
			#Creating an HTML page and response
		self.response.write(template.render(parameters_for_template))
		
# ---------------------------------------------------------------------------------
# class to login to the google account if the user is not login
# and show the status afterwards
# Handles /login
# ---------------------------------------------------------------------------------
class Login(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()  
        # if the user object exists (the user is logged in to google)
        if user:
            self.redirect('/mainpage')
        # The user object doesn't exist ( the user is not logged to google)
        # we will ask him to login and
        # provide the URI of the show_status page, to display the status afterwards
        else:      
            # force the user to login 
            self.redirect(users.create_login_url('/mainpage'))
# ---------------------------------------------------------------------------------
# class to logout from the google account if the user is not logout
# and show the status afterwards
# Handles /logout 
# ---------------------------------------------------------------------------------
class Logout(webapp2.RequestHandler):
    def get(self):
        # if the user is logged in - we will perform log out
        user = users.get_current_user()
        if user:
            # force the user to logout and redirect him afterward to 
            # show_status page, to display the status afterwards
            self.redirect(users.create_logout_url('/mainlogin'))

        else:

            self.redirect('/mainlogin')
# ---------------------------------------------------------------------------------
#app is the aplication for all the url that exists in our system
# ---------------------------------------------------------------------------------
app = webapp2.WSGIApplication([	('/info_order',      info_order),
								('/add_order2',      add_order2),
								('/all_walkers',     all_walkers),
								('/my_customers',    my_customers),
								('/home_walker',     home_walker),
								('/home_owner',      home_owner),
								('/add_order',       add_order),
								('/my_orders',       my_orders),
								('/add_dog',         add_dog),
								('/info_dog',        info_dog),
								('/info_walker',     info_walker),
								('/info_owner',      info_owner),
								('/mainlogin',       Main_login),
								('/mainpage',        Main_page),
								('/register_walker', Walker),
								('/register_owner',  Owner),
								('/aboutus',         AboutUs),
								('/contact',         ContactUs),
                               ('/login',            Login),
                               ('/logout',           Logout),
								('/.*',              Main_login)],
								debug=True)
