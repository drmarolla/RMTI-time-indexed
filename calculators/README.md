# RMTI Calculators (Excel) — v2.3.0

| File | Domain | Sheets |
|---|---|---|
| `RMTI_HCC_Calculator_v2.3.0.xlsx` | HCC / oncology | Cover · How to Use · RMTI Calculator · **Trajectory** · ALBI to Vulnerability · Reference · Data sources |
| `RMTI_Calculator_Disaster_v2.3.0.xlsx` | Disaster science | Cover · How to Use · Reference · RMTI Calculator · **Trajectory** |

**What changed from the previous workbooks:** only text (version strings, licence footers) and the Trajectory sheet. Every numeric value on the original sheets is unchanged (checked cell by cell after recalculation). The disaster workbook's Trajectory sheet is new.

**Worked cases.** The disaster workbook's six worked cities and two wildfire cases match the Python cohort field by field (`tools/check_cohort.py`). Nairobi, Dar es Salaam and Lusaka carry ρ after 0.65, 0.70 and 0.60.

**Using the Trajectory sheet.** Warm cells with blue text are inputs; grey cells calculate. One row per cycle, filled in order from t = 0, no blank rows between filled rows. Leave the observation blank for a missed visit. Set B13 = 0 to turn the filter off (memoryless). All parameters are uncalibrated placeholders and both examples are synthetic.

**Licence.** Apache License 2.0 (see `LICENSE`, `NOTICE`). The disaster workbook's footer was updated to match the project-wide Apache-2.0 policy.

Research prototype; not clinically validated; do not enter identifying information.
