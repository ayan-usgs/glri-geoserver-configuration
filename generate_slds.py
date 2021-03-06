'''
Created on Mar 19, 2015

@author: ayan
'''
import os
from create_sld.glri_sld_creation import create_glri_sld
from secure_params import ANIMATION_DIR


# figure out the directory to put the SLDs
file_path = file_path = os.path.abspath(os.path.dirname(__file__))
sld_path = os.path.join(file_path, 'files/slds/glri')

# create annual SLDs
annual_slds = create_glri_sld(ANIMATION_DIR, 'polygon',
                              xml_writepath=sld_path,
                              pretty_print=True
                              )


'''
# create monthly SLDs
monthly_slds = create_glri_sld(MONTHLY_ANIMATION_DIR, 'polygon', 
                               xml_writepath=sld_path,
                               pretty_print=True, sld_name_suffix='monthly'
                               )
'''
