# RMTI Sandbox — Disaster Science (Time-Indexed)

**v2.3.0.** Interactive, self-contained reference implementation of the Risk Mechanism Theory Index (RMTI) for urban, infrastructure and disaster-risk assessment. A single HTML file — no build step, no server, no external dependencies. Open `index.html` in any browser, or use the live page: **https://drmarolla.github.io/RMTI-time-indexed/disaster/**

## What's new in v2.2.0

A **Trajectory** panel under the result follows the score across cycles using the same L, E, C and starting ρ set above it. It shows the filtered R(t), the memoryless R(t) for comparison, tiers, ΔR and a chart against the fixed tier cut-points. Two synthetic examples are built in. The panel is experimental: parameters are uncalibrated placeholders and nothing is validated. The core equations, tiers and worked examples are unchanged.

## What it does

Implements **R = L·E·V·(1−ρ)** and **EAL = L·C·(1−ρ)**, a fixed five-tier scale, a log-normalized exposure helper, worked examples, and a Custom / Your Field mode with JSON export/import of saved cases (stored in this browser only; this edition uses its own storage key).

## The six worked cities

All six worked examples carry a ρ-after value, matching the Python cohort (`../rmti-python`) and the workbook (`../calculators`) exactly; `tools/check_cohort.py` in the repository verifies this. Bamako, Lagos and Lilongwe are the investment worked examples; Nairobi, Dar es Salaam and Lusaka are comparators with illustrative inputs (ρ after 0.65, 0.70, 0.60).

## Companion artifacts

Python package (`../rmti-python`, same math, 55 tests) and Excel calculators (`../calculators`) in this repository.

## Licence and citation

Apache License 2.0 — see `LICENSE` and `NOTICE`. Cite via `CITATION.cff`; the Zenodo DOI for this version is added after release.

## Intended use and limitations

Educational and research use only. See `../DISCLAIMER.md` — not a medical device, not clinically validated, not a professionally validated hazard assessment, no identifying information.
