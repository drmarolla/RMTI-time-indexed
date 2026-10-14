# Trajectory guide

How to use and read the time-indexed layer, what the model is, and how it could be tested. Everything here describes a **research prototype**: the parameters are uncalibrated placeholders and all examples are synthetic.

## 1. The model

| Level | Description | Status |
|---|---|---|
| 0 | Snapshot: R = L·E·V·(1−ρ) from one set of inputs (the published RMTI). | Published |
| 1 | Time-indexed inputs: V(t) and ρ(t) measured each cycle, R(t) = L·E·V(t)·(1−ρ(t)). Memoryless: V follows the latest observation. | Implemented (filter off) |
| 2 | Filtered: V(t) comes from a level-and-slope filter on the indicator, so one noisy reading moves the score less. | Implemented (filter on) |
| 3 | Behavioural channel: the hypothesis that disease burden changes adherence or behaviour in a detectable way before imaging can see it. | Not implemented; to be fitted only after Level 2 shows value on real serial data |

Per cycle *t*:

```
level(t) = level_pred + α · (y(t) − level_pred)         level_pred = level(t−1) + slope(t−1)
slope(t) = slope(t−1) + β · (y(t) − level_pred)
V*(t)    = v_lo + (v_hi − v_lo) · clip(level + κH·slope, 0, y_max) / y_max
ρ(t)     = clip(ρ(t−1) + λ · (delivery(t) − delivery(t−1)), 0, ρ_ceiling)
R(t)     = L · E · V*(t) · (1 − ρ(t))
```

Tier and posture use the fixed Table 3 bands. A missed observation carries the filter's prediction forward. L and E are held fixed in this release.

## 2. Reproduce the worked examples

Set **L = 0.30, E = 0.65, C = 3, ρ(0) = 0.20** (in the sandboxes, use the Custom tab sliders; the workbooks hold these in the Trajectory sheet). Load synthetic example A or B.

| Example | Observations (y) | Delivery | R(t), filter OFF | R(t), filter ON |
|---|---|---|---|---|
| A (improving) | 2, 1, 1, 0 | 0.40, 0.55, 0.70, 0.75 | 0.081, 0.055, 0.042, 0.031 | 0.0806, 0.0602, 0.0435, 0.0340 |
| B (worsening) | 2, 3, 4, 5 | 0.40, 0.40, 0.35, 0.35 | 0.081, 0.094, 0.113, 0.127 | 0.0806, 0.0871, 0.1041, 0.1187 |

The oncology sandbox and the HCC workbook use y = allostatic load on a 0–6 scale. The disaster sandbox defaults to a 0–10 indicator scale and loads its own example series, so use the Python module with `HCC_PARAMS` to reproduce this table exactly.

## 3. Parameters (all uncalibrated)

| Symbol | Default | Meaning |
|---|---|---|
| v_lo, v_hi | 0.35, 0.85 | V at the bottom and top of the indicator scale (ALBI grade-1 and grade-3 anchors in HCC; copied as placeholders for disaster) |
| y_max | 6 (HCC), 10 (disaster) | Top of the indicator scale |
| α, β | 0.41, 0.09 | Steady-state filter gains for q_level 0.05, q_slope 0.01, r_obs 0.8 (`steady_state_gains()` returns 0.4149, 0.0855) |
| κ·H | 1 | Cycles of slope added to the level |
| λ | 1 | Delivery → ρ gain. Must be estimated from real serial data; never calibrate it on the scenario ρ-after values in the main calculators, which are inputs and not observations |
| ρ ceiling | 0.95 | Modelling ceiling; the core rejects ρ ≥ 1 |

## 4. Reading the output

- **Filter off** is the memoryless snapshot repeated each cycle.
- **Filter on** smooths the path at the cost of lag after a real change.
- A raw tier change on a noisy path can be a false alert. `tier_changes()` is descriptive only; a probability-based alert rule should be pre-registered before any use.
- Neither version is a forecast.

## 5. Scope

Time-varying and dynamic risk prediction for HCC is an established field, and this repository does not claim novelty for it. The narrower question is whether a mechanism-structured, interpretable trajectory (vulnerability and resilience kept separate, with a fixed tier scale) adds information beyond a well-measured current level.

## 6. Study-design notes

**What would show the idea is wrong.** The trajectory adds no discrimination, calibration or net benefit over a well-measured current level in held-out data; or behavioural signals vanish once cirrhosis severity is matched; or filtered paths generate more false tier alerts than they prevent. Any of these is a useful result and should be reported.

**Staged program.** (1) Methods paper stating the trajectory-versus-level hypothesis with the corrected code and a clearly labelled synthetic illustration. (2) Pre-registered protocol and analysis plan before any real data are touched. (3) Retrospective validation on real serial data. (4) Prospective validation. (5) Mechanism work as a separate program. A gate between steps should be pre-registered, for example: the lower confidence bound of ΔAUC for trajectory over current level is above zero in held-out data and the calibration slope is within an agreed band.

**Sample size.** Use criteria designed for prediction-model sample size rather than a rule of thumb. The table only shows why event rate dominates, converting a target of 100 events (an illustration, not a requirement) into patients over three years of follow-up, ignoring attrition and competing risks, which raise the numbers.

| Annual HCC incidence | Cumulative 3-year risk | Patients for about 100 events |
|---|---|---|
| 1% | 3.0% | about 3,400 |
| 2% | 5.9% | about 1,700 |
| 3% | 8.7% | about 1,150 |
| 5% | 14.3% | about 700 |

**Ethics.** Real serial patient data require ethics review, data-use agreements and, for any animal work, institutional animal-care approval, obtained by the investigators. Nothing in this repository grants or implies those.

## 7. Known limits

No real-patient or real-disaster validation; no time-varying L(t) or E(t); no social-determinants modifier; and one small difference between implementations: if a delivery entry is blank at cycle t−1 and filled at cycle t, the workbook takes the change from 0 while Python and the sandboxes take it from the last observed value. The documented missed-visit workflow (leave the observation blank, keep the delivery entry) is unaffected.
