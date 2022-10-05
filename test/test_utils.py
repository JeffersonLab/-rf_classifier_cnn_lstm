from unittest import TestCase
import os
import sys
import unittest

import numpy as np
import pandas as pd

app_root = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__))))
app_lib = os.path.join(app_root, "lib")
sys.path.insert(0, app_lib)

import utils


class TestUtils(TestCase):

    def test_standard_scaling(self):
        df = pd.DataFrame({'a': [-1., 1., -1., 1.],
                           'b': [5., 5., 5., 5.],
                           'c': [10., 20., 10., 20.],
                           'd': [1, 2, 4, 5]})

        result = utils.standard_scaling(df, fill=-100.0)
        expected = pd.DataFrame({'a': [-1., 1., -1., 1.],
                                 'b': [-100., -100., -100., -100.],
                                 'c': [-1., 1., -1., 1.],
                                 'd': [-1.26491106, -0.63245553,  0.63245553,  1.26491106]})

        pd.testing.assert_frame_equal(expected, result)

    def test_softmax1(self):
        x = np.array([11, 11, 11, 11])
        exp_dist = np.array([0.25, 0.25, 0.25, 0.25])
        exp_idx = 0
        res_idx, res_dist = utils.softmax(x)
        np.testing.assert_equal(res_idx, exp_idx)
        np.testing.assert_equal(res_dist, exp_dist)

    def test_softmax2(self):
        x = np.array([0, 20, 0, 0])
        exp_dist = np.array([2.061153609693495e-09, 0.9999999938165391, 2.061153609693495e-09, 2.061153609693495e-09])
        exp_idx = 1
        res_idx, res_dist = utils.softmax(x)
        np.testing.assert_equal(res_idx, exp_idx)
        np.testing.assert_equal(res_dist, exp_dist)

    def test_softmax3(self):
        x = np.array([0, 0, -5, 5])
        exp_dist = np.array([0.006648056670790155, 0.006648056670790155, 4.4794253494700645e-05, 0.9866590924049249])
        exp_idx = 3
        res_idx, res_dist = utils.softmax(x)
        np.testing.assert_equal(res_idx, exp_idx)
        np.testing.assert_equal(res_dist, exp_dist)

