#!/usr/bin/env python3
"""Lambda -> p pi- with the native PODIO Frame API.

This reads the EDM4eic file the way the data model intends: PODIO deserialises
each event into a Frame, you `get` the ReconstructedChargedParticles collection,
and iterate over typed objects with methods like `.getPDG()` and `.getMomentum()`.

This is the "what's under the hood" example. It is also the heaviest to set up:
it REQUIRES a Key4hep / eic-shell environment with `podio` and the `edm4eic`
dictionaries available. That contrast is the lesson: uproot + MCP get you the
same Lambda peak with nothing but Docker, while this path needs the full stack.

Environment: eic-shell / Key4hep. Run with:
    eic-shell -- python3 lambda_podio.py ../../files/data/lambda_skim.root

Output: the peak window count printed to stdout (peak near 1.1157 GeV).
"""
import sys

import numpy as np
from podio.root_io import Reader

M_P, M_PI = 0.9382720813, 0.13957061
EDGES = np.linspace(1.05, 1.25, 201)


def energy(mom, m):
    return (mom.x ** 2 + mom.y ** 2 + mom.z ** 2 + m * m) ** 0.5


def main(path):
    counts = np.zeros(200, dtype=np.int64)
    n_events = n_pairs = 0

    reader = Reader(path)
    for frame in reader.get("events"):
        coll = frame.get("ReconstructedChargedParticles")
        protons = [p for p in coll if p.getPDG() == 2212]
        pions = [p for p in coll if p.getPDG() == -211]
        n_events += 1
        for pr in protons:
            mp = pr.getMomentum()
            Ep = energy(mp, M_P)
            for pi in pions:
                mpi = pi.getMomentum()
                Epi = energy(mpi, M_PI)
                E = Ep + Epi
                X, Y, Z = mp.x + mpi.x, mp.y + mpi.y, mp.z + mpi.z
                m = max(E * E - (X * X + Y * Y + Z * Z), 0.0) ** 0.5
                idx = int((m - 1.05) / 0.001)
                if 0 <= idx < 200:
                    counts[idx] += 1
                    n_pairs += 1

    centres = 0.5 * (EDGES[:-1] + EDGES[1:])
    print(f"events={n_events}  proton-pi- pairs={n_pairs}  "
          f"peak bin centre={centres[counts.argmax()]:.4f} GeV")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../../files/data/lambda_skim.root")
