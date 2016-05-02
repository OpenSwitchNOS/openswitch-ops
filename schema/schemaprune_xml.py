from types import *
import sys, xml.dom.minidom, logging, getopt

# Globals
enabled_features = []
CAN_DELETE, CANNOT_DELETE, UNTAGGED = range(0, 3)

# Command-line arguments
infile = outfile = featurefile = ''
logfile = "./schemaprune_xml.log"
loglevel = "CRITICAL"
sanitize_only = False

# ================================================================================
# Go through the file containing the list of (space separated) enabled-features
# and populate the list
def get_enabled_features():
    with open(featurefile) as f:
        for line in f:
            for entry in line.split():
                enabled_features.append(entry)

    logging.info("================================================================================")
    for feature in enabled_features:
        logging.info("enabled feature: %s" % feature)
    logging.info("================================================================================")

# ================================================================================
def delete_object(obj):
    parent = obj.parentNode
    logging.debug("parent = %s" % parent)
    parent.removeChild(obj)

# ================================================================================
def check_delete_object(obj, up_level_features):
    logging.debug("check_delete_object: up_level_features = %s" % (up_level_features))
    local_features = []

    for child in obj.childNodes:
        # Check for ELEMENT_NODE
        logging.debug("child.nodeType = %s child.nodeName = %s" % (child.nodeType, child.nodeName))
        if (child.nodeType == child.ELEMENT_NODE):
            logging.debug("check_delete_object: %s up_level_features = %s" % (child.nodeName, up_level_features))
            if (child.nodeName == "feature_list"):
                feature_list = child.getElementsByTagName("feature")
                logging.debug("len = %s" % len(feature_list))
                for i in range(0, (len(feature_list))):
                    feature = feature_list[i]
                    local_features.append(str(feature.childNodes[0].nodeValue))
                for i in range(0, len(feature_list)):
                    logging.debug("local_feature = %s" % local_features[i])

                delete_object(child)
                if bool(set(local_features) & set(enabled_features)):
                    logging.debug("There is at least 1 feature in the feature_list that has been enabled. Cannot delete object")
                    return CANNOT_DELETE, local_features
                else:
                    return CAN_DELETE, local_features

    #if "feature_list" was not found, make decision based on "up_level_features"
    if up_level_features and not local_features:
        logging.debug("Inheriting upper_level features %s" % up_level_features)
        if bool(set(up_level_features) & set(enabled_features)):
            logging.debug("There is at least 1 feature in the feature_list that has been enabled. Cannot delete object")
            return CANNOT_DELETE, up_level_features
        else:
            return CAN_DELETE, up_level_features

    # If feature_list is not found, return "UNTAGGED"
    return UNTAGGED, local_features

# ================================================================================
def handle_group(table, group, up_level_features):
    logging.debug("group: %s" % group.getAttribute("title"))
    del_group, group_features = check_delete_object(group, up_level_features)
    if (del_group == CANNOT_DELETE):
        logging.info("DELETE:N: (table: \"%s\"; group: \"%s\")" % \
                     (table.getAttribute("name"), group.getAttribute("title")))
        del_table = CANNOT_DELETE
    elif (del_group == UNTAGGED):
        logging.debug("UNTAGGED: (table: \"%s\"; group: \"%s\")" % \
                     (table.getAttribute("name"), group.getAttribute("title")))

    inner_groups = group.getElementsByTagName("group")
    for inner_group in inner_groups:
        logging.debug("inner group: %s" % inner_group.getAttribute("title"))
        handle_group(table, inner_group, group_features)

    columns = group.getElementsByTagName("column")
    for column in columns:
        logging.debug("column: %s; key: %s" % (column.getAttribute("name"), column.getAttribute("key")))

        del_column, column_features = check_delete_object(column, group_features)
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

# ================================================================================
def handle_column(column, up_level_features):
    logging.debug("column: %s; key: %s" % (column.getAttribute("name"), column.getAttribute("key")))

    del_column, column_features = check_delete_object(column, up_level_features)
    if (del_column == CAN_DELETE):
        logging.info("DELETE:Y: (column: \"%s\"; key: \"%s\")" % (column.getAttribute("name"), column.getAttribute("key")))
        delete_object(column)
    elif (del_column == CANNOT_DELETE):
        logging.info("DELETE:N: (column: \"%s\"; key: \"%s\")" % (column.getAttribute("name"), column.getAttribute("key")))
        del_table = CANNOT_DELETE
    elif (del_column == UNTAGGED):
        logging.debug("UNTAGGED: (column: \"%s\"; key: \"%s\")" % (column.getAttribute("name"), column.getAttribute("key")))

# ================================================================================
if __name__ == '__main__':
    exit

try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:f:l:L:S:", ["ifile=","ofile=","featurefile=","logfile=","loglevel=","sanitize_only="])
except getopt.GetoptError:
    logfile.critical("schemaprune_xml.py -i <infile> -o <outfile> -f <featurefile> -l <logfile> -L <loglevel> -S <SanitizeOnly:True/False>")
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print 'schemaprune_xml.py -i <infile> -o <outfile> -f <featurefile> -l <logfile> -L <loglevel; default CRITICAL> -S <sanitize_only; True/False>'
        sys.exit()
    elif opt in ("-i", "--ifile"):
        infile = arg
    elif opt in ("-o", "--ofile"):
        outfile = arg
    elif opt in ("-f", "--featurefile"):
        featurefile = arg
    elif opt in ("-l", "--logfile"):
        logfile = arg
    elif opt in ("-L", "--loglevel"):
        loglevel = arg
    elif opt in ("-S", "--sanitize_only"):
        sanitize_only = arg

logging.debug ("infile = %s, outfile = %s, featurefile = %s, logfile = %s, loglevel = %s, sanitize_only = %s" % \
              (infile, outfile, featurefile, logfile, loglevel, sanitize_only))

if (sanitize_only == "False"):
    if (infile is '' or outfile is '' or featurefile is ''):
        logging.critical("Incorrect usage")
        sys.exit(2)

# Set the logging level
log_level_list = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
if ((loglevel) and (loglevel in log_level_list)):
    logging.basicConfig(filename=logfile, filemode='w', level=loglevel)
else:
    logging.basicConfig(filename=logfile, filemode='w', level="INFO")

get_enabled_features()

# read the xml ovs schema
DOMTree = xml.dom.minidom.parse(infile)

# Walk the XML file containing the schema in XML format & delete items
# corresponding to features that have not been enabled
tables = DOMTree.getElementsByTagName("table")
for table in tables:
    del_table = del_group = del_column = UNTAGGED
    table_features = group_features = column_features = []

    logging.debug("================================================================================")
    logging.debug("table: %s" % table.getAttribute("name"))
    del_table, table_features = check_delete_object(table, table_features)
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
                handle_group(table, group, table_features)
            elif (child.nodeName == "column"):
                column = child
                handle_column(column, table_features)

    if (del_table == CAN_DELETE):
        logging.info("DELETE:Y: (table: \"%s\") features = %s" % (table.getAttribute("name"), table_features))
        delete_object(table)
    elif (del_table == CANNOT_DELETE):
        logging.info("DELETE:N: (table: \"%s\")" % table.getAttribute("name"))

logging.info("================================================================================")

# Generate the output schema file
file_handle = open(outfile, "w")
DOMTree.writexml(file_handle)
file_handle.close()
