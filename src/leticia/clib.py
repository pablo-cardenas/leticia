import ctypes
from numpy.ctypeslib import ndpointer

clib = ctypes.CDLL('libleticia.so')

clib.taken_distances.restype = ctypes.c_double
clib.taken_distances.argtypes = [
    ndpointer(dtype='bool', flags="C_CONTIGUOUS"),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_double,
    ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
    ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
]
clib.distances.restype = None
clib.distances.argtypes = [
    ndpointer(dtype='bool', flags="C_CONTIGUOUS"),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_double,
    ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
]
clib.neighbors_distances.restype = None
clib.neighbors_distances.argtypes = [
    ndpointer(dtype='bool', flags="C_CONTIGUOUS"),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_double,
    ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
    ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
]
