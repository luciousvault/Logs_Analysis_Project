# Logs_Analysis_Project
The Logs Analysis project is intended to expand the knowledge base of the student by interacting with sql databases and using virtual machines from a development standpoint. The project uses a fictional PostgreSQL database for imitating a news website. The assignment is to create a python script which answers 3 questions.

#Questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

#Requirements
1. Be a reviewer working for Udacity
2. Know how to setup a vagrant vm
	* Assuming that the virtual machine specified [here](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0) is used when testing. No I'm not even going to attempt to try to walk someone through setting up the vagrant vm
3. Knowledge of PostgreSQL

#Testing
* This project can be setup to be tested as a script against a PostgreSQL db locally or in vagrant vm.

# Quickstart\*
1. Clone https://github.com/luciousvault/Logs_Analysis_Project.git 
2. Unzip the newsdata.sql.zip file
3. Move the 'newsdata.sql' & 'Vagrantfile' to the approprate location for vagrant & postgresql.
	* Not explaining how to setup either the Vagrant vm or PostgreSQL news db.
3. cd into Logs_Analysis_Project/
4. run python3 news_analyzer.py to view the answered question output
	* can also be run by ./news_analyzer.py

\* quickstart was tested using a mac