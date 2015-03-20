'''
Created on Mar 19, 2015

@author: ayan
'''
from create_sld.glri_sld_creation import create_glri_sld


monthly_animation_dir = 'C:\\Users\\ayan\\Desktop\\tmp\\LKM_Nov2013_monthly_last10yrs\\hru_means'


monthly_slds = create_glri_sld(monthly_animation_dir, 'polygon', 
                               xml_writepath='C:\\Users\\ayan\\Desktop\\tmp\\montly_slds',
                               pretty_print=True, sld_name_suffix='monthly'
                               )