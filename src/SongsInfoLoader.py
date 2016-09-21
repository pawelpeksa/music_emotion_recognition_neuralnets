# -*- coding: utf-8 -*-
"""
@author: Paweł Pęksa
"""

import logging
import csv
import sys
from Keys import Keys
from Configuration import Configuration as Conf


class SongsInfoLoader:
    """Class used to load information about audio files"""
    def __init__(self, songs_info_path):
        logging.info("Initialising SongInfoLoader with {0} as song info file path".format(songs_info_path))
        self._songs_info_path = songs_info_path
        self._songs_list = list()
        self._songs_purpose_list = list()

    def get_songs_list(self):
        return self._process()

    def get_songs_purpose(self):
        self._get_purpose()
        return self._songs_purpose_list

    def _process(self):
        logging.info("Processing csv file")
        self._process_csv_file()
        return self._songs_list

    def _process_csv_file(self):
        logging.info("Process information about songs")
        try:
            with open(self._songs_info_path) as csvfile:
                song_info_reader = csv.reader(csvfile)
                for row in song_info_reader:
                    song_info = dict()

                    if not row[Conf.INDEX_SONG_ID] == row[Conf.INDEX_SONG_ID_2]:
                        error_info = "song_id and song_id_2 are not equal. Probably file {0} is corrupted"\
                            .format(self._songs_info_path)
                        logging.error(error_info)
                        sys.exit(1)

                    song_info[Keys.SONG_ID] = row[Conf.INDEX_SONG_ID]
                    song_info[Keys.SONG_FILE] = row[Conf.INDEX_FILE_NAME]
                    song_info[Keys.SONG_AROUSAL_AVG] = row[Conf.INDEX_MEAN_AROUSAL]
                    song_info[Keys.SONG_VALENCE_AVG] = row[Conf.INDEX_MEAN_VALENCE]

                    self._songs_list.append(song_info)

                self._songs_list.pop(0) # get rid of first entry which is just labels from csv file

        except IOError as e:
            logging.error(e)
            sys.exit(1)
        logging.info("Processing song information successful")

    def _get_purpose(self):
        logging.info("Get song purpose from csv")
        try:
            with open(self._songs_info_path) as csvfile:
                song_info_reader = csv.reader(csvfile)
                for row in song_info_reader:
                    song_purpose = dict()

                    if not row[Conf.INDEX_SONG_ID] == row[Conf.INDEX_SONG_ID_2]:
                        error_info = "song_id and song_id_2 are not equal. Probably file {0} is corrupted"\
                            .format(self._songs_info_path)
                        logging.error(error_info)
                        sys.exit(1)

                    song_purpose[Keys.SONG_ID] = row[Conf.INDEX_SONG_ID]
                    song_purpose[Keys.SONG_PURPOSE] = row[Conf.INDEX_PURPOSE]

                    self._songs_purpose_list.append(song_purpose)

                self._songs_purpose_list.pop(0)  # get rid of first entry which is just labels from csv file

        except IOError as e:
            logging.error(e)
            sys.exit(1)
        logging.info("Processing song information successful")


