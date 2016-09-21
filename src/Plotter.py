#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Paweł Pęksa
"""

from matplotlib import pylab as plt
from Configuration import Configuration as Conf
import numpy as np
import matplotlib.patches as mpatches


class Plotter:
    def __init__(self, results, targets):
        self._data = results
        self._targets = targets

        self._x_targets = [x for [x, y] in targets]
        self._y_targets = [y for [x, y] in targets]

        self._x = [x for [x, y] in results]
        self._y = [y for [x, y] in results]

        plt.rcParams['xtick.labelsize'] = Conf.X_TICK_LABELSIZE

    def plot_scatter(self, data, color="green", marker="o"):
        plt.scatter(self._x, self._y, c=color, marker=marker)

    def plot_valence(self):
        self._set_grid()
        self._set_axis_ranges()
        self._set_valence_labels()

        plt.plot(self._x, 'r.')
        plt.plot(self._x_targets, 'g.')
        self._set_legend()

    def plot_arousal(self):
        self._set_grid()
        self._set_axis_ranges()
        self._set_arousal_labels()

        plt.plot(self._y, 'r.')
        plt.plot(self._y_targets, 'g.')
        self._set_legend()

    @staticmethod
    def _set_arousal_labels():
        plt.xlabel('song no.')
        plt.ylabel('arousal')

    @staticmethod
    def _set_valence_labels():
        plt.xlabel('song no.')
        plt.ylabel('valence')

    @staticmethod
    def _set_grid():
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ticks = np.arange(0, 70, 1)
        ax.set_xticks(ticks)
        plt.grid(axis="x")

    @staticmethod
    def _set_axis_ranges():
        plt.xlim(-1, 70)
        plt.ylim(-1, 1)

    @staticmethod
    def _set_legend():
        plt.legend(["neural network result", "expected value"], loc="best", numpoints=1)

    @staticmethod
    def _set_ticks():
        fig = plt.figure()
        ax = fig.gca()
        ax.set_yticks(np.arange(0, 1., 0.1))

    @staticmethod
    def show():
        plt.show()

# how to put labels for each point
# labels = ['{0}'.format(i) for i in range(len(x_ev))]
# for label, x, y in zip(labels, x_ev, y_ev):
#    pl.annotate(label, xy=(x,y))
