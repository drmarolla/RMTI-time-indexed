# Changelog (oncoclastics)

## [1.0.0] — 2026-10-12 — first release

Terminology and mapping layer for the time-indexed RMTI. **No RMTI equation, tier threshold, anchor value, calculator or sandbox behaviour changed**; the 55 existing tests and `reproduce.py --check` pass unchanged.

### Added
- Step-by-step guide (`../docs/RMTI_Oncoclastics_Step_by_Step_Guide.pdf`).
- `RHO_BIO_ANCHORS.md`, `RHO_BIO_ANCHORS`, `RHO_BIO_DESCRIPTORS`, `rho_bio_from_anchor()`: five provisional, assigned anchor levels for biological adaptive reserve obtained (0.10, 0.25, 0.40, 0.55, 0.70), equally spaced across the span of the existing resilience ladders (0.10–0.70); order and wording from the manuscript's Table S4, restricted to biology; 6 of the 22 tests cover the anchors.
- Matching experimental panel in the oncology sandbox (`../oncology/index.html`) and `../tools/check_oncology_sandbox.py`, which compares the panel's JavaScript with the Python module over 3,888 input combinations. Released with repository version 2.3.0.
- `TERMINOLOGY_NOTE.md`: definition of *oncoclastics* in its two senses (biological, care-system), etymology and closest terms (oncolytic, osteoclast, clastogenic), operational reading of "oncoclastic event", relation to five neighbouring constructs, analogy and limits.
- Corrected mapping of the RMTI domains onto the two senses (Table 1 of the note; Table S9 of the manuscript).
- `rmti_oncoclastics.py` (`combine_rho`, `score_two_senses`, `care_disruption`, `run_two_sense_trajectory`, `oncoclastic_events`) and `test_oncoclastics.py` (22 tests).
