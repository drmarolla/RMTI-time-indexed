# Changelog

## [2.3.0] — 2026-10-12 — oncoclastics

Adds the term **oncoclastics** and its two senses (biological, care-system) to the time-indexed RMTI. **No RMTI equation, tier threshold, anchor value or calculator formula changed**; every existing numeric output is reproduced exactly (the 55 existing tests and `reproduce.py --check` pass unchanged).

### Added
- `oncoclastics/` (independently versioned, v1.0.0): citable terminology note, the mapping of the RMTI domains (L, E, V, ρ, C) onto the two senses, and `rmti_oncoclastics.py` with 22 tests. The module also provides provisional ρ_bio anchors (`RHO_BIO_ANCHORS`: five ordinal levels, 0.10 to 0.70, the span of the existing ρ ladders; order and wording from the manuscript's Table S4). The module combines resilience as ρ = 1 − (1 − ρ_bio)(1 − ρ_care) and, with ρ_bio = 0, reproduces the existing HCC ρ(t) (which is the care-system component).
- Oncology sandbox: an experimental **Oncoclastics** panel (shown on the oncology tab only) with clickable ρ_bio anchor levels. Default ρ_bio = 0.00 leaves every existing sandbox result unchanged.
- `docs/RMTI_Oncoclastics_Step_by_Step_Guide.pdf`: 9-page guide to entering values into the equations, with worked examples built from the repository's own published-cohort inputs and from sample values, a where-to-type page (Python, sandbox, workbook), common mistakes and a blank worksheet.
- `tools/check_oncology_sandbox.py`: runs the panel's JavaScript in Node and compares it with the Python module over 3,888 input combinations (tolerance 1e-12); added to the GitHub Actions workflow.

### Changed
- ρ inputs in both sandboxes (and the saved-case import) now stop at **0.99**, matching the workbooks' data validation; they previously allowed 1.00, which gives R = 0 while the Python core rejects ρ ≥ 1. No example, tier or cohort result changes.
- Version strings, `CITATION.cff` release dates and the versioned file names (`RMTI_HCC_Calculator_v2.3.0.xlsx`, `RMTI_Calculator_Disaster_v2.3.0.xlsx`, `RMTI_Calculator_Explainer_v2.3.0.docx`). Workbook and explainer content is otherwise unchanged apart from the version text.
- Keyword `oncoclastics` added to `CITATION.cff` and `.zenodo.json`; Zenodo description and notes updated.
- `UPLOAD_INSTRUCTIONS.md` rewritten for 2.3.0.

### Limitations carried with this release
the ρ_bio anchors are provisional and assigned (five levels across 0.10–0.70, the span of the existing ρ ladders), not validated; independence of ρ_bio and ρ_care is untested; the probability of a care disruption is not modeled; ρ_care overlaps with C through stage at detection. See `oncoclastics/TERMINOLOGY_NOTE.md`.

## [2.2.1] — 2026-10-10 — packaging correction

Restores the repository's intended folder layout. The version-2.2.0 archive on Zenodo (https://doi.org/10.5281/zenodo.23286786) was created from an upload in which the folders were flattened and `.zenodo.json` lost its leading dot, so that archive holds the right files in the wrong places: the Python package cannot be imported or tested as archived, and the sandboxes have no folder paths. **No code, equation, parameter, workbook value or sandbox behaviour changed.** Cite 2.2.1.

### Changed
- The Zenodo and citation title is now simply "RMTI Time-Indexed" (the description still spells out the Risk Mechanism Theory Index and the contents).
- Version strings, `CITATION.cff` release date, and the versioned file names (`RMTI_HCC_Calculator_v2.2.1.xlsx`, `RMTI_Calculator_Disaster_v2.2.1.xlsx`, `RMTI_Calculator_Explainer_v2.2.1.docx`).
- Archiving: the repository was recreated, so 2.2.1 is archived as a separate Zenodo record (new concept DOI) that points to the 2.2.0 record (10.5281/zenodo.23286786) as its predecessor. Cite 2.2.1.
- Wording that said a DOI would be assigned "at the first release" now refers to the DOI of the specific version.

## [2.2.0] — 2026-10-09 — time-indexed release (first release of this repository)

Adds a time-indexed (trajectory) layer. **No RMTI equation, tier threshold or anchor value changed**; every v2.1.0 numeric output is reproduced exactly (all 37 v2.1.0 tests pass unchanged; 18 new tests added, 55 total).

### Added
- `rmti-python/reproduce.py` and `docs/reproduce_expected_output.txt`: one command regenerates (and `--check` verifies) every numerical result, including the six-city cohort, HCC cohorts and trajectory examples.
- `tools/check_release.py` (versions, licences, metadata, links, file limits), `tools/check_workbooks.py` (each Trajectory sheet against the Python code, 80 values, agreement to ~1e-16), `tools/check_cohort.py` (Python cohort, workbook and sandbox examples agree field by field) and `tools/set_doi.py` (fills all Zenodo DOI placeholders in one pass).
- `.github/workflows/tests.yml`: tests and release checks on Python 3.8, 3.10 and 3.12.
- `docs/PAPER_SUPPORT.md`: citation, availability statement, results-to-code map, review-process notes, pre-submission checklist.
- Root `index.html` landing page; sandbox folders are named `oncology/` and `disaster/` so the live addresses are short (`.../oncology/`, `.../disaster/`).
- Module `__version__` strings in `oncology/rmti_hcc.py` and `disaster_climate/rmti_ssa.py` bumped to 2.2.0 to match the package (no code change in either module).
- Root `index.html` landing page; sandbox folders are named `oncology/` and `disaster/` so the live addresses are short (`.../oncology/`, `.../disaster/`).
- Module `__version__` strings in `oncology/rmti_hcc.py` and `disaster_climate/rmti_ssa.py` bumped to 2.2.0 to match the package (no code change in either module).
- `rmti-python/dynamic/rmti_dynamic.py` — Level-2 filtered trajectory: local-linear-trend filter for the vulnerability driver, delivery-driven ρ(t), scoring through the shared core. Includes `steady_state_gains()` (reproduces the workbook's α = 0.41, β = 0.09) and `tier_changes()`. It matches the workbook's Trajectory sheet to ~1e-16 and reproduces the draft's Patient A/B table.
- `core/rmti_core.py` v2.2.0: `IR_raw` / `R_raw` in `score()`; input validation (L, E, V in [0,1]; ρ in [0,1); C in 1–5); `RHO_ANCHORS_HCC`. These merge the trajectory-branch "v1.2.0" fixes into the v2.1.0 core. The trajectory-branch file was branched from v1.1.0 and lacked v2.1.0's `postures` argument and Apache header; both are kept here.
- `calculators/RMTI_HCC_Calculator_v2.2.1.xlsx` — v2.1.0 workbook plus the Trajectory sheet; all original numeric values unchanged.
- `calculators/RMTI_Calculator_Disaster_v2.2.1.xlsx` — disaster workbook plus a new Trajectory sheet (annual review cycles; indicator → V, delivery → ρ).
- Trajectory panel in both sandboxes (`oncology/`, `disaster/`).
- `DISCLAIMER.md`, root `NOTICE`, `CITATION.cff`, `.zenodo.json`.
- `docs/RMTI_Calculator_Explainer_v2.2.1.docx` — the calculator explainer, now covering the Trajectory sheet.

### Fixed
- Disaster workbook, Trajectory sheet: two column headers per example still read "AL level" / "AL slope" (oncology wording); now "Indicator level" / "Indicator slope".
- Sandboxes: the numbers under the tier bar (0, 0.05, 0.15, 0.35, 0.60, 1.0) were evenly spaced while the bar itself is linear in R, so labels did not sit under the tier boundaries. They are now positioned at their true locations.

### Changed
- **Worked cases aligned across all three artifacts.** The disaster workbook and sandbox now carry ρ-after for Nairobi, Dar es Salaam and Lusaka (0.65 / 0.70 / 0.60), matching the Python cohort and the published R-after figures (0.152 / 0.185 / 0.196). Previously the workbook left them blank and the sandbox set ρ-after equal to ρ-now. No other input or result differed (checked field by field). `tools/check_cohort.py` now guards this.
- **Licence footers in the disaster workbook** ("proprietary / not for redistribution") replaced with the Apache-2.0 notice, to match the project-wide v2.0.0 policy that every component is Apache 2.0.
- Sandbox saved-case storage keys are new (`..._ti_...`) so the time-indexed sandboxes do not share browser storage with the earlier standalone sandboxes.
- Version strings in the HCC workbook updated to 2.2.0.

### Known limits
- α, β, κ·H, λ, the V anchors and the ρ ceiling are uncalibrated placeholders. Nothing here is validated against incident HCC or real disaster outcomes.
- Edge case: if an adherence/delivery entry is blank at cycle t−1 and filled at cycle t, the workbook takes the change from 0 (blank = 0) whereas Python and the sandboxes take it from the last observed value. The documented missed-visit workflow (leave the observation blank, keep the adherence entry) is unaffected.
- No time-varying L(t) or E(t), and no social-determinants modifier (coefficients uncalibrated).

For history before 2.2.0 see `rmti-python/CHANGELOG.md`.
