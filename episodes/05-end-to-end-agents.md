---
title: "An end-to-end, reproducible Λ⁰ analysis"
teaching: 25
exercises: 30
---

<style>
/* Mermaid: force diagram label text dark so it stays readable on the
   light node fills in BOTH light and dark mode. The Carpentries dark
   theme sets `p`/`li` color and darkens `pre` backgrounds, which would
   otherwise turn mermaid's label text light (invisible on light nodes)
   and the diagram surface dark. We override both, with !important to
   beat the theme rules and mermaid's own inline styles. */
.mermaid { background: transparent !important; }
.mermaid .nodeLabel, .mermaid .edgeLabel, .mermaid .label,
.mermaid .cluster-label, .mermaid text, .mermaid tspan,
.mermaid span, .mermaid p, .mermaid foreignObject div {
  color: #10204a !important;
  fill: #10204a !important;
}
.mermaid .edgeLabel, .mermaid .edgeLabel p, .mermaid .edgeLabel rect {
  background-color: #e2e8f0 !important;
}
/* AI prompts: paste-into-your-assistant blocks. Styled like a normal
   code block (same neutral pre background/border as python etc.), with
   just a small "AI Prompt" tag in the corner. */
pre.ai-prompt, div.sourceCode.ai-prompt {
  border-top: 10px solid #7c3aed;
}
pre.ai-prompt::before, div.sourceCode.ai-prompt::before {
  content: "AI Prompt";
  display: block;
  margin-bottom: .5rem;
  font-weight: 600;
  font-size: .78em;
  letter-spacing: .03em;
  text-transform: uppercase;
  color: #7c3aed;
}
</style>

::::::::::::::::::::::::::::::::::::::::::::: questions

- How do assistant + server + skill compose into one analysis?
- How does the kernel scale from one file to the full sample?
- How is the yield extracted and made reproducible?

:::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::: objectives

- Run the full chain (resolve → histogram → fit → report) from one request.
- Scale the kernel from one file to the full sample.
- Extract the Λ⁰ yield and apply an audit checklist.

:::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::: callout

## Status of this episode

Specification of the end-to-end run, building on Episodes 1–3. Fixes the pipeline, scaling options, and acceptance criteria; the per-client walkthrough is to be added.

:::::::::::::::::::::::::::::::::::::::::::::

## The composed pipeline

The previous episodes combine into one procedure run from a single request: the lambda-fit skill (Episode 4) supplies the steps, the uproot tool server (Episode 3) supplies verifiable data access, and the agentic loop (Episode 1) carries it out and checks the result.

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'fontSize':'15px','lineColor':'#94a3b8','edgeLabelBackground':'#e2e8f0','clusterBkg':'#1f293720','clusterBorder':'#94a3b8','titleColor':'#94a3b8'}}}%%
flowchart LR
    accTitle: End-to-end agent run
    A["resolve input<br/>root:// file or file list"]:::data --> B["build m(p,π) histogram<br/>uproot MCP · execute_kernel"]:::tool
    B --> C["fit Gaussian + poly-2<br/>opencode prompt"]:::tool
    C --> D["report μ, σ, S, χ²/ndf<br/>+ plot + provenance"]:::out
    classDef data fill:#fff4e0,stroke:#f08c00,stroke-width:1.5px,color:#5c3b00;
    classDef tool fill:#e6f7ed,stroke:#2f9e44,stroke-width:1.5px,color:#0b3d1f;
    classDef out fill:#f3e8ff,stroke:#7048e8,stroke-width:1.5px,color:#2e1065;
```

## One file, end to end

With the three servers running and the lambda-fit skill available, one request runs the whole chain. Point it at one of the dataset's `root://` files. The assistant uses `rucio` tools to find a DIS dataset and `list_file_replicas` for the URLs, `xrootd` to confirm the file is there, then reads it in place:

```{.ai-prompt}
Using the lambda-fit skill, measure the Lambda0 peak in this file:
root://dtn-eic.jlab.org//... (one of the dataset's root:// files).
Build the proton-pion invariant-mass histogram with the uproot MCP server (tree 'events'),
fit it, and report mu, sigma, the yield, and chi2/ndf, with the plot.
```

The assistant calls `execute_kernel` (tree `events`, proton/pion branches) to build the histogram, then a follow-up prompt fits it with a Gaussian-plus-polynomial model. On a single file the peak sits at $\mu \approx 1.1157$ GeV; its significance is limited by the small event count, addressed next.

::::::::::::::::::::::::::::::::::::::::::::: callout

## Smaller models take shortcuts — verify the result, not the route

A capable model uses `execute_kernel` as instructed. A cheaper model may reach for `execute_kernel_dataset` on a single file, or write its own NumPy in the kernel — both produce the same histogram. The audit checklist below judges the *result* (peak position, width, $\chi^2/\text{ndf}$, recorded inputs), not which tool produced it.

:::::::::::::::::::::::::::::::::::::::::::::

## Scaling to the full sample

The same kernel applies unchanged to many files; only the tool differs. `execute_kernel` runs one file; `execute_kernel_dataset` dispatches the identical kernel across a whole file list and returns one merged histogram, so peak memory is independent of dataset size. Enumerate the files with `get_dataset_file_list`, then fan the kernel out:

```{.ai-prompt}
Using the lambda-fit skill, run the same proton-pion mass kernel across the dataset's files
with execute_kernel_dataset (tree 'events'), merge the histograms, then fit the result and
report mu, sigma, the yield, and chi2/ndf for both Lambda and anti-Lambda, with the plot.
```

The kernel sandbox is NumPy/awkward only (no imports, no I/O), so the assistant returns the merged histogram and runs a follow-up fit prompt. Over ~100 files this gives the full-statistics spectrum below: a clear Λ⁰ (and Λ̄) peak over the combinatorial background.

![Fitted Λ⁰ and Λ̄ invariant-mass spectra (100-file reference)](fig/lambda_fit.svg){alt='Proton–pion invariant-mass spectrum with Gaussian-plus-polynomial fits showing clear Lambda and anti-Lambda peaks near 1.1157 GeV'}

```output
Lambda      -> p pi-:   mu = 1116.30 +/- 0.32 MeV   sigma = 2.72 +/- 0.33 MeV   S = 123   chi2/ndf = 1.16
anti-Lambda -> pbar pi+: mu = 1116.06 +/- 0.33 MeV   sigma = 3.35 +/- 0.34 MeV   S = 160   chi2/ndf = 1.05
```

The fitted $\mu$ sits ~0.6 MeV above the PDG value (1.115683 GeV), a calibration-level offset typical of reconstructed momenta; $\sigma$ is the detector mass resolution, not the (negligible) Λ⁰ natural width.

## Extracting the yield

The fit model is a Gaussian signal on a second-order polynomial background over $[1.08, 1.16]$ GeV:

$$
f(m) = A \exp\!\left[ -\tfrac{1}{2} (m - \mu)^2 / \sigma^2 \right] + \left( c_0 + c_1 (m - m_\Lambda) + c_2 (m - m_\Lambda)^2 \right)
$$

The polynomial absorbs the combinatorial background (Episode 2); the integrated signal is $S = A\sqrt{2\pi}\,\sigma / (\text{bin width})$. Report $S$ with its uncertainty alongside $\mu$, $\sigma$, and $\chi^2/\text{ndf}$ — a bare bin count conflates signal with background.

## Reproducibility and audit

Before treating an automated result as final, confirm it meets the skill's criteria:

::::::::::::::::::::::::::::::::::::::::::::: callout

## Audit checklist

* **Signal.** $\mu$ within a few MeV of 1.115683 GeV; $\sigma$ consistent with detector resolution; $\chi^2/\text{ndf}$ of order unity; $S$ reported with an uncertainty.
* **Inputs pinned.** Dataset (campaign and file list), particle masses, mass window, binning, and fit range all fixed and recorded.
* **Provenance.** Tool calls and their arguments logged, so the run can be reconstructed.
* **Cost bounded.** File count capped during development before scaling up with `execute_kernel_dataset`.
* **Oversight.** A human inspected the fit before the result was reported.

:::::::::::::::::::::::::::::::::::::::::::::

## Exercises (specification)

* Run the single-file chain through your assistant and report $\mu$, $\sigma$, $S$, and $\chi^2/\text{ndf}$.
* Process 10 files with `execute_kernel_dataset` and compare the fitted parameters to the ~100-file result; comment on the change in statistical uncertainty.
* Complete the audit checklist for your run, attaching the recorded tool calls as provenance.

You now have the complete workflow: a free assistant, a portable tool server, a versioned skill, and a reproducible Λ⁰ measurement whose every step you can verify. The [final episode](06-eic-mcp-servers.md) catalogues the other MCP servers the EIC provides.

::::::::::::::::::::::::::::::::::::::::::::: keypoints

- The full analysis composes Episodes 2–4: an assistant, the uproot MCP tools, and the lambda-fit skill.
- The same kernel scales from `execute_kernel` (one root:// file) to `execute_kernel_dataset` (the full sample), merging into one histogram.
- The yield comes from a Gaussian-plus-polynomial fit; report $\mu$, $\sigma$, $S$, and $\chi^2/\text{ndf}$, not a bare count.
- Pinning inputs and recording tool calls make the measurement reproducible and auditable.

:::::::::::::::::::::::::::::::::::::::::::::
