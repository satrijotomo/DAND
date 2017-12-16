
# OpenMap Data Cleanup and Processing Project

This project showcases the data cleanup and processing by using Python and SQL. OSM map data file in XML format (in this project I use map of Plano, Texas) is processed and cleaned up with dataPrepSQL.py. The output are the CSV files which are then loaded into SQL database tables.
Subsequent analysis is performed with SQL queries to make sense of the data.

### Python Libraries Used:
csv
codecs
pprint
re
xml.etree.cElementTree
cerberus
schema
