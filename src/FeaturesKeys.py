# -*- coding: utf-8 -*-
"""
@author: Paweł Pęksa
"""


class FeaturesKeys(object):
    """
        Class provide keys for features as list
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

    ZERO_CROSS_RATE = "zero_crossing_rate"
    SPECTRAL_COMPLEXITY = "spectral_complexity"
    SPECTRAL_CENTROID = "spectral_centroid"
    SPECTRAL_ROLL_OFF = "spectral_roll_off"
    SPECTRAL_FLATNESS_DB = "spectral_flatness_db"
    DISSONANCE = "dissonance"
    SCALE = "scale"
    ONSET_RATE = "onset_rate"
    SPECTRAL_SPREAD = "spectral_spread"
    SPECTRAL_SKEWNESS = "spectral_skewness"
    SPECTRAL_KURTOSIS = "spectral_kurtosis"

