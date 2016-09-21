# -*- coding: utf-8 -*-
"""
@author: Paweł Pęksa
"""

from SongsInfoLoader import SongsInfoLoader
from AudioFeatureExtractor import AudioFeatureExtractor
from EmotionRecogniser import EmotionRecogniser
from Utils import *
from Plotter import Plotter
from timeit import default_timer as timer
from neurolab import error
from FeaturesMinMax import FeaturesMinMax


class Application(object):
    def __init__(self):
        self._recogniser = None
        self._processed_songs = None
        self._song_list = None
        self._song_purpose_list = None
        setup_logging(Conf.LOGGING_PATH, Conf.LOGGING_LEVEL, Conf.LOGGING_FORMAT)
        parser = setup_parser()
        self._args = parser.parse_args()
        self._set_flags()
        logging.info("Launched with arguments:{0}".format(self._args))

    def _timer(f):
        def wrapper(self):
            start_time = timer()
            f(self)
            end_time = timer()
            seconds = (end_time - start_time)
            minutes, rest_seconds = divmod(seconds, 60)
            logging.info("Execution time:{0} min and {1} sec".format(minutes, rest_seconds))
        return wrapper

    @_timer
    def run(self):
        if self._s_flag:
            self._evaluate_song()
            return

        set_hidden_neurons(self._args)
        self._load_song_info()
        self._process_songs(self._song_list)

        self._create_recogniser()
        eval_error = 0
        if self._e_flag:
            eval_results = self._recogniser.evaluate()
            eval_targets = self._recogniser.get_eval_targets()
            # 1st item in each list is valence
            # 2nd item in each list is arousal
            logging.info("Save eval results and eval targets to file")
            save_for_plot(eval_results, eval_targets)
            save_array(eval_results, Conf.EVAL_RESULTS_PATH)
            save_array(eval_targets, Conf.EVAL_TARGETS_PATH)
            save_for_plot(eval_targets, eval_results)
            eval_targets = eval_targets.astype(float)
            eval_error = error.SSE()(eval_targets, eval_results)
            save_list("plotting/error.dat", self._recogniser._error_list)
            logging.info("Error with evaluation dataset:{0}".format(eval_error))
            print "Check Overtrain:"
            dev_results = self._recogniser.evaluate_data(self._recogniser._dev_data[0:70])
            print self._recogniser._net.errorf(self._recogniser._dev_targets[0:70].astype(float), dev_results)
            if self._p_flag:
                self._plot(eval_results, eval_targets)

        run_bash("paste plotting/arousal.dat plotting/valence.dat plotting/processedSongs.dat > plotting/data.dat")
        pickle_object(self._recogniser, Conf.NET_FILE + str(self._recogniser._error)+ "__" + str(eval_error))

    def _set_flags(self):
        self._t_flag = True if getattr(self._args, Conf.ARG_TRAIN[1:]) else False
        self._a_flag = True if getattr(self._args, Conf.ARG_ANALYSE[1:]) else False
        self._p_flag = True if getattr(self._args, Conf.ARG_PLOT[1:]) else False
        self._e_flag = True if getattr(self._args, Conf.ARG_EVAL[1:]) else False
        self._s_flag = True if getattr(self._args, Conf.ARG_SONG[1:]) else False

    def _evaluate_song(self):
        logging.info("Analysing one song started")
        features = AudioFeatureExtractor(list()).process_song(getattr(self._args, Conf.ARG_SONG[1:]))
        logging.info("Features extracted")
        self._load_recogniser()
        # workaround
        # need to create dict song in order to use get_feature_list
        song = dict()
        song[Keys.SONG_FEATURES] = features
        features_list = get_feature_list(song)
        result = self._recogniser.evaluate_data([features_list])
        logging.info("[[valence, arousal]]")
        logging.info(result)

    def _load_song_info(self):
        songs_info_loader = SongsInfoLoader(Conf.SONG_INFO_WITH_ANNOTATIONS_PATH)
        self._song_list = songs_info_loader.get_songs_list()
        self._song_purpose_list = songs_info_loader.get_songs_purpose()

    def _process_songs(self, songs_list):
        if self._a_flag:
            logging.info("Start analysing songs")
            audio_feature_extractor = AudioFeatureExtractor(songs_list)
            self._processed_songs = audio_feature_extractor.process()
            # self._scale_features()
            pickle_object(self._processed_songs, Conf.PICKLED_SONGS_PATH)
        else:
            self._load_processed_songs()
            self._scale_features()
            self._save_processed_songs()
            # save

    def _load_processed_songs(self):
        try:
            self._processed_songs = open_pickle(Conf.PICKLED_SONGS_PATH)
            logging.info("Analysed songs loaded from: {0}".format(Conf.PICKLED_SONGS_PATH))
        except IOError as e:
            logging.error(e)
            logging.error("File with analysed songs hasn't been found. \
                Launch program with parameter -a in order to analyse songs")
            sys.exit(1)

    def _create_recogniser(self):
        dev_songs_list, eval_song_list = split_songs_for_purpose(self._processed_songs, self._song_purpose_list)

        dev_input, dev_targets = change_to_proper_format(dev_songs_list)
        eval_input, eval_targets = change_to_proper_format(eval_song_list)
        self._recogniser = EmotionRecogniser(dev_input, dev_targets, eval_input, eval_targets, get_all_features_min_max())

        if self._t_flag:
            logging.info("Starting neural network training")
            self._recogniser.train()
            logging.info("Neural network trained")
        else:
            self._load_recogniser()

    def _load_recogniser(self):
        try:
            self._recogniser = open_pickle(Conf.DEFAULT_NET_FILE)
            logging.info("Default neural network loaded from: {0}".format(Conf.DEFAULT_NET_FILE))
        except IOError as e:
            logging.error(e)
            logging.error("Default file with neural network hasn't been found\n. \
                Launch program with parameter -t in order to create and train new neural network")
            try:
                self._recogniser = open_pickle(Conf.NET_FILE)
                logging.info("Neural network loaded from: {0}".format(Conf.NET_FILE))
            except IOError as e:
                logging.error(e)
                logging.error("Any file with neural network hasn't been found\n. \
                Launch program with parameter -t in order to create and train new neural network")
                sys.exit(1)

    @staticmethod
    def _plot(eval_results, eval_targets):
        plotter = Plotter(eval_results, eval_targets)

        plotter.plot_arousal()
        plotter.show()

        plotter.plot_valence()
        plotter.show()

    def _scale_features(self):
        # def scale(x, min_value, max_value, a, b):
        a = -2.0
        b = 2.0
        feature_min_max = FeaturesMinMax()
        min_max = feature_min_max.get_all_members()
        features_keys = FeaturesKeys()
        features_keys_list = features_keys.get_all_members()

        for song in self._processed_songs:
            for key, min_max_key in zip(features_keys_list, min_max):

                min_max_value = getattr(feature_min_max,min_max_key)
                min_value = min_max_value[0]
                max_value = min_max_value[1]
                key = getattr(features_keys, key)
                original_value = song[Keys.SONG_FEATURES][key]
                song[Keys.SONG_FEATURES][key] = scale(original_value, min_value, max_value, a, b)

    def _save_processed_songs(self):
        f = open('plotting/processedSongs.dat', 'w')
        features_keys = FeaturesKeys()
        features_keys_list = features_keys.get_all_members()
        f.write
        for key in features_keys_list:
            f.write(key+" ")

        f.write("\n")
        for song, song_purpose in zip(self._processed_songs,self._song_purpose_list):
            if not song_purpose[Keys.SONG_PURPOSE] == Keys.EVALUATION_SONG:
                continue
            for key in features_keys_list:
                key = getattr(features_keys, key)
                f.write("{0}\t".format(song[Keys.SONG_FEATURES][key]))
            f.write("\n")

        f.close()