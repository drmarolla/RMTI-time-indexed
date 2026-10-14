# Copyright 2026 Cesar Marolla
# Licensed under the Apache License, Version 2.0 (see LICENSE).
"""Tests for the v2.2.0 time-indexed layer and the core v2.2.0 additions.

Expected workbook values below were read from the LibreOffice-recalculated
Trajectory sheet of calculators/RMTI_HCC_Calculator_v2.3.0.xlsx (not from this
module), so these are independent parity checks, not self-comparisons.
"""
import unittest
from dataclasses import replace

from core.rmti_core import score, assess, RHO_ANCHORS_HCC, RHO_TYPOLOGY_ANCHORS, __version__
from dynamic.rmti_dynamic import (HCC_PARAMS, DISASTER_PARAMS, TrajectoryParams,
                                  run_trajectory, steady_state_gains, tier_changes)

A_OBS, A_DLV = [2, 1, 1, 0], [.4, .55, .7, .75]
B_OBS, B_DLV = [2, 3, 4, 5], [.4, .4, .35, .35]


class CoreV22(unittest.TestCase):
    def test_version(self):
        self.assertEqual(__version__, "2.3.0")

    def test_raw_keys_and_unchanged_display(self):
        s = score(0.30, 0.65, 0.60, 0.50, 3)
        self.assertEqual(s["R"], 0.059)                     # the rounding-regression value
        self.assertAlmostEqual(s["R_raw"], 0.0585, places=12)
        self.assertAlmostEqual(s["IR_raw"], 0.117, places=12)

    def test_validation(self):
        for bad in (dict(L=1.1), dict(E_sel=-0.1), dict(V=2), dict(rho=1.0),
                    dict(rho=1.3), dict(rho=-0.2), dict(C=6)):
            kw = dict(L=.3, E_sel=.5, V=.5, rho=.2, C=3); kw.update(bad)
            with self.assertRaises(ValueError, msg=str(bad)):
                score(**kw)

    def test_postures_argument_kept_from_v21(self):
        custom = {f"Tier {i}": f"x{i}" for i in range(1, 6)}
        custom = {k: k for k in custom}
        r = assess(N=1000, L=.5, E_sel=.5, V=.5, rho_now=.2, postures={
            "Tier 1 - Low": "a", "Tier 2 - Moderate": "b", "Tier 3 - High": "c",
            "Tier 4 - Severe": "d", "Tier 5 - Critical": "e"})
        self.assertIn(r["posture_now"], "abcde")

    def test_ladders_distinct_and_labelled(self):
        self.assertEqual(RHO_ANCHORS_HCC["optimised"], 0.65)
        self.assertEqual(RHO_TYPOLOGY_ANCHORS["optimised"], 0.70)


class DynamicParity(unittest.TestCase):
    def test_filter_off_reproduces_draft_table(self):
        off = replace(HCC_PARAMS, filter_on=False)
        a = [r["R_display"] for r in run_trajectory(.3, .65, 3, .2, A_OBS, A_DLV, off)]
        b = [r["R_display"] for r in run_trajectory(.3, .65, 3, .2, B_OBS, B_DLV, off)]
        self.assertEqual(a, [0.081, 0.055, 0.042, 0.031])
        self.assertEqual(b, [0.081, 0.094, 0.113, 0.127])

    def test_filter_on_matches_workbook(self):
        a = run_trajectory(.3, .65, 3, .2, A_OBS, A_DLV)
        b = run_trajectory(.3, .65, 3, .2, B_OBS, B_DLV)
        for got, want in zip([r["R"] for r in a], [0.0806, 0.060206, 0.04355, 0.033967]):
            self.assertAlmostEqual(got, want, places=6)
        for got, want in zip([r["R"] for r in b], [0.0806, 0.0871, 0.104146, 0.118718]):
            self.assertAlmostEqual(got, want, places=6)
        for got, want in zip([r["rho"] for r in a], [.2, .35, .5, .55]):
            self.assertAlmostEqual(got, want, places=12)

    def test_tiers(self):
        a = run_trajectory(.3, .65, 3, .2, A_OBS, A_DLV)
        self.assertEqual([r["tier"][:6] for r in a], ["Tier 2", "Tier 2", "Tier 1", "Tier 1"])
        self.assertEqual(tier_changes(a)[0]["to"], "Tier 1 - Low")

    def test_steady_state_gains_match_workbook_defaults(self):
        al, be = steady_state_gains()
        self.assertEqual(round(al, 2), 0.41)
        self.assertEqual(round(be, 2), 0.09)


class DynamicBehaviour(unittest.TestCase):
    def test_missed_visit_carries_forward(self):
        rows = run_trajectory(.3, .65, 3, .2, [2, None, 1], [.4, .5, .6])
        self.assertAlmostEqual(rows[1]["level"], rows[0]["level"] + rows[0]["slope"])
        self.assertEqual(rows[1]["slope"], rows[0]["slope"])

    def test_missing_delivery_carries_rho(self):
        rows = run_trajectory(.3, .65, 3, .2, [2, 2, 2], [.4, None, .6])
        self.assertEqual(rows[1]["rho"], .2)
        self.assertAlmostEqual(rows[2]["rho"], .4)      # vs last observed delivery .4

    def test_rho_clamped_to_ceiling(self):
        rows = run_trajectory(.3, .65, 3, .9, [2, 2], [0.0, 1.0])
        self.assertEqual(rows[1]["rho"], HCC_PARAMS.rho_ceiling)

    def test_rho_clamped_at_zero(self):
        rows = run_trajectory(.3, .65, 3, .1, [2, 2], [1.0, 0.0])
        self.assertEqual(rows[1]["rho"], 0.0)

    def test_V_bounded_by_anchors(self):
        rows = run_trajectory(.3, .65, 3, .2, [0, 6, 0, 6, 0, 6], [.5] * 6)
        for r in rows:
            self.assertTrue(HCC_PARAMS.v_lo <= r["V"] <= HCC_PARAMS.v_hi)

    def test_input_validation(self):
        with self.assertRaises(ValueError): run_trajectory(.3, .65, 3, .2, [], [])
        with self.assertRaises(ValueError): run_trajectory(.3, .65, 3, .2, [1], [.5, .5])
        with self.assertRaises(ValueError): run_trajectory(.3, .65, 3, .2, [None], [.5])
        with self.assertRaises(ValueError): run_trajectory(.3, .65, 3, .2, [7], [.5])
        with self.assertRaises(ValueError): run_trajectory(.3, .65, 3, .2, [1], [1.5])
        with self.assertRaises(ValueError): run_trajectory(.3, .65, 3, .99, [1], [.5])
        with self.assertRaises(ValueError): TrajectoryParams(v_lo=.9, v_hi=.4)

    def test_uses_core_score_so_core_validation_applies(self):
        with self.assertRaises(ValueError):
            run_trajectory(1.2, .65, 3, .2, [1], [.5])        # L out of range, raised by core

    def test_disaster_preset_scale(self):
        rows = run_trajectory(.3, .65, 3, .2, [5, 4, 3], [.2, .4, .6], DISASTER_PARAMS)
        self.assertEqual(len(rows), 3)
        with self.assertRaises(ValueError):
            run_trajectory(.3, .65, 3, .2, [11], [.2], DISASTER_PARAMS)

    def test_custom_postures(self):
        post = {"Tier 1 - Low": "P1", "Tier 2 - Moderate": "P2", "Tier 3 - High": "P3",
                "Tier 4 - Severe": "P4", "Tier 5 - Critical": "P5"}
        rows = run_trajectory(.3, .65, 3, .2, [2], [.4], postures=post)
        self.assertEqual(rows[0]["posture"], "P2")


if __name__ == "__main__":
    unittest.main()
