'''
Created on Dec 9, 2014

@author: ayan
'''
from collections import namedtuple
from global_constants import (DS_SHP, DS_SHP_JOINING, NCDF_SHP_JOINING,
                              EPSG_900913, EPSG_4269, EPSG_4326,
                              GCS_N_AMERICA_1983, PRMS_CUSTOM_PROJECTION)


AfinchLayer = namedtuple('AfinchLayer', ['workspace', 
                                         'lyr_name',
                                         'native_name', 
                                         'native_srs',
                                         'declared_srs',
                                         'proj_policy',
                                         'styles',
                                         'store_type',
                                         'store_name',
                                         'desc',
                                         'shp_file',
                                         'dbase_file',
                                         'netcdf_file',
                                         'join_field',
                                         'station'
                                         ]
                         )
WORKSPACE_NAMES = ['glri']
AFINCH_WORKSPACES = [#'NHDPlusFlowlines', 
                     #'NHDPlusHUCs', 
                     'NHDCatchments', 
                     'glri-afinch'
                     ]
PERSON = 'Developer Dude'
EMAIL = 'devdude@usgs.gov'

INDIVIDUAL_DATASTORES = [{'workspace': WORKSPACE_NAMES[0], 
                          'datastore_type': 'PRMS Animation Directory Shapefile Joining Data Store', 
                          'datastore_name': 'annual_animation_feb2014', 
                          'shp_path': '/opt/tomcat/data/GLRI/PRMS/lkm_hru_simp/lkm_hru_SimplifyPolygon.shp',
                          'prms_animation': '/opt/tomcat/data/GLRI/PRMS/annual_animation_feb2014/',
                          'shapefile_nhru': 'GRIDCODE', 
                          }]

GLRI_PRMS_LAYERS = ['cccma_cgcm3_1.20c3m.1981-2000.annual', 'cccma_cgcm3_1.sresa1b.2046-2065.annual', 'cccma_cgcm3_1.sresa1b.2081-2100.annual', 
                    'cccma_cgcm3_1.sresa2.2046-2065.annual', 'cccma_cgcm3_1.sresa2.2081-2100.annual', 'cccma_cgcm3_1.sresb1.2046-2065.annual', 
                    'cccma_cgcm3_1.sresb1.2081-2100.annual', 'cnrm_cm3.20c3m.1981-2000.annual', 'cnrm_cm3.sresa1b.2046-2065.annual', 
                    'cnrm_cm3.sresa1b.2081-2100.annual', 'cnrm_cm3.sresa2.2046-2065.annual', 'cnrm_cm3.sresa2.2081-2100.annual', 
                    'cnrm_cm3.sresb1.2046-2065.annual', 'cnrm_cm3.sresb1.2081-2100.annual', 'csiro_mk3_5.20c3m.1981-2000.annual', 
                    'csiro_mk3_5.sresa1b.2046-2065.annual', 'csiro_mk3_5.sresa1b.2081-2100.annual', 'csiro_mk3_5.sresa2.2046-2065.annual', 
                    'csiro_mk3_5.sresa2.2081-2100.annual', 'csiro_mk3_5.sresb1.2046-2065.annual', 'csiro_mk3_5.sresb1.2081-2100.annual', 
                    'gfdl_cm2_0.20c3m.1981-2000.annual', 'gfdl_cm2_0.sresa1b.2046-2065.annual', 'gfdl_cm2_0.sresa1b.2081-2100.annual', 
                    'gfdl_cm2_0.sresa2.2046-2065.annual', 'gfdl_cm2_0.sresa2.2081-2100.annual', 'gfdl_cm2_0.sresb1.2046-2065.annual', 
                    'gfdl_cm2_0.sresb1.2081-2100.annual', 'giss_model_e_r.20c3m.1981-2000.annual', 'giss_model_e_r.sresa1b.2046-2065.annual', 
                    'giss_model_e_r.sresa1b.2081-2100.annual', 'giss_model_e_r.sresa2.2046-2065.annual', 'giss_model_e_r.sresa2.2081-2100.annual', 
                    'giss_model_e_r.sresb1.2046-2065.annual', 'giss_model_e_r.sresb1.2081-2100.annual', 'miub_echo_g.20c3m.1981-2000.annual', 
                    'miub_echo_g.sresa1b.2046-2065.annual', 'miub_echo_g.sresa1b.2081-2100.annual', 'miub_echo_g.sresa2.2046-2065.annual', 
                    'miub_echo_g.sresa2.2081-2100.annual', 'miub_echo_g.sresb1.2046-2065.annual', 'miub_echo_g.sresb1.2081-2100.annual', 
                    'mpi_echam5.20c3m.1981-2000.annual', 'mpi_echam5.sresa1b.2046-2065.annual', 'mpi_echam5.sresa1b.2081-2100.annual', 
                    'mpi_echam5.sresa2.2046-2065.annual', 'mpi_echam5.sresa2.2081-2100.annual', 'mpi_echam5.sresb1.2046-2065.annual', 
                    'mpi_echam5.sresb1.2081-2100.annual', 'mri_cgcm2_3_2a.20c3m.1981-2000.annual', 'mri_cgcm2_3_2a.sresa1b.2046-2065.annual', 
                    'mri_cgcm2_3_2a.sresa1b.2081-2100.annual', 'mri_cgcm2_3_2a.sresa2.2046-2065.annual', 'mri_cgcm2_3_2a.sresa2.2081-2100.annual', 
                    'mri_cgcm2_3_2a.sresb1.2046-2065.annual', 'mri_cgcm2_3_2a.sresb1.2081-2100.annual'
                    ]

GLRI_PRMS_SLDS = ['polygon', 
                  'soil_moist', 
                  'recharge', 
                  'hru_ppt', 
                  'hru_rain', 
                  'hru_snow', 
                  'tminf', 
                  'tmaxf', 
                  'potet', 
                  'hru_actet', 
                  'pkwater_equiv', 
                  'snowmelt', 
                  'hru_streamflow_out'
                  ]

AFINCH_LAYERS = [AfinchLayer(workspace=AFINCH_WORKSPACES[-1], 
                             lyr_name='GageLoc',
                             native_name='PlusFlowlineVAA',
                             native_srs=GCS_N_AMERICA_1983,
                             declared_srs=EPSG_900913,
                             proj_policy='REPROJECT_TO_DECLARED',
                             styles=('GageLocStreamOrder', ),
                             store_type=DS_SHP_JOINING, 
                             store_name=None, 
                             desc='AFINCH GageLoc Shapefile joined with NHDPlusFlowlineVAA DBF',
                             shp_file='/opt/tomcat/data/GLRI/AFINCH/GageLoc.shp',
                             dbase_file='/opt/tomcat/data/GLRI/AFINCH/PlusFlowlineVAA.dbf',
                             netcdf_file=None,
                             join_field='REACHCODE',
                             station=None
                             ),
                 AfinchLayer(workspace=AFINCH_WORKSPACES[-1], 
                             lyr_name='NHDFlowline',
                             native_name='PlusFlowlineVAA',
                             native_srs=GCS_N_AMERICA_1983, 
                             declared_srs=EPSG_900913,
                             proj_policy='REPROJECT_TO_DECLARED', 
                             styles=('FlowlineStreamOrder', ),
                             store_type=DS_SHP_JOINING, 
                             store_name=None, 
                             desc='AFINCH NHDFlowline Shapefile joined with NHD PlusFlowlineVAA DBF',
                             shp_file='/opt/tomcat/data/GLRI/AFINCH/NHDFlowline.shp',
                             dbase_file='opt/tomcat/data/GLRI/AFINCH/PlusFlowlineVAA.dbf',
                             netcdf_file=None,
                             join_field='COMID',
                             station=None
                             ),
                 AfinchLayer(workspace=AFINCH_WORKSPACES[-1], 
                             lyr_name='nhd_v2_1_flowline_w_streamorder',
                             native_name='NHDFlowline',
                             native_srs=GCS_N_AMERICA_1983,
                             declared_srs=EPSG_4269,
                             proj_policy='FORCE_DECLARED',
                             styles=('line', 'FlowlineStreamOrder'), 
                             store_type=DS_SHP, 
                             store_name=None, 
                             desc='NHDFlowline v2.1 with streamorder attrib',
                             shp_file='/opt/tomcat/data/GLRI/AFINCH/nhd_v21/flowline/NHDFlowline.shp',
                             dbase_file=None,
                             netcdf_file=None,
                             join_field=None,
                             station=None
                             ),
                 AfinchLayer(workspace=AFINCH_WORKSPACES[-1], 
                             lyr_name='nhd_v2_1_catch_w_afinch_data',
                             native_name='afinch_catch', 
                             native_srs=GCS_N_AMERICA_1983,
                             declared_srs=EPSG_4269,
                             proj_policy='FORCE_DECLARED',
                             styles=('polygon', 'afinch_catch_YCCMean'),
                             store_type=NCDF_SHP_JOINING, 
                             store_name=None, 
                             desc='NHD v2.1 catchments with AFINCH catchment data joined',
                             shp_file='/opt/tomcat/data/GLRI/AFINCH/nhd_v21/catchment/Catchment.shp',
                             netcdf_file='/opt/tomcat/data/GLRI/netcdf/afinch_catch.nc',
                             dbase_file=None,
                             join_field=None,
                             station='GRIDCODE'
                             ),
                 AfinchLayer(workspace=AFINCH_WORKSPACES[-1], 
                             lyr_name='throwaway_afinch_reach',
                             native_name='afinch_reach', 
                             native_srs=GCS_N_AMERICA_1983,
                             declared_srs=EPSG_4326,
                             proj_policy='FORCE_DECLARED',
                             styles=None, 
                             store_type=NCDF_SHP_JOINING, 
                             store_name='throwaway2',
                             desc=None,
                             shp_file='/opt/tomcat/data/GLRI/AFINCH/nhd_v21/flowline/NHDFlowline.shp',
                             dbase_file=None,
                             netcdf_file='/opt/tomcat/data/GLRI/netcdf/afinch_reach.nc',
                             join_field=None,
                             station='COMID'
                             )
                 ]