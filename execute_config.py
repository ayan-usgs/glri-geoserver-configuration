'''
Created on Jan 5, 2015

@author: ayan
'''

import argparse
from secure_params import USER, PASSWORD
from config.glri_geoserver import GlriGeoserver, GlriAfinch

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('tier', type=str)
    args = parser.parse_args()
    tier_name = args.tier.lower()
    
    if tier_name == 'dev':
        from tier import dev as c
    elif tier_name =='qa':
        from tier import qa as c
    elif tier_name == 'prod':
        from tier import prod as c
    else:
        raise Exception('Invalid tier name specified.')
    
    HOST = c.HOST
    
    # configure GLRI geoserver workspaces, styles, datastores, and layers
    config_glri_gs = GlriGeoserver(HOST, USER, PASSWORD, tier_name)
    # configure workspaces
    config_glri_gs.config_workspaces(c.WORKSPACE_NAMES, c.PERSON, c.EMAIL)
    # configure SLDs
    config_glri_gs.config_styles()
    # configure datastores
    config_glri_gs.config_datastores(c.INDIVIDUAL_DATASTORES)
    # configure PRMS annual layers
    annual_datastore = c.INDIVIDUAL_DATASTORES[0]['datastore_name']
    config_glri_gs.config_layers(layers=c.GLRI_PRMS_LAYERS, 
                                 layer_styles=c.GLRI_PRMS_SLDS, 
                                 projection=c.PRMS_CUSTOM_PROJECTION,
                                 datastore_name=annual_datastore
                                 )
    # configure PRMS monthly layers
    monthly_datastore = c.INDIVIDUAL_DATASTORES[1]['datastore_name']
    config_glri_gs.config_layers(layers=c.GLRI_PRMS_MONTHLY_LAYERS,
                                 layer_styles=None,  # still need to make these
                                 projection=c.PRMS_CUSTOM_PROJECTION,
                                 datastre_name=monthly_datastore
                                 )
    # configure GLRI AFINCH
    afinch_gs = GlriAfinch(HOST, USER, PASSWORD, tier_name)
    # configure AFINCH workspaces
    afinch_ws = afinch_gs.config_workspaces(workspace_names=c.AFINCH_WORKSPACES, 
                                            person='Developer Dude', 
                                            email='devdude@usgs.gov'
                                            )
    # configure AFINCH SLDs
    afinch_style = afinch_gs.config_afinch_styles()
    # configure AFINCH layers and datastores
    # configure glri-afinch workspace layers
    glri_afinch_layers = afinch_gs.create_glri_afinch_layers(c.AFINCH_LAYERS)