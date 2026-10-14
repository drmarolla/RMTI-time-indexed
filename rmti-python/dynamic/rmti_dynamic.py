# Copyright 2026 Cesar Marolla
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
rmti_dynamic.py -- Time-indexed RMTI (Level 2, "filtered") dynamic layer.

RESEARCH PROTOTYPE. Not validated against real outcomes. alpha, beta,
look_ahead (kappa*H) and lam (lambda) are uncalibrated placeholders. Whether a
trajectory adds information beyond a well-measured current level is an open,
testable hypothesis (see docs/TRAJECTORY_GUIDE.md).

This module is a thin layer ON TOP of core.rmti_core: it never re-implements
R, tier or EAL. Each cycle it estimates V(t) and rho(t) and then calls
core.rmti_core.score(), so any fix in core propagates here (the "do not fork
core" rule in core's own header).

Model (per cycle t = 0, 1, 2, ...), matching the Trajectory sheet in the
RMTI-HCC and RMTI disaster-science workbooks cell for cell:

    x(t) = [level, slope];  x(t) = F x(t-1) + w;  y(t) = level(t) + e
    F = [[1, 1], [0, 1]]
    predicted:  level_p = level(t-1) + slope(t-1);   slope_p = slope(t-1)
    update:     level(t) = level_p + alpha * (y(t) - level_p)
                slope(t) = slope_p + beta  * (y(t) - level_p)
                (a missed observation carries the prediction forward)
    V*(t)  = clip( v_lo + (v_hi - v_lo) * [level + look_ahead * slope]
                   / y_max ,  v_lo, v_hi )          # filter on
    V*(t)  = v_lo + (v_hi - v_lo) * clip(y(t), 0, y_max) / y_max   # filter off
    rho(t) = rho(t-1) + lam * (delivery(t) - delivery(t-1)),
             clipped to [0, rho_ceiling]
    R(t)   = L * E * V*(t) * (1 - rho(t));   tier/posture from core.

Domain-neutral names. The "indicator" y is the 0..y_max composite that drives
vulnerability and "delivery" is the 0..1 fraction that drives resilience:

    oncology (HCC):  y = allostatic-load composite (0-6, or 0-13);
                     delivery = surveillance adherence.
    disaster:        y = composite vulnerability-indicator index (Table 9.4,
                     RMTseen; default scale 0-10);
                     delivery = share of the planned resilience programme
                     delivered to date.
The disaster mapping is an extension proposed in this repository; it is not
part of the published RMTI papers and its anchors are placeholders.
"""
from dataclasses import dataclass, replace
from typing import List, Optional, Sequence

from core.rmti_core import score, tier, posture

__all__ = ["TrajectoryParams", "HCC_PARAMS", "DISASTER_PARAMS",
           "steady_state_gains", "run_trajectory", "tier_changes"]


@dataclass(frozen=True)
class TrajectoryParams:
    v_lo: float = 0.35          # V at indicator = 0 (ALBI grade-1 anchor in HCC)
    v_hi: float = 0.85          # V at indicator = y_max (ALBI grade-3 anchor)
    y_max: float = 6.0          # top of the indicator scale
    alpha: float = 0.41         # level gain  (steady-state Kalman, uncalibrated)
    beta: float = 0.09          # slope gain  (steady-state Kalman, uncalibrated)
    look_ahead: float = 1.0     # kappa*H: cycles of slope added to the level
    lam: float = 1.0            # delivery -> rho gain (placeholder)
    rho_ceiling: float = 0.95   # modelling ceiling; core rejects rho >= 1
    filter_on: bool = True      # False = memoryless (draft Eq. 4)

    def __post_init__(self):
        if not self.v_lo < self.v_hi:
            raise ValueError("v_lo must be < v_hi")
        if not (0.0 <= self.v_lo and self.v_hi <= 1.0):
            raise ValueError("v_lo and v_hi must lie in [0, 1]")
        if self.y_max <= 0:
            raise ValueError("y_max must be > 0")
        if not (0.0 <= self.alpha <= 1.0 and 0.0 <= self.beta <= 1.0):
            raise ValueError("alpha and beta must lie in [0, 1]")
        if not 0.0 <= self.rho_ceiling < 1.0:
            raise ValueError("rho_ceiling must lie in [0, 1)")


# HCC defaults mirror the workbook's Trajectory sheet (B5:B13).
HCC_PARAMS = TrajectoryParams()
# Disaster defaults: same Kalman gains and anchors, wider indicator scale.
# ALL of these are placeholders; no disaster calibration data exist.
DISASTER_PARAMS = TrajectoryParams(y_max=10.0)


def steady_state_gains(q_level: float = 0.05, q_slope: float = 0.01,
                       r_obs: float = 0.8, iters: int = 5000):
    """Steady-state Kalman gains (alpha, beta) of the local-linear-trend model
    for the given process/observation noise. With the defaults this returns
    (0.4149, 0.0855), which the workbook rounds to alpha = 0.41, beta = 0.09.
    Pure Python (no numpy); a 2x2 Riccati recursion run to convergence."""
    if min(q_level, q_slope) < 0 or r_obs <= 0:
        raise ValueError("noise variances must be >= 0 and r_obs > 0")
    a, b, c, d = 1.0, 0.0, 0.0, 1.0           # P = [[a, b], [c, d]]
    k1 = k2 = 0.0
    for _ in range(iters):
        pa, pb = a + b + c + d + q_level, b + d      # P_pred = F P F' + Q
        pc, pd = c + d, d + q_slope
        s = pa + r_obs
        k1, k2 = pa / s, pc / s
        a, b = pa - k1 * pa, pb - k1 * pb            # P = (I - K H) P_pred
        c, d = pc - k2 * pa, pd - k2 * pb
    return k1, k2


def _clip(x, lo, hi):
    return max(lo, min(hi, x))


def run_trajectory(L: float, E: float, C: int, rho0: float,
                   observations: Sequence[Optional[float]],
                   delivery: Sequence[Optional[float]],
                   params: TrajectoryParams = HCC_PARAMS,
                   postures: Optional[dict] = None) -> List[dict]:
    """Score one subject (patient / asset / city) across cycles.

    observations[t] -- indicator y(t) in [0, y_max], or None for a missed
                       visit (the filter carries its prediction forward).
                       observations[0] must be present.
    delivery[t]     -- delivery fraction in [0, 1], or None (rho carries
                       forward). Same length as observations.
    rho0            -- resilience at t = 0.
    postures        -- optional posture vocabulary (e.g.
                       oncology.rmti_hcc.HCC_TIER_POSTURE).

    Returns one dict per cycle with: t, y, delivery, level, slope, V, rho,
    R (rounded to 12 dp, as the workbook), R_display (3 dp), tier, posture,
    EAL, dR (change vs previous cycle, None at t = 0).
    """
    n = len(observations)
    if n == 0:
        raise ValueError("at least one cycle is required")
    if len(delivery) != n:
        raise ValueError("observations and delivery must have the same length")
    if observations[0] is None:
        raise ValueError("observations[0] (baseline) must be provided")
    for t, y in enumerate(observations):
        if y is not None and not 0.0 <= y <= params.y_max:
            raise ValueError(f"observations[{t}]={y} outside [0, {params.y_max}]")
    for t, d in enumerate(delivery):
        if d is not None and not 0.0 <= d <= 1.0:
            raise ValueError(f"delivery[{t}]={d} outside [0, 1]")
    if not 0.0 <= rho0 <= params.rho_ceiling:
        raise ValueError(f"rho0 must lie in [0, {params.rho_ceiling}]")

    p = params
    rows, level, slope, rho = [], None, None, rho0
    last_delivery, prev_R = None, None
    for t in range(n):
        y, dlv = observations[t], delivery[t]
        # --- state update (identical to Trajectory!D:E) --------------------
        if t == 0:
            level, slope = y, 0.0
        else:
            level_p = level + slope
            if y is None:
                level, slope = level_p, slope
            else:
                innov = y - level_p
                level, slope = level_p + p.alpha * innov, slope + p.beta * innov
        # --- V*(t) (Trajectory!F) ------------------------------------------
        if p.filter_on:
            drive = level + p.look_ahead * slope
        else:
            drive = level if y is None else y
        V = p.v_lo + (p.v_hi - p.v_lo) * _clip(drive, 0.0, p.y_max) / p.y_max
        # --- rho(t) (Trajectory!G) -----------------------------------------
        if t > 0 and dlv is not None:
            base = 0.0 if last_delivery is None else last_delivery
            rho = _clip(rho + p.lam * (dlv - base), 0.0, p.rho_ceiling)
        if dlv is not None:
            last_delivery = dlv
        # --- score through the shared core ---------------------------------
        s = score(L, E, V, rho, C)
        R = round(s["R_raw"], 12)              # workbook rounds to 12 dp before tier lookup
        tr = tier(R)
        rows.append({
            "t": t, "y": y, "delivery": dlv, "level": level, "slope": slope,
            "V": V, "rho": rho, "R": R, "R_display": s["R"], "tier": tr,
            "posture": (postures or {}).get(tr) if postures else posture(R),
            "EAL": s["EAL"],
            "dR": None if prev_R is None else R - prev_R,
        })
        prev_R = R
    return rows


def tier_changes(rows: List[dict]) -> List[dict]:
    """Cycles at which the tier differs from the previous cycle. A raw tier
    flip on a noisy path can be a false alert; treat this as
    a descriptive listing, not an alerting rule, until a probability-based
    rule (P(R beyond cut-point) > pre-set value) has been pre-registered."""
    out = []
    for prev, cur in zip(rows, rows[1:]):
        if cur["tier"] != prev["tier"]:
            out.append({"t": cur["t"], "from": prev["tier"], "to": cur["tier"],
                        "R_from": prev["R"], "R_to": cur["R"]})
    return out
