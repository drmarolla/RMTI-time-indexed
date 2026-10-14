# Copyright 2026 Cesar Marolla
# Licensed under the Apache License, Version 2.0 (see LICENSE).
"""
check_oncology_sandbox.py -- the oncoclastics panel of the oncology sandbox must
agree with the Python reference (oncoclastics/rmti_oncoclastics.py).

    python tools/check_oncology_sandbox.py        # needs: node

The pure functions between /*ONCO_ENGINE_START*/ and /*ONCO_ENGINE_END*/ in
oncology/index.html (oncoCombineRho, oncoScore, oncoMove), together with the
sandbox's own roundTo, tierIndex, score and constants, are run in Node over a
grid of inputs and compared with score_two_senses() from the Python module.
The sandbox's rho_bio anchor levels and descriptors must equal RHO_BIO_ANCHORS /
RHO_BIO_DESCRIPTORS. Exit status 0 = agree; 1 = at least one difference; 2 = cannot run.
"""
import itertools
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "oncoclastics"))
from rmti_oncoclastics import (RHO_BIO_ANCHORS, RHO_BIO_CEILING, RHO_BIO_DESCRIPTORS,  # noqa: E402
                               combine_rho,
                               score_two_senses)

TOL = 1e-12


def grab_function(src, name):
    m = re.search(r"function\s+" + name + r"\s*\(", src)
    if not m:
        raise ValueError(f"function {name} not found in oncology/index.html")
    i = src.index("{", m.end())
    depth = 0
    for j in range(i, len(src)):
        depth += (src[j] == "{") - (src[j] == "}")
        if depth == 0:
            return src[m.start():j + 1]
    raise ValueError(f"unbalanced braces in {name}")


def grab_const(src, name):
    m = re.search(r"const\s+" + name + r"\s*=\s*[^;]+;", src)
    if not m:
        raise ValueError(f"const {name} not found")
    return m.group(0)


def main():
    if not shutil.which("node"):
        print("node is required to run this check")
        return 2
    src = open(os.path.join(ROOT, "oncology", "index.html"), encoding="utf-8").read()
    a, b = src.find("/*ONCO_ENGINE_START*/"), src.find("/*ONCO_ENGINE_END*/")
    if a < 0 or b < a:
        print("ONCO_ENGINE markers not found in oncology/index.html")
        return 2
    engine = src[a:b]
    deps = "\n".join([grab_const(src, "C_VALUES"), grab_const(src, "TIER_BOUNDS"),
                      grab_function(src, "roundTo"), grab_function(src, "tierIndex"),
                      grab_function(src, "score")])
    Ls, Es, Vs = (0.15, 0.55, 0.9), (0.2, 0.65, 1.0), (0.1, 0.5, 0.85)
    rbs, rcs, rms = (0.0, 0.2, 0.5, 0.9), (0.0, 0.1, 0.45, 0.9), (0.0, 0.05, 0.5)
    cases = [dict(L=L, E=E, V=V, rb=rb, rc=rc, rm=rm, C=C)
             for L, E, V, rb, rc, rm, C in itertools.product(Ls, Es, Vs, rbs, rcs, rms, (1, 3, 5))]
    harness = (deps + "\n" + engine +
               "\nconst cases = " + json.dumps(cases) + ";\n"
               "const out = cases.map(c => ({c, s: oncoScore(c.L,c.E,c.V,c.rb,c.rc,c.C),"
               " m: oncoMove(c.L,c.E,c.V,c.rb,c.rc,c.rm,c.C), k: oncoCombineRho(c.rb,c.rc)}));\n"
               "console.log(JSON.stringify({out, anchors: ONCO_RHO_BIO_ANCHORS}));")
    r = subprocess.run(["node", "-"], input=harness, capture_output=True, text=True)
    if r.returncode != 0:
        print("node failed:", r.stderr[:500])
        return 2
    payload = json.loads(r.stdout)
    results, anchors = payload["out"], payload["anchors"]
    problems = 0
    js_anchor = {a["key"]: (a["rho"], a["desc"]) for a in anchors}
    py_anchor = {k: (RHO_BIO_ANCHORS[k], RHO_BIO_DESCRIPTORS[k]) for k in RHO_BIO_ANCHORS}
    # input bounds: rho inputs stop at 0.99 (as in the workbooks' data validation; the
    # core rejects rho >= 1) in both sandboxes; rho_bio stops at its top anchor.
    for sandbox in ("oncology", "disaster"):
        text = open(os.path.join(ROOT, sandbox, "index.html"), encoding="utf-8").read()
        for rid in ("in-rho", "in-rhoAfter"):
            m = re.search(r'id="' + rid + r'"[^>]*max="([0-9.]+)"', text)
            if not m or float(m.group(1)) != 0.99:
                problems += 1
                print(f"  DIFFERENCE {sandbox}/index.html: #{rid} max is {m.group(1) if m else 'missing'}, expected 0.99")
    m = re.search(r'id="in-rhoBio"[^>]*max="([0-9.]+)"', src)
    if not m or float(m.group(1)) != RHO_BIO_CEILING:
        problems += 1
        print(f"  DIFFERENCE oncology/index.html: #in-rhoBio max is {m.group(1) if m else 'missing'}, expected {RHO_BIO_CEILING}")
    if js_anchor != py_anchor:
        problems += 1
        print("  DIFFERENCE rho_bio anchors (keys, values or descriptors) between sandbox and Python module")

    def cmp(label, got, want, case):
        nonlocal problems
        if abs(got - want) > TOL:
            problems += 1
            if problems <= 10:
                print(f"  DIFFERENCE {label}: sandbox {got!r}, Python {want!r}, case {case}")

    def tier_no(t):
        return int(re.search(r"Tier (\d)", t).group(1)) - 1

    for item in results:
        c, s, m = item["c"], item["s"], item["m"]
        if c["rc"] >= 1.0 or c["rb"] >= 1.0:
            continue
        py = score_two_senses(c["L"], c["E"], c["V"], c["rb"], c["rc"], c["C"])
        py_after = score_two_senses(c["L"], c["E"], c["V"], c["rb"], c["rm"], c["C"])
        cmp("rho", s["rho"], py["rho"], c)
        cmp("rho (combine)", item["k"], combine_rho(c["rb"], c["rc"]), c)
        cmp("R", s["R"], py["R_raw"], c)
        cmp("R without care", s["RnoCare"], py["R_without_care"], c)
        cmp("R without bio", s["RnoBio"], py["R_without_bio"], c)
        cmp("care effect", s["careEffect"], py["care_effect"], c)
        cmp("bio effect", s["bioEffect"], py["bio_effect"], c)
        cmp("R after move", m["Rafter"], py_after["R_raw"], c)
        cmp("delta R", m["dR"], py_after["R_raw"] - py["R_raw"], c)
        if s["tier"] != tier_no(py["tier"]):
            problems += 1
            print(f"  DIFFERENCE tier: sandbox {s['tier']}, Python {py['tier']}, case {c}")
        if m["tierAfter"] != tier_no(py_after["tier"]):
            problems += 1
            print(f"  DIFFERENCE tier after move: sandbox {m['tierAfter']}, Python {py_after['tier']}, case {c}")
    if problems:
        print(f"FAILED: {problems} difference(s) over {len(results)} cases")
        return 1
    print(f"OK: oncology sandbox oncoclastics panel agrees with Python over {len(results)} cases (tol {TOL})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
