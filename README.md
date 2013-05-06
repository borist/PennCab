PennCab
=======

A web application to help students coordinate cab rides with each other.

Application is live at: [http://penncab.herokuapp.com/cabrides/](http://penncab.herokuapp.com/cabrides/)

Running The Project
-------------------

To run the project, you must:

+ Download and install all of the modules in "requirements.txt"
+ Create a (local or server-side) postgresql database named "penncab"
+ Enter your database credentials in `penncab/penncab/settings.py` in the `DATABASES` dictionary
+ To Run locally:
  - Comment out the last 4 lines in `penncab/penncab/settings.py`
  - Run the command `python penncab/manage.py runserver` or use heroku's `foreman start`

Using The App
-------------
+ Most private data is hidden unless signed in with a valid account
+ You must provide a `*.upenn.edu` to sign up to use the app
+ You can create a cab from any origin to any destination for any date and time in the future
  - Also specify the maximum number of passengers for the cab
+ You can join any cab ride that has capacity that you do not own and are not already a passenger of
  - Only once you're a participant in a cab ride will you be able to see other participants' phone numbers
+ You can leave a cab ride at any time if you are not the owner
  - You can delete a cab ride at any time that you are the owner of

Features
--------
+ Private data is hidden if user is not signed in
+ Phone numbers are not shared unless user is a participant of the cab ride
+ You can view additional drop-down information of any cab ride that includes:
  - A map of the shortest route of the cab ride
  - Distance of the shortest route
  - Estimated time for the cab ride based on the shortest route
+ You can search for any cab ride by destination
+ You can filter out and view only cab rides that you are a participant (and/or owner) of
+ Full cab rides are "greyed out" for easy recognition
+ Only cab rides that have **yet to occur** are displayed
+ Nice HTML/CSS errror handling for signup if using incorrect email address or non-matching passwords

Planned Features Moving Forward
-------------------------------
+ Add estimated taxi cab fare using third party API
+ Email notifications/reminders of cab rides
+ Better origin/destination address recognition
+ Ability to share cab rides (i.e. on Facebook, Twitter, etc)
