---
title: 'Instructor Notes'
---

## Scope and audience

This lesson is aimed at **graduate students and researchers** new to AI tooling. It assumes
command-line comfort and introductory particle-physics background (four-momentum, invariant mass,
histograms, fitting). It teaches a portable method — the agentic harness — applied to a real ePIC
measurement (Λ⁰ → p π⁻), and is deliberately **tool-agnostic**: learners pick one assistant
(opencode, Copilot, or Cursor) and everything else works through MCP.

## What is built vs. outlined

* **Episodes 1–3 are the hands-on core** — the agentic harness, the physics, and
  the MCP tool server (run, register, inspect, histogram).
* **Episode 4** is a how-to on `AGENTS.md` and `SKILL.md`, with full example files shipped under
  `files/skills/`.
* **Episode 5** is the end-to-end run (single file → full sample via `execute_kernel_dataset`,
  signal extraction, audit checklist), with a per-client setup section.
* **Episode 6** is a catalogue of the EIC MCP servers and the corun-ai ecosystem.

## Before the workshop

* Make sure learners have **eic-shell** working and **opencode** installed with a free model
  connected (Setup page). Everything else runs inside eic-shell.
* No JLab account or data download is needed: the `rucio` server signs in automatically with the
  shared read-only `eicread` account, and the assistant reads files over `root://` in place.
* Have learners run `eic-mcp up` once ahead of time — the first run bootstraps the three servers
  automatically, which takes a few minutes; every later start is seconds.

## Timing and pitfalls

* Total ≈ 2 h teaching + 1.5 h exercises (a half day). Episode 3 is the longest; budget time for
  the first `eic-mcp up` (one-time bootstrap) and connecting opencode to a model.
* **Common snag:** the assistant stays in "one-shot" mode and only prints code. Have learners
  confirm **Agent/edit mode** in the Setup page's "Check it works" exercise.
* **Servers not connected:** if `/mcp` shows nothing, check `eic-mcp status` and that
  `opencode.jsonc` (generate it with `eic-mcp config opencode`) is in the directory where
  `opencode` was launched.
* **Statistics:** peak clarity scales with how many `root://` files the assistant processes — a
  few files show a modest excess; tens of files give a clean fit. Set expectations accordingly.

## Verifying your own setup

Start the servers (`eic-mcp up`), launch `opencode`, run `/mcp` to confirm the three servers, and
ask it to histogram a branch of a discovered `root://` file. The `extras/` examples reproduce the
same peak in uproot, RDataFrame, TTreeReader, and PODIO.

## Currency of the market table

The Setup page's assistant table dates quickly. Pricing and free tiers change often —
check current vendor docs before teaching, and update the table. The *MCP* portability message is
the stable part.
