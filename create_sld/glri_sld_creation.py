import os
from py_geoserver_rest_requests import GeoServerLayers, GeoServerStyles
from py_geoserver_rest_requests.utilities import get_filename_from_path
from create_sld.write_sld import LxmlSLDAttrBins
from create_sld.utils import write_to_file
from parse_animations.statistics import PandasStats, SldBins
from parse_animations.utils import get_filenames_from_directory
from parse_animations.headers import ANIMATION_HEADERS, ATTRIBUTE_UNITS
from tier.global_constants import PRMS_CUSTOM_PROJECTION

# spectrum from red to green
COLORS = ('#E12300', '#E54C00', '#EA7500', '#EF9E00', '#F4C700', '#F9F000', '#D3DB0C', '#AEC618', '#89B124', '#649C32')
# 10 percentile bins
PERCENTILES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

FILE_PATH = os.path.abspath(os.path.dirname(__file__))
ABS_PATH = os.path.abspath(os.path.dirname(FILE_PATH))
SLD_PATH = os.path.normpath('{0}/files/slds/glri'.format(ABS_PATH))


def create_layer_names(directory_path, extension='*.nhru', existing_lyrs=None):
    """
    Returns a list of layer names based on the names of 
    animation files.
    
    :param str directory_path: path to a local copy of the animation files
    :param str extension: extension of the animation files
    :param list existing_lyrs: list of animation layers in GeoServer that should be left alone
    
    """
    filenames = get_filenames_from_directory(directory_path, extension)
    layer_names = []
    for filename in filenames:
        layer_name = get_filename_from_path(filename, '.animation.nhru')
        if existing_lyrs is not None:
            if layer_name not in existing_lyrs:
                layer_names.append(layer_name)
        else:
            layer_names.append(layer_name)
        
    return layer_names


def create_geoserver_layers(gs_host, gs_user, gs_pwd, ws_name, ds_name, layer_names, style):
    result_list = []
    for layer_name in layer_names:
        gsl = GeoServerLayers(gs_host, gs_user, gs_pwd, ws_name, ds_name, layer_name)
        feature_type_xml = gsl.create_feature_type_xml(native_name=layer_name, 
                                                       native_crs=PRMS_CUSTOM_PROJECTION
                                                       )
        post_feature = gsl.create_feature_type(feature_type_xml)
        recalc_feature = gsl.modify_feature_type(payload=feature_type_xml)
        layer_style_xml = gsl.create_lyr_style_xml(style)
        change_layer_style = gsl.modify_layer_style(layer_style_xml)
        result_dictionary = {'layer_name': layer_name,
                             'post_feature': post_feature.status_code,
                             'recalc_feature': recalc_feature.status_code,
                             'change_layer_style': change_layer_style.status_code
                             }
        result_list.append(result_dictionary)
    return result_list


def create_glri_sld(directory, style, xml_writepath=SLD_PATH, extension='*.nhru', 
                    column_names=ANIMATION_HEADERS, percentiles=PERCENTILES, 
                    colors=COLORS, attribute_units=ATTRIBUTE_UNITS, pretty_print=False,
                    sld_name_suffix=None):
    """
    Create an SLD from animation files.
    
    :param str directory: directory where animation files are kept locally
    :param str style: symobilizer to be used in the SLD
    :param str xml_writepath: location to write the SLD files; set to None to not write file
    :param str extension: extension of the animation files so they can be found
    :param list column_names: list of column names in the animation file in order from left to right
    :param percentiles: percentiles to be used for binning in the SLD
    :type percentiles: list or tuple of floats
    :param str colors: colors to be used for each percentile bin, must be the one less the length of percentiles
    :type colors: list or tuple of hex color strings
    :param dict attribute_units: mapping of units for each attribute
    :param bool pretty_print: specify whether XML should be formatted with spaces and line breaks
    :return: list containing dictionaries with keys 'sld_name' and 'sld_content'
    :rtype: list of dictionaries
    
    """
    slds = []
    files = get_filenames_from_directory(directory, extension)
    ps = PandasStats(file_pathnames=files, column_names=column_names, skiprows=21)
    df_combined = ps.create_concat_dataframe()
    hi = column_names[2:]
    df_pcnt = ps.calculate_df_percentiles(df_combined, percentiles, column_names=hi)
    df_describe = ps.parse_describe(df_pcnt, hi, 4, len(percentiles)+4)
    for attribute_describe in df_describe:
        sld_b = SldBins(data=attribute_describe)
        pre_coloring_bin = sld_b.create_bins()
        attribute_name = pre_coloring_bin['attribute']
        if attribute_name in ['potet', 'hru_actet', 'tminf', 'tmaxf']:  # these have red coloring to represent high values
            sld_b_with_colors = sld_b.bin_coloring_assignment(color_tuple=colors, 
                                                              sld_bin_dictionary=pre_coloring_bin, 
                                                              reverse_coloring=True
                                                              )
        else:
            sld_b_with_colors = sld_b.bin_coloring_assignment(color_tuple=colors, 
                                                              sld_bin_dictionary=pre_coloring_bin, 
                                                              reverse_coloring=False
                                                              )
        sld = LxmlSLDAttrBins(style)
        sld_content = sld.write_sld(sld_bin_dict=sld_b_with_colors, 
                                    attribute_units=attribute_units,
                                    pretty_print=pretty_print
                                    )
        if sld_name_suffix is not None:
            sld_name = '{0}_{1}'.format(attribute_name, sld_name_suffix)
        else:
            sld_name = '{0}'.format(attribute_name) 
        sld_data = {'sld_name': sld_name, 'sld_content': sld_content}
        slds.append(sld_data)
        if xml_writepath is not None:
            xml_filepath =  '{0}/{1}.sld'.format(xml_writepath, sld_name)
            write_to_file(sld_content, xml_filepath)
    return slds


def post_style_corrections_to_layers(layers, host, user, pwd, workspace, datastore, style):
    results = []
    for layer in layers:
        gsl = GeoServerLayers(gs_host=host, gs_user=user, 
                              gs_password=pwd, workspace_name=workspace, 
                              datastore_name=datastore, lyr_name=layer
                              )
        style_xml = gsl.create_lyr_style_xml(style_name=style)
        put_style = gsl.modify_layer_style(payload=style_xml)
        result = {'layer_name': layer,
                  'status_code': put_style.status_code,
                  'messages': put_style.text
                  }
        results.append(result) 
    return results
        

def post_sld_content(sld_data, host, user, pwd, ws=None):
    results = []
    sld_names = ('polygon',)
    for sld_datum in sld_data:
        sld_name = sld_datum['sld_name']
        sld_content = sld_datum['sld_content']
        gss = GeoServerStyles(gs_host=host, gs_user=user, gs_password=pwd, workspace_name=ws)
        create_style = gss.create_style(style_name=sld_name, style_file=sld_content)
        create_style_results = {'sld_name': sld_name,
                                'status_code': create_style.status_code,
                                'messages': create_style.text
                                }
        results.append(create_style_results)
        sld_names += (sld_name,)
    return (results, sld_names)