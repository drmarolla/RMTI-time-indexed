# Copyright 2026 Cesar Marolla
# Licensed under the Apache License, Version 2.0 (see LICENSE).
"""
set_doi.py -- fill the Zenodo DOIs into every placeholder in this repository.

Run once, after Zenodo has issued the DOIs for the first release:

    python tools/set_doi.py 10.5281/zenodo.<CONCEPT> 10.5281/zenodo.<VERSION>
    python tools/set_doi.py --dry-run 10.5281/zenodo.<CONCEPT> 10.5281/zenodo.<VERSION>

CONCEPT is the "all versions" DOI (cite it in running text); VERSION is the DOI
of exactly this archived release (cite it to pin what a reviewer saw). Both
appear on the Zenodo record page. Then run tools/check_release.py --release,
and commit. The change goes in a normal commit; it does not need a new release.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOI_RE = re.compile(r"^10\.\d{4,9}/[^\s]+$")


def rw(rel, fn, dry):
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        return 0
    old = open(path, encoding="utf-8").read()
    new = fn(old)
    if new != old:
        if not dry:
            open(path, "w", encoding="utf-8", newline="\n").write(new)
        print(("would update " if dry else "updated ") + rel)
        return 1
    return 0


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 2 or not all(DOI_RE.match(a) for a in args):
        print(__doc__)
        return 2
    concept, version = args
    changed = 0

    def cff(t):
        t = re.sub(r"^# doi:.*$", f"doi: {concept}", t, flags=re.M)
        return t

    def notice(t):
        return re.sub(
            r"Software citation: see CITATION\.cff\. A DOI for this version is assigned by Zenodo\s+"
            r"when the release is published; it is not yet known\.",
            "Software citation: see CITATION.cff. Archived on Zenodo: "
            f"https://doi.org/{concept} (all versions); this version: https://doi.org/{version}.",
            t)

    def html(t):
        t = re.sub(r"doi: '',[^\n]*\n", f"doi: '{concept}',   // concept DOI: always resolves to the latest version\n", t, count=1)
        t = re.sub(r"versionDoi: '',[^\n]*\n", f"versionDoi: '{version}',   // DOI of exactly this archived version\n", t, count=1)
        return t

    def readme(t):
        t = t.replace("The Zenodo DOI for this version is added after release.",
                      f"Archived on Zenodo: [{concept}](https://doi.org/{concept}) (all versions); "
                      f"this version: [{version}](https://doi.org/{version}).")
        t = t.replace("the Zenodo DOI for this version is added after release.",
                      f"archived on Zenodo: [{concept}](https://doi.org/{concept}).")
        return t

    for c in ("", "rmti-python/", "calculators/", "oncology/", "disaster/"):
        changed += rw(c + "CITATION.cff", cff, dry)
        changed += rw(c + "NOTICE", notice, dry)
        changed += rw(c + "README.md", readme, dry)
    for sb in ("oncology", "disaster"):
        changed += rw(f"{sb}/index.html", html, dry)
    print(f"\n{changed} file(s) {'would change' if dry else 'changed'}. "
          "Next: python tools/check_release.py --release")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
