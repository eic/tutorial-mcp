---
title: 'Instructor Notes'
---

## Scope and audience

This lesson is aimed at **graduate students and researchers** new to AI tooling. It assumes
command-line comfort and introductory particle-physics background (four-momentum, invariant mass,
histograms, fitting). It teaches a portable method — the agentic harness — applied to a real ePIC
measurement (Λ⁰ → p π⁻), and is deliberately **tool-agnostic**: learners pick one assistant
(Copilot, Claude Code, or opencode) and everything else works through MCP.

## What is built vs. outlined

* **Episodes 1–3 are the hands-on core** — the agentic harness, workspace setup + the physics, and
  the MCP tool server (run, register, inspect, histogram).
* **Episode 4** is a how-to on `AGENTS.md` and `SKILL.md`, with full example files shipped under
  `files/skills/`.
* **Episode 5** is a specification of the end-to-end run (single file, streaming vs. asynchronous
  scaling, signal extraction, audit checklist) for a second build pass.
* **Episode 6** is a catalogue of the EIC MCP servers and the corun-ai ecosystem.

## Before the workshop

* Make sure learners have **eic-shell** working and **opencode** installed with a free model
  connected (Setup page). Everything else runs inside eic-shell.
* No JLab account or data download is needed: the `rucio` server signs in automatically with the
  shared read-only `eicread` account, and the assistant reads files over `root://` in place.
* Have learners run `eic-mcp setup` ahead of time — the first build of the three servers takes a
  few minutes.

## Timing and pitfalls

* Total ≈ 2 h teaching + 1.5 h exercises (a half day). Episode 3 is the longest; budget time for
  `eic-mcp setup` (first build) and connecting opencode to a model.
* **Common snag:** the assistant stays in "one-shot" mode and only prints code. Have learners
  confirm **Agent/edit mode** in Episode 2's first-contact exercise.
* **Servers not connected:** if `/mcp` shows nothing, check `eic-mcp status` and that
  `opencode.jsonc` is in the directory where `opencode` was launched.
* **Statistics:** peak clarity scales with how many `root://` files the assistant processes — a
  few files show a modest excess; tens of files give a clean fit. Set expectations accordingly.

## Verifying your own setup

Start the servers (`eic-mcp up`), launch `opencode`, run `/mcp` to confirm the three servers, and
ask it to histogram a branch of a discovered `root://` file. The `extras/` examples reproduce the
same peak in uproot, RDataFrame, TTreeReader, and PODIO.

## Currency of the market table

Episode 2's tool table is a dated snapshot (mid-2026). Pricing and free tiers change often —
check current vendor docs before teaching, and update the table. The *MCP* portability message is
the stable part.
