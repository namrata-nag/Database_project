
#collection.create_index([('your_field_name', 1)], unique=True)

requiredCol = []
propertiesCol = {}
isPrimaryCol = ""
validation_table = {
     "$jsonschema":{
        "bsonType": "object",
        "required": [],
        "properties": {

        }

     }
}


for column in mysql_columns:
        # print("column->",column)
        column_name = column[0]
        data_type = column[1]
        # isRequired = column[2] #not null
        # isPrimaryCol = column[3]
        # default_value = column[4]
        # extra = column[5]
        mongo_data_type = data_type_mapping.get(data_type, 'string')