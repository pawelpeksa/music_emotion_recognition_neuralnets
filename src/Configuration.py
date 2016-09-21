# -*- coding: utf-8 -*-
"""
@author: Paweł Pęksa
"""
import logging


class Configuration(object):
    """Class containing configuration constants"""
    def __init__(self):
        pass

    # ------------------ Neural network parameteres ------------------ #

    # two outputs, one for valence, one for arousal, should not be change unless you want to describe
    # emotion using in diffrent way
    OUTPUTS = 2

    # number of neurons in hidden layer
    HIDDEN_NEURONS = -1  # this is going to be changed to DEFAULT_HIDDEN_NEURONS if nothing is passed in command line
    DEFAULT_HIDDEN_NEURONS = 30

    # ----------------------------------------------------------------- #

    # ------------------ Flags ------------------ #

    ARG_ANALYSE = "-a"
    ARG_ANALYSE_HELP = "Analyse songs during program execution. " \
                       "Otherwise it's going to load alread processed songs if exist"

    ARG_TRAIN = "-t"
    ARG_TRAIN_HELP = "Train neural network during program execution. " \
                     "Otherwise it's going to load ready neural network if exists"

    ARG_NEURONS = "-n"
    ARG_NEURONS_HELP = "Set amount of hidden neurons in net. By default " + str(DEFAULT_HIDDEN_NEURONS)

    ARG_PLOT = "-p"
    ARG_PLOT_HELP = "Plot comparison of neural network recognition and expected results. Use only with -e"

    ARG_EVAL = "-e"
    ARG_EVAL_HELP = "Evaluate neural network"

    ARG_SONG = "-s"
    ARG_SONG_HELP = "Flag allows to analyze one song which is loaded and then analysed by neural network if any exist\n" \
                    "Should be used without any other argument"
    # ----------------------------------------------------------------- #

    # ------------------ logging configuration ------------------ #

    LOGGING_PATH = "outputs/emusic.log"
    LOGGING_FORMAT = "%(asctime)s %(levelname)s %(message)s "
    LOGGING_LEVEL = logging.DEBUG

    # ----------------------------------------------------------------- #

    # ------------------ file paths ------------------ #

    # songs info file paths
    SONG_INFO_WITH_ANNOTATIONS_PATH = "resources/annotations/song_list_static_annotations_scaled.csv"
    #  SONG_INFO_WITH_ANNOTATIONS_PATH = "resources/annotations/trimmedList.csv"

    # path to folder with songs
    SONG_FOLDER_PATH = "resources/clips/"

    # neural network file path
    NET_FILE = "outputs/new/neuralNetwork.obj"

    # default neural network file path
    DEFAULT_NET_FILE = "bestEvalNetwork.obj"

    # pickled songs file path
    PICKLED_SONGS_PATH = "outputs/pickledSongs.obj"

    # error list file path
    PICKLED_ERR_PATH = "outputs/err.obj"

    # evalution results file paths
    EVAL_RESULTS_PATH = "outputs/evalResults.txt"
    EVAL_TARGETS_PATH = "outputs/evalTargets.txt"

    # ----------------------------------------------------------------- #

    # ------------------ audio files information ------------------ #

    SAMPLE_RATE = 44100  # not needed to pass to functions because default sample rate = 44100

    # ----------------------------------------------------------------- #

    # ------------------ other ------------------ #

    # lower limit of human hearing range
    MIN_HEARING_RANGE = 20
    WINDOWING_TYPE = "hann"

    # CSV SONG_INFO_WITH_ANNOTATIONS_PATH indexes
    INDEX_SONG_ID = 0
    INDEX_SONG_ID_2 = 8
    INDEX_FILE_NAME = 1
    INDEX_MEAN_AROUSAL = 13
    INDEX_MEAN_VALENCE = 14
    INDEX_PURPOSE = 7

    # ploter configuration
    X_TICK_LABELSIZE = 10

    # ----------------------------------------------------------------- #




