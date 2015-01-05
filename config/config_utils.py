'''
Created on Dec 10, 2014

@author: ayan
'''
from py_geoserver_rest_requests import GeoServerWorkspace, GeoServerDataStore


def setup_workspace(host, user, password, workspace_name,
                    person, organization, email,
                    wms_xml, wfs_xml, wcs_xml):
    # setup the workspace
    gsw = GeoServerWorkspace(host, user, password, workspace_name)
    ws_xml = gsw.create_workspace_xml()
    create_ws = gsw.create_workspace(payload=ws_xml)
    ns_xml = gsw.create_namespace_xml()
    mn = gsw.modify_namespace(payload=ns_xml)
    ms_xml = gsw.create_settings_xml(contact_name=person, organization=organization, email=email)
    ms = gsw.modify_settings(payload=ms_xml)
    # enable map services
    wms = gsw.create_services_xml(wms_xml)
    wms_enable = gsw.enable_map_services(service='wms', payload=wms)
    wfs = gsw.create_services_xml(wfs_xml)
    wfs_enable = gsw.enable_map_services(service='wfs', payload=wfs)
    wcs = gsw.create_services_xml(wcs_xml)
    wcs_enable = gsw.enable_map_services(service='wcs', payload=wcs)
    report_str = ('Created workspace {workspace_name}\n'
                  '\tCreate workspace status: {create_ws_status}\n'
                  '\tModify namespace status: {mod_ns_status}\n'
                  '\tModify settings status: {mod_settings_status}\n'
                  '\tEnable WMS status: {enable_wms_status}\n'
                  '\tEnable WFS status: {enable_wfs_status}\n'
                  '\tEnable WCS status: {enable_wcs_status}\n'
                  )
    setup_report = report_str.format(workspace_name=workspace_name,
                                     create_ws_status=create_ws.status_code,
                                     mod_ns_status=mn.status_code,
                                     mod_settings_status=ms.status_code,
                                     enable_wms_status=wms_enable.status_code,
                                     enable_wfs_status=wfs_enable.status_code,
                                     enable_wcs_status=wcs_enable.status_code
                                     )
    print(setup_report)
    results = {'create workspace': create_ws,
               'workspace name': workspace_name,
               'modify namespace': mn,
               'modify settings': ms,
               'Enable WMS': wms_enable,
               'Enable WFS': wfs_enable,
               'Enable WCS': wcs_enable
               }
    return results


def create_prms_datastore(host, user, password, workspace,
                          datastore_type, datastore, shapefile_path,
                          prms_animation, shapefile_nhru):
    gsds = GeoServerDataStore(host, user, password, workspace, datastore)
    ds_xml = gsds.create_ds_xml(datastore_type, desc='PRMS joining store', shapefile=shapefile_path,
                                prms_animation=prms_animation, shapefile_nhru=shapefile_nhru)
    ds_post = gsds.create_datastore(ds_xml)
    return ds_post


def create_shapefile_datastore(host, user, password, workspace,
                               datastore, shapefile_path, desc,
                               datastore_type='Shapefile'):
    shp_ds = GeoServerDataStore(host, user, password, workspace, datastore)
    ds_xml = shp_ds.create_ds_xml(datastore_type, desc, url=shapefile_path)
    ds_post = shp_ds.create_datastore(ds_xml)
    return ds_post


def parse_layernames(layers, sep=':'):
    layer_names = []
    for layer in layers:
        layer_name = layer.split(sep)[1]
        layer_names.append(layer_name)
    return layer_names