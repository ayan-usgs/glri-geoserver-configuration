import unittest
from pandas import DataFrame
import mock
from glri_sld_files.parse_animations.statistics import PandasStats, SldBins
from ..utils import ResultNamedTuple, BinSizeNamedTuple

class TestPandasStats(unittest.TestCase):
    
    def setUp(self):
        
        self.d_1 = {'one': [1, 2, 3, 4],
                    'two': [5, 6, 7, 8]}
        self.d_2 = {'one': [-1, -2, -3, -4],
                    'two': [-5, -6, -7, -8]}
        self.d_3 = {'one': [10, 20, 30, 40, None],
                    'two': [1, 2, 3, 4, None]}
        self.column_names = ['one', 'two']
        self.test_path = ['some_path']
        self.skip_rows = 1
        self.df_1 = DataFrame(self.d_1)
        self.df_2 = DataFrame(self.d_2)
        self.df_3 = DataFrame(self.d_3)
        self.df_list = [self.df_1, self.df_2]
        self.ps = PandasStats(self.test_path, self.column_names, self.skip_rows)
    
    @mock.patch('glri_sld_files.parse_animations.statistics.read_csv')    
    def test_load_file(self, mock_load_file):
        
        ps = self.ps
        mock_load_file.return_value = self.df_1
        df_list = ps.load_file_data()
        self.assertEqual(len(df_list), 1)
    
    @mock.patch('glri_sld_files.parse_animations.statistics.PandasStats.load_file_data')
    def test_create_concat_dataframe(self, mock_lfd):
        
        ps = self.ps
        mock_lfd.return_value = self.df_list
        concat_df = ps.create_concat_dataframe()
        len_df = len(concat_df)
        self.assertEqual(len_df, 8)
        
    def test_calculate_df_mean(self):
        
        ps = self.ps
        means = ps.calculate_df_mean(dataframe=self.df_3)
        
        means_len = len(means)
        expected_means_len = 2
        self.assertEqual(means_len, expected_means_len)
        
        value_1 = means['one']
        expected_value_1 = 25
        self.assertEqual(value_1, expected_value_1)
        
        value_2 = means['two']
        expected_value_2 = 2.5
        self.assertEqual(value_2, expected_value_2)
        
    def test_calculate_df_mean_with_column(self):
        
        ps = self.ps
        mean = ps.calculate_df_mean(dataframe=self.df_3, column_names=['one'])
        
        mean_len = len(mean)
        expected_len = 1
        self.assertEqual(mean_len, expected_len)
        
        mean_value = mean['one']
        expected_value = 25
        self.assertEqual(mean_value, expected_value)
        
    def test_calculate_df_min(self):
        
        ps = self.ps
        mins = ps.calculate_df_min(dataframe=self.df_3)
        
        mins_len = len(mins)
        expected_len = 2
        self.assertEqual(mins_len, expected_len)
        
        mins_1 = mins['one']
        expected_value_1 = 10
        self.assertEqual(mins_1, expected_value_1)
        
        mins_2 = mins['two']
        expected_value_2 = 1
        self.assertEqual(mins_2, expected_value_2)
        
    def test_calculate_df_min_with_column(self):
        
        ps = self.ps
        min_calc = ps.calculate_df_min(dataframe=self.df_3, column_names=['one'])
        
        min_len = len(min_calc)
        expected_len = 1
        self.assertEqual(min_len, expected_len)
        
        min_value = min_calc['one']
        expected_val = 10
        self.assertEqual(min_value, expected_val)
        
    def test_calculate_df_percentiles(self):
        
        ps = self.ps
        desc_df = ps.calculate_df_percentiles(dataframe=self.df_3, percentiles=[0.4, 0.5, 0.6])
        desc_df_len = len(desc_df)
        expected_len = 8
        self.assertEqual(desc_df_len, expected_len)
        
    def test_parse_describe(self):
        
        ps = self.ps
        desc_df = ps.calculate_df_percentiles(dataframe=self.df_3, percentiles=[0.4, 0.5, 0.6])
        parsed = ps.parse_describe(describe_df=desc_df, column_list=['one', 'two'], range_start=4, range_end=7)
        parsed_len = len(parsed)
        expected_len = 2
        self.assertEqual(parsed_len, expected_len)
        
        item_0 = parsed[0]
        item_attr = item_0.attribute
        item_attr_expected = 'one'
        self.assertEqual(item_attr, item_attr_expected)
        
        item_pcts = item_0.pct_values
        item_pct_len = len(item_pcts)
        item_pct_len_expected = 3
        self.assertEqual(item_pct_len, item_pct_len_expected)
        

    
class TestSldBins(unittest.TestCase):
    
    def setUp(self):
        
        self.data = ResultNamedTuple(attribute='soil_moist', 
                                     pct_values=(0.17290962499999998, 
                                                 0.57754375000000002, 
                                                 1.1396362499999999, 
                                                 1.6435799999999998, 
                                                 2.1250499999999999, 
                                                 2.86293, 
                                                 5.3624425000000002))
        self.colors = ('#FF0000', '#FFA500', '#FFFF00', '#9ACD32', '#008000', '#0000FF', '#4B0082', '#9400D3')
        self.more_colors = ('#FF0000', '#FFA500', '#FFFF00', '#9ACD32', '#008000', '#0000FF', '#4B0082', '#9400D3', '#000000')
        self.fewer_colors = ('#FF0000', '#FFA500', '#FFFF00')
        self.bin_tuple = BinSizeNamedTuple
        self.sb = SldBins(data=self.data)
    
    def test_create_bins(self):
        
        bins_dictionary = self.sb.create_bins()
        bins_len = len(bins_dictionary)
        expected_dict_len = 2
        bin_ranges = bins_dictionary['bins']
        bin_ranges_len = len(bin_ranges)
        expected_bin_ranges_len = 8
        self.assertEqual(bins_len, expected_dict_len)
        self.assertEqual(bin_ranges_len, expected_bin_ranges_len)
        
    def test_bin_coloring_assignment(self):

        result = self.sb.bin_coloring_assignment(color_tuple=self.colors)
        result_len = len(result)
        expected_result_len = 2
        result_bins = result['bins']
        result_bins_len = len(result_bins)
        expected_result_bins_len = 8
        expected_result_bins_0 = self.bin_tuple(bin_no=1, bin_range=('0.0', '0.17291'), bin_color='#FF0000')
        result_bins_0 = result_bins[0]
        self.assertEqual(result_len, expected_result_len)
        self.assertEqual(result_bins_len, expected_result_bins_len)
        self.assertEqual(result_bins_0, expected_result_bins_0)
        
    def test_reverse_bin_coloring_assignment(self):
        
        result = self.sb.bin_coloring_assignment(color_tuple=self.colors, reverse_coloring=True)
        result_bins = result['bins']
        result_bins_0 = result_bins[0]
        expected_result_bins_0 = self.bin_tuple(bin_no=1, bin_range=('0.0', '0.17291'), bin_color='#9400D3')
        self.assertEqual(result_bins_0, expected_result_bins_0)
        
    def test_exception_raise_more_colors(self):
        
        with self.assertRaises(Exception) as cm:
            self.sb.bin_coloring_assignment(self.more_colors)
            
        exception_str = str(cm.exception)
        expected_exception = 'There are more colors than bins.'
        self.assertEqual(exception_str, expected_exception)
            
    def test_exception_raise_fewer_colors(self):
        
        with self.assertRaises(Exception) as cm:
            self.sb.bin_coloring_assignment(self.fewer_colors)
            
        exception_str = str(cm.exception)
        expected_exception = 'There are more bins than colors.'
        self.assertEqual(exception_str, expected_exception)
        