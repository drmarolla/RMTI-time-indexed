# RMTI Sandbox — Oncology and Public Health Surveillance (Time-Indexed)

**v2.3.0.** Interactive, self-contained reference implementation of the Risk Mechanism Theory Index (RMTI) for hepatocellular carcinoma (HCC) surveillance and public-health surveillance. A single HTML file — no build step, no server, no external dependencies. Open `index.html` in any browser, or use the live page: **https://drmarolla.github.io/RMTI-time-indexed/oncology/**

## What's new in v2.2.0

A **Trajectory** panel under the result follows the score across cycles using the same L, E, C and starting ρ set above it. It shows the filtered R(t), the memoryless R(t) for comparison, tiers, ΔR and a chart against the fixed tier cut-points. Two synthetic examples are built in. The panel is experimental: parameters are uncalibrated placeholders and nothing is validated. The core equations, tiers and worked examples are unchanged.

## What it does

Implements **R = L·E·V·(1−ρ)** and **EAL = L·C·(1−ρ)**, a fixed five-tier scale, a log-normalized exposure helper, worked examples, and a Custom / Your Field mode with JSON export/import of saved cases (stored in this browser only; this edition uses its own storage key).

## Oncoclastics

The sandbox has an experimental **Oncoclastics** panel (oncology tab only). It reads the ρ slider as the care-system component, ρ_care, adds an optional biological component ρ_bio (default 0.00, which leaves every other result unchanged), combines them as ρ = 1 − (1 − ρ_bio)(1 − ρ_care), and shows the score with and without each component and for a moved ρ_care. ρ_bio is scored on five provisional, assigned anchor levels (`../oncoclastics/RHO_BIO_ANCHORS.md`), not validated. The panel's math is checked against `../oncoclastics/rmti_oncoclastics.py` by `../tools/check_oncology_sandbox.py`.

The two senses in which this sandbox's terms are read for cancer trajectories (biological and care-system) are defined in `../oncoclastics/TERMINOLOGY_NOTE.md`.

## Companion artifacts

Python package (`../rmti-python`, same math, 55 tests) and Excel calculators (`../calculators`) in this repository.

## Licence and citation

Apache License 2.0 — see `LICENSE` and `NOTICE`. Cite via `CITATION.cff`; the Zenodo DOI for this version is added after release.

## Intended use and limitations

Educational and research use only. See `../DISCLAIMER.md` — not a medical device, not clinically validated, not a professionally validated hazard assessment, no identifying information.
