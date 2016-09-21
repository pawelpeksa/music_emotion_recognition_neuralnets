#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Paweł Pęksa
"""

import neurolab as nl
from SongsInfoLoader import SongsInfoLoader
from Utils import *
from Configuration import Configuration as Conf
from matplotlib import pylab as pl
from pprint import pprint


def some_func():
    try:
        net = nl.load(Conf.NET_FILE)
    except IOError as e:
        print e

    songs_info_loader = SongsInfoLoader(Conf.SONG_INFO_WITH_ANNOTATIONS_PATH)
    songs_list = songs_info_loader.get_songs_list()

    # split song for development list and evaluate list
    dev_songs_list, eval_song_list = split_songs_for_purpose(songs_list)

    dev_input, dev_targets = change_to_proper_format(dev_songs_list)
    eval_input, eval_targets = change_to_proper_format(eval_song_list)
    result = net.sim(dev_targets)
    pprint(result)


if __name__ == "__main__":
    err = open_pickle(Conf.PICKLED_ERR_PATH)
    processed_songs = open_pickle(Conf.PICKLED_SONGS_PATH)
    net = nl.load(Conf.NET_FILE)

    # ev = net.sim(eval_data)
    pl.plot(err)
    pl.show()

