import os


def get_filename_without_ext(filepath):
    base_name = os.path.basename(filepath)
    file_name, ext = os.path.splitext(base_name)
    return file_name


def get_filename(filepath):
    base_name = os.path.basename(filepath)
    file_name, ext = os.path.splitext(base_name)
    return file_name + ext
