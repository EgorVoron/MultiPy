import os


def gen_fp(output_path, number):
    return os.path.join(output_path, number + '.jpg')


def valid_file_path(path):
    valid_extensions = ['.mp4', '.m4a']
    return os.path.isfile(path) and os.path.getsize(path) > 0 and os.path.splitext(path)[1] in valid_extensions
