import os, os.path, platform
from setuptools import setup, Extension
from Cython.Build import cythonize

#dirklinux
#CLFFT_DIR = r'C:\users\dbs660\research_subjects\fresnel_imaging\dev\clFFT-2.2.0-Windows-x64'
CLFFT_DIR = r'E:\dirk\research_subjects\fresnel_imaging\dev\clFFT-2.2.0-Windows-x64'

CL_INCL_DIRS = []
if 'Windows' in platform.system():
    try:
        CL_DIR = os.getenv('AMDAPPSDKROOT')
        CL_INCL_DIRS = [os.path.join(CL_DIR, 'include')]
    except:
        print "CUDA?"
        CL_DIR = r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v6.5'
        print CL_DIR
        CL_INCL_DIRS = [os.path.join(CL_DIR, 'include')]
        if False:
            print "intel?"
            CL_DIR = os.getenv('INTELOCLSDKROOT')
            CL_INCL_DIRS = [os.path.join(CL_DIR, 'include')]
            print CL_DIR

    library_dirs = [os.path.join(CLFFT_DIR, 'lib64', 'import'),]
    print library_dirs
else:
# linux
    CLFFT_DIR = '../clFFT/src/'
    CL_DIR = '/usr/local/cuda-6.5/'
    CL_INCL_DIRS = [os.path.join(CL_DIR, 'include')]
    library_dirs = [ '../clFFT/src/package/lib64/']

import Cython.Compiler.Options
Cython.Compiler.Options.generate_cleanup_code = 2

#TODO: see https://github.com/matthew-brett/du-cy-numpy

extensions = [
    Extension("gpyfft.gpyfftlib",
              [os.path.join('gpyfft', 'gpyfftlib.pyx')],
              include_dirs = [os.path.join(CLFFT_DIR, 'include'),] + CL_INCL_DIRS,
              extra_compile_args = [],
              extra_link_args = [],
              libraries = ['clFFT'],
              library_dirs = library_dirs,
              )
    ]

def copy_clfftso_to_package():
    import shutil
    try:
        shutil.copy(
            os.path.join(CLFFT_DIR, 'package/lib64', 'libclFFT.so'),
            'gpyfft')
        
        shutil.copy(
            os.path.join(CLFFT_DIR, 'package/lib64', 'libStatTimer.so'),
            'gpyfft')

        shutil.copy(
            os.path.join(CLFFT_DIR, 'package/lib64', 'libclFFT.so.2'),
            'gpyfft')

    except:
        print "Failed to copy. Trying to continue anyway"


def copy_clfftdll_to_package():
    import shutil
    try:
        shutil.copy(
            os.path.join(CLFFT_DIR, 'bin', 'clFFT.dll'),
            'gpyfft')
        
        shutil.copy(
            os.path.join(CLFFT_DIR, 'bin', 'StatTimer.dll'),
            'gpyfft')
        print "copied clFFT.dll, StatTimer.dll"
    except Exception as e:
        print "Failed to copy. Trying to continue anyway"
        print e

#    # copy the relevant header file
#    shutil.copy(
#        os.path.join(CLFFT_DIR, 'include', 'clFFT.h'),
#        'gpyfft')
#
#    shutil.copy(
#        os.path.join(CLFFT_DIR, 'include', 'clFFT.version.h'),
#        'gpyfft')
#                 
package_data = {}
if 'Windows' in platform.system():
    copy_clfftdll_to_package()
    package_data.update({'gpyfft': ['clFFT.dll', 'StatTimer.dll']},)

else:
    copy_clfftso_to_package()
    package_data.update({'gpyfft': [ 'libclFFT.so.2', 'libclFFT.so', 'libStatTimer.so']},)

setup(
    name = 'Gpyfft',
    version = '0.2.1',
    description = 'A Python wrapper for the OpenCL FFT library clFFT by AMD',
    url = r"https://github.com/geggo/gpyfft",
    maintainer='Gregor Thalhammer',
    maintainer_email = 'gregor.thalhammer@gmail.com',
    license = 'LGPL',
    packages = ['gpyfft'],
    ext_modules = cythonize(extensions),
    package_data = package_data
    )

