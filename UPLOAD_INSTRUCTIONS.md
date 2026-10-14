# Publish v2.3.0

Version 2.3.0 adds `oncoclastics/` and an oncoclastics panel in the oncology sandbox. Choose the path that matches what is online now.

**Path A: the repository `RMTI-time-indexed` already exists on GitHub (2.2.1 was published).** Follow sections 0-4.
**Path B: 2.2.1 was never published (or the repository does not exist yet).** Publish 2.3.0 directly: follow "Path B" at the end.

## 0. Prepare (both paths)
1. Extract the whole zip to a simple place such as `C:\RMTI\`.
2. In File Explorer turn on View, Show, **Hidden items**. The extracted folder must show exactly 18 entries: 8 folders (`.github`, `calculators`, `disaster`, `docs`, `oncoclastics`, `oncology`, `rmti-python`, `tools`) and 10 files (`.gitignore`, `.zenodo.json`, `CHANGELOG.md`, `CITATION.cff`, `DISCLAIMER.md`, `LICENSE`, `NOTICE`, `README.md`, `UPLOAD_INSTRUCTIONS.md`, `index.html`).
3. Optional, if Python (and Node.js) are installed, in that folder:
```
python tools/check_release.py
python tools/check_oncology_sandbox.py
python -m unittest discover -s oncoclastics -p "test_*.py"
```
The first should end with "All checks passed"; the others with "OK".

## 1. Path A: update the existing repository
In **GitHub Desktop**, with the existing local clone of `RMTI-time-indexed`:
1. Copy the extracted contents over the clone's folder (replace when asked). The two workbooks and the explainer are **renamed** (`...v2.2.1...` becomes `...v2.3.0...`); delete the old-named files if they are still there.
2. The Changes list should show the new `oncoclastics/` folder (about 12 files), the renamed calculators and explainer, the updated sandboxes and the version changes. Summary: `RMTI Time-Indexed v2.3.0: oncoclastics`. **Commit to main**, then **Push origin**.
3. Open the **Actions** tab: the `tests` workflow should turn green (Python 3.8, 3.10, 3.12, plus the release checks and the sandbox check).

## 2. Check GitHub Pages
After a minute or two confirm these open, and that the oncology page shows the **Oncoclastics** panel under the Trajectory panel (oncology tab only):
- https://drmarolla.github.io/RMTI-time-indexed/
- https://drmarolla.github.io/RMTI-time-indexed/oncology/
- https://drmarolla.github.io/RMTI-time-indexed/disaster/

## 3. Release
GitHub -> Releases -> **Draft a new release**, tag `v2.3.0`, title "RMTI Time-Indexed v2.3.0: oncoclastics", paste the 2.3.0 entry from `CHANGELOG.md`, **Publish release**. Zenodo (switched ON for this repository) archives it as a new version under the same concept DOI. Do not publish until step 1 shows the expected files, because Zenodo archives whatever is in the repository at that moment. On Zenodo check the title, Apache-2.0 licence, resource type Software and your ORCID.

## 4. Fill in the DOIs
Copy the **concept DOI** ("Cite all versions") and the new **version DOI**, then:
```
python tools/set_doi.py 10.5281/zenodo.<CONCEPT> 10.5281/zenodo.<VERSION>
python tools/check_release.py --release          # strict: must pass
```
Commit ("Add Zenodo DOIs") and push; no new release is needed. `set_doi.py` does not cover `oncoclastics/CITATION.cff` or `oncoclastics/ZENODO_METADATA.json`: enter the DOI there by hand if you archive the note separately (see `oncoclastics/README.md`).

## Path B: publish 2.3.0 as a fresh repository
GitHub Desktop -> File -> Add local repository -> the extracted folder -> create a repository here, name `RMTI-time-indexed` (no README, no .gitignore, no licence) -> Commit (the Changes list shows 74 files) -> Publish repository (public) -> Settings -> Pages -> `main` / root -> Zenodo -> Account -> GitHub -> Sync now, switch the repository ON -> release `v2.3.0` (section 3) -> section 4. The Zenodo metadata already lists the 2.2.0 record (10.5281/zenodo.23286786) as the predecessor.

## For the manuscript
Cite the version DOI of 2.3.0 (see `docs/PAPER_SUPPORT.md`). In the manuscript, S8 and reference 2026d describe this release; replace the two highlighted DOI placeholders once the DOIs exist.

## Items to confirm before you publish
- `DISCLAIMER.md` (root, plus a copy in each component folder and in `oncoclastics/`) applies to the oncoclastics panel: research prototype, not validated, not a medical device.
- The rho_bio anchors in the oncoclastics panel are provisional and assigned (five levels across 0.10-0.70, the span of the existing rho ladders), not validated; the default 0.00 (not scored) leaves every existing result unchanged.
- No unpublished manuscript drafts are included.
