#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema

expected = ["Street", "Avenue", "Drive","Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons","Ridge","Post-N-Paddock","Circle","Cove","Crossing","East",
           "Expressway","Falls","Green","Highway","K.", "McDermott","Oaks","Park","Pass","Point","Run",
           "S","Sol","South","Stars","Terrace","Trace","Way","Wells","100","101","110","1192","121","221","3",
            "440","544","644","700-285","M","P","S","#1","1"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Rd": "Road",
            "Rd." : "Road",
            "Ave" : "Avenue",
            "Dr" : "Drive",
           "Blvd":"Boulevard",
           "Expessway" : "Expressway",
           "Expy" : "Expressway",
           "Exressway" : "Expressway",
           "Pkwy" : "Parkway",
           "dr" : "Drive",
           "spalding":"Spalding"
            }
OSM_PATH = "/Volumes/USB128GB/1_UDACITY_DATA_ANALYSIS/P3 Data Wranging/PROJECT/openMap/PlanoTest.osm"
#OSM_PATH = "/Volumes/USB128GB/1_UDACITY_DATA_ANALYSIS/P3 Data Wranging/PROJECT/openMap/Plano_sample.xml"
#OSM_PATH = "example.osm"
NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

def update_name(name, mapping):

    # YOUR CODE HERE
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        #print "s_t", street_type
        if street_type not in expected:
            better_name = street_type_re.sub(mapping[street_type],name)
            #print "better name update_name", better_name
        else:
            better_name = name
    return better_name

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # YOUR CODE HERE
    if element.tag=="node":
        for i in node_attr_fields:
            node_attribs[i]=element.get(i)
        #print "shape_start"
        #print node_attribs
        id1=element.attrib["id"]
        #print "id1"
        #print id1
        for tag in element.iter("tag"):
            ntag={}
            ntag["id"]=id1
            k = tag.attrib["k"]
            
            if re.search(LOWER_COLON, k):
                d=k.find(":")
                ntag["key"]=tag.attrib["k"][d+1:]
                #if ntag["key"] == "street":
                    #print "GOTCH STREET!!"
                    #print ntag.get("value")
            else:
                ntag["key"]=tag.attrib["k"]
            ntag["value"]=tag.attrib["v"]
            if re.search(LOWER_COLON, k):
                d=k.find(":")
                ntag["type"]=tag.attrib["k"][:d] ##tag k="addr:street:name" v="Lincoln", ->:d=addr ->type=addr
            else:
                ntag["type"]="regular"
            #tags.append(ntag)
            #print ntag
            if ntag["key"] == "street":
                print ntag["value"]
                ntag["value"] = update_name(ntag.get('value'), mapping)
                #print ntag["value"]
            #print ntag
            tags.append(ntag)
            #print "TAG HERE!!!"
            #print tags
            
        #print "TAG HERE"
        #print tags
        return {'node': node_attribs, 'node_tags': tags}
    
    elif element.tag=="way":
        for i in way_attr_fields:
            way_attribs[i]=element.get(i)
        #print(way_attribs)
        id2=element.attrib["id"]
        for tag in element.iter("tag"):
            wtag={}
            wtag["id"]=id2
            k=tag.attrib['k']
            if re.search(LOWER_COLON, k):
                d=k.find(":")
                wtag["key"]=tag.attrib["k"][d+1:]
            else:
                wtag["key"]=tag.attrib["k"]
            wtag["value"]=tag.attrib["v"]
            if re.search(LOWER_COLON, k):
                d=k.find(":")
                wtag["type"]=tag.attrib["k"][:d]
            else:
                wtag["type"]="regular"
            if wtag["key"] == "street":
                print wtag["value"]
                wtag["value"] = update_name(wtag.get('value'), mapping)
                #print ntag["value"]
            tags.append(wtag)
        #print tags
        i=0
        for tag in element.iter("nd"):
            wnd={}
            wnd["id"]=id2
            wnd["position"]=i
            i=i+1
            wnd["node_id"]=tag.attrib["ref"]
            #print wnd
            way_nodes.append(wnd)
        #print(way_nodes)
        #print way_attribs
        #print way_nodes
        #print tags
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}
    

# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])
        


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)
