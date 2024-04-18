from flask import Flask
from pymongo import MongoClient
import mysql.connector
import datetime

# connect to MySQL
mysql_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root1234',
    database='DBPROJ',
    auth_plugin='mysql_native_password'
)

# connect to MongoDB
mongo_client = MongoClient('mongodb://localhost:27017')
mongo_db = mongo_client['database_proj']

mysql_cursor = mysql_conn.cursor()

# Create a dictionary to map MySQL data types to MongoDB data types
data_type_mapping = {
'int': 'int',
'bigint': 'int64',
'varchar': 'string',
'text': 'string',
'date' : 'date',
'datetime': 'datetime',
# Add more mappings as needed
}

# Function to create MongoDB collection from MySQL table
def migrate_table(mysql_table_name, mongo_collection_name):
    # mysql_cursor.execute(f"DESCRIBE {mysql_table_name}")
    # mysql_columns = mysql_cursor.fetchall()
    # print(f"mysql_columns -> {mysql_columns}")
    # Check for foreign keys
    mysql_cursor.execute(f"SELECT CONSTRAINT_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME = '{mysql_table_name}' AND CONSTRAINT_NAME != 'PRIMARY'")
    foreign_keys = mysql_cursor.fetchall()
    print(f"foreign_keys -> {foreign_keys}")

    # Create MongoDB collection
    mongo_collection = mongo_db[mongo_collection_name]
    # Migrate data
    # for column in mysql_columns:
    #     # print("column->",column)
    #     column_name = column[0]
    #     data_type = column[1]
    #     # isRequired = column[2] #not null
    #     # isPrimaryCol = column[3]
    #     # default_value = column[4]
    #     # extra = column[5]
    #     mongo_data_type = data_type_mapping.get(data_type, 'string')

    # Create MongoDB documents from MySQL rows

    # mysql_cursor.execute(f"SELECT {column_name} FROM {mysql_table_name}")
    # mongo_documents = [{column_name: row[0]} for row in mysql_cursor.fetchall()]
    # print("mongo_documents",mongo_documents)
    # mongo_collection.insert_many(mongo_documents)

     # # Preserve foreign keys
    for foreign_key in foreign_keys:
        constraint_name, column_name, referenced_table_name, referenced_column_name = foreign_key
        mongo_collection.update_many({}, {'$lookup': {
        'from': referenced_table_name,
        'localField': column_name,
        'foreignField': referenced_column_name,
        'as': column_name
        }})


# document (table) will be created under the database 'test'


mysql_cursor.execute("SHOW TABLES")
tables = mysql_cursor.fetchall()

# loop through each table
for (table_name,) in tables:
    
    mysql_cursor.execute(f"DESCRIBE {table_name}")
    columns = mysql_cursor.fetchall()

    # extract data from MySQL
    mysql_cursor.execute(f"SELECT * FROM {table_name}")
    rows = mysql_cursor.fetchall()
    
    # convert data to MongoDB format
    mongo_collection = mongo_db[table_name]

    for row in rows:
        data = {}
        for i, column in enumerate(columns):
            data[column[0]] = row[i]
            if(isinstance(data[column[0]], datetime.date)):
                date_time = data[column[0]].isoformat()
                data[column[0]] = date_time
        
        try:
            # insert data into MongoDB
            result = mongo_collection.insert_one(data)
            print(f"inserted document with _id: {result.inserted_id}")
            
        except Exception as e:
            print(f"error: {e}")
# for (table_name,) in tables:
#     migrate_table(table_name, table_name)
# Close connections
mysql_conn.close()
mongo_client.close()

app = Flask(__name__)

@app.route("/members")
def members():
    return {"members" : [1,2,3,4]}
if __name__ =="__main__":
        app.run(debug= True)
