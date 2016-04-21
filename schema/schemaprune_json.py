from types import *
import json
import sys
import logging

# Globals
enabled_features = []
CAN_DELETE, CANNOT_DELETE, UNTAGGED = range(0, 3)

def get_enabled_features():
    with open(sys.argv[3]) as f:
        for line in f:
            for entry in line.split():
                enabled_features.append(entry)

    logging.info("================================================================================")
    for feature in enabled_features:
        logging.info("enabled feature: %s" % feature)
    logging.info("================================================================================")

if __name__ == '__main__':
    exit

# sanitize the arguments
if len(sys.argv) < 4:
    logging.critical("This script takes 3 arguments:")
    logging.critical("1. input-schema json file")
    logging.critical("2. output-schema json file")
    logging.critical("3. file containing the enabled-features (space separated)")
    logging.critical("The 4th argument is optional:")
    logging.critical("4. Log-level for the script: DEBUG, INFO, WARNING, ERROR, CRITICAL")
    sys.exit(0)

# Set the logging level
log_level_list = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
if ((sys.argv[4:]) and (sys.argv[4] in log_level_list)):
    logging.basicConfig(level=logging.sys.argv[4])
else:
    logging.basicConfig(level=logging.CRITICAL)

# Create enabled_feature_list
# Here we'll go thru the IMAGE_FEATURES variable & create the list.
# For now we're testing with the following static list
get_enabled_features()

# read the json ovs schema
with open(sys.argv[1]) as x:
    fs = x.read()
    ovsschema =  json.loads(fs)

# Walk the JSON file containing the schema in JSON format & delete items
# corresponding to features that have not been enabled
tables = ovsschema['tables']
for table in tables.keys():
    logging.debug("================================================================================")
    logging.debug("table: \"%s\"" % table)
    del_table = del_column = del_enum = UNTAGGED
    table_tagged = False
    table_features = column_features = enum_features = features = []

    table_data = tables[table]
    if 'feature_list' in table_data:
        table_tagged = True
        table_features = features = table_data['feature_list']
        logging.debug("features = %s" % features)

        if bool(set(features) & set(enabled_features)):
            logging.info("DELETE:N: (table: \"%s\")" % table)
            del_table = CANNOT_DELETE
        else:
            logging.info("DELETE:Y: (table: \"%s\")" % table)
            del_table = CAN_DELETE

        del table_data['feature_list']
    else:
        logging.debug("UNTAGGED: (table: \"%s\")" % table)

    if 'columns' in table_data:
        columns = table_data['columns']
        for column in columns.keys():
            logging.debug("column = %s" % column)
            del_column = del_enum = UNTAGGED
            column_tagged = False
            column_features = features = []
            column_data = columns[column]
            if 'feature_list' in column_data:
                column_tagged = True
                column_features = features = column_data['feature_list']
                logging.debug("features = %s" % features)
                if bool(set(features) & set(enabled_features)):
                    logging.info("DELETE:N: (table: \"%s\"; column: \"%s\")" % (table, column))
                    del_column = CANNOT_DELETE
                    del_table = CANNOT_DELETE
                else:
                    logging.info("DELETE:Y: (table: \"%s\"; column: \"%s\")" % (table, column))
                    del_column = CAN_DELETE

                del column_data['feature_list']
            else:
                logging.debug("UNTAGGED: (table: \"%s\"; column: \"%s\")" % (table, column))
                if (table_tagged == True):
                    #Just inherit from the table feature-list
                    features = table_features
                    logging.debug("Inheriting table \"%s\" feature-list" % (table))
                    if bool(set(features) & set(enabled_features)):
                        logging.info("DELETE:N: (table: \"%s\"; column: \"%s\")" % (table, column))
                        del_column = CANNOT_DELETE
                        del_table = CANNOT_DELETE
                    else:
                        logging.info("DELETE:Y: (table: \"%s\"; column: \"%s\")" % (table, column))
                        del_column = CAN_DELETE

            if 'type' in column_data:
                type_data = column_data['type']
                logging.debug("type_data = %s" % type_data)
                if 'key' in type_data:
                    key_data = type_data['key']
                    logging.debug("key_data = %s" % key_data)
                    if 'enum' in key_data:
                        enum_data = key_data['enum']
                        logging.debug("enum_data = %s" % enum_data)
                        if 'set' in enum_data:
                            enum_index = len(enum_data[1]) - 1
                            while enum_index >= 0:
                                elem = enum_data[1][enum_index]
                                logging.debug("enum = %s" % elem)
                                enum_features = features = []
                                del_enum = UNTAGGED
                                if type(elem) is DictType:
                                    if 'feature_list' and 'val' in elem:
                                        enum_features = features = elem['feature_list']
                                        enum_val = elem['val']
                                        logging.debug("features = %s enum_val = %s" % (features, enum_val))
                                        if bool(set(features) & set(enabled_features)):
                                            logging.info("DELETE:N: (table: \"%s\"; column: \"%s\"; enum: \"%s\")" % (table, column, enum_val))
                                            del_enum = CANNOT_DELETE
                                            del_column = CANNOT_DELETE
                                            del_table = CANNOT_DELETE
                                        else:
                                            logging.info("DELETE:Y: (table: \"%s\"; column: \"%s\"; enum: \"%s\")" % (table, column, enum_val))
                                            del_enum = CAN_DELETE

                                        # Now delete the DictType entry from the enum
                                        enum_data[1].pop(enum_index)
                                        if (del_enum == CANNOT_DELETE):
                                            # Add regular entry to the enum
                                            enum_data[1].insert(enum_index, enum_val)
                                    else:
                                        logging.info("ERROR: UNTAGGED: (table: \"%s\"; column: \"%s\"; enum: \"%s\")" % (table, column, enum_val))
                                        #This is not allowed & will be flagged as an error by "make" that will follow.
                                else:
                                    logging.debug("UNTAGGED: (table: \"%s\"; column: \"%s\"; enum: \"%s\")" % (table, column, elem))
                                    if (column_tagged == True): 
                                        #Just inherit from the column feature-list
                                        logging.debug("Inheriting column \"%s\" feature-list" % (column))
                                        features = column_features
                                    elif (table_tagged == True):
                                        #Just inherit from the table feature-list
                                        logging.debug("Inheriting table \"%s\" feature-list" % (table))
                                        features = table_features

                                    if ((column_tagged == True) or (table_tagged == True)):
                                        if bool(set(features) & set(enabled_features)):
                                            logging.info("DELETE:N: (table: \"%s\"; column: \"%s\"; enum: \"%s\")" % (table, column, elem))
                                            del_enum = CANNOT_DELETE
                                            del_column = CANNOT_DELETE
                                            del_table = CANNOT_DELETE
                                        else:
                                            logging.info("DELETE:Y: (table: \"%s\"; column: \"%s\"; enum: \"%s\")" % (table, column, elem))
                                            del_enum = CAN_DELETE
                                            enum_data[1].pop(enum_index)

                                enum_index -= 1

            if (del_column == CAN_DELETE):
                columns.pop(column, None)

    if (del_table == CAN_DELETE):
        tables.pop(table, None)

logging.info("================================================================================")

# Generate the output schema file
with open(sys.argv[2], 'w') as fo:
    json.dump(ovsschema, fo, sort_keys = True, indent=4, separators=(',', ': '))
    fo.write('\n')
