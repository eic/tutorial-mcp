# Alternative analysis approaches

Four self-contained implementations of the **same** Λ⁰ → p π⁻ invariant-mass analysis used in
the main lesson. They all read the same EDM4eic file, use the same particle masses and binning,
and produce the same peak near **1.1157 GeV** — the point being that PODIO/MCP is one choice
among many, not a requirement.

These are linked from Episode 3 and from `_extras/analysis-approaches.md`.

## Pick an input file

No data ships with the lesson; every script takes an EDM4eic reconstruction file as its argument
and reads it in place over `root://`. Find one from inside eic-shell, either by browsing the
store directly:

```bash
xrdfs root://dtn-eic.jlab.org ls /volatile/eic/EPIC/RECO
```

or by letting your assistant discover a dataset with the rucio/xrootd MCP tools
([Episode 3](../episodes/03-mcp-servers.md)). Below, `$FILE` stands for the full URL, e.g.
`root://dtn-eic.jlab.org//volatile/eic/EPIC/RECO/<campaign>/epic_craterlake/DIS/...root`.

## Run them

| Folder | Tool | Environment | Run it |
|---|---|---|---|
| `standalone_uproot/` | plain Python + uproot (no MCP) | Python venv: `uproot awkward numpy` | `python3 lambda_uproot.py $FILE` |
| `rdataframe/` | ROOT RDataFrame (PyROOT) | ROOT / eic-shell | `eic-shell -- python3 lambda_rdf.py $FILE` |
| `ttreereader/` | ROOT TTreeReader (C++ macro) | ROOT / eic-shell | `eic-shell -- root -l -b -q 'lambda_ttreereader.C("'$FILE'")'` |
| `podio_frame/` | native PODIO Frame API | Key4hep / eic-shell (needs `podio` + `edm4eic`) | `eic-shell -- python3 lambda_podio.py $FILE` |

Only `standalone_uproot` runs in a plain `pip` environment. The other three need a ROOT/Key4hep
stack — the easiest source is the ePIC [`eic-shell`](https://eic.github.io/) container. That
contrast is itself a lesson: the uproot-through-MCP path in the main episodes reproduces the same
physics with nothing heavier than eic-shell.

The stand-alone uproot example writes its histogram to `output/lambda_hist_uproot.json`; fit it
with an `execute_kernel` call as in [Episode 5](../episodes/05-end-to-end-agents.md) (Gaussian +
2nd-order polynomial over [1.08, 1.16] GeV), or with any fitter you like.
