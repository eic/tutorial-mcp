---
title: "Alternative Analysis Approaches"
---

In the main episodes we read EDM4eic data with **uproot**, through an MCP server, because that
needs nothing heavier than the tools already inside `eic-shell`. But uproot is one choice among
many. This page collects the **same** Λ⁰ → p π⁻ analysis written four different ways — every one
of them reproduces the same peak near **1.1157 GeV**. Use whichever fits the stack you already
have.

Each example reads one of the dataset's `root://` files directly (the same file the MCP servers
discover with rucio and verify with xrootd — no download), selects protons (PDG `2212`) and π⁻
(PDG `-211`), builds proton–π⁻ pairs, and histograms the invariant mass. The full scripts are in
the lesson's [`extras/`](https://github.com/aprozo/tutorial-mcp/tree/main/extras) folder. In the
commands below, replace `root://dtn-eic.jlab.org//...` with the file you located.

::::::::::::::::::::::::::::::::::::::::::::: callout

## All four agree

Same masses (`M_p = 0.9382720813`, `M_π = 0.13957061` GeV), same 200 bins over 1.05–1.25 GeV,
same peak. The physics does not care which library you use — so choose for convenience, not
dogma.

:::::::::::::::::::::::::::::::::::::::::::::

## 1. Stand-alone uproot (no MCP)

Plain Python, no server, no ROOT install — the whole analysis in one file. This is the engine
the MCP server runs internally.

* **Environment:** a `pip` venv with `uproot awkward numpy`.
* **Script:** [`extras/standalone_uproot/lambda_uproot.py`](https://github.com/aprozo/tutorial-mcp/blob/main/extras/standalone_uproot/lambda_uproot.py)

```bash
$ python3 extras/standalone_uproot/lambda_uproot.py root://dtn-eic.jlab.org//...
```

The core is just a four-vector build and a Cartesian pairing:

```python
protons = four_vectors(px[pdg == 2212], ..., M_PROTON)
pions   = four_vectors(px[pdg == -211], ..., M_PION)
m = pair_mass(protons, pions)          # invariant mass of every p x pi- pair
```

## 2. ROOT RDataFrame (PyROOT)

Columnar and declarative; a JIT-compiled C++ helper does the per-event pairing, RDataFrame
histograms it in one pass. Scales to many files and cores for free.

* **Environment:** ROOT (e.g. inside `eic-shell`).
* **Script:** [`extras/rdataframe/lambda_rdf.py`](https://github.com/aprozo/tutorial-mcp/blob/main/extras/rdataframe/lambda_rdf.py)

```bash
$ eic-shell -- python3 extras/rdataframe/lambda_rdf.py root://dtn-eic.jlab.org//...
```

```python
df = ROOT.RDataFrame("events", path)
df = df.Define("m_lambda", "lambda_mass(ReconstructedChargedParticles.PDG, ...)")
h  = df.Histo1D(("h", ";m(p,pi) [GeV];pairs", 200, 1.05, 1.25), "m_lambda")
```

## 3. ROOT TTreeReader (C++ macro)

The classic ROOT event loop — explicit, easy to read, and the form most ePIC analysis code is
written in. Note the reconstructed momentum branches are `float`, so the `TTreeReaderArray` must
be templated on `<float>`.

* **Environment:** ROOT (e.g. inside `eic-shell`).
* **Script:** [`extras/ttreereader/lambda_ttreereader.C`](https://github.com/aprozo/tutorial-mcp/blob/main/extras/ttreereader/lambda_ttreereader.C)

```bash
$ eic-shell -- root -l -b -q 'extras/ttreereader/lambda_ttreereader.C("root://dtn-eic.jlab.org//...")'
```

## 4. Native PODIO Frame API

Reading the data the way the data model intends: PODIO deserialises each event into a `Frame`,
and you iterate over typed objects (`p.getPDG()`, `p.getMomentum()`).

* **Environment:** Key4hep / `eic-shell` — needs the `podio` and `edm4eic` dictionaries. This is
  the **heaviest** option to set up.
* **Script:** [`extras/podio_frame/lambda_podio.py`](https://github.com/aprozo/tutorial-mcp/blob/main/extras/podio_frame/lambda_podio.py)

```bash
$ eic-shell -- python3 extras/podio_frame/lambda_podio.py root://dtn-eic.jlab.org//...
```

::::::::::::::::::::::::::::::::::::::::::::: callout

## Same physics, lower barrier

The PODIO example needs the full Key4hep stack; the uproot path in the main episodes needs only
the tools already inside `eic-shell`. Both find the same Λ⁰. That is exactly why pairing an AI
assistant with an uproot MCP server is such a cheap on-ramp: you get real analysis without the
heavy install.

:::::::::::::::::::::::::::::::::::::::::::::
