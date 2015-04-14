'''
Created on Apr 14, 2015

@author: ayan


    This script must be run as tomcat to
    be effective. Remember to restart
    the geoserver instance after running
    this script.
    
    Example:
        python animation_layer_xml.py <directory with the incorrect xml files>
        tomcat restart geoserver
        
    This script should be run after setting
    PRMS animation layer. It is a temporary
    measure until the underlying problem is 
    fixed by a Java developer.
    
    
'''
import os
import sys
import glob
import xml.etree.ElementTree as ET


def list_xml_files(file_directory, file_name='*.xml'):
    search_path = os.path.join(file_directory, file_name)
    xml_files = glob.glob(search_path)
    return xml_files


def set_timestep_records_to_record_count(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    record_count = root.find('.//recordCount')
    record_count_value = int(record_count.text)
    timestep_record_count = root.find('.//timeStepRecordCount')
    timestep_record_count_value = int(timestep_record_count.text)
    if timestep_record_count_value == -1:
        new_timestep_record_value = str(record_count_value)
        timestep_record_count.text = new_timestep_record_value
        tree.write(xml_file)
        print(xml_file)
    else:
        pass


if __name__ == '__main__':
    
    script, file_directory = sys.argv
    xml_files = list_xml_files(file_directory)
    for xml_file in xml_files:
        set_timestep_records_to_record_count(xml_file)