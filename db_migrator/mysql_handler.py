import re
from .selectQuery import convert_sql_to_mongodb
from .isertQuery import sql_to_mongodb
from .sqlparser import convert_sql_to_mongodb_join
def selectQuery(sql_query):
    return convert_sql_to_mongodb(sql_query)

def insertQuery(insert_string):
    return sql_to_mongodb(insert_string)

def joinQuery(join_string):
    return convert_sql_to_mongodb_join(join_string)
    pass


# SELECT orders.OrderID, customers.CustomerName, orders.OrderDate FROM orders INNER JOIN customers ON orders.CustomerID=customers.CustomerID;
# SELECT * FROM orders INNER JOIN customers ON orders.CustomerID=customers.CustomerID;