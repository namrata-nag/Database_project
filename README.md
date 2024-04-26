# Database_project

Step to install locally
$ source venv/bin/activate to activate the python env
$ python3 server.py to run server

source venv/bin/activate

Below is the output of the table

[('categories',), ('customers',), ('employees',), ('order_details',), ('orders',), ('products',), ('shippers',), ('suppliers',)]


Below are the column read

[('CategoryID', 'int', 'NO', 'PRI', None, 'auto_increment'), ('CategoryName', 'varchar(255)', 'YES', '', None, ''), ('Description', 'varchar(255)', 'YES', '', None, '')]

[('CustomerID', 'int', 'NO', 'PRI', None, 'auto_increment'), ('CustomerName', 'varchar(255)', 'YES', '', None, ''), ('ContactName', 'varchar(255)', 'YES', '', None, ''), ('Address', 'varchar(255)', 'YES', '', None, ''), ('City', 'varchar(255)', 'YES', '', None, ''), ('PostalCode', 'varchar(255)', 'YES', '', None, ''), ('Country', 'varchar(255)', 'YES', '', None, '')]

[('EmployeeID', 'int', 'NO', 'PRI', None, 'auto_increment'), ('LastName', 'varchar(255)', 'YES', '', None, ''), ('FirstName', 'varchar(255)', 'YES', '', None, ''), ('BirthDate', 'date', 'YES', '', None, ''), ('Photo', 'varchar(255)', 'YES', '', None, ''), ('Notes', 'text', 'YES', '', None, '')]

[('OrderDetailID', 'int', 'NO', 'PRI', None, 'auto_increment'), ('OrderID', 'int', 'YES', 'MUL', None, ''), ('ProductID', 'int', 'YES', 'MUL', None, ''), ('Quantity', 'int', 'NO', '', None, '')]
[('OrderID', 'int', 'NO', 'PRI', None, 'auto_increment'), ('CustomerID', 'int', 'YES', 'MUL', None, ''), ('EmployeeID', 'int', 'YES', 'MUL', None, ''), ('OrderDate', 'date', 'YES', '', None, ''), ('ShipperID', 'int', 'YES', 'MUL', None, '')]

[('ProductID', 'int', 'NO', 'PRI', None, 'auto_increment'), ('ProductName', 'varchar(255)', 'YES', '', None, ''), ('SupplierID', 'int', 'YES', 'MUL', None, ''), ('CategoryID', 'int', 'YES', 'MUL', None, ''), ('Unit', 'varchar(255)', 'YES', '', None, ''), ('Price', 'double', 'YES', '', None, '')]

[('ShipperID', 'int', 'NO', 'PRI', None, 'auto_increment'), ('ShipperName', 'varchar(255)', 'YES', '', None, ''), ('Phone', 'varchar(255)', 'YES', '', None, '')]

[('SupplierID', 'int', 'NO', 'PRI', None, 'auto_increment'), ('SupplierName', 'varchar(255)', 'YES', '', None, ''), ('ContactName', 'varchar(255)', 'YES', '', None, ''), ('Address', 'varchar(255)', 'YES', '', None, ''), ('City', 'varchar(255)', 'YES', '', None, ''), ('PostalCode', 'varchar(255)', 'YES', '', None, ''), ('Country', 'varchar(255)', 'YES', '', None, ''), ('Phone', 'varchar(255)', 'YES', '', None, '')]


https://www.mongodb.com/docs/v5.2/reference/operator/query/jsonSchema/#mongodb-query-op.-jsonSchema


Task
1. Create api for isert/update/delete
2. Check how to integrate foreign key - lookup
3. Check how to implement trigger -   maybe later
4. Check out the validation schema and how to use it to integerate required_column, datatype, null value and other column properties
5. Create a mapping for select statement - select (*/column_name), from - single table, where
6. Create a mapping for insert statement - insert, into, where
7. Create a mapping for join - multiple joins, where 
8. Create mapping for aggregate function -  
9. Handle group by and having
10. Create mapping for sql functions
11. Create a mapping for delete statement
12. Handle nested queries


