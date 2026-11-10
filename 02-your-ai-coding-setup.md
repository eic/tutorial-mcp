---
title: "The measurement: Λ⁰ → p π⁻"
teaching: 5
exercises: 0
---


::::::::::::::::::::::::::::::::::::::::::::: questions

- What is the p π⁻ invariant-mass observable, and its peak and background?
- Which EDM4eic collections and units does it need?

:::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::: objectives

- Write m(p, π) in terms of the four branches and the PDG masses.
- State the expected peak position, width scale, and background shape before looking at data.

:::::::::::::::::::::::::::::::::::::::::::::

## The observable

The Λ⁰ decays weakly to p π⁻ (branching fraction ≈ 63.9%, cτ ≈ 7.9 cm). It is neutral, so we
reconstruct it from its charged daughters. Assign the proton mass to one track and the pion mass to
the other, using the reconstructed particle ID:

$$E_i = \sqrt{|\vec{p}_i|^2 + m_i^2}, \qquad
m(p, \pi) = \sqrt{(E_1 + E_2)^2 - |\vec{p}_1 + \vec{p}_2|^2}$$

True Λ⁰ decays accumulate in a **peak at 1.115683 GeV**. Its width, a few MeV, is the detector
resolution; the natural width is negligible. Random proton–pion pairs form a smooth
**combinatorial background** under the peak, so the yield comes from a fit: a Gaussian on a
second-order polynomial ([Episode 5](05-end-to-end-agents.md)). The charge-conjugate mode
Λ̄ → p̄ π⁺ is reconstructed the same way.

| Quantity | Value |
| --- | --- |
| m(Λ⁰) | 1.115683 GeV |
| m(p) | 0.9382720813 GeV |
| m(π±) | 0.13957061 GeV |

## The data model

ePIC reconstruction output uses **EDM4eic**. A file contains an `events` tree; each entry is one
event, each branch a **collection**. We need one collection and four members:

```
events  (tree; one entry per event)
    ReconstructedChargedParticles.PDG          reconstructed particle-ID hypothesis
    ReconstructedChargedParticles.momentum.x   p_x  [GeV]
    ReconstructedChargedParticles.momentum.y   p_y  [GeV]
    ReconstructedChargedParticles.momentum.z   p_z  [GeV]
```

Select protons (`2212`) and π⁻ (`-211`) for Λ⁰, antiprotons (`-2212`) and π⁺ (`211`) for Λ̄.

You do not download a file. In [Episode 3](03-mcp-servers.md) the assistant uses the
[**rucio**](https://github.com/eic/rucio-eic-mcp-server) tools to find a DIS dataset and
[**xrootd**](https://github.com/eic/xrootd-mcp-server) to verify its files, then reads one of the
dataset's `root://` URLs (e.g. `root://epicxrd1.sdcc.bnl.gov:1095//...`) **in place** with the
[**uproot**](https://github.com/eic/uproot-mcp-server) tools. It reads these branches without you
writing any I/O code.

::::::::::::::::::::::::::::::::::::::::::::: keypoints

- The Λ⁰ shows up as a peak at 1.1157 GeV in the proton–pion invariant mass.
- The peak width comes from detector resolution.

:::::::::::::::::::::::::::::::::::::::::::::
