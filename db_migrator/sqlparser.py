import re
def convert_sql_to_mongodb_join(sql_query):
    # Remove leading and trailing whitespaces
    sql_query = sql_query.strip()
    sql_query = re.sub(r'(\()', r' \1', sql_query)
    sql_query = re.sub(r'(\))', r'\1 ', sql_query)

    sql_query = sql_query.replace('( ', '(')
    sql_query = sql_query.replace(' )', ')')

    sql_query = ' '.join(sql_query.split())

    # Split SQL query into SELECT, FROM, WHERE clauses
    select_clause, from_clause, where_clause = re.findall(r'SELECT (.+?) FROM (.+?)(?: WHERE (.*))?$', sql_query, re.IGNORECASE)[0]

    # If SELECT clause exists
    if from_clause:
        # Extract fields from SELECT clause
        fields = [field.strip() for field in select_clause.split(',')]
        #print(fields, type(fields))

    # If FROM clause exists
    if from_clause:
        if bool(re.search(r"\b(JOIN|CROSS JOIN|INNER JOIN|LEFT JOIN|RIGHT JOIN)\b", from_clause, flags=re.IGNORECASE)):
            # Find all matches of table names
            collection_names = re.findall(r'\b(\w+)\s+(?:JOIN|CROSS JOIN|INNER JOIN|LEFT JOIN|RIGHT JOIN)\s+(\w+)\b', from_clause, re.IGNORECASE)[0]

            # Find all '(a=b)' or '(x.a=y.b)' but a='xxx', a=100, x.a=b will fail to be extracted
            tmp_extra = re.findall(r"\w+\.\w+\s*[=><!]+\s*\w+\.\w+|\w+\s*[=><!]+\s*\w+", from_clause, re.IGNORECASE)
            #print(tmp_extra)
            
            conditions_by_from = []
            for c in tmp_extra:
                condition = re.findall(r'(.*)\s*([=><!]+)\s*(.*)', c, re.IGNORECASE)
                conditions_by_from.append(condition[0])
            
            #print(conditions_by_from)
        else:
            collection_names = [from_clause.strip()]

    # If WHERE clause exists
    if where_clause:
        # Extract conditions_by_where from WHERE clause, where ([=><!]+) captures relational operators like =, <, >, !, etc
        conditions_by_where = re.findall(r'(\w+?)\s*([=><!]+)\s*([\'"\w\s]+)(?:\s+AND\s+|$)', where_clause, re.IGNORECASE)

    conditions = []
    
    # if WHERE has conditions
    if 'conditions_by_where' in locals():
        #print("\nBy_where:", conditions_by_where)
        for c in conditions_by_where:
            # Trim values within each tuple
            conditions.append(tuple(element.strip() for element in c))

    # if FROM has conditions
    if 'conditions_by_from' in locals():
        #print("\nBy_from:", conditions_by_from)
        for c in conditions_by_from:
            conditions.append(tuple(element.strip() for element in c))

    # Map SQL operators to MongoDB operators
    operator_map = {
        '=': '$eq',
        '>': '$gt',
        '>=': '$gte',
        '<': '$lt',
        '<=': '$lte',
        '!=': '$ne'
    }

    # Initialize MongoDB find query
    mongo_query = {}
    
    queryFormat = 'single' if len(collection_names) == 1 else 'joins'
    lookup_block = match_block = project_block = ''


    # Construct MongoDB single query
    if queryFormat == 'single':
        # $match
        if 'conditions_by_where' in locals():
            match_block += '''
"$match": {'''

            for c in conditions_by_where:
                mongo_operator = operator_map.get(c[1])
                match_block += f'''
    "{c[0]}": {{ "{mongo_operator}": {c[2]} }},'''

            match_block += '''
}'''

        # $project
        project_block += '''
"$project": {
    "_id": 0,'''

        if not (fields[0] == '*' and len(fields) == 1):
            for field in fields: 
                project_block += f'''
    "{field}": 1,'''

        project_block += '''
}'''

        # scripts
        first_collection = collection_names[0]        
        if match_block:
            mongo_query = f"{{ {match_block} }}"
            if project_block:
                mongo_query += f",{{ {project_block} }}"
        else:
            if project_block:
                mongo_query = f"{{ {project_block} }}"

        eval_script = f"db.{first_collection}.aggregate(["
        eval_script += mongo_query
        eval_script += f"])"

        result_cursor = eval(eval_script)
        result = list(result_cursor)
        for doc in result: print(doc)

    elif queryFormat == 'joins':
        first_collection = collection_names[0]
        
        # only one joining table is considered
        if len(collection_names) > 1:
            joining_collection = collection_names[1]
            stage_result_collection = joining_collection.lower()+f"_result"

        # $lookup
        lookup_block += '''
"$lookup": {'''
        lookup_block += f'''
    "from": "{joining_collection}",'''

        if 'conditions_by_from' in locals():
            for c in conditions_by_from:
                tmp1 = c[0].split('.')[-1]
                tmp2 = c[2].split('.')[-1]
                lookup_block += f'''
    "localField": "{tmp1}",
    "foreignField": "{tmp2}",'''

        lookup_block += f'''
    "as": "{stage_result_collection}"'''

        lookup_block += '''
}'''


        # $match
        if 'conditions_by_where' in locals():
            match_block += '''
"$match": {'''

            for c in conditions_by_where:
                mongo_operator = operator_map.get(c[1])
                match_block += f'''
    "{stage_result_collection}.{c[0]}": {{ "{mongo_operator}": {c[2]} }}'''

            match_block += '''
}'''

        print(match_block)

        # $project
        project_block += '''
"$project": {
    "_id": 0,'''

        if not (fields[0] == '*' and len(fields) == 1):
            for field in fields: 
                project_block += f'''
    "{field}": 1,'''

        project_block += '''
}'''

        mongo_query = f"{{ {lookup_block} }}" if lookup_block else ''
        mongo_query += f",{{ {match_block} }}" if match_block else ''
        mongo_query += f",{{ {project_block} }}" if project_block else ''
                
                
        eval_script = f"db.{first_collection}.aggregate(["
        eval_script += mongo_query
        eval_script += f"])"

        return eval_script