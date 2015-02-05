from pandas.io.parsers import read_csv
from pandas import concat

from utils import ResultNamedTuple, BinSizeNamedTuple

    
class PandasStats(object):
    """
    Use Panda to create a dataframe from a
    list of csv files and calculate some 
    statistics.
    
    """
    ResultTuple = ResultNamedTuple
    
    def __init__(self, file_pathnames, column_names, skiprows, comment='#', delimiter='\t'):
        self.path_list = file_pathnames
        self.dlmt = delimiter
        self.headers = column_names
        self.cmnt = comment
        self.skip_rows = skiprows
    
    def load_file_data(self):
        """
        Create a series of dataframes from the list
        of files provided.
        
        """
        dataframes = []
        for file_pathname in self.path_list:
            dataframe = read_csv(filepath_or_buffer=file_pathname, sep=self.dlmt, names=self.headers, comment=self.cmnt, skiprows=self.skip_rows)
            dataframes.append(dataframe)
        return dataframes
    
    def create_concat_dataframe(self):
        """
        Concatenate a list of dataframes into
        a single dataframe.
        
        """
        dataframes = self.load_file_data()
        concat_dataframe = concat(dataframes)
        return concat_dataframe
    
    def calculate_df_mean(self, dataframe, column_names=None, axis=0, skip_nans=True):
        """
        Calculate the mean of a column or columns in a dataframe.
        
        """
        if column_names is not None:
            df_mean = dataframe[column_names].mean(axis=axis, skipna=skip_nans)
        else:
            df_mean = dataframe.mean(axis=axis, skipna=skip_nans)
        return df_mean
    
    def calculate_df_min(self, dataframe, column_names=None, axis=0, skip_nans=True):
        """
        Calculate the min of a column or columns in a dataframe
        
        """
        if column_names is not None:
            df_min = dataframe[column_names].min(axis=axis, skipna=skip_nans)
        else:
            df_min = dataframe.min(axis=axis, skipna=skip_nans) 
        return df_min
    
    def calculate_df_max(self, dataframe, column_names=None, axis=0, skip_nans=True):
        """
        Calculate the max of a column or columns in a dataframe
        
        """
        if column_names is not None:
            df_max = dataframe[column_names].max(axis=axis, skipna=skip_nans)
        else:
            df_max = dataframe.max(axis=axis, skipna=skip_nans) 
        return df_max
    
    def calculate_df_percentiles(self, dataframe, percentiles=None, column_names=None):
        """
        Run a describe on the dataframe for the specified columns
        for percentiles that are requested.
        
        """
        if column_names is not None:
            df_pcnt = dataframe[column_names].describe(percentiles=percentiles, percentile_width=None)
        else:
            df_pcnt = dataframe.describe(percentiles=percentiles, percentile_width=None)
        return df_pcnt
    
    def parse_describe(self, describe_df, column_list, range_start, range_end):
        """
        range_start is the first of interest,
        range_end is the last row of interest
        
        """
        indexes = range(range_start, range_end)
        results = []
        for column in column_list:
            values_tuple = ()
            for index in indexes:
                pct_value = describe_df.iloc[index][column]
                values_tuple += (pct_value,)
            result_tuple = self.ResultTuple(attribute=column, pct_values=values_tuple)
            results.append(result_tuple)
        return results
    
    
class SldBins(object):
    """
    This class creates bins for an SLD. An object must
    be instantiated with a list of namedtuples. The nametuples
    should have the following attributes: 'attributes', 'pct_values'.
    The PandasStats.parse_describe method is able to create such
    a list.
    
    """
    BinSize = BinSizeNamedTuple
    
    def __init__(self, data):
        self.data = data
        self.upper_range_limit = len(self.data.pct_values) + 2
        self.bin_no_range = range(1, self.upper_range_limit)
        
    def _convert_to_rounded_string(self, numeric_value, ndigits=3):
        """
        Round a number to the specified number of
        decimal places. Handles ValueError and
        TypeError exceptions in case of None values
        being passed.
        
        """
        try:
            value_float = float(str(numeric_value))
        except ValueError:
            value_float = numeric_value
        try:
            value_rounded = round(value_float, ndigits)
            value_rounded_str = str(value_rounded)
        except TypeError:
            value_rounded_str = value_float   
        return value_rounded_str
        
    def create_bins(self):
        """
        Create bins for an attribute based on the
        percentiles calculated by Pandas. Returns
        a dictionary of attribute name and a list of
        the bins. The bins are reported as a tuple of
        form (x, y), where x and y are the bin lower
        and upper limit respectively.
        
        """
        attribute_name = self.data.attribute
        bins = []
        for bin_no in self.bin_no_range:
            pct_values = self.data.pct_values
            try:
                upper_index = bin_no - 1
                lower_index = bin_no - 2
                upper_value = pct_values[upper_index]
                if lower_index < 0:
                    lower_value = 0
                else:
                    lower_value = pct_values[lower_index]
            except IndexError:
                upper_value = None
                lower_value = pct_values[-1]
            upper_value_str = self._convert_to_rounded_string(numeric_value=upper_value)
            lower_value_str = self._convert_to_rounded_string(numeric_value=lower_value)
            bin_range = (lower_value_str, upper_value_str)
            sld_bin = self.BinSize(bin_no=bin_no, bin_range=bin_range, bin_color=None)
            bins.append(sld_bin)
            bin_dictionary = {'attribute': attribute_name, 'bins': bins}   
        return bin_dictionary
    
    def bin_coloring_assignment(self, color_tuple, sld_bin_dictionary=None, reverse_coloring=False):
        """
        Assign colors for each bin. The number of colors specified
        in the color tuple must be the same as the the number of
        desired bins. If SLD bins are not provided, this method will
        create the requiresite dictionary.
        
        """
        if sld_bin_dictionary is None:
            bins_dictionary = self.create_bins()
        else:
            bins_dictionary = sld_bin_dictionary
        bin_attribute = bins_dictionary['attribute']
        bins = bins_dictionary['bins']
        # check that the number of colors is equal to the number of bins
        # raise an exception if they are not equal
        bins_length = len(bins)
        colors_length = len(color_tuple)
        if bins_length > colors_length:
            raise Exception('There are more bins than colors.')
        elif bins_length < colors_length:
            raise Exception('There are more colors than bins.')
        else:
            pass
        bin_list = []
        indexes = range(0, bins_length)
        for index in indexes:
            sld_bin = bins[index]
            bin_no = sld_bin.bin_no
            bin_range = sld_bin.bin_range
            if not reverse_coloring:
                color_index = index
            else:
                color_index = (index + 1)*-1
            color = color_tuple[color_index]
            sld_bin_with_color = self.BinSize(bin_no=bin_no, bin_range=bin_range, bin_color=color)
            bin_list.append(sld_bin_with_color)
        bins_dictionary_with_color = {'attribute': bin_attribute, 'bins': bin_list}
        return bins_dictionary_with_color       