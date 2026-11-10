# AGENTS.md — Lambda analysis in ePIC data

## Data access
- Find datasets with the `rucio` MCP tools; keep `limit` at 50 or less.
- A file's URL is root://epicxrd1.sdcc.bnl.gov:1095//eic/EPIC followed by its
  rucio name (/RECO/...). The `xrootd` tools take the path /eic/EPIC/RECO/...
- Read files only through the `uproot` MCP tools. No downloads, no local
  ROOT/uproot, no software installs.
- Never call get_tree_info on an EDM4eic file (it returns 1.5 MB). Check
  branches with validate_dataset_schema.

## Data model
- Tree `events`, collection ReconstructedChargedParticles:
  .PDG, .momentum.x, .momentum.y, .momentum.z (GeV).
- m(p) = 0.9382720813, m(pi) = 0.13957061, m(Lambda) = 1.115683 GeV.

## Kernels (uproot sandbox)
- np and ak are predefined. No `import`, no tuple unpacking in for-loops,
  np.sum(x) not x.sum().
- Test a kernel on one file with execute_kernel before a dataset call: the
  dataset tools do not show the error.

## When a tool fails
- A timeout means the server is busy. Wait, retry once, then stop and report.

## Definition of done
- Every number comes from a tool call in this session and is reported with the
  dataset DID and the file list.
