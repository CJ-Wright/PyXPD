__author__ = 'arkilic'
from xpd_architecture.dataapi.reciprocal_space_calculator.define_reciprocal_space import *


def init(geometry_name):
    addref()
    calculate_ub()
    return status


def angle_to_hkl():
    """
    Converts motor positions into hkl given UB matrix
    """