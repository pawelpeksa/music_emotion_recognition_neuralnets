#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Paweł Pęksa
"""

import logging
import os
import sys
import neurolab as nl
import numpy as np
import pickle
import argparse
import subprocess
from Keys import Keys
from FeaturesKeys import FeaturesKeys
from FeaturesMinMax import FeaturesMinMax
from pprint import pprint
from Configuration import Configuration as Conf
import numpy as np


class LessThanFilter(logging.Filter):
    """Class used to filter logging messages"""
    def __init__(self, exclusive_maximum, name=""):
        super(LessThanFilter, self).__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record):
        # non-zero return means we log this message
        return 1 if record.levelno < self.max_level else 0


def setup_parser():
    parser = argparse.ArgumentParser(description="Emusic")
    parser.add_argument(Conf.ARG_ANALYSE, action="store_true", help=Conf.ARG_ANALYSE_HELP)
    parser.add_argument(Conf.ARG_TRAIN, action="store_true", help=Conf.ARG_TRAIN_HELP)
    parser.add_argument(Conf.ARG_PLOT, action="store_true", help=Conf.ARG_PLOT_HELP)
    parser.add_argument(Conf.ARG_EVAL, action="store_true", help=Conf.ARG_EVAL_HELP)
    parser.add_argument(Conf.ARG_SONG, type=str, help=Conf.ARG_SONG_HELP, metavar="FILE")

    parser.add_argument(Conf.ARG_NEURONS,
                        action="store",
                        type=int,
                        default=Conf.DEFAULT_HIDDEN_NEURONS,
                        help=Conf.ARG_NEURONS_HELP)
    return parser


def setup_logging(log_path, logging_level, logging_format):
    # remove log file if exists
    try:
        os.remove(log_path)
    except OSError:
        pass

    logging.basicConfig(filename=log_path, level=logging_level, format=logging_format)

    std_out = logging.StreamHandler(stream=sys.stdout)
    std_err = logging.StreamHandler(stream=sys.stderr)

    std_err.setLevel(logging.ERROR)
    std_out.addFilter(LessThanFilter(logging.ERROR))

    logging.getLogger().addHandler(std_err)
    logging.getLogger().addHandler(std_out)

    logging.info("Logging has been initialised")


def split_songs_for_purpose(all_songs_list, song_purpose_list):
    dev_song_list = list()
    eva_song_list = list()

    for song, song_purpose in zip(all_songs_list, song_purpose_list):
        if not song[Keys.SONG_ID] == song_purpose[Keys.SONG_ID]:
                        error_info = "song_id and song_id_2 are not equal. Something went wrong"
                        logging.error(error_info)
                        sys.exit(1)

        if song_purpose[Keys.SONG_PURPOSE] == Keys.DEVELOPMENT_SONG:
            dev_song_list.append(song)
        else:
            eva_song_list.append(song)

    return [dev_song_list, eva_song_list]


def change_to_proper_format(input_data):
    """returns tuple (features ndarray, expected results ndarray)"""
    targets = list()
    songs_features = list()

    for song in input_data:
        targets.append([song[Keys.SONG_VALENCE_AVG], song[Keys.SONG_AROUSAL_AVG]])
        feature_list = get_feature_list(song)
        songs_features.append(feature_list)

    return np.array(songs_features), np.array(targets)


def get_all_feature_keys():
    feature_keys_cls = FeaturesKeys()
    return feature_keys_cls.get_all_members()


def get_feature_list(song):
    feature_keys = get_all_feature_keys()
    feature_list = list()
    for key in feature_keys:
        feature_list.append(song[Keys.SONG_FEATURES][getattr(FeaturesKeys, key)])
    return feature_list


def print_weights_of_saved_net(path):
    try:
        net = nl.load(path)
        for layer in net.layers:
            pprint(layer.np['w'])
    except IOError as e:
        logging.error("Can not open file to print weights of net")
        logging.error(e)


def pickle_object(obj, file_path):
    """serialise object at file path"""
    try:
        with open(file_path, "wb") as pickle_file:
            pickle.dump(obj, pickle_file)
            logging.info("Succesfully pickled object at:{0}".format(file_path))
    except IOError as e:
        logging.error("Can not pickle object")
        logging.error(e)


def open_pickle(file_path):
    """open pickle at file path"""
    with open(file_path, "rb") as pickle_file:
        obj = pickle.load(pickle_file)
        logging.info("Succesfully load pickled object")
        return obj


def get_all_features_min_max():
    """Get list of [min,max] from class FeaturesMinMax"""
    features_min_max = FeaturesMinMax()
    class_members = features_min_max.get_all_members()
    values = list()

    for member in class_members:
        value = getattr(features_min_max, member)
        values.append(value)

    return values


def set_hidden_neurons(args):
    """set the value for hidden neurons amount"""
    Conf.HIDDEN_NEURONS = getattr(args, Conf.ARG_NEURONS[1:])


def save_array(array, file_path):
    with open(file_path, "w") as file:
        for sub_arr in array:
            for num in sub_arr:
                file.write(str(num))
                file.write(" ")
            file.write("\n")


def scale(x, min_value, max_value, a, b):
    return (((b-a)*(x-min_value))/(max_value-min_value)) + a


def save_for_plot(eval_results, eval_targets):
    # 1st item in each list is valence
    # 2nd item in each list is arousal
    valence_file = open("plotting/valence.dat", "w")
    arousal_file = open("plotting/arousal.dat", "w")

    valence_file.write("#valence_output valence_target\n")
    arousal_file.write("#arousal_output arousal_target\n")

    for result, target in zip(eval_results, eval_targets):
        valence_file.write("{0}\t\t{1}\n".format(target[0], result[0]))
        arousal_file.write("{0}\t\t{1}\n".format(target[1], result[1]))

    valence_file.close()
    arousal_file.close()


def run_bash(command):
    call_bash = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    return call_bash.communicate()[0]


def save_list(file_path, list):
    with open(file_path, "w") as f:
        for i in list:
            f.write("{0}\n".format(i))

