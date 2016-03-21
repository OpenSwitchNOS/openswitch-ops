from types import *
import sys
import xml.dom.minidom
import logging

# Globals
enabled_features = []
MAX_FEATURES = 100
CAN_DELETE, CANNOT_DELETE, UNTAGGED = range(0, 3)

# Go through the file containing the list of (space separated) enabled-features
# and populate the list
def get_enabled_features():
    with open(sys.argv[3]) as f:
        for line in f:
            for entry in line.split():
                enabled_features.append(entry)

    logging.info("================================================================================")
    for feature in enabled_features:
        logging.info("enabled feature: %s" % feature)
    logging.info("================================================================================")


def delete_object(obj):
    parent = obj.parentNode
    logging.debug("parent = %s" % parent)
    parent.removeChild(obj)

# Go through the feature_list defined in obj & return if the obj is deletable
def check_delete_object(obj):
    local_features = ['']*MAX_FEATURES

    for child in obj.childNodes:
        # Check for ELEMENT_NODE
        if (child.nodeType == 1):
            logging.debug(child.nodeName)
            if (child.nodeName == "feature_list"):
                feature_list = child.getElementsByTagName("feature")
                logging.debug("len = %s" % len(feature_list))
                for i in range(0, (len(feature_list))):
                    feature = feature_list[i]
                    local_features[i] = str(feature.childNodes[0].nodeValue)
                for i in range(0, len(feature_list)):
                    logging.debug("local_feature = %s" % local_features[i])

                delete_object(child)
                if bool(set(local_features) & set(enabled_features)):
                    logging.debug("There is at least 1 feature in the feature_list that has been enabled. Cannot delete object")
                    return CANNOT_DELETE
                else:
                    return CAN_DELETE

    # If feature_list is not found, return "UNTAGGED"
    return UNTAGGED


if __name__ == '__main__':
    exit

# sanitize the arguments
if len(sys.argv) < 4:
    logging.critical("This script takes 3 arguments:")
    logging.critical("1. input-schema xml file")
    logging.critical("2. output-schema xml file")
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

get_enabled_features()

# read the xml ovs schema
DOMTree = xml.dom.minidom.parse(sys.argv[1])

# Walk the XML file containing the schema in XML format & delete items
# corresponding to features that have not been enabled
tables = DOMTree.getElementsByTagName("table")
for table in tables:
    del_table = del_group = del_column = UNTAGGED

    logging.debug("================================================================================")
    logging.debug("table: %s" % table.getAttribute("name"))
    del_table = check_delete_object(table)
    if (del_table == CANNOT_DELETE):
        logging.info("DELETE:N: (table: \"%s\")" % table.getAttribute("name"))
    elif (del_table == UNTAGGED):
        logging.debug("UNTAGGED: (table: \"%s\")" % table.getAttribute("name"))

    for child in table.childNodes:
        # Check for ELEMENT_NODE
        if (child.nodeType == 1):
            logging.debug(child.nodeName)
            if (child.nodeName == "group"):
                group = child
                logging.debug("group: %s" % group.getAttribute("title"))
                del_group = check_delete_object(group)
                if (del_group == CANNOT_DELETE):
                    logging.info("DELETE:N: (table: \"%s\"; group: \"%s\")" % \
                                  (table.getAttribute("name"), group.getAttribute("title")))
                    del_table = CANNOT_DELETE
                elif (del_group == UNTAGGED):
                    logging.debug("UNTAGGED: (table: \"%s\"; group: \"%s\")" % \
                                  (table.getAttribute("name"), group.getAttribute("title")))

                columns = group.getElementsByTagName("column")
                for column in columns:
                    logging.debug("column: %s; key: %s" % (column.getAttribute("name"), column.getAttribute("key")))

                    del_column = check_delete_object(column)
                    if (del_column == CAN_DELETE):
                        logging.info("DELETE:Y: (table: \"%s\"; group: \"%s\"; column: \"%s\"; key: \"%s\")" % \
                               (table.getAttribute("name"), group.getAttribute("title"), column.getAttribute("name"), column.getAttribute("key")))
                        delete_object(column)
                    elif (del_column == CANNOT_DELETE):
                        logging.info("DELETE:N: (table: \"%s\"; group: \"%s\"; column: \"%s\"; key: \"%s\")" % \
                               (table.getAttribute("name"), group.getAttribute("title"), column.getAttribute("name"), column.getAttribute("key")))
                        del_group = CANNOT_DELETE
                    elif (del_column == UNTAGGED):
                        logging.debug("UNTAGGED: (table: \"%s\"; group: \"%s\"; column: \"%s\"; key: \"%s\")" % \
                               (table.getAttribute("name"), group.getAttribute("title"), column.getAttribute("name"), column.getAttribute("key")))

                if (del_group == CAN_DELETE):
                    logging.info("DELETE:Y: (table: \"%s\"; group: \"%s\")" % \
                                  (table.getAttribute("name"), group.getAttribute("title")))
                    delete_object(group)
                elif (del_group == CANNOT_DELETE):
                    logging.info("DELETE:N: (table: \"%s\"; group: \"%s\")" % \
                                  (table.getAttribute("name"), group.getAttribute("title")))
                    del_table = CANNOT_DELETE

            elif (child.nodeName == "column"):
                column = child
                logging.debug("column: %s; key: %s" % (column.getAttribute("name"), column.getAttribute("key")))

                del_column = check_delete_object(column)
                if (del_column == CAN_DELETE):
                    logging.info("DELETE:Y: (column: \"%s\"; key: \"%s\")" % (column.getAttribute("name"), column.getAttribute("key")))
                    delete_object(column)
                elif (del_column == CANNOT_DELETE):
                    logging.info("DELETE:N: (column: \"%s\"; key: \"%s\")" % (column.getAttribute("name"), column.getAttribute("key")))
                    del_table = CANNOT_DELETE
                elif (del_column == UNTAGGED):
                    logging.debug("UNTAGGED: (column: \"%s\"; key: \"%s\")" % (column.getAttribute("name"), column.getAttribute("key")))

    if (del_table == CAN_DELETE):
        logging.info("DELETE:Y: (table: \"%s\")" % table.getAttribute("name"))
        delete_object(table)
    elif (del_table == CANNOT_DELETE):
        logging.info("DELETE:N: (table: \"%s\")" % table.getAttribute("name"))

logging.info("================================================================================")

# Generate the output schema file
file_handle = open(sys.argv[2], "w")
DOMTree.writexml(file_handle)
file_handle.close()
