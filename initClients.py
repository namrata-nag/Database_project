from pymongo import MongoClient
import mysql.connector
mongo_client=None
def initiate():
    mysql_client = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1234',
        database='DBPROJ',
        auth_plugin='mysql_native_password'
    )
    mongo_client = MongoClient('mongodb://localhost:27017')
    return mongo_client, mysql_client
     



# connect to MongoDB

