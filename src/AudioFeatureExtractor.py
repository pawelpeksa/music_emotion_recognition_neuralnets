# -*- coding: utf-8 -*-
"""
@author: Paweł Pęksa
"""

import logging
import sys
import matplotlib.pyplot as plt
from Configuration import Configuration as Conf
from essentia import *
from essentia.standard import *
from Keys import Keys
from FeaturesKeys import FeaturesKeys
import psutil
import numpy as np


class AudioFeatureExtractor(object):
    """class used to perform feature extraction on songs"""
    def __init__(self, song_list):
        self._song_number = len(song_list)
        self._song_list = song_list
        self._current_song_signal = None
        self._current_song_spectrum = None
        self._cuurent_song_power_spectrum = None
        self._current_song_spectral_peaks = None
        self._curent_song_centralmoments = None

        self._dissonance_array = list()
        self._zero_cross_rate_array = list()
        self._spectral_complexity_array = list()
        self._spectral_centroid_array = list()
        self._spectral_roll_off_array = list()
        self._spectral_flatness_db_array = list()
        self._scale_array = list()
        self._onset_rate_array = list()
        self._spectral_spread_array = list()
        self._spectral_skewness_array = list()
        self._spectral_kurtosis_array = list()

    def process(self):
        logging.info("Extract feature from all songs({0})".format(self._song_number))

        song_counter = 1
        for song in self._song_list:
            logging.info("Extract feature from song {0}/{1}".format(song_counter, self._song_number))
            logging.info("Song:{0}".format(song[Keys.SONG_FILE]))
            song_file_path = Conf.SONG_FOLDER_PATH + song[Keys.SONG_FILE]
            song_features = self.process_song(song_file_path)
            song[Keys.SONG_FEATURES] = song_features
            logging.info("Extract feature from song {0} finished".format(self._song_number))
            logging.debug("Memory usage {0}%".format(psutil.virtual_memory().percent))
            song_counter += 1


        # printing min max
        print "Dissonance:\n"
        print "min:{0} max:{1}".format(min(self._dissonance_array), max(self._dissonance_array))

        print "Onset:\n"
        print "min:{0} max:{1}".format(min(self._onset_rate_array), max(self._onset_rate_array))

        print "Spectral Centroid:\n"
        print "min:{0} max:{1}".format(min(self._spectral_centroid_array), max(self._spectral_centroid_array))

        print "Spectra kurtosis:\n"
        print "min:{0} max:{1}".format(min(self._spectral_kurtosis_array), max(self._spectral_kurtosis_array))

        print "Spectral skewness:\n"
        print "min:{0} max:{1}".format(min(self._spectral_skewness_array), max(self._spectral_skewness_array))

        print "Spectral complexity:\n"
        print "min:{0} max:{1}".format(min(self._spectral_complexity_array), max(self._spectral_complexity_array))

        print "Zero crossing:\n"
        print "min:{0} max:{1}".format(min(self._zero_cross_rate_array), max(self._zero_cross_rate_array))

        print "flatness:\n"
        print "min:{0} max:{1}".format(min(self._spectral_flatness_db_array), max(self._spectral_flatness_db_array))

        print "Spectral spread:\n"
        print "min:{0} max:{1}".format(min(self._spectral_spread_array), max(self._spectral_spread_array))

        print "Roll off:\n"
        print "min:{0} max:{1}".format(min(self._spectral_roll_off_array), max(self._spectral_roll_off_array))

        print "Scale:\n"
        print "min:{0} max:{1}".format(min(self._scale_array), max(self._scale_array))

        logging.info("Feature extraction finished successfully")
        return self._song_list

    def process_song(self, file_path):
        features = dict()
        # prepare song to analysis
        try:
            self._current_song_signal = MonoLoader(filename=file_path)()
        except IOError as e:
            logging.error(e)
            sys.exit(1)

        self._preprocess()
        self._spectrum()
        self._spectral_peaks()

        # calculate particular features
        features[FeaturesKeys.ZERO_CROSS_RATE] = self._zero_crossing_rate()
        self._zero_cross_rate_array.append(features[FeaturesKeys.ZERO_CROSS_RATE])

        features[FeaturesKeys.SPECTRAL_COMPLEXITY] = self._spectral_complexity()
        self._spectral_complexity_array.append(features[FeaturesKeys.SPECTRAL_COMPLEXITY])

        features[FeaturesKeys.SPECTRAL_CENTROID] = self._spectral_centroid()
        self._spectral_centroid_array.append(features[FeaturesKeys.SPECTRAL_CENTROID])

        features[FeaturesKeys.SPECTRAL_ROLL_OFF] = self._spectral_roll_off()
        self._spectral_roll_off_array.append(features[FeaturesKeys.SPECTRAL_ROLL_OFF])

        features[FeaturesKeys.SPECTRAL_FLATNESS_DB] = self._spectral_flatness_db()
        self._spectral_flatness_db_array.append(features[FeaturesKeys.SPECTRAL_FLATNESS_DB])

        features[FeaturesKeys.DISSONANCE] = self._dissonance()
        self._dissonance_array.append(features[FeaturesKeys.DISSONANCE])

        features[FeaturesKeys.SCALE] = self._scale()
        self._scale_array.append(features[FeaturesKeys.SCALE])

        features[FeaturesKeys.ONSET_RATE] = self._onset_rate()
        self._onset_rate_array.append(features[FeaturesKeys.ONSET_RATE])

        (spectral_spread, spectral_skewness, spectral_kurtosis) = self._distribution_shape()
        features[FeaturesKeys.SPECTRAL_SPREAD] = spectral_spread
        self._spectral_spread_array.append(features[FeaturesKeys.SPECTRAL_SPREAD])

        features[FeaturesKeys.SPECTRAL_SKEWNESS] = spectral_skewness
        self._spectral_skewness_array.append(features[FeaturesKeys.SPECTRAL_SKEWNESS])

        features[FeaturesKeys.SPECTRAL_KURTOSIS] = spectral_kurtosis
        self._spectral_kurtosis_array.append(features[FeaturesKeys.SPECTRAL_KURTOSIS])

        return features

    def _preprocess(self):
        EqualLoudness()(self._current_song_signal)

    def _zero_crossing_rate(self):
        return ZeroCrossingRate(threshold=0.00)(self._current_song_signal)

    def _spectrum(self):
        self._current_song_signal = Windowing(type=Conf.WINDOWING_TYPE)(self._current_song_signal)
        self._current_song_spectrum = Spectrum()(self._current_song_signal)
        self._curent_song_power_spectrum = self._current_song_spectrum ** 2;
        self._curent_song_centralmoments = CentralMoments()(self._curent_song_power_spectrum)

    def _distribution_shape(self):
        return DistributionShape()(self._curent_song_centralmoments)

    def _spectral_complexity(self):
        return SpectralComplexity(magnitudeThreshold=0.01)(self._current_song_spectrum)

    def _spectral_centroid(self):
        return Centroid(range=1)(self._current_song_spectrum) # correctness of range needs to be checked

    def _spectral_roll_off(self):
        return RollOff()(self._current_song_spectrum)

    def _spectral_flatness_db(self):
        return FlatnessDB()(self._current_song_spectrum)

    def _spectral_peaks(self):
        spectral_peaks_alg = SpectralPeaks(maxFrequency=Conf.SAMPLE_RATE/2,
                                           minFrequency=Conf.MIN_HEARING_RANGE,
                                           orderBy="frequency",
                                           maxPeaks=1000)
        self._current_song_spectral_peaks = spectral_peaks_alg(self._current_song_spectrum)

    def _dissonance(self):
        return Dissonance()(*self._current_song_spectral_peaks)

    def _scale(self):
        pcp = HPCP()(*self._current_song_spectral_peaks)
        (key, scale, strength, first_to_second_relative_strength) = Key()(pcp)
        if scale == "major":
            return 0
        else:
            return 1

    def _onset_rate(self):
        (onset_time, onset_rate) = OnsetRate()(self._current_song_signal)
        return onset_rate

