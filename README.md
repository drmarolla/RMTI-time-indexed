# RMTI Time-Indexed — Oncology and Disaster Science

[![tests](https://github.com/drmarolla/RMTI-time-indexed/actions/workflows/tests.yml/badge.svg)](https://github.com/drmarolla/RMTI-time-indexed/actions/workflows/tests.yml)

**v2.3.0 · research prototype.** The Risk Mechanism Theory Index (RMTI) — a single, decision-ready risk score **R = L·E·V·(1−ρ)** with an Expected Annual Loss layer **EAL = L·C·(1−ρ)** — taken from a snapshot to a **trajectory**: V(t) and ρ(t) updated cycle by cycle. Author: Cesar Marolla (ORCID: 0000-0001-8498-7380).

> **Status, plainly.** Designed and prototyped, not validated. The equations of the core are unchanged from the published RMTI work. The time-indexed layer is new; its parameters (α, β, κ·H, λ, V anchors) are uncalibrated placeholders and every trajectory example is synthetic. The open question this repository exists to test: *does trajectory add information beyond a well-measured current level?* See `DISCLAIMER.md`.

## What's here

| Folder | What it is |
|---|---|
| `index.html` | Landing page for the live site (links to both sandboxes). |
| `rmti-python/` | Tested Python reference implementation: shared `core/`, `oncology/` (HCC), `disaster_climate/`, and the new `dynamic/` trajectory layer. 55 tests. |
| `calculators/` | `RMTI_HCC_Calculator_v2.3.0.xlsx` (oncology) and `RMTI_Calculator_Disaster_v2.3.0.xlsx` (disaster science), each with a **Trajectory** sheet. |
| `oncology/` | Interactive single-file HTML sandbox, HCC and public-health surveillance, with a **Trajectory** panel and an experimental **Oncoclastics** panel. Live: https://drmarolla.github.io/RMTI-time-indexed/oncology/ |
| `disaster/` | Interactive single-file HTML sandbox, urban, infrastructure and disaster risk, with a **Trajectory** panel. Live: https://drmarolla.github.io/RMTI-time-indexed/disaster/ |
| `oncoclastics/` | The term **oncoclastics** and its two senses (biological, care-system): citable definition note, the RMTI domains mapped onto both senses, and a small tested module (`rmti_oncoclastics.py`); the oncology sandbox has a matching experimental panel. Independently versioned (v1.0.0); no RMTI equation changed. |
| `docs/` | Trajectory guide, a 9-page step-by-step guide to entering values into the equations (sample values, with a blank worksheet), calculator explainer (v2.3.0), manuscript support (citation, availability statement, reproducibility map), and the stored reproduction output. |
| `tools/` | `check_release.py` (pre-release gate), `check_workbooks.py` (Excel vs Python parity), `check_cohort.py` (cohort, workbook and sandbox agree) and `set_doi.py` (fills Zenodo DOIs in one pass). |
| `.github/` | Continuous-integration workflow (tests on Python 3.8, 3.10, 3.12). |

## The time-indexed model (Level 2, "filtered")

Each cycle *t* (six-monthly surveillance for HCC; annual review for disaster risk):

```
x(t) = [level, slope]           local-linear-trend state; y(t) = level(t) + noise
V*(t) = v_lo + (v_hi − v_lo) · clip(level + κH·slope, 0, y_max) / y_max
ρ(t)  = clip(ρ(t−1) + λ·Δdelivery, 0, ρ_ceiling)
R(t)  = L · E · V*(t) · (1 − ρ(t))        tier and posture from the fixed Table 3 bands
```

| | oncology (HCC) | disaster science |
|---|---|---|
| indicator y(t) driving V | allostatic load composite (0–6, or 0–13) | composite vulnerability-indicator index (default 0–10) |
| delivery driving ρ(t) | surveillance adherence | share of the planned resilience programme delivered |
| status | follows the trajectory guide | **extension proposed here**, not in the published papers |

With the filter off the model is memoryless and reproduces the draft's Patient A/B table exactly (R = 0.081, 0.055, 0.042, 0.031 and 0.081, 0.094, 0.113, 0.127). The Python module, both workbooks and both sandboxes were cross-checked against each other (agreement to ~1e-16 between Python and Excel). See `docs/TRAJECTORY_GUIDE.md`.

## Quick start

```bash
cd rmti-python
python -m unittest discover -s tests -t . -v      # expect: Ran 55 tests ... OK
python reproduce.py --check                       # every reported number, deterministic
```

```python
from dynamic.rmti_dynamic import run_trajectory, HCC_PARAMS

rows = run_trajectory(L=0.30, E=0.65, C=3, rho0=0.20,
                      observations=[2, 1, 1, 0],        # allostatic load per cycle (None = missed visit)
                      delivery=[0.40, 0.55, 0.70, 0.75]) # adherence per cycle
for r in rows:
    print(r["t"], round(r["R"], 4), r["tier"])
```

Open `oncology/index.html` or `disaster/index.html` directly in a browser (no build step, no network, no dependencies), or open the workbooks in Excel.

## Oncoclastics

*Oncoclastics* is the application of hazard–exposure–vulnerability–resilience assessment, as developed in disaster-risk reduction, to the fragmentation of cancer-related trajectories, in two senses that are always named: **biological** (progression from chronic injury toward cancer) and **care-system** (disruption of surveillance and care along that path). In the RMTI the care-system sense enters only through ρ (the oncology sandbox has an experimental panel for this); the time-indexed HCC layer already separates the two (V(t) from an allostatic-load indicator, ρ(t) from surveillance adherence). Definition, mapping and limits: `oncoclastics/TERMINOLOGY_NOTE.md`.

## Licence, attribution, citation

- **Apache License 2.0 for everything in this repository**, code, calculators, rubric text, tier descriptions and examples alike — see `LICENSE` and `NOTICE` (each component folder carries its own copy).
- Cite via `CITATION.cff` (GitHub's "Cite this repository" button). The Zenodo DOI for this version is added after release.
- Derived from three earlier RMTI records: Python `10.5281/zenodo.21445892`, oncology sandbox `10.5281/zenodo.22909090`, disaster sandbox `10.5281/zenodo.22909081`.

## Intended use and limitations

Educational and research use only. Not a medical device; not clinically validated; not for patient-care decisions; not a professionally validated hazard assessment. No real patient data are included — do not enter identifying information. Independent academic tool, not an official product of any institution. Full statement: `DISCLAIMER.md`.
