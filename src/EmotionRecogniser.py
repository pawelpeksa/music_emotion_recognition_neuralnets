# -*- coding: utf-8 -*-
"""
@author: Paweł Pęksa
"""

import neurolab as nl
import numpy as np
import matplotlib.pyplot as plt
from Configuration import Configuration as Conf
from FeaturesMinMax import FeaturesMinMax
import logging
from neurolab import trans


class EmotionRecogniser(object):
    """Class containing neural network object, used to train and evaluate"""
    def __init__(self, dev_data, dev_targets, eval_data, eval_targets, features_min_max):
        # init data
        logging.info("Initialising emotion recognising")
        self._error = -1
        self._dev_data = dev_data
        self._dev_targets = dev_targets
        self._eval_data = eval_data
        self._eval_targets = eval_targets
        self._error_list = list()
        # init neural network
        self._net = nl.net.newff(
                                [[-2.0, 2.0],
                                 [-2.0, 2.0],
                                 [-2.0, 2.0],
                                 [-2.0, 2.0],
                                 [-2.0, 2.0],
                                 [-2.0, 2.0],
                                 [-2.0, 2.0],
                                 [-2.0, 2.0],
                                 [-2.0, 2.0],
                                 [-2.0, 2.0],
                                 [-2.0, 2.0]
                                 ],

                                [Conf.HIDDEN_NEURONS, Conf.OUTPUTS]
                                )
        # self._net.trainf = nl.train.train_rprop
        logging.info("Neural network created")

    def get_eval_targets(self):
        return self._eval_targets

    def set_net(self, net):
        self._net = net

    def train(self):
        # self._net.trainf = nl.train.train_gdx
        # self._net.init()
        err = self._net.train(self._dev_data, self._dev_targets)
        self._error_list = err
        self._error = err.pop()
        logging.info("Neural network trained")
        return err

    def evaluate(self):
        ev = self._net.sim(self._eval_data)
        logging.info("Neural network evaluated")
        return ev

    def evaluate_data(self, data):
        ev = self._net.sim(data)
        logging.info("Neural network evaluated")
        return ev

    def save_net(self, path):
        try:
            self._net.save(path+str(self._error))
            logging.info("Neural succesfully network saved at:{0}".format(Conf.NET_FILE))
        except IOError as e:
            logging.error(e)



