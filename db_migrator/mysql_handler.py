import re
def selectQuery(sql_query, db):
    sql_query = sql_query.strip()
    
    # Split SQL query into SELECT, FROM, WHERE clauses
    select_clause, from_clause, where_clause = re.findall(r'SELECT (.+?) FROM (.+?)(?: WHERE (.*))?$', sql_query, re.IGNORECASE)[0]
    
    # Extract fields from SELECT clause
    fields = [field.strip() for field in select_clause.split(',')]

    # Extract collection name from FROM clause
    collection_name = from_clause.strip()
    
    # Initialize MongoDB find query
    mongo_query = {}
    
    # If WHERE clause exists
    if where_clause:
        # Extract conditions from WHERE clause
        conditions = re.findall(r'(\w+?)\s*([=><!]+)\s*([\'"\w\s]+)(?:\s+AND\s+|$)', where_clause)
        #print(conditions)
        # Construct MongoDB query
        for condition in conditions:
            #print(condition)
            field, operator, value = condition
            if value.isnumeric():
                value = int(value)
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]  # Remove leading and trailing single quotes
            elif value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False

            # Map SQL operators to MongoDB operators
            operator_map = {
                '=': '$eq',
                '>': '$gt',
                '>=': '$gte',
                '<': '$lt',
                '<=': '$lte',
                '!=': '$ne'
            }
            mongo_operator = operator_map.get(operator)

            if mongo_operator:
                if mongo_operator == '$eq':
                    mongo_query[field] = value
                else:
                    if field not in mongo_query:
                        mongo_query[field] = {}
                    mongo_query[field][mongo_operator] = value
                    #print(mongo_query[field][mongo_operator])
            elif operator == 'IN':
                mongo_query[field] = {'$in': [v.strip() for v in value.split(',')]}
            else:
                mongo_query[field] = value
    print("mongo_query",mongo_query)
    print("fields",fields)
    # Construct MongoDB find query
    mongo_query_result = f"mongo_db.{collection_name}.find({mongo_query}, {{"
    for field in fields:
        mongo_query_result += f" '{field}': 1,"
    mongo_query_result = mongo_query_result[:-1]  # Remove the trailing comma
    mongo_query_result += "})"
    
    # mongo_query_result = eval(mongo_query_result)
    print("mongo_query_result",mongo_query_result)
    return mongo_query_result
    # Implement MySQL select query execution here

def insertQuery(insert_string):
    # Implement MySQL insert query execution here
    pass