from pymongo import MongoClient
import pymongo

from testingMongoSql import sql_to_mongodb, sql_to_mongodb_select

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['sqlNoSqlproject1']  # Replace 'test_database' with your database name

# Test function to run a MongoDB query from a converted SQL insert
def test_mongodb_insert(mongodb_query):
    eval(mongodb_query)

# def test_mongodb_select(db, mongodb_query):
#     result = eval(mongodb_query)
#     return list(result)

def test_mongodb_select(db, mongodb_query):
    command, query = sql_to_mongodb_select(mongodb_query)
    if command:
        result = eval(command)
        return list(result)
    else:
        return "Error in query format"
# # Example SQL query
# sql_query = "INSERT INTO customers (name, address, nickName) VALUES ('Raj', 'Pearl 2212', 'Natu_Natu');"
# mongodb_query = sql_to_mongodb(sql_query)

# Run the test
# test_mongodb_insert(mongodb_query)

# # Verify insertion by fetching data
# for customer in db.customers.find():
#     print(customer)


# Test SELECT
# sql_select_query = "SELECT * FROM customers WHERE name = 'John';"
# mongodb_select_query = sql_to_mongodb_select(sql_select_query)
# select_results = test_mongodb_select(db, mongodb_select_query)
# print("Results of SELECT query:", select_results)

# Example SQL SELECT query and its conversion
# sql_select_query = "SELECT * FROM customers WHERE name = 'John' AND address != 'Highway 1'"

sql_select_query = "SELECT * FROM customers WHERE name = 'John' OR address = 'Highway 27'"

select_results = test_mongodb_select(db, sql_select_query)
print("Results of SELECT query:", select_results)
