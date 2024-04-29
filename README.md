# Database_project

# TechStack
- python 3
- MongoDB
- MySQL

# Database
- To create the mySQL database you can run `w3schools.sql` file in your workbench.

# Step to install locally
$ source venv/bin/activate to activate the python env
$ pip install mysql.connector, MongoClient, CodecOptions, re, datetime

# Run Server
The serever will ask user input. There are 4 function that has been exposed. Below is how you can use the exposed function : 
- migrate "Db_Name"
- selectQuery "sql_statement"
- inserQuery "sql_statement"
- joinQuery "sql_statement"

Each exposed function will take a sql statement in string format wrapped in double quotes. Make sure to keep table name in lowercase as mongo saves collection in lowercase.


