# Copyright 2026 Cesar Marolla
# Licensed under the Apache License, Version 2.0 (see ../LICENSE).
"""Tests for rmti_oncoclastics.py. Run from the repository root:

    python -m unittest discover -s oncoclastics -p "test_*.py" -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rmti_oncoclastics import (RHO_BIO_ANCHORS, RHO_BIO_CEILING, RHO_BIO_DESCRIPTORS, care_disruption,  # noqa: E402
                               combine_rho, oncoclastic_events, rho_bio_from_anchor,
                               run_two_sense_trajectory, score_two_senses)
from core.rmti_core import score  # noqa: E402
from dynamic.rmti_dynamic import HCC_PARAMS, run_trajectory  # noqa: E402

A_OBS, A_DLV = [2, 1, 1, 0], [.40, .55, .70, .75]
B_OBS, B_DLV = [2, 3, 4, 5], [.40, .40, .35, .35]


class Anchors(unittest.TestCase):
    def test_aligned_with_existing_resilience_ladders(self):
        from core.rmti_core import RHO_ANCHORS_HCC, RHO_TYPOLOGY_ANCHORS
        scored = [v for k, v in RHO_BIO_ANCHORS.items() if k != "not_scored"]
        # same span as the disaster-risk ladder; top anchor not below the HCC ladder's
        self.assertEqual(min(scored), min(RHO_TYPOLOGY_ANCHORS.values()))
        self.assertEqual(max(scored), max(RHO_TYPOLOGY_ANCHORS.values()))
        self.assertGreaterEqual(max(scored), max(RHO_ANCHORS_HCC.values()))
        self.assertEqual(RHO_BIO_CEILING, max(scored))

    def test_equally_spaced(self):
        scored = sorted(v for k, v in RHO_BIO_ANCHORS.items() if k != "not_scored")
        steps = {round(b - a, 12) for a, b in zip(scored, scored[1:])}
        self.assertEqual(steps, {0.15})

    def test_ordered_bounded_and_complete(self):
        vals = [RHO_BIO_ANCHORS[k] for k in ("not_scored", "little", "limited", "moderate", "good", "excellent")]
        self.assertEqual(vals, sorted(vals))
        self.assertEqual(len(set(vals)), 6)
        self.assertEqual(RHO_BIO_ANCHORS["not_scored"], 0.0)
        self.assertTrue(all(0.0 <= v <= RHO_BIO_CEILING for v in vals))
        self.assertEqual(set(RHO_BIO_ANCHORS), set(RHO_BIO_DESCRIPTORS))

    def test_lookup_and_unknown(self):
        self.assertEqual(rho_bio_from_anchor("moderate"), 0.40)
        with self.assertRaises(ValueError):
            rho_bio_from_anchor("high")

    def test_every_anchor_combines_and_zero_is_standard_score(self):
        for name, rb in RHO_BIO_ANCHORS.items():
            s = score_two_senses(0.30, 0.65, 0.60, rb, 0.20, 3)
            self.assertAlmostEqual(s["rho"], 1 - (1 - rb) * (1 - 0.20), places=12)
        s0 = score_two_senses(0.30, 0.65, 0.60, RHO_BIO_ANCHORS["not_scored"], 0.20, 3)
        self.assertEqual(s0["R_raw"], score(0.30, 0.65, 0.60, 0.20, 3)["R_raw"])

    def test_descriptors_score_biology_only(self):
        for text in RHO_BIO_DESCRIPTORS.values():
            for word in ("surveillance", "adherence", "follow-up", "access"):
                self.assertNotIn(word, text.lower())


class CombineRho(unittest.TestCase):
    def test_manuscript_s5_example(self):
        self.assertAlmostEqual(combine_rho(0.50, 0.40), 0.70, places=12)

    def test_reduces_to_single_component(self):
        self.assertEqual(combine_rho(0.0, 0.45), 0.45)
        self.assertEqual(combine_rho(0.45, 0.0), 0.45)

    def test_symmetric_bounded_monotone(self):
        self.assertAlmostEqual(combine_rho(0.3, 0.6), combine_rho(0.6, 0.3), places=12)
        self.assertLess(combine_rho(0.9, 0.9), 1.0)
        self.assertGreater(combine_rho(0.31, 0.5), combine_rho(0.30, 0.5))
        self.assertLess(combine_rho(0.5, 0.4), 0.5 + 0.4)       # never simple addition

    def test_rejects_out_of_range(self):
        for a, b in ((-0.1, 0.2), (0.2, 1.0), (1.2, 0.2)):
            with self.assertRaises(ValueError):
                combine_rho(a, b)


class TwoSenseScore(unittest.TestCase):
    def test_matches_core_with_combined_rho(self):
        s = score_two_senses(0.30, 0.65, 0.60, 0.50, 0.40, 3)
        ref = score(0.30, 0.65, 0.60, 0.70, 3)
        self.assertEqual(s["R_raw"], ref["R_raw"])
        self.assertEqual(s["tier"], ref["tier"])
        self.assertEqual(s["EAL"], ref["EAL"])

    def test_counterfactuals_and_effects(self):
        s = score_two_senses(0.30, 0.65, 0.60, 0.30, 0.45, 3)
        self.assertEqual(s["R_without_care"], score(0.30, 0.65, 0.60, 0.30, 3)["R_raw"])
        self.assertEqual(s["R_without_bio"], score(0.30, 0.65, 0.60, 0.45, 3)["R_raw"])
        self.assertGreater(s["care_effect"], 0)
        self.assertGreater(s["bio_effect"], 0)
        self.assertAlmostEqual(s["care_effect"], s["R_without_care"] - s["R_raw"], places=15)

    def test_no_bio_equals_care_only_score(self):
        s = score_two_senses(0.30, 0.65, 0.60, 0.0, 0.45, 3)
        self.assertEqual(s["R_raw"], score(0.30, 0.65, 0.60, 0.45, 3)["R_raw"])
        self.assertAlmostEqual(s["bio_effect"], 0.0, places=15)


class CareDisruption(unittest.TestCase):
    def test_disruption_raises_risk_biology_fixed(self):
        d = care_disruption(0.30, 0.65, 0.60, 0.30, 0.45, 0.15)
        self.assertGreater(d["delta_R"], 0)
        self.assertEqual(d["tier_before"], "Tier 1 - Low")
        self.assertEqual(d["tier_after"], "Tier 2 - Moderate")
        self.assertTrue(d["tier_changed"])

    def test_no_change_no_delta(self):
        d = care_disruption(0.30, 0.65, 0.60, 0.30, 0.45, 0.45)
        self.assertEqual(d["delta_R"], 0.0)
        self.assertFalse(d["tier_changed"])


class Trajectory(unittest.TestCase):
    def test_rho_bio_zero_reproduces_published_hcc_trajectory(self):
        # The existing time-indexed HCC rho is the care-system component.
        for obs, dlv in ((A_OBS, A_DLV), (B_OBS, B_DLV)):
            base = run_trajectory(0.30, 0.65, 3, 0.20, obs, dlv, HCC_PARAMS)
            two = run_two_sense_trajectory(0.30, 0.65, 3, 0.0, 0.20, obs, dlv, HCC_PARAMS)
            for b, t in zip(base, two):
                self.assertAlmostEqual(t["R_two_sense"], b["R"], places=12)
                self.assertEqual(t["tier_two_sense"], b["tier"])
                self.assertEqual(t["R"], b["R"])             # original keys untouched
                self.assertEqual(t["rho_total"], b["rho"])

    def test_example_a_values_unchanged(self):
        two = run_two_sense_trajectory(0.30, 0.65, 3, 0.0, 0.20, A_OBS, A_DLV, replace_filter_off())
        self.assertEqual([round(r["R_two_sense"], 3) for r in two], [0.081, 0.055, 0.042, 0.031])

    def test_bio_resilience_lowers_every_cycle(self):
        base = run_two_sense_trajectory(0.30, 0.65, 3, 0.0, 0.20, B_OBS, B_DLV)
        more = run_two_sense_trajectory(0.30, 0.65, 3, 0.25, 0.20, B_OBS, B_DLV)
        for a, b in zip(base, more):
            self.assertLess(b["R_two_sense"], a["R_two_sense"])

    def test_series_rho_bio_length_checked(self):
        with self.assertRaises(ValueError):
            run_two_sense_trajectory(0.30, 0.65, 3, [0.1, 0.1], 0.20, A_OBS, A_DLV)


class Events(unittest.TestCase):
    ROWS = None

    @classmethod
    def setUpClass(cls):
        cls.ROWS = run_two_sense_trajectory(0.30, 0.65, 3, 0.20, 0.20,
                                            [2, 2, None, 3, 3], [.40, .55, .55, .30, .30])

    def test_flags_missed_visit_and_delivery_fall(self):
        ev = oncoclastic_events(self.ROWS)
        care = [(e["t"], e["kind"]) for e in ev if e["sense"] == "care-system"]
        self.assertIn((2, "missed visit"), care)
        self.assertIn((3, "delivery fell"), care)

    def test_flags_biological_rise_only_when_V_rises(self):
        ev = oncoclastic_events(self.ROWS)
        bio_t = [e["t"] for e in ev if e["sense"] == "biological"]
        self.assertEqual(bio_t, [3, 4])
        self.assertEqual([e for e in oncoclastic_events(self.ROWS, v_step=0.05)
                          if e["sense"] == "biological"], [])

    def test_improving_series_has_no_events(self):
        rows = run_two_sense_trajectory(0.30, 0.65, 3, 0.0, 0.20, A_OBS, A_DLV)
        self.assertEqual(oncoclastic_events(rows), [])


def replace_filter_off():
    from dataclasses import replace
    return replace(HCC_PARAMS, filter_on=False)


if __name__ == "__main__":
    unittest.main()
