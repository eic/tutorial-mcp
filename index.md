---
site: sandpaper::sandpaper_site
---

In most analyses the limiting factor is not the physics but the software around it: locating data,
decoding a data model, getting branch names and units right, and iterating on fitting and plotting
code. This lesson shows how to delegate that overhead to an AI assistant **without giving up
rigour** — every step produces a quantity you can check, and the whole procedure is reproducible.

The worked example is a real measurement from the ePIC experiment: reconstructing the weak decay
**Λ⁰ → p π⁻** and extracting its yield from the proton–pion invariant-mass spectrum.

The lesson develops three ideas and applies them end to end:

* an **agentic assistant** — a language model placed in a loop where it can read files, run code,
  and condition on the results, rather than only returning text;
* the **Model Context Protocol (MCP)** — an open standard for exposing analysis tools to any
  assistant, so the workflow is portable; and
* **persistent instructions** (`AGENTS.md` and `SKILL.md`) — versioned context and procedures that
  make a run repeatable and auditable.

The treatment is tool-agnostic: the method is demonstrated with several free assistants, and the
components you assemble (MCP tool servers, a skill) work with any of them.

::::::::::::::::::::::::::::::::::::::::::::: callout

## What you will produce

A workflow in which an assistant opens a real ePIC reconstruction file, queries its schema through
a verifiable tool interface, builds the Λ⁰ invariant-mass spectrum, and fits it — driven by
natural-language requests, with results and provenance you can independently check.

:::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::: prereq

## Prerequisites

* Comfort at the command line (running commands, editing files).
* Working knowledge of Python or ROOT is useful; the assistant writes most of the code.
* Introductory particle-physics concepts (four-momentum, invariant mass, histograms, fitting).
* No prior experience with AI tooling is assumed, and the core episodes need no paid account or GPU.

See the [Setup](learners/setup.md) page for installation.

:::::::::::::::::::::::::::::::::::::::::::::

This lesson originated at an ePIC workshop on generative AI for physics. It complements the other
[EIC tutorials](https://eic.github.io/documentation/tutorials.html), which cover locating and
reading the data.
