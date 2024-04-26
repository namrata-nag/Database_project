from pymongo import MongoClient
import mysql.connector
import datetime
import re
from bson.codec_options import CodecOptions

pattern = r'(\w+?)\((.*)\)'
required_mapping={
    'NO': True, #null not allowed
    'YES': False #null  allowed
}

data_type_mapping = {
'int': 'int',
'bigint': 'int64',
'varchar': 'string',
'text': 'string',
'text': 'string',
'enum':'enum',
'date' : 'date',
'datetime': 'datetime',
# Add more mappings as needed
}

key_mapping = {
    'PRI': 'primary_key'
}
extra_mapping = {

}

def migrate(mongo_client, mysql_client, sql_db_name):
    # Connect to MongoDB
    
    mongo_db_name = sql_db_name
    # Check if database exists in MongoDB
    if mongo_db_name in mongo_client.list_database_names():
        print(f"Database '{mongo_db_name}' already exists in MongoDB. Skipping migration.")
        return
    mongo_db = mongo_client[mongo_db_name]
    mysql_client.execute("SHOW TABLES")
    tables = mysql_client.fetchall()
    
    if(len(tables) == 0):
        printf(f"No table exists in the database '{sql_db_name}'. Skipping migration.")
        return
    
    for (table_name,) in tables:
        prop  = {}
        required = []
        mongo_data_type = ""
        mysql_client.execute(f"DESCRIBE {table_name}")
        mysql_columns = mysql_client.fetchall()
        
        for column in mysql_columns:
        
            # print("column->",column)
            column_name = column[0]
            data_type = column[1]
            isRequired = column[2] #not null

            #if a required column i.e null is not allowed then insert into required array
            if(required_mapping[isRequired]):
                required.append(column_name)
            
            #parse datatype of format varchar(*)/text(*)/enum(*)
            matches = re.match(pattern, data_type)
            if matches:
                data_type = matches.group(1)
                value = matches.group(2)
                mongo_data_type = data_type_mapping.get(data_type, 'string')
                if(mongo_data_type != "enum"):
                    prop[column_name] = {
                        "bsonType": mongo_data_type,  
                    }
                else:
                    val = value.split(",")
                    val = [item.strip().strip("'") for item in val]
                    prop[column_name] = {
                        "enum": val
                    }
            else:
                mongo_data_type = data_type_mapping.get(data_type, 'string')
                prop[column_name] = {
                    "bsonType": mongo_data_type,  
                }
            # isPrimaryCol = column[3]
            # default_value = column[4]
            # extra = column[5]
        mysql_client.execute(f"SELECT * FROM {table_name}")
        rows = mysql_client.fetchall()
        
        validator  = {
            "$jsonSchema":{
                "bsonType": "object",
                "required": required,
                "properties": prop
            }  
        }
        
        codec_options = CodecOptions()
        
        mongo_collection = mongo_db.create_collection(table_name, codec_options=codec_options, validator=validator)
        
        for row in rows:
            data = {}
            for i, column in enumerate(mysql_columns):
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
    # Migration logic from SQL to MongoDB
    # Here you would write code to migrate data from SQL to MongoDB
    print(f"Migrating data from SQL database '{sql_db_name}' to MongoDB '{mongo_db_name}'...")
    # Example migration steps:
    # 1. Connect to MySQL database
    # 2. Retrieve data from MySQL tables
    # 3. Insert data into MongoDB collections
    # 4. Close connections

    print("Migration completed successfully.")