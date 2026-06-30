# Alternative analysis approaches

Four self-contained implementations of the **same** Λ⁰ → p π⁻ invariant-mass analysis used in
the main lesson. They all read the same EDM4eic file, use the same particle masses and binning,
and produce the same peak near **1.1157 GeV** — the point being that PODIO/MCP is one choice
among many, not a requirement.

These are linked from Episode 3 and from `_extras/analysis-approaches.md`.

| Folder | Tool | Environment | Run it |
|---|---|---|---|
| `standalone_uproot/` | plain Python + uproot (no MCP) | Python venv: `uproot awkward numpy` | `python3 lambda_uproot.py ../../files/data/lambda_skim.root` |
| `rdataframe/` | ROOT RDataFrame (PyROOT) | ROOT / eic-shell | `eic-shell -- python3 lambda_rdf.py ../../files/data/lambda_skim.root` |
| `ttreereader/` | ROOT TTreeReader (C++ macro) | ROOT / eic-shell | `eic-shell -- root -l -b -q 'lambda_ttreereader.C("../../files/data/lambda_skim.root")'` |
| `podio_frame/` | native PODIO Frame API | Key4hep / eic-shell (needs `podio` + `edm4eic`) | `eic-shell -- python3 lambda_podio.py ../../files/data/lambda_skim.root` |

Only `standalone_uproot` runs in a plain `pip` environment. The other three need a ROOT/Key4hep
stack — the easiest source is the ePIC [`eic-shell`](https://eic.github.io/) container. That
contrast is itself a lesson: the uproot-through-MCP path in the main episodes reproduces the same
physics with nothing heavier than Docker.

The stand-alone uproot example writes a histogram JSON that the lesson's fitter understands:

```bash
cd standalone_uproot
python3 lambda_uproot.py ../../files/data/lambda_skim.root
python3 ../../files/code/fit_lambda.py --in output/lambda_hist_uproot.json --charge lambda
```
