ANIMATION_HEADERS = ['timestamp', 
                     'nhru', 
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

ATTRIBUTE_UNITS = {'soil_moist': u'in',
                   'recharge': u'in',
                   'hru_ppt': u'in',
                   'hru_rain': u'in',
                   'hru_snow': u'in',
                   'tminf': u'\xb0F',  # ASCII Hex code for degree symbol used
                   'tmaxf': u'\xb0F',  # ASCII Hex code for degree symbol used
                   'potet': u'in',
                   'hru_actet': u'in',
                   'pkwater_equiv': u'in',
                   'snowmelt': u'in',
                   'hru_streamflow_out': u'cfs'
                   }