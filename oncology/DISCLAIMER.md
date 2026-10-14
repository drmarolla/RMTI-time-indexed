# Disclaimer and intended use

**Applies to everything in this repository** (Python package, Excel calculators, both sandboxes, documentation).

## What this is

The Risk Mechanism Theory Index (RMTI) turns the numbers you enter into a relative, rubric-based score (R = L·E·V·(1−ρ)), a fixed tier, and an Expected Annual Loss index. This repository adds an **experimental, time-indexed (trajectory) layer** that follows V and ρ across review cycles using a simple level-and-slope filter.

## What it is not

- **Research prototype.** The trajectory layer is **not validated** against real outcomes. Its parameters (α, β, κ·H, λ, the V anchors, the ρ ceiling) are **uncalibrated placeholders**, and every worked trajectory example is **synthetic**. Whether a trajectory adds information beyond a well-measured current level is an open, testable hypothesis.
- **Not a medical device.** It has not been reviewed, cleared or approved by the FDA or any other regulator. It does not diagnose, stage, predict outcomes for an individual patient, or prescribe treatment. Scores are not probabilities that a person will develop cancer. On-screen readings (including surveillance-posture text) are readings of a research framework for discussion by a clinical team, not recommendations for any patient. Decisions about patient care rest with the treating clinicians, current guidelines and their professional judgment.
- **Not a professionally validated hazard or risk assessment.** For disaster, infrastructure and climate use, scores are relative, rubric-based indices, not forecasts, engineering assessments or actuarial figures; worked examples are teaching illustrations. The disaster-domain trajectory mapping (vulnerability indicator → V, programme delivery → ρ) is an extension proposed in this repository and is not part of the published RMTI papers.
- **Independent academic work.** Not an official product of the World Bank Group, Harvard University or any other institution.

## Your data

The sandboxes and calculators run entirely locally; nothing is uploaded. **Do not enter patient names or any identifying information** in any field, saved-case name, or spreadsheet cell.

## Human-subjects and animal research

This repository contains **no real patient data and no human-subjects or animal data**. Any future use of real serial patient data (for example the validation studies outlined in `docs/TRAJECTORY_GUIDE.md`) requires its own ethics review (IRB/REC), data-use agreements and, for animal work, IACUC approval, obtained by the investigators running those studies. None of that is granted or implied by this repository's licence.

## Warranty

Provided "as is", without warranties or conditions of any kind (Apache License 2.0, §§ 7–8). See `LICENSE`.
