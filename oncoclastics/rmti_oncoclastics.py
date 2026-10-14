# Copyright 2026 Cesar Marolla
# Licensed under the Apache License, Version 2.0 (see ../LICENSE).
"""
rmti_oncoclastics.py -- the two senses of oncoclastics, expressed through the
unchanged RMTI core.

RESEARCH PROTOTYPE. Nothing here is validated against real outcomes. All
examples are synthetic. Not a medical device. See ../DISCLAIMER.md.

Oncoclastics is the application of hazard-exposure-vulnerability-resilience
assessment (as developed in disaster-risk reduction) to the fragmentation of
cancer-related trajectories. Two senses are kept apart:

    biological   -- progression from chronic injury toward cancer in one
                    patient.   Carried by L, E, V and the biological part of
                    resilience, rho_bio.
    care-system  -- disruption of surveillance and care along that path.
                    Carried only by rho_care (and, in the time-indexed layer,
                    by the delivery series that drives rho_care).

This module adds NO new equation to R = L * E * V * (1 - rho). It only
(a) combines the two resilience components as in the manuscript's
Supplementary Material S5,

        rho = 1 - (1 - rho_bio) * (1 - rho_care),

(b) reports each component's marginal effect on R, and (c) lists descriptive
"oncoclastic events" in a time-indexed run. Scoring always goes through
core.rmti_core.score(), so any fix in core propagates here.

Backward compatibility. In the published HCC-surveillance work and in
dynamic/rmti_dynamic.py, rho is the surveillance-effectiveness ladder (and,
over time, surveillance adherence): that is rho_care. rho_bio is not scored
there. With rho_bio = 0 the combined rho equals rho_care, so every existing
HCC number is reproduced exactly (tested).

Anchors for rho_bio. RHO_BIO_ANCHORS gives a five-level ordinal ladder for
biological adaptive reserve, equally spaced across the range already used by
the RMTI's resilience ladders (disaster-risk typology 0.10-0.70; HCC
surveillance 0.15-0.65): 0.10 little, 0.25 limited, 0.40 moderate, 0.55 good,
0.70 excellent. The order and wording follow the manuscript's Table S4 rho
column (excellent to little reserve), restricted to biology: S4's wording
about access, follow-up and care belongs to rho_care. The values are ASSIGNED,
not estimated; like every anchor in the RMTI they are advisory reference
points (values between anchors are allowed) and a starting point for consensus
(Delphi) refinement, not validated. No rho_bio above RHO_BIO_CEILING (the top
anchor) has a defined meaning. 0.00 means "not scored" and reproduces the
standard score.

Assumptions that must be stated wherever the combined rho is used:
  1. Independence. The combination treats biological and care-system
     absorption as acting independently on the same inherent risk. This is a
     proposition to be tested, not a finding.
  2. No double counting. rho_bio must be built from information that does not
     describe surveillance delivery; rho_care must not include hepatic
     reserve (which belongs to rho_bio, or to V when read as accrued cost).
  3. Care-system capacity can also shape C (stage at detection). C is not
     modified here; the rho/C overlap is a stated limitation of the framework.
"""
import os
import sys
from decimal import Decimal
from typing import List, Optional, Sequence, Union

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rmti-python"))

from core.rmti_core import score  # noqa: E402
from dynamic.rmti_dynamic import HCC_PARAMS, TrajectoryParams, run_trajectory  # noqa: E402

__version__ = "1.0.0"
__all__ = ["RHO_BIO_ANCHORS", "RHO_BIO_CEILING", "RHO_BIO_DESCRIPTORS", "rho_bio_from_anchor", "combine_rho", "score_two_senses", "care_disruption",
           "run_two_sense_trajectory", "oncoclastic_events"]


# ---- Provisional anchors for rho_bio (biological adaptive reserve) ----------
# Five equally spaced levels across the range of the existing resilience
# ladders (0.10-0.70); order and wording from manuscript Table S4. Assigned,
# not estimated; not validated. Keep in step with ONCO_RHO_BIO_ANCHORS in
# oncology/index.html (tools/check_oncology_sandbox.py compares them).
RHO_BIO_ANCHORS = {"not_scored": 0.00, "little": 0.10, "limited": 0.25,
                   "moderate": 0.40, "good": 0.55, "excellent": 0.70}
RHO_BIO_CEILING = 0.70   # top anchor; the sandbox's rho_bio slider stops here

# Descriptors score biology only. Surveillance, access, follow-up and adherence
# are rho_care. Where ALBI already sets V (HCC application), do not use
# ALBI-derived reserve here: assign each measure to one term.
RHO_BIO_DESCRIPTORS = {
    "not_scored": "Not scored. The combined score equals the standard score.",
    "little": "Little biological reserve: decompensated or near-decompensated liver function; no demonstrated capacity to recover after injury.",
    "limited": "Limited reserve: reduced but compensated functional reserve; marked metabolic inflexibility; little or no recovery after exposure is reduced.",
    "moderate": "Moderate reserve: function preserved with measurable decline; impaired metabolic flexibility; partial or inconsistent recovery after exposure is reduced.",
    "good": "Good reserve: normal or near-normal function; mildly impaired metabolic flexibility; recovery after exposure reduction is slower or partial.",
    "excellent": "Excellent reserve: full functional reserve; preserved metabolic flexibility; prompt resolution of injury when exposure is reduced.",
}


def rho_bio_from_anchor(name: str) -> float:
    """rho_bio for a named anchor level (see RHO_BIO_ANCHORS)."""
    try:
        return RHO_BIO_ANCHORS[name]
    except KeyError:
        raise ValueError(f"unknown rho_bio anchor {name!r}; use one of {sorted(RHO_BIO_ANCHORS)}") from None


def _check_component(name: str, x: float) -> None:
    if not 0.0 <= x < 1.0:
        raise ValueError(f"{name} must lie in [0, 1); got {x}")


def combine_rho(rho_bio: float, rho_care: float) -> float:
    """rho = 1 - (1 - rho_bio)(1 - rho_care). Bounded in [0, 1), monotone in
    each argument, and equal to rho_care when rho_bio = 0 (and vice versa).
    Example from the manuscript (S5): 0.50 and 0.40 give 0.70, not the 0.90
    that simple addition would give."""
    _check_component("rho_bio", rho_bio)
    _check_component("rho_care", rho_care)
    # Decimal arithmetic from the string form of each input, as core.score()
    # does, so that e.g. rho_bio = 0 returns rho_care exactly (binary floats
    # give 0.44999999999999996 for 1 - (1 - 0) * (1 - 0.45)).
    return float(1 - (1 - Decimal(str(rho_bio))) * (1 - Decimal(str(rho_care))))


def score_two_senses(L: float, E: float, V: float, rho_bio: float,
                     rho_care: float, C: int = 3) -> dict:
    """Score one state with both resilience components, through core.score().

    Besides the combined score it returns two counterfactuals, each holding
    the other component fixed:
        R_without_care -- R if care-system capacity were absent (rho_care = 0)
        R_without_bio  -- R if biological reserve were absent (rho_bio = 0)
    and the marginal effects care_effect = R_without_care - R and
    bio_effect = R_without_bio - R. Marginal effects are order-dependent and
    do not sum to the total absorbed risk (IR - R); they answer "what does
    this component add, given the other?", not "how is the total divided?".
    """
    rho = combine_rho(rho_bio, rho_care)
    s = score(L, E, V, rho, C)
    s_nocare = score(L, E, V, rho_bio, C)
    s_nobio = score(L, E, V, rho_care, C)
    return {
        "rho_bio": rho_bio, "rho_care": rho_care, "rho": rho,
        "IR_raw": s["IR_raw"], "R_raw": s["R_raw"], "R": s["R"],
        "tier": s["tier"], "EAL": s["EAL"],
        "R_without_care": s_nocare["R_raw"], "R_without_bio": s_nobio["R_raw"],
        "care_effect": s_nocare["R_raw"] - s["R_raw"],
        "bio_effect": s_nobio["R_raw"] - s["R_raw"],
    }


def care_disruption(L: float, E: float, V: float, rho_bio: float,
                    rho_care_before: float, rho_care_after: float,
                    C: int = 3) -> dict:
    """Care-system oncoclastics at one time point: the same patient, the same
    biology (L, E, V, rho_bio), with care-system capacity moving from
    rho_care_before to rho_care_after (a disruption if after < before).
    Reports R before and after, the change, and whether the tier changed."""
    a = score_two_senses(L, E, V, rho_bio, rho_care_before, C)
    b = score_two_senses(L, E, V, rho_bio, rho_care_after, C)
    return {"R_before": a["R_raw"], "R_after": b["R_raw"],
            "delta_R": b["R_raw"] - a["R_raw"],
            "tier_before": a["tier"], "tier_after": b["tier"],
            "tier_changed": a["tier"] != b["tier"]}


def run_two_sense_trajectory(L: float, E: float, C: int, rho_bio: Union[float, Sequence[float]],
                             rho0_care: float, observations: Sequence[Optional[float]],
                             delivery: Sequence[Optional[float]],
                             params: TrajectoryParams = HCC_PARAMS) -> List[dict]:
    """Time-indexed run with both senses.

    dynamic.run_trajectory() supplies V*(t) (biological, from the allostatic-
    load indicator) and rho(t) (care-system, from surveillance delivery).
    Here that rho(t) is treated as rho_care(t) and combined with rho_bio
    (a constant, or one value per cycle). Every key of the underlying row is
    kept unchanged; the two-sense keys are added:
        rho_bio, rho_care, rho_total, R_two_sense, tier_two_sense,
        R_without_care, care_effect, bio_effect.
    With rho_bio = 0, R_two_sense equals the underlying row's R."""
    rows = run_trajectory(L, E, C, rho0_care, observations, delivery, params)
    series = list(rho_bio) if isinstance(rho_bio, (list, tuple)) else [rho_bio] * len(rows)
    if len(series) != len(rows):
        raise ValueError("rho_bio must be a number or have one value per cycle")
    out = []
    for r, rb in zip(rows, series):
        s = score_two_senses(L, E, r["V"], rb, r["rho"], C)
        out.append({**r, "rho_bio": rb, "rho_care": r["rho"], "rho_total": s["rho"],
                    "R_two_sense": s["R_raw"], "tier_two_sense": s["tier"],
                    "R_without_care": s["R_without_care"],
                    "care_effect": s["care_effect"], "bio_effect": s["bio_effect"]})
    return out


def oncoclastic_events(rows: List[dict], v_step: float = 0.0) -> List[dict]:
    """Descriptive listing of candidate oncoclastic events in a run (rows from
    run_trajectory or run_two_sense_trajectory). Each event names its sense.

    care-system : (a) a missed visit (indicator y is None), or
                  (b) a fall in delivery between consecutive recorded cycles.
    biological  : V*(t) rises by more than v_step relative to the previous
                  cycle (v_step = 0.0 means any rise).

    These are OPERATIONAL, PROVISIONAL definitions proposed for testing. They
    are not validated, v_step is not calibrated, and a flag is not an alert,
    a diagnosis or a recommendation (compare tier_changes() in the dynamic
    layer, which carries the same caveat)."""
    events = []
    last_delivery = rows[0].get("delivery") if rows else None
    for prev, cur in zip(rows, rows[1:]):
        t = cur["t"]
        if cur.get("y") is None:
            events.append({"t": t, "sense": "care-system", "kind": "missed visit"})
        d = cur.get("delivery")
        if d is not None:
            if last_delivery is not None and d < last_delivery:
                events.append({"t": t, "sense": "care-system", "kind": "delivery fell",
                               "from": last_delivery, "to": d})
            last_delivery = d
        if cur["V"] - prev["V"] > v_step:
            events.append({"t": t, "sense": "biological", "kind": "V* rose",
                           "from": prev["V"], "to": cur["V"]})
    return events


def _demo() -> None:
    print("rmti_oncoclastics demo -- synthetic inputs, research prototype\n")
    print("1. Combining resilience (manuscript S5 example)")
    print(f"   rho_bio 0.50, rho_care 0.40 -> rho = {combine_rho(0.50, 0.40):.2f}  (addition would give 0.90)\n")
    print("2. One patient, two senses  (L 0.30, E 0.65, V 0.60, C 3)")
    s = score_two_senses(0.30, 0.65, 0.60, 0.30, 0.45)
    print(f"   rho_bio 0.30, rho_care 0.45 -> rho {s['rho']:.3f}, R {s['R_raw']:.4f}, {s['tier']}")
    print(f"   without care: R {s['R_without_care']:.4f}   care adds {s['care_effect']:.4f}")
    print(f"   without bio : R {s['R_without_bio']:.4f}   bio adds  {s['bio_effect']:.4f}\n")
    print("3. Care-system disruption, biology held fixed (rho_care 0.45 -> 0.15)")
    d = care_disruption(0.30, 0.65, 0.60, 0.30, 0.45, 0.15)
    print(f"   R {d['R_before']:.4f} -> {d['R_after']:.4f}  (delta {d['delta_R']:+.4f}); "
          f"{d['tier_before']} -> {d['tier_after']}\n")
    print("4. Time-indexed run with a missed visit and a delivery drop (synthetic)")
    rows = run_two_sense_trajectory(0.30, 0.65, 3, 0.20, 0.20,
                                    [2, 2, None, 3, 3], [0.40, 0.55, 0.55, 0.30, 0.30])
    print("   t  y     deliv  rho_care  V*      R_two_sense  tier")
    for r in rows:
        y = "-" if r["y"] is None else r["y"]
        print(f"   {r['t']}  {y!s:<5} {r['delivery']:.2f}   {r['rho_care']:.3f}     "
              f"{r['V']:.4f}  {r['R_two_sense']:.4f}       {r['tier_two_sense']}")
    print("   candidate events:")
    for e in oncoclastic_events(rows):
        print("    ", e)


if __name__ == "__main__":
    _demo()
