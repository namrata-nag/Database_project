from initClients import initiate
from db_migrator import selectQuery, insertQuery, migrate
import re

import sys
pattern = r'(\w+)\s+"([^"]+)"'

def main():
    mongo_client, mysql_client = initiate()
    mysql_cursor = mysql_client.cursor()
    print("This app is to run the migration package in command line mode. DB Migrattion package exposes three function. For the ussage please follow readme.")
    print("1. selectQuery - It parses the select sql query to noSQL query and return the result after reading data from Mongo")
    print("2. insertQuery - It parses the insert sql query to noSQL query and insert the value")
    print("3. migrate - It will migrate the MySQL database to MongoDB.")
    print("Type your command...")
    while True:
        command = input("$")
        if command == "exit":
            break
        print("You entered:", command)
        print("mongo_client",mongo_client)
        match = re.match(pattern, command)
        if match:
            command = match.group(1)
            input_param = match.group(2)
            print("Command:", command)
            print("Input Param:", input_param)
            if(command == 'migrate'):
                migrate(mongo_client, mysql_cursor, input_param)
            elif(command == 'selectQuery'):
                mongo_db = mongo_client['DBPROJ']
                results = selectQuery(input_param, mongo_db)
                result_final = eval(results)
                print(result_final)
            elif(command == 'insertQuery'):
                mongo_client = mongo_client['DBPROJ']
                print("insertQuery")
            else:
                print("Please enter a valid commad. For reference go to Readme.",mongo_client)
        else:
            print("Please enter a valid commad. For reference go to Readme.")

if __name__ == "__main__":
    main()


# # for (table_name,) in tables:
# #     migrate_table(table_name, table_name)
# # Close connections
# mysql_conn.close()
# mongo_client.close()

# app = Flask(__name__)

# @app.route("/members")
# def members():
#     return {"members" : [1,2,3,4]}
# if __name__ =="__main__":
#         app.run(debug= True)
