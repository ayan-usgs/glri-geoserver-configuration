'''
Created on Jan 5, 2015

@author: ayan
'''

# Datastore Types
DS_SHP = 'Shapefile'
DS_SHP_JOINING = 'Dbase Shapefile Joining Data Store'
NCDF_SHP_JOINING = 'NetCDF DSG Directory Shapefile Joining Data Store'
EPSG_900913 = 'EPSG:900913'
EPSG_4269 = 'EPSG:4269'
EPSG_4326 = 'EPSG:4326'

GCS_N_AMERICA_1983 = """
GEOGCS["GCS_North_American_1983", 
  DATUM["D_North_American_1983", 
    SPHEROID["GRS_1980", 6378137.0, 298.257222101]], 
  PRIMEM["Greenwich", 0.0], 
  UNIT["degree", 0.017453292519943295], 
  AXIS["Longitude", EAST], 
  AXIS["Latitude", NORTH]]
"""

PRMS_CUSTOM_PROJECTION = """
PROJCS["NAD_1983_Albers", 
  GEOGCS["GCS_North_American_1983", 
    DATUM["D_North_American_1983", 
      SPHEROID["GRS_1980", 6378137.0, 298.257222101]], 
    PRIMEM["Greenwich", 0.0], 
    UNIT["degree", 0.017453292519943295], 
    AXIS["Longitude", EAST], 
    AXIS["Latitude", NORTH]], 
  PROJECTION["Albers_Conic_Equal_Area"], 
  PARAMETER["central_meridian", -96.0], 
  PARAMETER["latitude_of_origin", 23.0], 
  PARAMETER["standard_parallel_1", 29.5], 
  PARAMETER["false_easting", 0.0], 
  PARAMETER["false_northing", 0.0], 
  PARAMETER["standard_parallel_2", 45.5], 
  UNIT["m", 1.0], 
  AXIS["x", EAST], 
  AXIS["y", NORTH]]
"""