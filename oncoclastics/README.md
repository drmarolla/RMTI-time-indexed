# Oncoclastics for RMTI Time-Indexed

**v1.0.0 · research framework.** The definition of the term *oncoclastics*, the corrected mapping of the Risk Mechanism Theory Index (RMTI) domains onto its two senses, and a small tested reference module, for use alongside the time-indexed RMTI in this repository. Author: Cesar Marolla (ORCID: 0000-0001-8498-7380).

> **Status, plainly.** A terminology and mapping layer. No RMTI equation, tier threshold or anchor changed. Nothing here is validated against real outcomes, all examples are synthetic, and nothing is a medical device or a clinical recommendation. See `DISCLAIMER.md`.

## What the term is

**Oncoclastics** (adjective **oncoclastic**) is the application of hazard–exposure–vulnerability–resilience assessment, as developed in disaster-risk reduction, to the fragmentation of cancer-related trajectories. Two senses, always named:

- **Biological oncoclastics**: the progression from chronic injury toward cancer in one patient (carried by L, E, V and ρ_bio).
- **Care-system oncoclastics**: the disruption of surveillance and care along that path (carried by ρ_care).

Full definition, etymology, closest terms and limits: **`TERMINOLOGY_NOTE.md`**.

## What's here

| File | What it is |
|---|---|
| `TERMINOLOGY_NOTE.md` | The citable definition note. Contains the corrected mapping of the RMTI domains (L, E, V, ρ, C) onto the two senses (Table S9 of the manuscript). |
| `../docs/RMTI_Oncoclastics_Step_by_Step_Guide.pdf` | Step-by-step guide: how to enter values into each equation, with worked examples (sample values, not validated) and a blank worksheet. |
| `RHO_BIO_ANCHORS.md` | The five provisional anchor levels for ρ_bio (biological adaptive reserve), where the numbers come from, and the rules for using them. |
| `rmti_oncoclastics.py` | Reference module (standard library only). Scores both senses through the unchanged `core.rmti_core`. |
| `test_oncoclastics.py` | 22 tests. |
| `../oncology/index.html` | The oncology sandbox's experimental **Oncoclastics** panel (oncology tab only), checked against the module by `../tools/check_oncology_sandbox.py`. |
| `CHANGELOG.md`, `CITATION.cff`, `ZENODO_METADATA.json`, `NOTICE`, `LICENSE`, `DISCLAIMER.md` | Release and legal files (Apache License 2.0). |

## Using it academically

Give "Risk Mechanism Theory Index (RMTI)" in full at first use; state the sense at every use of *oncoclastic*; cite the note (below) and the RMTI sources; do not use the term for a therapy, for tumor destruction, or as a synonym for cancer progression. Keywords: *oncoclastics; Risk Mechanism Theory Index; RMTI; disaster-risk reduction; surveillance; hepatocellular carcinoma*.

## Using it oncologically

Run from the repository root (Python 3.8+, no dependencies):

```bash
python oncoclastics/rmti_oncoclastics.py                                   # demo, synthetic inputs
python -m unittest discover -s oncoclastics -p "test_*.py" -v              # expect: Ran 22 tests ... OK
```

```python
import sys; sys.path.insert(0, "oncoclastics")
from rmti_oncoclastics import combine_rho, score_two_senses, care_disruption, run_two_sense_trajectory, oncoclastic_events

combine_rho(0.50, 0.40)                                   # 0.70  (not 0.90)
score_two_senses(L=0.30, E=0.65, V=0.60, rho_bio=0.30, rho_care=0.45, C=3)
care_disruption(0.30, 0.65, 0.60, 0.30, 0.45, 0.15)       # same biology, care capacity falls
rows = run_two_sense_trajectory(0.30, 0.65, 3, rho_bio=0.20, rho0_care=0.20,
                                observations=[2, 2, None, 3, 3],         # None = missed visit
                                delivery=[0.40, 0.55, 0.55, 0.30, 0.30])
oncoclastic_events(rows)                                  # descriptive flags, not alerts
```

Design points a reviewer can check:

- **Same equations.** Every score goes through `core.rmti_core.score()`; R = L·E·V·(1−ρ) and EAL = L·C·(1−ρ) are untouched.
- **Combined resilience** ρ = 1 − (1 − ρ_bio)(1 − ρ_care), as in Supplementary Material S5, computed in exact decimal arithmetic like the core.
- **Backward compatible.** The existing HCC ρ(t) is surveillance-driven, i.e. ρ_care. With ρ_bio = 0 the two-sense run reproduces the published HCC trajectory values exactly (tested, including the 0.081 / 0.055 / 0.042 / 0.031 example).
- **Same numbers in the sandbox.** The sandbox panel runs the same math in JavaScript; `python tools/check_oncology_sandbox.py` compares it with this module over 3,888 input combinations (tolerance 1e-12). Its default rho_bio = 0.00 leaves every existing sandbox result unchanged.
- **Provisional events.** "Oncoclastic event" is given an operational reading (missed visit or delivery fall; rise in V*) that is uncalibrated and exists to be tested.

## Cite

> Marolla, C. (2026). *Oncoclastics: a terminology note* (Version 1.0.0) [Computer software and definition note]. Zenodo. https://doi.org/[DOI added at release]

GitHub's "Cite this repository" reads `CITATION.cff` in this folder when the folder is the root of its own repository. Inside the parent repository, cite the parent via its own `CITATION.cff` and this note via the reference above.

## Archiving this note as its own Zenodo record

The manuscript cites a Zenodo-archived terminology note. The parent repository's Zenodo record is the software release, so for a separate DOI: create a new GitHub repository whose root is this folder's contents, copy `ZENODO_METADATA.json` to `.zenodo.json`, switch the repository on in Zenodo, and publish a release `v1.0.0`. Then enter the DOI in `CITATION.cff` and in the reference above by hand (`tools/set_doi.py` does not cover this folder). Alternatively, publish a new release of the parent repository and cite its version DOI.

## Intended use and limitations

Educational and research use only; see `DISCLAIMER.md`. Specific limits: independence of ρ_bio and ρ_care is untested; the probability of a care disruption is not modeled; ρ_care overlaps with C; event thresholds are uncalibrated; the ρ_bio anchors are assigned, not validated.
