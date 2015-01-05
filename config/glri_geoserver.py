'''
Created on Dec 9, 2014

@author: ayan
'''
import os
import glob
from py_geoserver_rest_requests import GeoServerLayers, GeoServerDataStore, GeoServerWorkspace
from py_geoserver_rest_requests.map_services import WFS, WCS, WMS
from py_geoserver_rest_requests.utilities import get_filename_from_path, get_items_of_interest
from geoserver.catalog import Catalog
from config.config_utils import setup_workspace, create_prms_datastore, create_shapefile_datastore
from tier.global_constants import DS_SHP, DS_SHP_JOINING, NCDF_SHP_JOINING


class GlriGeoserver(object):
    
    file_path = os.path.abspath(os.path.dirname(__file__))
    abs_path = os.path.abspath(os.path.dirname(file_path))
    
    def __init__(self, host, user, password, tier_name):
        self.host = host
        self.user = user
        self.password = password
        self.tier_name = tier_name
        
    def config_workspaces(self, workspace_names, person, email,
                          org_name='USGS Center for Integrated Data Analytics'):
        ws_config_requests = []
        for workspace_name in workspace_names:
            setup_ws = setup_workspace(self.host, self.user, self.password,
                                       workspace_name, person, org_name,
                                       email, WMS, WFS, WCS
                                       )
            ws_config_requests.append(setup_ws)
        return ws_config_requests
    
    def config_styles(self, sld_path='/files/slds/glri/*.sld'):
        catalog = Catalog(self.host, self.user, self.password, True)
        sld_path = '{0}{1}'.format(self.abs_path, sld_path)
        norm_sld_path = os.path.normpath(sld_path)
        sld_files = glob.glob(norm_sld_path)
        configured_styles = []
        for sld_file in sld_files:
            with open(sld_file, 'r') as sld:
                sld_filename = os.path.basename(sld_file)
                sld_name = os.path.splitext(sld_filename)[0]
                sld_content = sld.read()
                if catalog.get_style(sld_name) is None:
                    catalog.create_style(sld_name, sld_content)
                    created_sld_str = 'Created {0}\n'.format(sld_name)
                    print(created_sld_str)
                    configured_styles.append(created_sld_str)
                else:
                    catalog.create_style(sld_name, sld_content, overwrite=True)
                    overwrite_sld_str = 'Overwrote {0}\n'.format(sld_name)
                    print(overwrite_sld_str)
                    configured_styles.append(overwrite_sld_str)
        return configured_styles
    
    def config_datastores(self, datastores):
        config_ds_requests = []
        for datastore in datastores:
            workspace = datastore['workspace']
            ds_type = datastore['datastore_type']
            ds_name = datastore['datastore_name']
            shp_path = datastore['shp_path']
            prms_animation = datastore['prms_animation']
            nhru = datastore['shapefile_nhru']
            create_ds = create_prms_datastore(self.host, self.user, self.password, 
                                              workspace, ds_type, ds_name, 
                                              shp_path, prms_animation, nhru
                                              )
            result_dict = {'datastore name': ds_name, 'create status code': create_ds}
            report_str = ('Created datastore {datastore_name} on {host_name}\n'
                          '\tWorkspace name: {workspace}\n'
                          '\tStatus Code: {create_ds_status}\n'
                          )
            config_ds_report = report_str.format(datastore_name=ds_name,
                                                 host_name=self.host,
                                                 workspace=workspace,
                                                 create_ds_status=create_ds.status_code
                                                 )
            print(config_ds_report)
            config_ds_requests.append(result_dict)
        return config_ds_requests
    
    def config_layers(self, layers, layer_styles, projection, workspace_name='glri'):
        lyr_config_requests = []
        for layer in layers:
            gsl = GeoServerLayers(gs_host=self.host, gs_user=self.user, 
                                  gs_password=self.password, 
                                  workspace_name=workspace_name, 
                                  datastore_name='annual_animation_feb2014', 
                                  lyr_name=layer
                                  )
            feature_type_xml = gsl.create_feature_type_xml(native_name=layer, native_crs=projection)
            post_feature = gsl.create_feature_type(payload=feature_type_xml)
            recalc_feature = gsl.modify_feature_type(payload=feature_type_xml)
            layer_style_xml = gsl.create_lyr_style_xml(style_name=layer_styles)
            change_layer_style = gsl.modify_layer_style(payload=layer_style_xml)
            requests = {'layer name': layer,
                        'post feature': post_feature,
                        'recalc feature': recalc_feature,
                        'change layer style': change_layer_style
                        }
            report_str = ('Created layer {layer_name} on {host_name}\n'
                          '\tWorkspace name: {workspace}\n'
                          '\tDatastore name: {datastore}\n'
                          '\tPost feature status: {post_feature_status}\n'
                          '\tRecalculate feature status: {recalc_status}\n'
                          '\tChange layer style status: {change_style_status}\n'
                          )
            config_lyr_report = report_str.format(layer_name=layer,
                                                  host_name=self.host,
                                                  workspace=gsl.workspace_name,
                                                  datastore=gsl.ds_name,
                                                  post_feature_status=post_feature.status_code,
                                                  recalc_status=recalc_feature.status_code,
                                                  change_style_status=change_layer_style.status_code
                                                  )
            print(config_lyr_report)
            lyr_config_requests.append(requests)
        return lyr_config_requests
    
    
class GlriAfinch(object):
    
    file_path = os.path.abspath(os.path.dirname(__file__))
    abs_path = os.path.abspath(os.path.dirname(file_path))
    
    def __init__(self, host, user, password, tier_name):
        self.host = host
        self.user = user
        self.pwd = password
        self.tier_name = tier_name
        self.glri_config = GlriGeoserver(self.host, self.user, 
                                         self.pwd, self.tier_name
                                         )
        
    def config_workspaces(self, workspace_names, person, email):
        config_ws = self.glri_config.config_workspaces(workspace_names, person, email)
        return config_ws
    
    def config_afinch_styles(self, sld_path='/files/slds/afinch/*.sld'):
        config_styles = self.glri_config.config_styles(sld_path)
        return config_styles
    
    def create_glri_afinch_layers(self, afinch_layers):
        all_results = []
        for afinch_layer in afinch_layers:
            workspace = afinch_layer.workspace
            store_type = afinch_layer.store_type
            store_name = afinch_layer.store_name
            store_desc = afinch_layer.desc
            lyr_name = afinch_layer.lyr_name
            # create the necessary datastores
            if store_name is None:
                store_name = lyr_name
            datastore = GeoServerDataStore(self.host, self.user, self.pwd,
                                           workspace, store_name
                                           )
            if store_type == DS_SHP:
                store_params = {'url': afinch_layer.shp_file}
                ds_xml = datastore.create_ds_xml(store_type, store_desc, **store_params)
                create_ds = datastore.create_datastore(ds_xml)
            elif store_type == DS_SHP_JOINING:
                store_params = {'dbase_field': afinch_layer.join_field,
                                'dbase_file': afinch_layer.dbase_file,
                                'shapefile': afinch_layer.shp_file
                                }
                ds_xml = datastore.create_ds_xml(store_type, store_desc, **store_params)
                create_ds = datastore.create_datastore(ds_xml)
            elif store_type == NCDF_SHP_JOINING:
                store_params = {'shapefile_path': afinch_layer.shp_file,
                                'shapefile_station': afinch_layer.station,
                                'netcdf_path': afinch_layer.netcdf_file,
                                'default': False
                                }
                ds_xml = datastore.create_ds_xml(store_type, store_desc, **store_params)
                create_ds = datastore.create_datastore(ds_xml)
            else:
                raise Exception('Unknown datastore type specified in AfinchLayer specification.')
            # create the layers after the stores have been created
            layer = GeoServerLayers(self.host, self.user, self.pwd,
                                    workspace, store_name, lyr_name
                                    )
            feature_type_xml = layer.create_feature_type_xml(native_name=afinch_layer.native_name, 
                                                             native_crs=afinch_layer.native_srs, 
                                                             srs=afinch_layer.declared_srs, 
                                                             desc_str='Contents of file',
                                                             proj_policy=afinch_layer.proj_policy
                                                             )
            create_feature_type = layer.create_feature_type(feature_type_xml)
            recalc_feature_type = layer.modify_feature_type(feature_type_xml, True)
            feature_styling_xml = layer.create_lyr_style_xml(style_name=afinch_layer.styles)
            update_style = layer.modify_layer_style(feature_styling_xml)
            
            message_template = ('Created {layer} on {host_name}\n'
                                '\tWorkspace name: {workspace}\n'
                                '\tDatastore name: {datastore}\n'
                                '\tCreate datastore: {ds_create_status}\n'
                                '\tCreate feature: {feature_create_status}\n'
                                '\tRecalculate bounds: {recalc_status}\n'
                                '\tUpdate styling: {update_style_status}\n'
                                )
            report_message = message_template.format(layer=lyr_name,
                                                     host_name=self.host,
                                                     datastore=store_name,
                                                     workspace=workspace,
                                                     ds_create_status=create_ds.status_code,
                                                     feature_create_status=create_feature_type.status_code,
                                                     recalc_status=recalc_feature_type.status_code,
                                                     update_style_status=update_style.status_code
                                                     )
            print(report_message)
            results = {'workspace': workspace,
                       'layer_name': lyr_name,
                       'datastore': store_name,
                       'create_ds': create_ds,
                       'create_feature': create_feature_type,
                       'recalc_bounds': recalc_feature_type,
                       'update_style': update_style
                       }
            all_results.append(results)
        return all_results
            
    def create_nhdflowline_layers(self, path_list, style, 
                                  workspace_name='NHDPlusFlowlines', 
                                  join_field='COMID', 
                                  description='NHDFlowlines'):
        result_list = []
        for path_tuple in path_list:
            subregion = path_tuple.subregion
            dbf_path = path_tuple.dbf_path
            shp_path = path_tuple.shp_path
            layer_native_name = get_filename_from_path(dbf_path, '.dbf')
            layer_name = '{0}_{1}'.format(layer_native_name, subregion)
            gsds = GeoServerDataStore(gs_host=self.host, 
                                      gs_user=self.user, 
                                      gs_password=self.pwd,
                                      workspace_name=workspace_name, 
                                      datastore_name=subregion
                                      )
            gsl = GeoServerLayers(gs_host=self.host, 
                                  gs_user=self.user, 
                                  gs_password=self.pwd,
                                  workspace_name=workspace_name, 
                                  datastore_name=subregion,
                                  lyr_name=layer_name
                                  )
            ds_type = 'Dbase Shapefile Joining Data Store'
            ds_xml = gsds.create_ds_xml(datastore_type=ds_type, 
                                        desc=description,
                                        dbase_field=join_field, 
                                        dbase_file=dbf_path, 
                                        shapefile=shp_path
                                        )
            create_ds = gsds.create_datastore(ds_xml)
            feature_xml = gsl.create_feature_type_xml(layer_native_name)
            create_feature = gsl.create_feature_type(feature_xml)
            recalc_feature = gsl.modify_feature_type(feature_xml, True)
            change_lyr_style_xml = gsl.create_lyr_style_xml(style)
            change_lyr_style = gsl.modify_layer_style(change_lyr_style_xml)
            lyr_config_str = ('Configuration of layer {layer_name} on {host_name}\n'
                              '\tWorkspace name: {workspace}\n'
                              '\tDatastore name: {datastore}\n'
                              '\tCreated datastore: {datastore_status}\n'
                              '\tPosted Feature: {create_feature_status}\n'
                              '\tRecalculated BBox: {recalc_feature_status}\n'
                              '\tChanged Layer Style: {change_style_status}\n'
                              )
            lyr_config_report = lyr_config_str.format(layer_name=layer_name,
                                                      host_name=self.host,
                                                      workspace=workspace_name,
                                                      datastore=gsds.ds_name,
                                                      datastore_status=create_ds.status_code,
                                                      create_feature_status=create_feature.status_code,
                                                      recalc_feature_status=recalc_feature.status_code,
                                                      change_style_status=change_lyr_style.status_code
                                                      )
            print(lyr_config_report)
            results = {'create datastore': create_ds,
                       'post feature': create_feature,
                       'recalc bbox': recalc_feature,
                       'change layer style': change_lyr_style
                       }
            result_list.append(results)
        return result_list
    
    def create_nhdhuc_layers(self, huc_workspace, huc_shp_path, huc_shp_style, 
                             native_projection='EPSG:4269', desc='shapefile'):
        layer_name = get_filename_from_path(huc_shp_path, '.shp')
        create_huc_ds = create_shapefile_datastore(self.host, self.user, self.pwd,
                                                   huc_workspace, layer_name,
                                                   huc_shp_path, desc
                                                   )
        create_huc_ds_status_template = ('Created datastore {ds_name} on {host_name}\n'
                                         '\tWorkspace name: {workspace}\n'
                                         '\tShapefile path: {shp_path}\n'
                                         '\tStyle: {style}\n'
                                         '\tStatus code: {status_code}\n'
                                         )
        ds_create_message = create_huc_ds_status_template.format(ds_name=layer_name,
                                                                 host_name=self.host,
                                                                 workspace=huc_workspace,
                                                                 shp_path=huc_shp_path,
                                                                 style=huc_shp_style,
                                                                 status_code=create_huc_ds.status_code
                                                                 )
        print(ds_create_message)
        create_huc_lyr = self.glri_config.config_layers(layers=[layer_name], 
                                                        layer_styles=huc_shp_style, 
                                                        projection=native_projection, 
                                                        workspace_name=huc_workspace
                                                        )
        return create_huc_ds, create_huc_lyr
    
    def config_nhdflowline_lyr_grp(self, workspace_name, lyr_grp_name, 
                                   style, search='PlusFlowlineVAA', 
                                   min_x='0', max_x='0', min_y='0', max_y='0'):
        gsw = GeoServerWorkspace(self.host, self.user, self.pwd, workspace_name)
        existing_layers = gsw.get_ws_layers()
        interesting_layers = get_items_of_interest(existing_layers, search)
        lyr_grp_xml = gsw.create_ws_lyr_grp_xml(lyr_grp_name=lyr_grp_name, 
                                                layer_list=interesting_layers, 
                                                style_name=style, 
                                                min_x=min_x, 
                                                max_x=max_x, 
                                                min_y=min_y, 
                                                max_y=max_y
                                                )
        post_lyr_grp = gsw.create_ws_layer_grp(lyr_grp_xml)
        report_str = ('Posted layer group xml for {lyr_grp_name} on {host_name}\n'
                      '\tStatus Code: {status_code}\n'
                      )
        post_report = report_str.format(lyr_grp_name=lyr_grp_name,
                                        host_name=self.host, 
                                        status_code=post_lyr_grp.status_code
                                        )
        print(post_report)
        return post_lyr_grp