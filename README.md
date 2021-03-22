# Content-Management-System
CMS using Python Flask Framework

Steps for project setup and and running 

1. Please make sure following libraries are installed in a virtual environment:
	Steps to install a virtual environment
	1. $ python -m venv venv
	2. To activate a virtual environment 
		if Unix-based operating system
		$ source venv/bin/activate
		(venv) $ _

		if you are using Windows 
		$ venv\Scripts\activate
		(venv) $ _
	Your main directory should contain venv,project folders and flaskenv,run,README files
	3. Install the following packages
	
		Flask              1.1.2
		Flask-SQLAlchemy   2.5.1	
		PyJWT              2.0.1
		python-dotenv      0.15.0	
		SQLAlchemy         1.4.2

2. Type "flask run" in the terminal to start the development server.
3. Create a database (if database not present)
	..\project>python
	>>> from project import db
	>>> from project.models import Content
	>>> db.create_all()

4. Use Postman to check the Api Endpoints. 

Here are some the API Endpoints I have created along with the request body format and the headers required -

1. /signup (POST)
	request body = {
		    "email":"",	
		    "password":"",
		    "full_name":"",
		    "phone_number":"",
		    "address":"",
		    "city":"",
		    "state":"",
		    "country":"",
		    "admin":""
		}
 	Make sure that admin field is a Boolean field, hence enter true or false
	Create two users with different email.
	{
    		"email":"abc@abc.com",
    		"password":"testing123",
    		"full_name":"Test normal User",
    		"phone_number":"235489845",
    		"address":" Test Address",
    		"city":" Test city",
    		"state":" Test state",
    		"country":" Test country",
    		"admin":false
	}
	and 
	{
    		"email":"abc1@abc.com",
    		"password":"testing123",
    		"full_name":"Test admin User",
    		"phone_number":"235489845",
    		"address":" Test Address",
    		"city":" Test city",
    		"state":" Test state",
    		"country":" Test country",
    		"admin":true
	}

2. /signup (GET)
3. /login (GET)
	set Authorisation to basic auth and enter the credentials of user. It will generate a token(copy the token for further use)
4. /logout (GET)
	set the headers as 
	key = x-access-token : value = generated token
5.  /content (POST)
	request body = {
		    "title":"",	
		    "body":"",
		    "summary":""		    
		}
	set the headers as 
	key = x-access-token : value = generated token
6. /content (GET)
	set the headers as 
	key = x-access-token : value = generated token

7. /content/id (GET)
	url example = /content/2
	set the headers as 
	key = x-access-token : value = generated token
8. /content/id (DELETE)
	url example = /content/2
	set the headers as 
	key = x-access-token : value = generated token
9. /content/id (PUT)
	to edit a content
	url example = /content/2
	set the headers as 
	key = x-access-token : value = generated token
10. /content/search (GET)	
	request body = {
		    "search":" a keyword to search"		    
		}
	