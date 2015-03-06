'''
Created on Mar 6, 2015

@author: ayan
'''
from secure_params import USER, PASSWORD
from config.glri_geoserver import GlriGeoWebCache
from tier.dev import GWC_HOST, HOST, TILE_CACHED_WORKSPACES


glri_gwc = GlriGeoWebCache(GWC_HOST, HOST, USER, 
                           PASSWORD, TILE_CACHED_WORKSPACES
                           )
glri_gwc.tile_cache()