from initClients import initiate
from db_migrator import selectQuery, insertQuery, migrate, joinQuery
import re

import sys
pattern = r'(\w+)\s+"([^"]+)"'

def main():
    mongo_client, mysql_client = initiate()
    mysql_cursor = mysql_client.cursor()
    print("This app is to run the migration package in command line mode. DB Migrattion package exposes three function. For the ussage please follow readme.")
    print("1. selectQuery - It parses the select sql query to noSQL query and return the result after reading data from Mongo")
    print("3. joinQuery - It parses the sql query with join condition to noSQL query and return the result")
    print("4. insertQuery - It parses the insert sql query to noSQL query and insert the value")
    print("5. migrate - It will migrate the MySQL database to MongoDB.")
    print("Type your command...")
    while True:
        command = input("$  ")
        if command == "exit":
            break
        print("You entered:", command)
        print("mongo_client",mongo_client)
        match = re.match(pattern, command)
        if match:
            command = match.group(1)
            input_param = match.group(2)
            if(command == 'migrate'):
                migrate(mongo_client, mysql_cursor, input_param)
            elif(command == 'selectQuery'):
                db = mongo_client['DBPROJ']
                results = selectQuery(input_param)
                result_final = eval(results)
                print("Below is the search result:")
                print("")
                print("")
                for document in result_final:
                    print(document)
            elif(command == 'insertQuery'):
                db = mongo_client['DBPROJ']
                results = insertQuery(input_param)
                result_final = eval(results)
                print("Inser Complete")
            elif(command=='joinQuery'):
                db = mongo_client['DBPROJ']
                results = joinQuery(input_param)
                result_final = eval(results)
                print("Below is the join result:")
                print("")
                print("")
                for document in result_final:
                    print(document)
            else:
                print("Please enter a valid commad. For reference go to Readme.",mongo_client)
        else:
            print("Please enter a valid commad. For reference go to Readme.")

if __name__ == "__main__":
    main()
