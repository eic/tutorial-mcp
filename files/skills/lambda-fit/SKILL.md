---
name: lambda-fit
description: >
  Reconstruct and fit the Lambda0 -> p pi- invariant-mass peak in ePIC EDM4eic
  data. Use when asked to measure the Lambda yield, mass, or width, or to
  reproduce the Lambda peak from a .root file or a file list.
---

# Lambda invariant-mass fit

## Steps
1. Check the input files with validate_dataset_schema.
2. Histogram m(p pi-) and m(pbar pi+) over [1.08, 1.16] GeV in 80 bins, and
   return the counts and their sum. One file: execute_kernel. Many files:
   execute_kernel_dataset with reduce_code, at most 10 files per call.
3. Fit each histogram in one more execute_kernel call: Gaussian + 2nd-order
   polynomial. Scan mu and sigma on a grid and solve the other four parameters
   by weighted linear least squares.
4. Report mu, sigma, the yield S = A sqrt(2 pi) sigma / bin width, and
   chi2/ndf, with uncertainties.

## Success criteria (check before reporting success)
- The entries in the fitted histogram equal the sum returned in step 2. If
  not, counts were lost in copying: redo the fit.
- At least 50 entries. With fewer, report insufficient statistics and stop.
- |mu - 1.115683 GeV| < 0.005 GeV.
- sigma in [0.001, 0.005] GeV (detector resolution).
- chi2/ndf between 0.5 and 1.5.
If any check fails, report the failure and the fit numbers, not a result.

## Provenance
List the dataset DID, the files used, and the tool calls with their arguments.
