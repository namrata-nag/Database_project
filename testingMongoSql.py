import re

def sql_to_mongodb(sql_query):
    # Example SQL: INSERT INTO customers (name, address) VALUES ('John', 'Highway 21'), ('Jane', 'Sideway 163');
    pattern = r"INSERT INTO (\w+) \(([^)]+)\) VALUES (.+);"
    match = re.match(pattern, sql_query.strip(), re.IGNORECASE)

    if not match:
        return "Query format not recognized"

    table, fields, values = match.groups()
    fields = [field.strip() for field in fields.split(',')]
    raw_values = values.strip().split('),')

    documents = []

    for val in raw_values:
        val = val.strip('() ')
        value_parts = val.split(',')
        value_parts = [v.strip().strip("'") for v in value_parts]
        document = dict(zip(fields, value_parts))
        documents.append(document)

    if len(documents) == 1:
        return f"db.{table}.insert_one({documents[0]})"
    else:
        return f"db.{table}.insert_many({documents})"
    


# def sql_to_mongodb_select(sql_query):
#     # Simple pattern for "SELECT * FROM table WHERE condition"
#     pattern = r"SELECT \* FROM (\w+)( WHERE (.+))?"
#     match = re.match(pattern, sql_query.strip(), re.IGNORECASE)

#     if not match:
#         return "Query format not recognized"

#     table, _, condition = match.groups()
#     query = {}
#     if condition:
#         # Very basic condition handling: "field = value"
#         field, value = condition.split('=')
#         field = field.strip()
#         value = value.strip().strip("'")
#         query = {field: value}

#     return f"db.{table}.find({query})"

def sql_to_mongodb_select(sql_query):
    # Pattern to extract the table name and where clause
    pattern = r"SELECT \* FROM (\w+)( WHERE (.+))?"
    match = re.match(pattern, sql_query.strip(), re.IGNORECASE)

    if not match:
        return "Query format not recognized", None

    table, _, condition = match.groups()
    query = {}
    
    if condition:
        # Find all conditions split by AND (assuming no OR for simplicity)
        condition_matches = re.findall(r"(\w+)\s*(!=|=)\s*'([^']+)'", condition)
        
        for field, operator, value in condition_matches:
            if operator == '=':
                query[field] = value
            elif operator == '!=':
                query[field] = {"$ne": value}

    return f"db.{table}.find({query})", query



# # Example usage:
# sql_query = "INSERT INTO customers (name, address) VALUES ('John', 'Highway 21'), ('Jane', 'Sideway 163');"
# print(sql_to_mongodb(sql_query))


# Example usage:
# sql_query1 = "SELECT * FROM customers WHERE name = 'John'"
# print(sql_to_mongodb_select(sql_query1))

# # Example usage:
# sql_query = "SELECT * FROM customers WHERE name = 'John' AND address = 'Highway 21'"
# print(sql_to_mongodb_select(sql_query))

# sql_query2 = "SELECT * FROM customers WHERE name = 'John' AND address != 'Highway 1'"
# print(sql_to_mongodb_select(sql_query2))
