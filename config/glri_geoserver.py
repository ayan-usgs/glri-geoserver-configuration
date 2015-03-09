'''
Created on Dec 9, 2014

@author: ayan
'''
import os
import glob
import time
import datetime
from py_geoserver_rest_requests import GeoServerLayers, GeoServerDataStore, GeoWebCacheSetUp
from py_geoserver_rest_requests.map_services import WFS, WCS, WMS
from py_geoserver_rest_requests.utilities import get_filename_from_path, get_ws_layers, get_layer_default_styles
from geoserver.catalog import Catalog
from config_utils import setup_workspace, create_prms_datastore, create_shapefile_datastore
from tier.global_constants import DS_SHP, DS_SHP_JOINING, NCDF_SHP_JOINING
from tier.dev import AFINCH_LAYERS


class GlriGeoWebCache(object):
    """
    Create a tile cache. All layers in the specified
    workspaces will be cached.
    
    :param str gwc_host: geowebcache rest URL
    :param str gs_host: geoserver rest URL
    :param str gs_user: geoserver username
    :param str gw_password: geoserver password
    :param workspaces: iterable of workspaces containing layers to be tile cached
    :type workspaces: list or tuple
    
    """
    def __init__(self, gwc_host, gs_host, gs_user, gs_password, workspaces):
        self.gwc_host = gwc_host
        self.gs_host = gs_host
        self.gs_user = gs_user
        self.gs_pwd = gs_password
        self.workspaces = workspaces
        
    def _get_layers(self):
        """
        Get all the layers belonging to the
        specified workspaces.
        
        :return: list of tuples of form (workspace_name, [list of layers belonging to the workspace])
        :rtype: list
        
        """
        layers = get_ws_layers(self.gs_host, self.gs_user, 
                               self.gs_pwd, self.workspaces
                               )
        return layers
    
    def _get_layer_default_styles(self):
        """
        Get the default style for each layer.
        
        :return: list of tuples containing the workspace name and a dictionary; the dictionary contains keys: layer_name, style_name
        :rtype: list
        
        """
        layers = self._get_layers()
        layers_with_default_styles = get_layer_default_styles(self.gs_host, 
                                                              self.gs_user, 
                                                              self.gs_pwd, 
                                                              layers
                                                              )
        return layers_with_default_styles
    
    def tile_cache(self, zoom_start=0, zoom_end=12, 
                   threads=2, check_interval=10, 
                   layer_data=AFINCH_LAYERS, seed_type='seed',
                   gridset_id='EPSG:900913'):
        """
        Execute the tile cache for the specified workspaces.
        
        :param int zoom_start: starting zoom level
        :param int zoom_end: ending zoom level
        :param int threads: number of threads to be used for tile caching
        :param float check_interval: frequency in seconds to check on tile caching progress for a layer
        :param layer_data: GLRI AFINCH layer parameters
        :type layer_data: list of named tuples
        :param str seed_type: specify 'seed', 'reseed', or 'truncate'
        :param str gridset_id: projection that should be cached; this should be the same as the map project used in the app
        :return: urls and status codes of posted seed requests
        :rtype: list
        
        """
        seed_requests = []
        for layer_datum in layer_data:
            tile_cache = layer_datum.tile_cache
            if tile_cache:
                workspace_name = layer_datum.workspace
                layer_name = layer_datum.lyr_name
                defined_cache_style = layer_datum.cache_style
                if defined_cache_style is not None:
                    cache_style = defined_cache_style
                else:
                    cache_style = layer_datum.styles[0]
                gwc = GeoWebCacheSetUp(self.gwc_host, self.gs_user, self.gs_pwd, 
                                       workspace_name, layer_name
                                       )
                seed_xml = gwc.create_seed_xml(cache_style, zoom_start=zoom_start, 
                                               zoom_stop=zoom_end, threads=threads,
                                               gridset_id=gridset_id, seed_type=seed_type
                                               )
                seed = gwc.seed_request(seed_xml)
                # post_url = '{0}/seed/{1}:{2}.xml'.format(self.gwc_host, workspace_name, layer_name)
                # seed = gwc.req_sess.post(post_url, data=seed_xml, params={'workspace': workspace_name})
                seed_url = seed.url
                seed_status = seed.status_code
                seed_message = ('Posted seed xml to {0} ' 
                                'with a {1} status code.').format(seed_url, seed_status)
                print(seed_message)
                progress_message = 'Caching progress on {0}:'.format(layer_name)
                print(progress_message)
                array_length = 1
                while array_length > 0:
                    progress = gwc.query_task_status()
                    progress_str = '{0}: {1} - {2}'.format(datetime.datetime.now(), layer_name, progress[1])
                    print(progress_str)
                    long_array = progress[1]['long-array-array']
                    array_length = len(long_array)
                    time.sleep(check_interval)
                seed_requests.append((seed_url, seed_status))
        return seed_requests
        

class GlriGeoserver(object):
    """
    This class contains methods for the configuration
    of the glri workspace on GLRI GeoServer instances.
    
    :param str host: geoserver rest URL
    :param str user: geoserver username
    :param str password: geoserver password
    :param str tier_name: tier of the geoserver instance (e.g. local, dev, qa, prod)
    
    """
    
    file_path = os.path.abspath(os.path.dirname(__file__))
    abs_path = os.path.abspath(os.path.dirname(file_path))
    
    def __init__(self, host, user, password, tier_name):
        self.host = host
        self.user = user
        self.password = password
        self.tier_name = tier_name
        
    def config_workspaces(self, workspace_names, person, email,
                          org_name='USGS Center for Integrated Data Analytics'):
        """
        Create the workspaces
        
        :param list workspace_names: list of workspace names to be created
        :param str person: person responsible for the workspace
        :param str email: person's email address
        :param str org_name: name of organization that the person works for
        :return: list of requests objects
        :rtype: list
        
        """
        ws_config_requests = []
        for workspace_name in workspace_names:
            setup_ws = setup_workspace(self.host, self.user, self.password,
                                       workspace_name, person, org_name,
                                       email, WMS, WFS, WCS
                                       )
            ws_config_requests.append(setup_ws)
        return ws_config_requests
    
    def config_styles(self, sld_path='/files/slds/glri/*.sld'):
        """
        Create SLDs within GeoServer.
        
        :param str sld_path: path to sld files relative to the project directory
        :return: list of strings reporting post/overwrite statuses
        :rtype: list
        
        """
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
        """
        Configure glri datastores.
        
        :param datastores: list of dictionaries containing datastore parameters
        :type datastores: list of dictionaries
        :return: list of dictionaries containing the datastore name (datstore_name) and request object (ds_request)
        :rtype: list
        
        """
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
            result_dict = {'datastore_name': ds_name, 'ds_request': create_ds}
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
    
    def config_layers(self, layers, layer_styles, projection, 
                      workspace_name='glri', datastore_name='annual_animation_feb2014'):
        """
        Configure glri layers.
        
        :param list layers: list of layers to be created
        :param list layer_styles: styles that the layers should be published with
        :param str projection: projection that should be used for the feature type
        :param str workspace_name: workspace that the layers belong to
        :param str datastore_name: datastore that the layers belong to
        :return: list of dictionaries containing request objects
        :rtype: list
        
        """
        lyr_config_requests = []
        for layer in layers:
            gsl = GeoServerLayers(gs_host=self.host, gs_user=self.user, 
                                  gs_password=self.password, 
                                  workspace_name=workspace_name, 
                                  datastore_name=datastore_name, 
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
    """
    This class contains methods for the configuration
    of the glri-afinch, NHDPlusFlowlines, and NHDPlusHUCs 
    workspaces on GLRI GeoServer instances.
    
    :param str host: geoserver rest URL
    :param str user: geoserver username
    :param str password: geoserver password
    :param str tier_name: tier of the geoserver instance (e.g. local, dev, qa, prod)
    
    """
    
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
        """
        Configure workspaces.
        
        :param list workspace_names: list of workspace names to be created
        :param str person: person responsible for the workspace
        :param str email: person's email address
        :return: list of requests objects
        :rtype: list
        
        .. note:: composition of GlriGeoserver.config_workspaces
        .. seealso:: :classmethod:'GlriGeoserver.config_workspaces'
        
        """
        config_ws = self.glri_config.config_workspaces(workspace_names, person, email)
        return config_ws
    
    def config_afinch_styles(self, sld_path='/files/slds/afinch/*.sld'):
        """
        Create SLDs within GeoServer.
        
        :param str sld_path: path to sld files relative to the project directory
        :return: list of strings reporting post/overwrite statuses
        :rtype: list
        
        .. note:: composition of GlriGeoserver.config_styles
        .. seealso:: :classmethod:'GlriGeoserver.config_styles'
        
        """
        config_styles = self.glri_config.config_styles(sld_path)
        return config_styles
    
    def create_glri_afinch_layers(self, afinch_layers):
        """
        Configure GLRI AFINCH layers.
        
        :param afinch_layers: AFINCH layer names and parameters
        :type afinch_layers: list of namedtuples, nametuples should contain the following attributes: 
                             workspace, lyr_name, native_name, native_srs, declared_srs, proj_policy, styles, store_type,
                             store_name, desc, shp_file, dbase_file, netcdf_file, join_field, station
        :return: dictionaries containing requests objects from datastore creation, feature type creation, recalculation, and updating styles
        :rtype: list
        
        """
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
    
    def create_nhdhuc_layers(self, huc_workspace, huc_shp_path, huc_shp_style, 
                             native_projection='EPSG:4269', desc='shapefile'):
        """
        Create datastores and layers for the NHDPlusHUCs workspace.
        
        :param str huc_workspace: workspace where the datastores and layers should live
        :param str huc_shp_path: absolute path to the HUC shapefile on the server
        :param huc_shp_style: style(s) that should be associated with HUC layers
        :type huc_shp_style: str or list or tuple
        :param str native_projection: native projection of the HUC shapefile
        :param str desc: description for the layer
        :return: requests.request object from datastore and layer (this is a dictionary) creation
        :rtype: tuple
        
        .. note:: layer creation execution via composition from GlriGeoServer.config_layers
        
        """
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
    