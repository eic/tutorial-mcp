---
name: lambda-fit
description: >
  Reconstruct and fit the Lambda0 -> p pi- invariant-mass peak in ePIC EDM4eic
  data. Use when asked to measure the Lambda yield, mass, or width, or to
  reproduce the Lambda peak from a .root file or a file list.
---

# Lambda invariant-mass fit

## When to use
Any request to find, fit, or quantify the Lambda0 (or its antiparticle) in ePIC
reconstructed data via the proton-pion invariant mass.

## Inputs
- file: one EDM4eic .root URL (a root:// file from a DIS dataset), or
- file_list: the dataset's root:// files for the full sample
  (resolve both with the rucio tools: list_dids, list_files, list_file_replicas).

## Steps
1. Confirm the uproot MCP server is connected: get_tree_info on the input.
2. Build the proton-pion invariant-mass histogram with execute_kernel (one file)
   or execute_kernel_dataset (many files), tree_name 'events' and the
   ReconstructedChargedParticles momentum/PDG branches. For a large sample, cap
   the file count first; for more than ~10 files use submit_kernel_dataset and
   poll, in batches of ~20 files per job (one big job can hit an upstream idle
   timeout), so no single tool call outlives the client's timeout. Write any
   reduce/merge code as plain NumPy array operations (the sandbox rejects tuple
   unpacking in loops).
3. Fit the histogram with a second execute_kernel call (Gaussian + 2nd-order
   polynomial over [1.08, 1.16] GeV; NumPy/awkward only, no imports).
4. Report mu, sigma, signal yield S, and chi2/ndf.

## Success criteria (check before reporting success)
- At least ~50 entries in the fit window. With fewer, report insufficient
  statistics and stop — a low-stats fit lets the polynomial absorb the peak and
  can pass the checks below by accident.
- |mu - 1.115683 GeV| < 0.005 GeV.
- sigma in ~[0.001, 0.005] GeV (this is detector resolution, not natural width).
- chi2/ndf of order 1.
If any check fails, report the failure and the fit diagnostics, not a result.

## Provenance
List the tool calls and their parameters, and the dataset used (campaign and
file list), so the run can be reproduced.
