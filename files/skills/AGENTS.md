# AGENTS.md — Lambda analysis project

## What this project does
Reconstruct Lambda0 -> p pi- in ePIC EDM4eic data and fit the invariant-mass
peak near 1.115683 GeV.

## Environment
- Python 3.10+ with: uproot, awkward, numpy, scipy, matplotlib.
- Docker, for the uproot MCP tool server (ghcr.io/eic/uproot-mcp-server:latest).
- Example data: files/data/lambda_skim.root (committed); full sample via a file list.

## Tools
- Use the `uproot` MCP server (get_file_structure, get_tree_info, histogram_branch,
  execute_kernel, and the dataset/async tools) for all ROOT file access.
- Do NOT write bespoke file I/O; the server already handles it.

## Data model
- Tree: events.  Collection: ReconstructedChargedParticles.
- Members: .PDG, .momentum.x, .momentum.y, .momentum.z   (momenta in GeV).
- PDG codes: proton 2212, pi- -211, antiproton -2212, pi+ 211.

## Physics constants (PDG)
- m(proton) = 0.9382720813 GeV, m(pi) = 0.13957061 GeV, m(Lambda) = 1.115683 GeV.

## Conventions
- Invariant mass over [1.05, 1.25] GeV, 200 bins.
- Fit a Gaussian + 2nd-order polynomial over [1.08, 1.16] GeV.
- Write results as JSON; save plots under output/.

## Definition of done
- Fitted peak within a few MeV of 1.115683 GeV and chi2/ndf of order 1.
- Always run the fit and check these before reporting a result.
