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
- file:      one EDM4eic .root file (default files/data/lambda_skim.root), or
- file_list: a text file of paths/URLs for the full sample.

## Steps
1. Confirm the uproot MCP server is connected: get_file_structure on the input.
2. Build the histogram via execute_kernel (one file) or submit_kernel_dataset
   (a file list), using files/code/lambda_kernel_mcp.py (KERNEL_CODE, BRANCHES).
   For a large sample, call estimate_dataset_cost first and cap the file count.
3. Save the returned histogram to output/lambda_hist.json.
4. Fit it:  python3 files/code/fit_lambda.py --in output/lambda_hist.json
5. Report mu, sigma, signal yield S, and chi2/ndf; show output/lambda_fit.png.

## Success criteria (check before reporting success)
- |mu - 1.115683 GeV| < 0.005 GeV.
- sigma in ~[0.001, 0.005] GeV (this is detector resolution, not natural width).
- chi2/ndf of order 1.
If any check fails, report the failure and the fit diagnostics, not a result.

## Provenance
List the tool calls and their parameters, and the dataset used (campaign and
file list), so the run can be reproduced.

## Bundled scripts
A self-contained copy of this skill would also include the two scripts it calls:
  - lambda_kernel_mcp.py  (from files/code/)
  - fit_lambda.py         (from files/code/)
