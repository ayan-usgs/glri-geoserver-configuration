from lxml import etree


class SldOgcAttributes(object):

    """
    Define useful OGC SLD attributes
    """
    
    def __init__(self, ogc_ns):
        
        self.ogc = '{%s}' % ogc_ns
        self.filter = self.ogc + 'Filter'
        self.prop_eq = self.ogc + 'PropertyIsEqualTo'
        self.prop_nte = self.ogc + 'PropertyIsNotEqualTo'
        self.prop_lt = self.ogc + 'PropertyIsLessThan'
        self.prop_lte = self.ogc + 'PropertyIsLessThanOrEqualTo'
        self.prop_gt = self.ogc + 'PropertyIsGreaterThan'
        self.prop_gte = self.ogc + 'PropertyIsGreaterThanOrEqualTo'
        self.ogc_and = self.ogc + 'And'
        self.ogc_or = self.ogc + 'Or'
        self.prop_name = self.ogc + 'PropertyName'
        self.literal = self.ogc + 'Literal'


class LxmlSLDAttrBins(object):
    
    """
    Write an SLD per GLRI's requirements.
    """
    
    def __init__(self, symbolizer, namespace='http://www.opengis.net/sld', ogc='http://www.opengis.net/ogc', 
                 xlink='http://www.w3.org/1999/xlink', xsi='http://www.w3.org/2001/XMLSchema-instance',
                 schema_location='http://www.opengis.net/sld StyledLayerDescriptor.xsd', version='1.0.0'):
        
        self.SLD = '{%s}' % namespace
        self.ogc = '{%s}' % ogc
        self.NSMAP = {'xsi': xsi,
                      'xlink': xlink,
                      'ogc': ogc,
                      None: namespace
                      }
        self.schema_location = {"{" + xsi + "}schemaLocation": schema_location}
        self.version = version
        self.oa = SldOgcAttributes(ogc)
        self.symbolizer_lower = symbolizer.lower()
        if self.symbolizer_lower == 'point':
            self.symbolizer_attr = 'PointSymbolizer'
        elif self.symbolizer_lower == 'line':
            self.symbolizer_attr = 'LineSymbolizer'
        elif self.symbolizer_lower == 'polygon':
            self.symbolizer_attr = 'PolygonSymbolizer'
        else:
            raise Exception('Cannot recognize symbolizer type...')
        
    def write_sld(self, sld_bin_dict, attribute_units, pretty_print=False, 
                  lyr_name=None, usr_style_title_text=None):
        
        attribute_name = sld_bin_dict['attribute']
        try:
            attribute_unit = attribute_units[attribute_name]
        except KeyError:
            attribute_missing = 'There is no unit specified for %s.' % attribute_name
            raise Exception(attribute_missing) 
        
        sld = etree.Element(self.SLD + 'StyledLayerDescriptor', version=self.version, 
                            attrib=self.schema_location, nsmap=self.NSMAP
                            )  
        
        named_lyr = etree.SubElement(sld, 'NamedLayer') 
        nl_name = etree.SubElement(named_lyr, 'Name')  
        if lyr_name is None:
            nl_name.text = '%s_layer' % attribute_name
        else:
            nl_name.text = lyr_name
        
        usr_style = etree.SubElement(named_lyr, 'UserStyle')  
        usr_style_title = etree.SubElement(usr_style, 'Title')  
        if usr_style_title_text is None:
            usr_style_title.text = '%s styling' % attribute_name
        else:
            usr_style_title.text = usr_style_title_text
        
        feature_type_style = etree.SubElement(usr_style, 'FeatureTypeStyle')  
        
        sld_bin_list = sld_bin_dict['bins']
        for sld_bin in sld_bin_list:
            sld_bin_no = sld_bin.bin_no
            sld_rule = etree.SubElement(feature_type_style, 'Rule')  
            sld_rule_name = etree.SubElement(sld_rule, 'Name')  
            sld_rule_name.text = '%s_bin_no_%s' % (attribute_name, sld_bin_no)

            sld_bin_range = sld_bin.bin_range
            lower_limit, upper_limit = sld_bin_range
            bin_hex_color = sld_bin.bin_color
            if float(lower_limit) == 0:
                filter_title = etree.SubElement(sld_rule, 'Title')
                filter_title.text = 'Less than %s' % upper_limit
                ogc_filter = etree.SubElement(sld_rule, self.oa.filter)
                ogc_prop_lt = etree.SubElement(ogc_filter, self.oa.prop_lt)
                ogc_prop_name = etree.SubElement(ogc_prop_lt, self.oa.prop_name)
                ogc_prop_name.text = attribute_name
                ogc_literal = etree.SubElement(ogc_prop_lt, self.oa.literal)
                ogc_literal.text = upper_limit
            elif upper_limit is None:
                filter_title = etree.SubElement(sld_rule, 'Title')
                filter_title.text = 'greater than %s' % lower_limit
                ogc_filter = etree.SubElement(sld_rule, self.oa.filter)
                ogc_prop_gt = etree.SubElement(ogc_filter, self.oa.prop_gt)
                ogc_prop_gt_name = etree.SubElement(ogc_prop_gt, self.oa.prop_name)
                ogc_prop_gt_name.text = attribute_name
                ogc_literal = etree.SubElement(ogc_prop_gt, self.oa.literal)
                ogc_literal.text = lower_limit
            else:
                filter_title = etree.SubElement(sld_rule, 'Title')
                filter_title.text = '%s to %s %s' % (lower_limit, upper_limit, attribute_unit)
                ogc_filter = etree.SubElement(sld_rule, self.oa.filter)
                ogc_and = etree.SubElement(ogc_filter, self.oa.ogc_and)
                ogc_prop_gte = etree.SubElement(ogc_and, self.oa.prop_gte)
                ogc_prop_gte_name = etree.SubElement(ogc_prop_gte, self.oa.prop_name)
                ogc_prop_gte_name.text = attribute_name
                ogc_literal_gte = etree.SubElement(ogc_prop_gte, self.oa.literal)
                ogc_literal_gte.text = lower_limit
                
                ogc_prop_lt = etree.SubElement(ogc_and, self.oa.prop_lt)
                ogc_prop_lt_name = etree.SubElement(ogc_prop_lt, self.oa.prop_name)
                ogc_prop_lt_name.text = attribute_name
                ogc_literal_lt = etree.SubElement(ogc_prop_lt, self.oa.literal)
                ogc_literal_lt.text = upper_limit                
            
            symbolizer = etree.SubElement(sld_rule, self.symbolizer_attr)
            if self.symbolizer_attr == 'PointSymbolizer':
                graphic = etree.SubElement(symbolizer, 'Graphic')
                mark = etree.SubElement(graphic, 'Mark')
                well_known_name = etree.SubElement(mark, 'WellKnownName')
                well_known_name.text = 'circle'
                fill = etree.SubElement(mark, 'Fill')
                css_param = etree.SubElement(fill, 'CssParameter', {'name': 'fill'})
                css_param.text = bin_hex_color
                size = etree.SubElement(graphic, 'Size')
                size.text = '8'
            elif self.symbolizer_attr == 'PolygonSymbolizer':
                fill = etree.SubElement(symbolizer, 'Fill')
                css_param = etree.SubElement(fill, 'CssParameter', {'name': 'fill'})
                css_param.text = bin_hex_color
            else:
                stroke = etree.SubElement(symbolizer, 'Stroke')
                css_param_stroke = etree.SubElement(stroke, 'CssParameter', {'name':'stroke'})
                css_param_stroke.text = bin_hex_color
                css_param_stroke_width = etree.SubElement(stroke, 'CssParameter', {'name':'width'})
                css_param_stroke_width.text = '3'
        # filter out Lake Michigan
        lake_mi_rule = etree.SubElement(feature_type_style, 'Rule')
        lake_mi_name = etree.SubElement(lake_mi_rule, 'Name')
        lake_mi_name.text = 'exclude_lake_michigan'
        lake_mi_filter = etree.SubElement(lake_mi_rule, self.oa.filter)
        lake_mi_prop = etree.SubElement(lake_mi_filter, self.oa.prop_nte)
        lake_mi_prop_name = etree.SubElement(lake_mi_prop, self.oa.prop_name)
        lake_mi_prop_name.text = 'GRIDCODE'
        lake_mi_literal = etree.SubElement(lake_mi_prop, self.oa.literal)
        lake_mi_literal.text = '47'
        
        sld_content = etree.tostring(sld, pretty_print=pretty_print)
        
        return sld_content 