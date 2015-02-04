from glob import glob
from collections import namedtuple

def get_filenames_from_directory(directory_path, pattern='*'):
    
    path_as_list = list(directory_path)
    if path_as_list[-1] in ['\\', '/']:
        directory_path = directory_path[:-1]
    file_path_pattern = '%s/%s' % (directory_path, pattern)
    file_list = glob(file_path_pattern)
    
    return file_list

ResultNamedTuple = namedtuple('ResultTuple', ['attribute', 'pct_values'])

BinSizeNamedTuple = namedtuple('BinSize', ['bin_no', 'bin_range', 'bin_color'])