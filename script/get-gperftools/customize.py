from utils import *
from mlc import utils
import os
import subprocess


def preprocess(i):

    env = i['env']
    state = i['state']

    if is_true(env.get('MLC_TCMALLOC_LIB_PATH_PROVIDED', '')):
        return {'return': 0}

    os_info = i['os_info']

    return {'return': 0}


def postprocess(i):

    env = i['env']
    state = i['state']

    os_info = i['os_info']

    # Case 1: user-provided library path (path.# variation)
    if is_true(env.get('MLC_TCMALLOC_LIB_PATH_PROVIDED', '')):
        lib_path = env.get('MLC_TCMALLOC_LIB_PATH', '')
        if not lib_path or not os.path.isdir(lib_path):
            return {'return': 1, 'error': 'Provided MLC_TCMALLOC_LIB_PATH does not exist: ' + str(lib_path)}
        env['MLC_TCMALLOC_LIB_PATH'] = lib_path
        env['MLC_GPERFTOOLS_PATH'] = os.path.dirname(lib_path)
        env['+LD_LIBRARY_PATH'] = [lib_path]
        env['MLC_DEPENDENT_CACHED_PATH'] = lib_path
        return {'return': 0}

    # Case 2: source build
    lib_path = os.path.join(os.getcwd(), "install", "lib")

    env['+LD_LIBRARY_PATH'] = [lib_path]
    env['MLC_GPERFTOOLS_PATH'] = os.path.dirname(lib_path)
    env['MLC_TCMALLOC_LIB_PATH'] = lib_path
    env['MLC_DEPENDENT_CACHED_PATH'] = os.path.join(lib_path, "libtcmalloc.so")

    return {'return': 0}
