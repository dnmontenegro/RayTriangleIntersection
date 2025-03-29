import sys

def get_filename(path):
    if sys.platform == "win32":
        path_sep = '\\'
    else:
        path_sep = '/'
    start = path.rfind(path_sep)
    end = path.rfind(".")
    if end == -1:
        end = len(path)
    return path[start+1:end]

def get_extension(path):
    last_index = path.rfind(".")
    if last_index == -1:
        return ""
    else:
        path[last_index+1:]

def get_directory(path):
    if sys.platform == "win32":
        path_sep = '\\'
    else:
        path_sep = '/'
    last_index = path.rfind(path_sep)
    if last_index == -1:
        return ""
    return path[:last_index+1]