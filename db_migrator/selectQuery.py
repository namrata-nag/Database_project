import re

def convert_sql_to_mongodb(sql_query):
    # Remove leading and trailing whitespaces
    sql_query = sql_query.strip()

    # Split SQL query into SELECT, FROM, WHERE, ORDER BY, LIMIT, and SKIP clauses
    select_clause, from_clause, where_clause, order_by_clause, limit_clause, skip_clause = re.findall(r'SELECT (.+?) FROM (.+?)(?: WHERE (.*?))?(?: ORDER BY (.*?))?(?: LIMIT (\d+))?(?: SKIP (\d+))?$', sql_query, re.IGNORECASE)[0]

    # Extract collection name from FROM clause
    collection_name = from_clause.strip()

    # Initialize MongoDB find query
    mongo_query = {}

    # If ORDER BY clause exists
    if order_by_clause:
        order_by_match = re.findall(r'(\w+)\s+(ASC|DESC)', order_by_clause.strip(), re.IGNORECASE)
        if order_by_match:
            field, order = order_by_match[0]
            order_by = {field: 1 if order.upper() == 'ASC' else -1}
        else:
            field = order_by_clause
            order_by = {field: 1}
    else:
        order_by = None

    # If LIMIT clause exists
    if limit_clause:
        limit = int(limit_clause)
    else:
        limit = None

    # If SKIP clause exists
    if skip_clause:
        skip = int(skip_clause)
    else:
        skip = None

    # Construct MongoDB find query
    mongo_query_result = f"db.{collection_name}.find("

    # Adding WHERE clause if present
    if where_clause:
        # Extract conditions from WHERE clause
        or_conditions = where_clause.split(' OR ')
        
        # Construct MongoDB query
        or_expressions = []
        for or_condition in or_conditions:
            and_expressions = []
            and_conditions = or_condition.split(' AND ')
            for and_condition in and_conditions:
                field, operator, value = re.findall(r'(\w+?)\s*([=><!]+)\s*([\'"\w\s]+)', and_condition)[0]
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
                    and_expressions.append({field: {mongo_operator: value}})
                elif operator == 'IN':
                    and_expressions.append({field: {'$in': [v.strip() for v in value.split(',')]}})
                else:
                    and_expressions.append({field: value})
            or_expressions.append({'$and': and_expressions})
        
        mongo_query.update({'$or': or_expressions})
        mongo_query_result += f"{mongo_query},"

    # Close MongoDB find query
    mongo_query_result += ")"

    # Adding ORDER BY clause if present
    if order_by is not None:
        mongo_query_result += ".sort(" + str(order_by) + ")"

    # Adding LIMIT clause if present
    if limit is not None:
        mongo_query_result += ".limit(" + str(limit) + ")"

    # Adding SKIP clause if present
    if skip is not None:
        mongo_query_result += ".skip(" + str(skip) + ")"

    return mongo_query_result

# Example usage:
# sql_query = "SELECT * FROM customers WHERE CustomerName = 'Alfreds Futterkiste' OR City = 'London' ORDER BY CustomerId DESC LIMIT 3"
# mongo_query_result = convert_sql_to_mongodb(sql_query)
# print(mongo_query_result)