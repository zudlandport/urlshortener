# urlshortener
Code sample for a bit.ly-like URL shortener / redirect web application, including option for custom redirect text.

![21_0609a SCREENPRINT url shortner](https://user-images.githubusercontent.com/54818691/121521768-71803c80-c9c2-11eb-9387-5ad2cc104304.png)

##  Setup:
Before you can run this application, you will need to install Python and Django, download my code from GitHub, perform 2 command line statements to set up and populate the database, then 1 command line statement to run the Django server.  Here is how I did this:

1. I installed Python and Django locally; this should explain how to do this:
	* [Installing Django](https://docs.djangoproject.com/en/3.0/topics/install/)
	* For example:  I installed Python 3.8.1,
	* and Django 3.0
	* on a Windows 7 machine
1. Download this GitHub code base
1. Then run the Django database migration, to create (and populate where applicable) my application's database tables into Django's built-in database:
	* for example, in Windows with Python installed, open the Command Line, change-directory to the 'urlshortener\urlshortener' folder with its manage.py file, and enter:
	*  `python manage.py makemigrations trackart`
	* then enter:
	*  `python manage.py migrate`
	* this will create the database tables.
1. Next you run the Django server for this Project;
	* for example, in Windows with Python installed, for example, open the Command Line, change-directory to the 'urlshortener\urlshortener' folder with its manage.py file, and enter:
	*  `python manage.py runserver`
1. Then you can see the application running locally at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
