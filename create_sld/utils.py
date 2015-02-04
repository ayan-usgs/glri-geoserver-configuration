def write_to_file(content, file_pathname):
    
    """
    Write some content to a file.
    """
    
    with open(file_pathname, 'w') as f:
        f.write(content)       