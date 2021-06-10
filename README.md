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
	*  `python manage.py makemigrations writeandfwd`
	* then enter:
	*  `python manage.py migrate`
	* this will create the database tables.
1. Next you run the Django server for this Project;
	* for example, in Windows with Python installed, for example, open the Command Line, change-directory to the 'urlshortener\urlshortener' folder with its manage.py file, and enter:
	*  `python manage.py runserver`
1. Then you can see the application running locally at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)



## Design Decisions - Challenges:

The biggest challenge was that 2 elements of this assignment included significant ramp-up time for me, one of which I overcame (though my overall assignment completion time was closer to 10 hours than 4 hours -- I will have a branch that marks my initial uploaded after 5.25 hour progress, which shows architecture but has no Module implementation yet) and the other of which I did not.


Challenge 1 was that the completed product had to be encapsulated in GitHub; that meant I would either have to,

A) use Python/Django, which is a language and framework I have installed locally and uploaded to GitHub before, but which I have only written one project in before.

B) or if I used my go-to server-side language, PHP, I would have to learn how to run it and a database locally.

I went with (A), as I want to spend more time increasing my Python/Django fluency.


Challenge 2 was that I've never worked with JSON API before; if I finished the application in time, I hoped to learn enough to replace the standard HTTP interface with a JSON API, but I didn't have the time.



### Tests of Less Obvious Functionality:

-Go to "Add a URL", add the same URL twice (it will only create a shortened URL once, so the 2nd+ time you try, it will take you to the existing record -- ie the first Random Forwarding String)

-Go to "Show All URLs", follow a forwarding URL, click "Fwding Count" to see that your hit was tracked / further drilldown to see the hit-by-day count

-Create a Custom Forwarder; repeat with multiple Custom Forwarders that all point at the same webpage


### Branches:
I will (shortly) be creating a `After 5.25 hours` branch on GitHub, if that's of use, before I merge my final-version changes into the main branch.


## Design Decisions - Cool Stuff:

### Cool Thing 1 - Random Forwarding String saved as Integer (not implemented):

The coolest thing I planned but didn't end up implementing was my idea about storing the "Random Forwarding Url String" in the database as an Integer, which gets translated to a base-64 string for the user.  This idea was rooted in my (perhaps obsolete) impression that repeatedly querying a database table based on an Integer is more efficient than querying based on a varchar.  (I'm not sure if this is obsolete with the more abstracted Database nature of frameworks like Django).  When it became apparent I was going to be over 4 hours, and the translation of an integer to/from a base-64 string might take me 20-90 minutes, I abandoned this idea.  (There were several cool corollary ideas -- like, we know many Custom Forwarding Strings are not Random Strings if they are longer than Random Strings can possibly be; and if Customs are shorter, we store them in the database's Int field as if they were random -- so we're never querying the database Twice to find our lookup).


### Cool Thing 2 - Random Forwarding String generation / a bit about Custom Strings

It's a six-character base-64 string; meaning there are 68 million possible random URLs (64 ^ 6).  All the work about its generation is encapsulated in `\urlshortener\writeandfwd\fushelper.py`  (FUS = Forwarding Url String).

How it represents a Base-64 string is a little hacky / a little straightforward; different areas of numbers are mapped to either 0-9, or A-Z, or a-z, or the characters - and _ (the 64 characters that YouTube uses for its random generations, so they're URL-friendly).

Also it takes 5 tries at generating an unused Forwarding String, in case the random number generator is so poorly-randomized (or the number of URLs created is so vast) that it rolls the same 6 numbers again and hits an already-used combination from those 68 million possibilities.  (Obviously if it really starts filling up, you'd want to do something other than rerolling -- though the standard 'when even near filling up, exponentially increase it' approach should be fine:  track when you have 34 million rows and then go from six-character strings to seven-character strings).

The Customer Forwarding Strings are saved in the same space as the Random ones, so all URL Forwarding actions are querying the same field (though there's a boolean field that stores whether or not they were randomly generated).  A concern is that Custom Forwarding Strings ARE case-sensitive\* -- something that Custom Forwarding String creators must be aware of to use this application.  (\*: or, are as case-sensitive as the server behind the application, anyway... if the server is NOT case sensitive, my program will break on that faultline (forwarding URLs distinct only by case will clobber each other)).


### Cool Thing 3 - Hit Tracking

Forwardings are tracked by inserting a row into its hit-tracker database each time a forwarding link is used, storing the Link and the time.  This is more robust for heavy usage than incrementing 1 row in a database.  It also allows actual "# of hits per link per day" counts, rather than just "average hits per day since the forwarder was created".

Also, knowing the granularity of reporting that is required -- # per day in this case -- lets us expand the application by doing regular 'cleanups' of the Hit Tracking table -- turning the Hit Tracking table into a "live data only" table, and flushing condensed versions of it into another table on a regular basis (for example, a table whose rows are Forwarder, Day, # of Hits Total On That Day).



### Plan / Design Documentation:

This repository includes 3 non-code documents:

I included my 2 planning documents I created during my first 30-45 minutes of thinking about the project:

`21_0608a Build Outline Plan.txt`  -- my overall project estimate

`12_0608c App Plan.txt`  -- where I jotted down an outline of the endpoints / functionality


I also included my basic time-tracking, broken down by task:
`21_0608b time tracking.txt`
