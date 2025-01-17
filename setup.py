#!/usr/bin/env python3
import os, glob, shutil
from os.path import abspath, join, dirname, exists
from setuptools import setup

def get_extensions():
    import torch
    from torch.utils.cpp_extension import BuildExtension, CUDAExtension, include_paths
    
    _PVN3D_ROOT = abspath(dirname(__file__))
    _ext_src_root = join(_PVN3D_ROOT, "pvn3d/_ext-src")
    _ext_sources = glob.glob("{}/src/*.cpp".format(_ext_src_root)) + glob.glob(
        "{}/src/*.cu".format(_ext_src_root)
    )
    _ext_headers = glob.glob("{}/include/*".format(_ext_src_root))
    _torch_cpp_include_dirs = include_paths()
    
    return [
        CUDAExtension(
            name='pvn3d/lib/pointnet2_utils._ext',
            sources=_ext_sources,
            include_dirs=_torch_cpp_include_dirs,
            extra_compile_args={
                "cxx": ["-O2", f"-I{_ext_src_root}/include", "-v"],
                "nvcc": ["-O2", f"-I{_ext_src_root}/include", "-v"],
            },
        )
    ]

_PVN3D_ROOT = abspath(dirname(__file__))
kwargs = {
    'name': 'pvn3d',
    'cmdclass': {},
}

try:
    kwargs['ext_modules'] = get_extensions()
    from torch.utils.cpp_extension import BuildExtension
    kwargs['cmdclass']['build_ext'] = BuildExtension
except ImportError:
    print(f"Failed to import torch.utils.cpp_extension.BuildExtension due to {ImportError}. You probably need to install pytorch.")

setup(**kwargs)

if os.path.exists('build'):  shutil.rmtree('build')  # clean up build directory after setup

# `try:
#     src_pth = './build'
#     tg_pth = join(_PVN3D_ROOT, "pvn3d/lib/pointnet2_utils/")
#     fd_lst = os.listdir(src_pth)
#     for fd in fd_lst:
#         if 'lib' in fd:
#             src_pth = join(src_pth, fd, 'pointnet2_utils')
#             f_nm = os.listdir(src_pth)[0]
#             src_pth = join(src_pth, f_nm)
#             tg_pth = join(tg_pth, f_nm)
#     os.system('cp {} {}'.format(src_pth, tg_pth))
#     print(
#         src_pth, '==>', tg_pth,
#     )
# except:
#     print(
#         "\n****************************************************************\n",
#         "Failed to copy builded .so to ./pvn3d/lib/pointnet2_utils/.\n",
#         "Please manually copy the builded .so file (_ext.cpython*.so) in ./build"+\
#         " to ./pvn3d/lib/pointnet2_utils/.",
#         "\n****************************************************************\n"
#     )
#     print(f"PVN3D root: {_PVN3D_ROOT}")
#     print(f"ext src root: {_ext_src_root}")`

# vim: ts=4 sw=4 sts=4 expandtab
