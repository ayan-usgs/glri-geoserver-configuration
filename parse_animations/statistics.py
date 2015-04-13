from pandas.io.parsers import read_csv
from pandas import concat

from utils import ResultNamedTuple, BinSizeNamedTuple

    
class PandasStats(object):
    """
    Use Panda to create a dataframe from a
    list of csv files and calculate some 
    statistics.
    
    This class is instantiated with the following
    parameters:
    
    :param list file_pathnames: list of full file pathnames
    :param list column_names: list of column names in the csv files
    :param int skiprows: number of rows to skip at the beginning of a file
    :param str comment: character that is used in the csv to denote a comment
    :param str delimiter: delimiter used in the csv
    
    """
    ResultTuple = ResultNamedTuple
    
    def __init__(self, file_pathnames, column_names, skiprows, **kwargs):
        self.path_list = file_pathnames
        self.headers = column_names
        self.skip_rows = skiprows
        self.kwargs = {'comment':'#'}
        self.kwargs.update(kwargs)
    
    def load_file_data(self, sep='\t', index_col=False):
        """
        Create a series of dataframes from the list
        of files provided.
        
        """
        # sep=self.dlmt, comment=self.cmnt,
        dataframes = []
        for file_pathname in self.path_list:
            dataframe = read_csv(filepath_or_buffer=file_pathname,
                                 sep=sep,
                                 index_col=index_col,
                                 names=self.headers,
                                 skiprows=self.skip_rows,
                                 **self.kwargs
                                 )
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
        
        :param pandas.DataFrame dataframe: a pandas dataframe object
        :param list column_names: list of columns that should have their averages calculated
        :param int axis: axis of dataframe that the average should be calculated on
        :param bool skip_nans: specify whether nans should be included in the average
        :return: mean of the dataframe columns
        :rtype: pandas.Series
        
        """
        if column_names is not None:
            df_mean = dataframe[column_names].mean(axis=axis, skipna=skip_nans)
        else:
            df_mean = dataframe.mean(axis=axis, skipna=skip_nans)
        return df_mean
    
    def calculate_df_min(self, dataframe, column_names=None, axis=0, skip_nans=True):
        """
        Calculate the min of a column or columns in a dataframe
        
        :param pandas.DataFrame dataframe: a pandas dataframe object
        :param list column_names: list of columns that should have their min determined
        :param int axis: axis of dataframe that the min should be calculated on
        :param bool skip_nans: specify whether nans should be included in the min
        :return: mininum value of the dataframe columns
        :rtype: pandas.Series
        
        """
        if column_names is not None:
            df_min = dataframe[column_names].min(axis=axis, skipna=skip_nans)
        else:
            df_min = dataframe.min(axis=axis, skipna=skip_nans) 
        return df_min
    
    def calculate_df_max(self, dataframe, column_names=None, axis=0, skip_nans=True):
        """
        Calculate the max of a column or columns in a dataframe
        
        :param pandas.DataFrame dataframe: a pandas dataframe object
        :param list column_names: list of columns that should have their max determined
        :param int axis: axis of dataframe that the max should be calculated on
        :param bool skip_nans: specify whether nans should be included in the max
        :return: maximum value of the dataframe columns
        :rtype: pandas.Series
        
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
        
        :param pandas.DataFrame dataframe: a pandas DataFrame
        :param list percentiles: a list of floats representing the percentiles that should be calculated
        :param list column_names: columns that should have percentiles calculated
        :return: percentiles for the columns specified for the dataframe
        :rtype: pandas.DataFrame 
        
        """
        if column_names is not None:
            df_pcnt = dataframe[column_names].describe(percentiles=percentiles, 
                                                       percentile_width=None
                                                       )
        else:
            df_pcnt = dataframe.describe(percentiles=percentiles, 
                                         percentile_width=None
                                         )
        return df_pcnt
    
    def parse_describe(self, describe_df, column_list, range_start, range_end):
        """
        Parse a dataframe containing percentiles
        
        :param pandas.DataFrame describe_df: the dataframe returned from pandas.DataFrame.describe()
        :param list column_list: columns that should have their percentiles parsed out
        :param int range_start: dataframe index for the first row of interest,
        :param int range_end: dataframe index for the last row of interest
        :return: percentiles for each column
        :rtype: list of collections.namedtuple
        
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
    
    :param collections.namedtuple data: list containing tuples with attribute name and percentiles
    
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
            if abs(value_float) < 1:
                round_decimal_places = ndigits  # number of decimal places if the value is less than 1
            else:
                round_decimal_places = ndigits - 1  # number of decimal places if the value is greater or equal to 1
            format_str = '{{{0}:.{1}f}}'.format(0, round_decimal_places)
            value_rounded = format_str.format(value_float)
            value_rounded_str = value_rounded
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