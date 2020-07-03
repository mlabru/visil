# -*- coding: utf-8 -*-
"""
data

simple data loader module. Loads data files from the "data" directory shipped with application.
Enhancing this to handle caching etc.

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import os

# < module data >----------------------------------------------------------------------------------

# data
M_DATA_PY = os.path.abspath(os.path.dirname(__file__))
M_DATA_DIR = os.path.normpath(os.path.join(M_DATA_PY, "../.."))

# -------------------------------------------------------------------------------------------------
def filepath(f_filename):
    """
    determine the path to a file in the data directory
    """
    # return
    return os.path.join(M_DATA_DIR, f_filename)

# -------------------------------------------------------------------------------------------------
def load(f_filename, f_mode="rb"):
    """
    open a file in the data directory
    """
    # return
    return open(os.path.join(M_DATA_DIR, f_filename), f_mode)

# < the end >--------------------------------------------------------------------------------------
