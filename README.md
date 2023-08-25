# sqlalchemy-challenge
Challenge for Module 10

This repository contains the files for the Module 10 assignmnent. 

The SurfsUp folder contains the Jupyter Notebook file used to perform the data queries in pythin and the Python file used to create the Flask web framework. 
The resources folder contains the original CSV files and the sqlite file used for analysis. 

Additional Notes:
In the Jupyter Notebook file when running some of the filter queries, the program would treat ">=" and "<=" as ">" and "<" respectively. I'm not sure why it did this, but as a work around, I added / subrtacted extra days and used ">" and "<" on some filters. This probably looks clunky but it was the only way I could get the correct outputs. 

Some of that >, < logic is in the App.py file as well, but on later code sections in the py file, the >= and =< worked correctly. 

For the station pull in the flask portion of the assignmnet, the assignment did not specify if it wanted you to pull the name, the ID or both. I opted for just the name since that was the most user friendly.

The assignment also mentioned needing to perform a join for some of the work with Flask. Based on the assignment asks, this did not seem necessary and I wonder if that hint was left over from a previous version of the assignmnet. I was able to perform all the required pulls using only one or the other databases. 
