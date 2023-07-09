"""Test package functions"""

import unittest
import numpy as np
from numpy.testing import assert_allclose, assert_equal
import pyppr


class TestPPRFunctions(unittest.TestCase):
    """Test package functions."""

    def test_ppr_tr(self):
        """Test the ppr_tr() function"""
        func = pyppr.ppr_tr

        assert_equal(func(4, True), 0.08)
        assert_equal(func(5, True), 0.08)
        assert_equal(func(8, True), 0.08)
        assert_equal(func(9, True), 0.08)
        assert_equal(func(4, False), 0.215)
        assert_equal(func(5, False), 0.172)
        assert_equal(func(8, False), 0.086)
        assert_equal(func(9, False), 0.086)

    def test_ppr_net_fv(self):
        """Test the ppr_net_fv() function"""
        func = pyppr.ppr_net_fv

        assert_allclose(func(0.07, 20, 2000, 0.0075, 0, True), 6284.96604462885)
        assert_allclose(func(0.08, 20, 2000, 0.0075, 0, True), 7537.3984722273)
        assert_allclose(func(0.07, 30, 2000, 0.0075, 0, True), 11334.9764510809)
        assert_allclose(func(0.07, 20, 5000, 0.0075, 0, True), 15712.4151115721)
        assert_allclose(func(0.07, 20, 2000, 0.0090, 0, True), 6102.46272758026)
        assert_allclose(func(0.07, 20, 2000, 0.0075, 0.2, True), 7541.9592535546)
        assert_allclose(func(0.07, 4, 2000, 0.0075, 0, False), 2426.9023353861)
        assert_allclose(func(0.07, 20, 2000, 0.0075, np.array([0, 0.2]), 0.08),
                        [6284.9660446288, 7541.9592535546],
                        )
        assert_allclose(func(0.07, 20, np.array([10000, 2000]), 0.0075, np.array([0, 0.2]), 0.08),
                        [31424.830223144, 7541.9592535546],
                        )

    def test_matching_ppr_cost_rate(self):
        """Test the matching_ppr_cost_rate() function"""
        func = pyppr.matching_ppr_cost_rate

        assert_allclose(func(0.07, 30, 0.28, 0.1, 0, True), 0.003749355)
        assert_allclose(func(0.08, 30, 0.28, 0.1, 0, True), 0.0040453035)
        assert_allclose(func(0.07, 20, 0.28, 0.1, 0, True), 0.0038951990)
        assert_allclose(func(0.07, 30, 0.21, 0.1, 0, True), 0.0011480218)
        assert_allclose(func(0.07, 30, 0.28, 0.08, 0, True), 0.0043663720)
        assert_allclose(func(0.07, 30, 0.28, 0.1, 0.2, True), 0.009870102)
        assert_allclose(func(0.07, 30, 0.28, 0.1, 0, False), 0.00356391195)
        assert_allclose(func(0.07, 30, 0.28, 0.1, np.array([0, 0.2]), True),
                        [0.003749355, 0.009870102],
                        )

    def test_matching_underlying_assets_cagr(self):
        """Test the matching_underlying_assets_cagr() function"""
        func = pyppr.matching_underlying_assets_cagr

        assert_allclose(func(20, 0.28, 0.03, 0.005, 0, True), 0.0425058431669653)
        assert_allclose(func(30, 0.28, 0.03, 0.005, 0, True), 0.0487639191457141)
        assert_allclose(func(20, 0.21, 0.03, 0.005, 0, True), 0.104885771066143)
        assert_allclose(func(20, 0.28, 0.05, 0.005, 0, True), 0.0529580684369604)
        assert_allclose(func(20, 0.28, 0.03, 0.0075, 0, True), 0.074191614710127)
        assert_allclose(func(20, 0.28, 0.17, 0.005, 0.2, True), 0.0198595625251912)
        assert_allclose(func(20, 0.28, 0.03, 0.005, 0, False), 0.0442031116675074)
        assert_allclose(func(20, 0.28, np.array([0.05, 0.1]), 0.0075, np.array([0, 0.2]), True),
                        [0.0941281436701107, 0.0149095359038968],
                        )

    def test_matching_ppr_extra_value(self):
        """Test the matching_ppr_extra_value() function"""
        func = pyppr.matching_ppr_extra_value

        assert_allclose(func(0.07, 20, 0.28, 0.0075, 0, True), 0.0248877718180402)
        assert_allclose(func(0.08, 20, 0.28, 0.0075, 0, True), 0.0365275417642938)
        assert_allclose(func(0.07, 30, 0.28, 0.0075, 0, True), -0.0162017466874923)
        assert_allclose(func(0.07, 20, 0.21, 0.0075, 0, True), -0.0381284875935851)
        assert_allclose(func(0.07, 20, 0.28, 0.01, 0, True), -0.0242433779172004)
        assert_allclose(func(0.07, 20, 0.28, 0.0075, 0.2, True), 0.229865326181649)
        assert_allclose(func(0.07, 20, 0.28, 0.0075, 0, False), 0.0203307177264629)
        assert_allclose(func(0.07, 20, 0.28, np.array([0.005, 0.0075]), 0, True),
                        [0.0764274396173414, 0.0248877718180402]
                        )
