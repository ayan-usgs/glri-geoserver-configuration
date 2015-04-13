<StyledLayerDescriptor xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:ogc="http://www.opengis.net/ogc" xmlns="http://www.opengis.net/sld" version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd">
  <NamedLayer>
    <Name>soil_moist_layer</Name>
    <UserStyle>
      <Title>soil_moist styling</Title>
      <FeatureTypeStyle>
        <Rule>
          <Name>soil_moist_bin_no_1</Name>
          <Title>Less than or equal to 0.129 in</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsLessThanOrEqualTo>
                <ogc:PropertyName>soil_moist</ogc:PropertyName>
                <ogc:Literal>0.129</ogc:Literal>
              </ogc:PropertyIsLessThanOrEqualTo>
              <ogc:PropertyIsNotEqualTo>
                <ogc:PropertyName>GRIDCODE</ogc:PropertyName>
                <ogc:Literal>47</ogc:Literal>
              </ogc:PropertyIsNotEqualTo>
            </ogc:And>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#E12300</CssParameter>
            </Fill>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>soil_moist_bin_no_2</Name>
          <Title>0.129 to 0.386 in</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThan>
                <ogc:PropertyName>soil_moist</ogc:PropertyName>
                <ogc:Literal>0.129</ogc:Literal>
              </ogc:PropertyIsGreaterThan>
              <ogc:PropertyIsLessThanOrEqualTo>
                <ogc:PropertyName>soil_moist</ogc:PropertyName>
                <ogc:Literal>0.386</ogc:Literal>
              </ogc:PropertyIsLessThanOrEqualTo>
              <ogc:PropertyIsNotEqualTo>
                <ogc:PropertyName>GRIDCODE</ogc:PropertyName>
                <ogc:Literal>47</ogc:Literal>
              </ogc:PropertyIsNotEqualTo>
            </ogc:And>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#E54C00</CssParameter>
            </Fill>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>soil_moist_bin_no_3</Name>
          <Title>0.386 to 0.756 in</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThan>
                <ogc:PropertyName>soil_moist</ogc:PropertyName>
                <ogc:Literal>0.386</ogc:Literal>
              </ogc:PropertyIsGreaterThan>
              <ogc:PropertyIsLessThanOrEqualTo>
                <ogc:PropertyName>soil_moist</ogc:PropertyName>
                <ogc:Literal>0.756</ogc:Literal>
              </ogc:PropertyIsLessThanOrEqualTo>
              <ogc:PropertyIsNotEqualTo>
                <ogc:PropertyName>GRIDCODE</ogc:PropertyName>
                <ogc:Literal>47</ogc:Literal>
              </ogc:PropertyIsNotEqualTo>
            </ogc:And>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#EA7500</CssParameter>
            </Fill>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>soil_moist_bin_no_4</Name>
          <Title>0.756 to 1.28 in</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThan>
                <ogc:PropertyName>soil_moist</ogc:PropertyName>
                <ogc:Literal>0.756</ogc:Literal>
              </ogc:PropertyIsGreaterThan>
              <ogc:PropertyIsLessThanOrEqualTo>
                <ogc:PropertyName>soil_moist</ogc:PropertyName>
                <ogc:Literal>1.28</ogc:Literal>
              </ogc:PropertyIsLessThanOrEqualTo>
              <ogc:PropertyIsNotEqualTo>
                <ogc:PropertyName>GRIDCODE</ogc:PropertyName>
                <ogc:Literal>47</ogc:Literal>
              </ogc:PropertyIsNotEqualTo>
            </ogc:And>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#EF9E00</CssParameter>
            </Fill>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>soil_moist_bin_no_5</Name>
          <Title>1.28 to 1.65 in</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThan>
                <ogc:PropertyName>soil_moist</ogc:PropertyName>
                <ogc:Literal>1.28</ogc:Literal>
              </ogc:PropertyIsGreaterThan>
              <ogc:PropertyIsLessThanOrEqualTo>
                <ogc:PropertyName>soil_moist</ogc:PropertyName>
                <ogc:Literal>1.65</ogc:Literal>
              </ogc:PropertyIsLessThanOrEqualTo>
              <ogc:PropertyIsNotEqualTo>
                <ogc:PropertyName>GRIDCODE</ogc:PropertyName>
                <ogc:Literal>47</ogc:Literal>
              </ogc:PropertyIsNotEqualTo>
            </ogc:And>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#F4C700</CssParameter>
            </Fill>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>soil_moist_bin_no_6</Name>
          <Title>1.65 to 2.02 in</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThan>
                <ogc:PropertyName>soil_moist</ogc:PropertyName>
                <ogc:Literal>1.65</ogc:Literal>
              </ogc:PropertyIsGreaterThan>
              <ogc:PropertyIsLessThanOrEqualTo>
                <ogc:PropertyName>soil_moist</ogc:PropertyName>
                <ogc:Literal>2.02</ogc:Literal>
              </ogc:PropertyIsLessThanOrEqualTo>
              <ogc:PropertyIsNotEqualTo>
                <ogc:PropertyName>GRIDCODE</ogc:PropertyName>
                <ogc:Literal>47</ogc:Literal>
              </ogc:PropertyIsNotEqualTo>
            </ogc:And>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#F9F000</CssParameter>
            </Fill>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>soil_moist_bin_no_7</Name>
          <Title>2.02 to 2.44 in</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThan>
                <ogc:PropertyName>soil_moist</ogc:PropertyName>
                <ogc:Literal>2.02</ogc:Literal>
              </ogc:PropertyIsGreaterThan>
              <ogc:PropertyIsLessThanOrEqualTo>
                <ogc:PropertyName>soil_moist</ogc:PropertyName>
                <ogc:Literal>2.44</ogc:Literal>
              </ogc:PropertyIsLessThanOrEqualTo>
              <ogc:PropertyIsNotEqualTo>
                <ogc:PropertyName>GRIDCODE</ogc:PropertyName>
                <ogc:Literal>47</ogc:Literal>
              </ogc:PropertyIsNotEqualTo>
            </ogc:And>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#D3DB0C</CssParameter>
            </Fill>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>soil_moist_bin_no_8</Name>
          <Title>2.44 to 3.47 in</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThan>
                <ogc:PropertyName>soil_moist</ogc:PropertyName>
                <ogc:Literal>2.44</ogc:Literal>
              </ogc:PropertyIsGreaterThan>
              <ogc:PropertyIsLessThanOrEqualTo>
                <ogc:PropertyName>soil_moist</ogc:PropertyName>
                <ogc:Literal>3.47</ogc:Literal>
              </ogc:PropertyIsLessThanOrEqualTo>
              <ogc:PropertyIsNotEqualTo>
                <ogc:PropertyName>GRIDCODE</ogc:PropertyName>
                <ogc:Literal>47</ogc:Literal>
              </ogc:PropertyIsNotEqualTo>
            </ogc:And>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#AEC618</CssParameter>
            </Fill>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>soil_moist_bin_no_9</Name>
          <Title>3.47 to 5.98 in</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThan>
                <ogc:PropertyName>soil_moist</ogc:PropertyName>
                <ogc:Literal>3.47</ogc:Literal>
              </ogc:PropertyIsGreaterThan>
              <ogc:PropertyIsLessThanOrEqualTo>
                <ogc:PropertyName>soil_moist</ogc:PropertyName>
                <ogc:Literal>5.98</ogc:Literal>
              </ogc:PropertyIsLessThanOrEqualTo>
              <ogc:PropertyIsNotEqualTo>
                <ogc:PropertyName>GRIDCODE</ogc:PropertyName>
                <ogc:Literal>47</ogc:Literal>
              </ogc:PropertyIsNotEqualTo>
            </ogc:And>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#89B124</CssParameter>
            </Fill>
          </PolygonSymbolizer>
        </Rule>
        <Rule>
          <Name>soil_moist_bin_no_10</Name>
          <Title>Greater than 5.98 in</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThan>
                <ogc:PropertyName>soil_moist</ogc:PropertyName>
                <ogc:Literal>5.98</ogc:Literal>
              </ogc:PropertyIsGreaterThan>
              <ogc:PropertyIsNotEqualTo>
                <ogc:PropertyName>GRIDCODE</ogc:PropertyName>
                <ogc:Literal>47</ogc:Literal>
              </ogc:PropertyIsNotEqualTo>
            </ogc:And>
          </ogc:Filter>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#649C32</CssParameter>
            </Fill>
          </PolygonSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
