# Anchors for ρ_bio (biological adaptive reserve)

**Status: provisional and assigned, not estimated and not validated.** Like every anchor in the RMTI (the surveillance-effectiveness ladder, the ALBI-derived V values, the BCLC-anchored C scale), these are reference points that let an analyst score a domain without a quantitative model. They are a starting point for consensus (Delphi) refinement.

## What "anchor" means here

An anchor is a defined reference level on a bounded scale, with a descriptor and a value, so that two analysts scoring the same patient land on the same level. It has nothing to do with slider tick marks or with the user-interface library. Until this release ρ_bio had no such levels; the sandbox said so.

## The ladder

| Level | ρ_bio | Descriptor (biology only) |
|---|---|---|
| Not scored | 0.00 | Not scored. The combined score equals the standard score. |
| Little | 0.10 | Decompensated or near-decompensated liver function; no demonstrated capacity to recover after injury. |
| Limited | 0.25 | Reduced but compensated functional reserve; marked metabolic inflexibility; little or no recovery after exposure is reduced. |
| Moderate | 0.40 | Function preserved with measurable decline; impaired metabolic flexibility; partial or inconsistent recovery after exposure is reduced. |
| Good | 0.55 | Normal or near-normal function; mildly impaired metabolic flexibility; recovery after exposure reduction is slower or partial. |
| Excellent | 0.70 | Full functional reserve; preserved metabolic flexibility; prompt resolution of injury when exposure is reduced. |

Like the other RMTI ladders these are **advisory reference points, not a categorical lookup**: a value between two anchors is allowed and is analyst judgment, not a measurement. No ρ_bio above 0.70 has a defined meaning, so the sandbox slider stops there. "Not scored" is not a level of reserve; it means ρ_bio is left out and the score is the standard one (the combined ρ then equals ρ_care).

## Alignment with the existing resilience ladders

| Ladder | Range | Source |
|---|---|---|
| Disaster-risk coping-capacity typology | 0.10 – 0.70 | `RHO_TYPOLOGY_ANCHORS` in `core/rmti_core.py` |
| HCC surveillance effectiveness (ρ_care) | 0.15 – 0.65 | `RHO_ANCHORS_HCC` in `core/rmti_core.py`; the HCC workbook's Reference tab |
| **Biological adaptive reserve (ρ_bio)** | **0.10 – 0.70, five levels, step 0.15** | `RHO_BIO_ANCHORS` in `oncoclastics/rmti_oncoclastics.py` |

The ρ_bio ladder spans exactly the disaster-risk range and tops out just above the HCC ladder's 0.65, so adding it cannot by itself move the combined ρ beyond what the existing ladders already allow in practice (largest combination with the HCC ladder: 1 − (1 − 0.70)(1 − 0.65) = 0.895). `test_aligned_with_existing_resilience_ladders` fails if the span or the ceiling drifts from the core's ladders.

## Where the numbers and the order come from

Table S4 of the accompanying manuscript gives five ordinal descriptors of adaptive reserve, from excellent to little, ordered as rows of a shared rubric. The anchors keep that order and wording, restricted to biology, and take their values from the existing ladders: five equally spaced levels over 0.10–0.70, so that higher ρ_bio always means more reserve, as ρ does everywhere else in the framework.

## Rules for using the anchors

1. **Biology only.** Surveillance delivery, access, follow-up and adherence are ρ_care and are scored on the surveillance-effectiveness ladder, not here. (S4's descriptors mixed the two; these do not.)
2. **One term per measure.** Hepatic functional reserve is a candidate measure for ρ in Table S3, but in the HCC-surveillance application ALBI already sets V. Where it does, do not use ALBI-derived reserve to place ρ_bio; use other evidence (for example metabolic flexibility, or documented recovery after exposure was reduced), or leave ρ_bio unscored. L, E, V and ρ must be built from information not used in L (main text, "Where the framework sits").
3. **Record the evidence.** Grade the evidence behind each placement prospectively, as in the Weight-of-Evidence scheme of Risk Mechanism Theory (Marolla, 2018).
4. **Do not read 0.70 as a measured 70% absorption.** The top anchor is the top of an ordinal rubric, as 0.70 is in the disaster ladder.

## Input bounds across the toolkit

All ρ inputs now stop at 0.99. The core accepts 0 ≤ ρ < 1; the workbooks' data validation allows 0–0.99; both sandboxes' ρ sliders (and the saved-case import) previously allowed 1.00, which gives R = 0 in the sandbox while the Python core rejects it, and now stop at 0.99. The time-indexed layer's modelling ceiling is 0.95 (`TrajectoryParams.rho_ceiling`), which is a property of its state update and is unchanged. `tools/check_oncology_sandbox.py` checks the 0.99 bounds in both sandboxes and the 0.70 stop of the ρ_bio slider.

## What this does not do

It does not make ρ_bio validated, does not provide cut-offs for any laboratory or imaging measure, and does not say how to measure metabolic flexibility or recovery capacity (S3 lists these as the least mature measures in the framework). It also does not change any tier threshold or any existing result: with ρ_bio unscored, every score is exactly what it was.

## Where it lives

`RHO_BIO_ANCHORS`, `RHO_BIO_DESCRIPTORS` and `rho_bio_from_anchor()` in `rmti_oncoclastics.py` (6 tests); `ONCO_RHO_BIO_ANCHORS` in `oncology/index.html` (clickable levels in the Oncoclastics panel); `tools/check_oncology_sandbox.py` compares the two, including the descriptors.
