# AGENTS.md — Lambda analysis project

## What this project does
Reconstruct Lambda0 -> p pi- in ePIC EDM4eic data and fit the invariant-mass
peak near 1.115683 GeV.

## Environment
- Everything runs inside eic-shell; the MCP servers are started with `eic-mcp up`.
- Data lives on the grid: find a DIS dataset with the `rucio` tools and read its
  root:// files in place with `uproot` — no download.

## Tools
- Use the `rucio` MCP server (list_dids, list_files, list_file_replicas) to locate
  a dataset and resolve its root:// URLs.
- Use the `xrootd` MCP server (check_file_exists, get_file_info) to verify a file.
- Use the `uproot` MCP server (get_tree_info, histogram_branch, execute_kernel,
  execute_kernel_dataset) for all ROOT file access. Prefer get_tree_info over
  get_file_structure: on an EDM4eic file the latter returns megabytes.
- Do NOT write bespoke file I/O; the servers already handle it.

## When a tool fails

- Never install software (no `pip install`, above all not `--break-system-packages`)
  and never re-implement the analysis with local uproot/ROOT.
- A timed-out call means the server is BUSY, not broken: it is single-threaded and
  still working on the previous request. Wait, retry once, and if it still fails,
  stop and report which tool failed with which arguments.
- Never reuse a cached earlier tool result as if it were fresh. A number that did
  not come from the MCP servers is not reproducible, so it is not an answer.

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
