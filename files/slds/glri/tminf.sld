<StyledLayerDescriptor xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:ogc="http://www.opengis.net/ogc" xmlns="http://www.opengis.net/sld" version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd"><NamedLayer><Name>tminf_layer</Name><UserStyle><Title>tminf styling</Title><FeatureTypeStyle><Rule><Name>tminf_bin_no_1</Name><Title>Less than 35.16029</Title><ogc:Filter><ogc:PropertyIsLessThan><ogc:PropertyName>tminf</ogc:PropertyName><ogc:Literal>35.16029</ogc:Literal></ogc:PropertyIsLessThan></ogc:Filter><PolygonSymbolizer><Fill><CssParameter name="fill">#9400D3</CssParameter></Fill></PolygonSymbolizer></Rule><Rule><Name>tminf_bin_no_2</Name><Title>35.16029 to 37.6475</Title><ogc:Filter><ogc:And><ogc:PropertyIsGreaterThanOrEqualTo><ogc:PropertyName>tminf</ogc:PropertyName><ogc:Literal>35.16029</ogc:Literal></ogc:PropertyIsGreaterThanOrEqualTo><ogc:PropertyIsLessThan><ogc:PropertyName>tminf</ogc:PropertyName><ogc:Literal>37.6475</ogc:Literal></ogc:PropertyIsLessThan></ogc:And></ogc:Filter><PolygonSymbolizer><Fill><CssParameter name="fill">#4B0082</CssParameter></Fill></PolygonSymbolizer></Rule><Rule><Name>tminf_bin_no_3</Name><Title>37.6475 to 39.4709</Title><ogc:Filter><ogc:And><ogc:PropertyIsGreaterThanOrEqualTo><ogc:PropertyName>tminf</ogc:PropertyName><ogc:Literal>37.6475</ogc:Literal></ogc:PropertyIsGreaterThanOrEqualTo><ogc:PropertyIsLessThan><ogc:PropertyName>tminf</ogc:PropertyName><ogc:Literal>39.4709</ogc:Literal></ogc:PropertyIsLessThan></ogc:And></ogc:Filter><PolygonSymbolizer><Fill><CssParameter name="fill">#0000FF</CssParameter></Fill></PolygonSymbolizer></Rule><Rule><Name>tminf_bin_no_4</Name><Title>39.4709 to 41.06115</Title><ogc:Filter><ogc:And><ogc:PropertyIsGreaterThanOrEqualTo><ogc:PropertyName>tminf</ogc:PropertyName><ogc:Literal>39.4709</ogc:Literal></ogc:PropertyIsGreaterThanOrEqualTo><ogc:PropertyIsLessThan><ogc:PropertyName>tminf</ogc:PropertyName><ogc:Literal>41.06115</ogc:Literal></ogc:PropertyIsLessThan></ogc:And></ogc:Filter><PolygonSymbolizer><Fill><CssParameter name="fill">#008000</CssParameter></Fill></PolygonSymbolizer></Rule><Rule><Name>tminf_bin_no_5</Name><Title>41.06115 to 42.5799</Title><ogc:Filter><ogc:And><ogc:PropertyIsGreaterThanOrEqualTo><ogc:PropertyName>tminf</ogc:PropertyName><ogc:Literal>41.06115</ogc:Literal></ogc:PropertyIsGreaterThanOrEqualTo><ogc:PropertyIsLessThan><ogc:PropertyName>tminf</ogc:PropertyName><ogc:Literal>42.5799</ogc:Literal></ogc:PropertyIsLessThan></ogc:And></ogc:Filter><PolygonSymbolizer><Fill><CssParameter name="fill">#9ACD32</CssParameter></Fill></PolygonSymbolizer></Rule><Rule><Name>tminf_bin_no_6</Name><Title>42.5799 to 44.1731</Title><ogc:Filter><ogc:And><ogc:PropertyIsGreaterThanOrEqualTo><ogc:PropertyName>tminf</ogc:PropertyName><ogc:Literal>42.5799</ogc:Literal></ogc:PropertyIsGreaterThanOrEqualTo><ogc:PropertyIsLessThan><ogc:PropertyName>tminf</ogc:PropertyName><ogc:Literal>44.1731</ogc:Literal></ogc:PropertyIsLessThan></ogc:And></ogc:Filter><PolygonSymbolizer><Fill><CssParameter name="fill">#FFFF00</CssParameter></Fill></PolygonSymbolizer></Rule><Rule><Name>tminf_bin_no_7</Name><Title>44.1731 to 46.2511</Title><ogc:Filter><ogc:And><ogc:PropertyIsGreaterThanOrEqualTo><ogc:PropertyName>tminf</ogc:PropertyName><ogc:Literal>44.1731</ogc:Literal></ogc:PropertyIsGreaterThanOrEqualTo><ogc:PropertyIsLessThan><ogc:PropertyName>tminf</ogc:PropertyName><ogc:Literal>46.2511</ogc:Literal></ogc:PropertyIsLessThan></ogc:And></ogc:Filter><PolygonSymbolizer><Fill><CssParameter name="fill">#FFA500</CssParameter></Fill></PolygonSymbolizer></Rule><Rule><Name>tminf_bin_no_8</Name><Title>greater than 46.2511</Title><ogc:Filter><ogc:PropertyIsGreaterThan><ogc:PropertyName>tminf</ogc:PropertyName><ogc:Literal>46.2511</ogc:Literal></ogc:PropertyIsGreaterThan></ogc:Filter><PolygonSymbolizer><Fill><CssParameter name="fill">#FF0000</CssParameter></Fill></PolygonSymbolizer></Rule></FeatureTypeStyle></UserStyle></NamedLayer></StyledLayerDescriptor>