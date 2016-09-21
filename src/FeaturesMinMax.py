# -*- coding: utf-8 -*-
"""
@author: Paweł Pęksa
"""


class FeaturesMinMax(object):
    """
        Class provides [min max] for features as list
        don't add more methods to this class
        unless you rewrite get_all_members
        to get rid of all members functions of this class
    """

    def __init__(self):
        pass

    def get_all_members(self):
        members = [attr for attr in dir(self) if not callable(attr) and not attr.startswith("__")]
        members.remove(self.get_all_members.__name__)
        return members

    ZERO_CROSS_RATE_MIN_MAX = [0.006, 1.8]  # ok
    SPECTRAL_COMPLEXITY_MIN_MAX = [0, 100]  # ok
    SPECTRAL_CENTROID_MIN_MAX = [0.017, 0.29]  # ok
    SPECTRAL_ROLL_OFF_MIN_MAX = [50, 9820]  # ok
    SPECTRAL_FLATNESS_DB_MIN_MAX = [0.06, 1]  # ok
    DISSONANCE_MIN_MAX = [0.433, 0.5]  # ok
    SCALE_MIN_MAX = [0, 1]  # ok
    ONSET_RATE_MIN_MAX = [0.04, 7.3]  # ok
    SPECTRAL_SPREAD_MIN_MAX = [0, 0.041]  # ok
    SPECTRAL_SKEWNESS_MIN_MAX = [-1.55, 38]  # ok
    SPECTRAL_KURTOSIS_MIN_MAX = [-1.433, 1800]  # ok