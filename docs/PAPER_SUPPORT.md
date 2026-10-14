# Support for the manuscript

Material for citing this software, stating availability, and letting reviewers reproduce every number. Placeholders in square brackets are filled in after the Zenodo release (see `UPLOAD_INSTRUCTIONS.md`, `tools/set_doi.py`).

## 1. Citing the software

Cite the **version DOI** to pin exactly what a reviewer saw, and mention the concept DOI for "all versions".

```bibtex
@software{marolla_rmti_time_indexed_2026,
  author    = {Marolla, Cesar},
  title     = {{RMTI Time-Indexed}},
  year      = {2026},
  version   = {2.3.0},
  publisher = {Zenodo},
  doi       = {[version DOI, 10.5281/zenodo.xxxxxxx]},
  url       = {https://github.com/drmarolla/RMTI-time-indexed},
  license   = {Apache-2.0}
}
```

Plain text: Marolla, C. (2026). *RMTI Time-Indexed* (Version 2.3.0) [Computer software]. Zenodo. https://doi.org/[version DOI]

Cite the version you used. Version 2.3.0 adds oncoclastics (see `oncoclastics/`). The earlier 2.2.0 archive (10.5281/zenodo.23286786) holds the same time-indexed content in a flattened folder layout and is superseded.

Earlier records this work derives from: Python reference implementation 10.5281/zenodo.21445892, oncology sandbox 10.5281/zenodo.22909090, disaster-science sandbox 10.5281/zenodo.22909081.

## 2. Code and data availability statement (ready to paste)

> The Risk Mechanism Theory Index (RMTI) time-indexed software, comprising a Python reference implementation, Excel calculators and interactive browser sandboxes for oncology and disaster science, is openly available under the Apache License 2.0 at https://github.com/drmarolla/RMTI-time-indexed and is archived on Zenodo (version 2.3.0; https://doi.org/[version DOI]). Interactive sandboxes are available at https://drmarolla.github.io/RMTI-time-indexed/. All trajectory examples in this paper are synthetic and are produced by the archived code (`rmti-python/reproduce.py`); no patient-level or human-subjects data were used. Published cohort values used for comparison are taken from the cited sources.

## 3. Reproduce every number

```bash
git clone https://github.com/drmarolla/RMTI-time-indexed && cd RMTI-time-indexed/rmti-python
python -m unittest discover -s tests -t . -v     # 55 tests
python reproduce.py --check                      # compares with docs/reproduce_expected_output.txt
python reproduce.py                              # print the full report
```

Python 3.8 or newer, standard library only. The report is deterministic: no random numbers, clocks or network access. `python tools/check_workbooks.py` (needs `pip install openpyxl`) reads each calculator's Trajectory sheet, runs the Python code on the sheet's own inputs and parameters, and compares every computed column; the two agree to about 1e-16. The sandboxes' JavaScript engine reproduces the same values.

## 4. What each result is supported by

| Result | Where it is reproduced |
|---|---|
| Six-city disaster cohort R now / R after / tiers; wildfire cases | `reproduce.py` section 1; `tests/test_rmti.py` (cohort tests); `tools/check_cohort.py` (workbook and sandbox agree with it) |
| HCC cohort mean V (0.52 and 0.48) and published HCC cases | `reproduce.py` section 2; `tests/test_rmti.py` |
| Memoryless trajectory table, examples T-A and T-B (0.081, 0.055, 0.042, 0.031 and 0.081, 0.094, 0.113, 0.127) | `reproduce.py` section 3; `tests/test_dynamic.py` |
| Filtered trajectory values and the filter gains (0.4149, 0.0855) | `reproduce.py` section 3; `tests/test_dynamic.py` |
| Workbook agrees with code | `tools/check_workbooks.py` (both Trajectory sheets against `dynamic/rmti_dynamic.py`) |
| Combined resilience ρ = 1 − (1 − ρ_bio)(1 − ρ_care) (S5 example 0.50, 0.40 → 0.70); ρ_bio = 0 reproduces the HCC trajectory; the sandbox panel agrees with Python | `oncoclastics/test_oncoclastics.py` (22 tests); `tools/check_oncology_sandbox.py` |

**Not supported by this repository:** any claim that the trajectory layer is validated, calibrated or clinically useful, or that it outperforms a well-measured current level. The parameters are placeholders and the examples are synthetic. Those are questions for the pre-registered studies described in `TRAJECTORY_GUIDE.md`, section 6.

## 5. Notes for the review process

- **Freeze what reviewers see.** Tag and archive the release before submission and cite the version DOI. Do not push changes to the tagged release afterwards; later edits go in a new version.
- **Double-blind review.** The repository carries the author's name in `LICENSE`, `NOTICE`, `CITATION.cff` and the sandbox footers. If the journal is double-blind, supply an anonymised copy of the release zip for review and point to the public repository after acceptance.
- **One set of worked cases everywhere.** The Python cohort, the disaster workbook and the disaster sandbox carry identical inputs and results for all worked cases, including Nairobi, Dar es Salaam and Lusaka (ρ-after 0.65, 0.70, 0.60; R-after 0.152, 0.185, 0.196). `python tools/check_cohort.py` verifies this field by field and fails if any of the three drifts.
- **Ethics.** The software uses no human-subjects or animal data. Any validation on real serial patient data needs its own ethics approval and data-use agreements.

## 6. Pre-submission checklist

- [ ] `python tools/check_release.py` passes (placeholder warnings only)
- [ ] `python rmti-python/reproduce.py --check` passes
- [ ] `python tools/check_workbooks.py` and `python tools/check_cohort.py` pass (after any workbook edit, recalculate and save first)
- [ ] 55 tests pass locally (and 22 oncoclastics tests: `python -m unittest discover -s oncoclastics -p "test_*.py"`), `python tools/check_oncology_sandbox.py` passes, and the GitHub Actions run on `main` is green
- [ ] Release `v2.3.0` created on GitHub; Zenodo record published; DOIs noted
- [ ] `python tools/set_doi.py <concept> <version>` run, then `python tools/check_release.py --release` passes, committed
- [ ] GitHub Pages is live and all three addresses open (landing page, `/oncology/`, `/disaster/`)
- [ ] Every number in the manuscript matches `docs/reproduce_expected_output.txt`
- [ ] Limitations in the manuscript match `DISCLAIMER.md` (uncalibrated parameters, synthetic examples, not validated, not a medical device)
- [ ] Availability statement and software citation above are filled in
- [ ] After acceptance: add a `preferred-citation` entry for the paper to `CITATION.cff` and publish a new version
