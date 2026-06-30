#!/usr/bin/env python3
"""Stand-alone Lambda -> p pi-  (plain uproot, NO MCP server).

This is the whole analysis in one self-contained file: read an EDM4eic file with
uproot, select protons (PDG 2212) and pi- (PDG -211), build every proton-pi- pair,
compute the invariant mass, and histogram it. It produces the SAME histogram as the
uproot MCP server's execute_kernel path and as the ROOT examples next to this one —
that is the point: PODIO/MCP is one choice among many, the physics is identical.

Environment: a plain Python venv with `uproot awkward numpy` (see setup.md).
No ROOT, no PODIO, no Key4hep install needed.

Usage:
    python3 lambda_uproot.py [path/to/file.root] [--out output/lambda_hist_uproot.json]

The output JSON is compatible with ../../files/code/fit_lambda.py, so you can fit it:
    python3 ../../files/code/fit_lambda.py --in output/lambda_hist_uproot.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import awkward as ak
import numpy as np
import uproot

# PDG particle masses (GeV) and the bins — identical to lambda_kernel.py
M_PROTON, M_PION = 0.9382720813, 0.13957061
MASS_RANGE, N_BINS = (1.05, 1.25), 200

BRANCHES = [
    "ReconstructedChargedParticles.PDG",
    "ReconstructedChargedParticles.momentum.x",
    "ReconstructedChargedParticles.momentum.y",
    "ReconstructedChargedParticles.momentum.z",
]


def four_vectors(px, py, pz, m):
    """Build (px, py, pz, E) records for a jagged momentum selection."""
    E = np.sqrt(px * px + py * py + pz * pz + m * m)
    return ak.zip({"px": px, "py": py, "pz": pz, "E": E})


def pair_mass(a, b):
    """Invariant mass of every a x b pair, per event, flattened."""
    pair = ak.cartesian({"a": a, "b": b}, axis=1)
    sa, sb = pair["a"], pair["b"]
    m2 = ((sa["E"] + sb["E"]) ** 2
          - (sa["px"] + sb["px"]) ** 2
          - (sa["py"] + sb["py"]) ** 2
          - (sa["pz"] + sb["pz"]) ** 2)
    return ak.flatten(np.sqrt(ak.where(m2 > 0, m2, 0.0)))


def main(path, out):
    edges = np.linspace(*MASS_RANGE, N_BINS + 1)
    counts = np.zeros(N_BINS, dtype=np.int64)
    n_events = n_pairs = 0

    # Stream in batches so memory stays low even on big files.
    for ev in uproot.iterate(f"{path}:events", expressions=BRANCHES,
                             step_size=5000, library="ak"):
        pdg = ev["ReconstructedChargedParticles.PDG"]
        px = ev["ReconstructedChargedParticles.momentum.x"]
        py = ev["ReconstructedChargedParticles.momentum.y"]
        pz = ev["ReconstructedChargedParticles.momentum.z"]

        protons = four_vectors(px[pdg == 2212], py[pdg == 2212], pz[pdg == 2212], M_PROTON)
        pions = four_vectors(px[pdg == -211], py[pdg == -211], pz[pdg == -211], M_PION)

        m = pair_mass(protons, pions)
        h, _ = np.histogram(np.asarray(m), bins=edges)
        counts += h
        n_events += len(pdg)
        n_pairs += len(m)

    peak = 0.5 * (edges[:-1] + edges[1:])[counts.argmax()]
    print(f"events={n_events}  proton-pi- pairs={n_pairs}  peak bin centre={peak:.4f} GeV")

    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps({
        "dataset":            "stand-alone uproot",
        "edges":              edges.tolist(),
        "counts_lambda":      counts.tolist(),
        "counts_antilambda":  [0] * N_BINS,   # this minimal example does Lambda only
        "n_events":           n_events,
        "n_pairs_lambda":     n_pairs,
    }, indent=2))
    print(f"histogram -> {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?",
                    default="../../files/data/lambda_skim.root")
    ap.add_argument("--out", default="output/lambda_hist_uproot.json")
    a = ap.parse_args()
    main(a.path, a.out)
