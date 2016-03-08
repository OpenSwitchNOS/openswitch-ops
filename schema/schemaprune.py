from types import *
import json
import sys

#Temporarily maintaining a static list for enabled features
enabled_features = ["bgp", "ntp", "ntp_client"]

if __name__ == '__main__':
    exit

# sanitize the arguments
if len(sys.argv) < 3:
    print("Error: Script needs 2 argument (input-schema delete-list output-schema)")
    sys.exit(0)

# read the json ovs schema
with open(sys.argv[1]) as x: 
    fs = x.read()
    ovsschema =  json.loads(fs)

# Walk the JSON file containing the schema in JSON format & delete items
# corresponding to features that have not been enabled
tables = ovsschema['tables']
for table in tables.keys():
    #print("table = %s" % table)
    del_table = del_column = del_enum = 0

    table_data = tables[table]
    if 'feature_list' in table_data:
        #print("table = %s" % table)
        features = table_data['feature_list']
        #print("features = %s" % features)

        if bool(set(features) & set(enabled_features)):
            print("There is at least 1 feature in the feature_list that has been enabled")
        else:
            del_table = 1
            print("Table %s can be deleted" % table)

    if 'columns' in table_data:
        columns = table_data['columns']
        for column in columns.keys():
            #print("column = %s" % column)
            column_data = columns[column]
            if 'feature_list' in column_data:
                #print("table = %s; column = %s" % (table, column))
                features = column_data['feature_list']
                #print("features = %s" % features)
                if bool(set(features) & set(enabled_features)):
                    print("There is at least 1 feature in the feature_list that has been enabled")
                    del_table = 0
                else:
                    del_column = 1
                    print("table %s column %s can be deleted" % (table, column))
                    columns.pop(column, None)
                    del_column = 0

    if (del_table == 1):
        tables.pop(table, None)

# Generate the output schema file
with open(sys.argv[2], 'w') as fo:
    json.dump(ovsschema, fo, sort_keys = True, indent=4, separators=(',', ': '))
    fo.write('\n')
