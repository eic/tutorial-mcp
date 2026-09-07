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
* **Episode 6** is a catalog of the EIC MCP servers and the corun-ai ecosystem.

## Before the workshop

* Make sure learners have **eic-shell** working and **opencode** installed with a free model
  connected (Setup page). Only the tool servers run inside eic-shell.
* No JLab account or data download is needed: the `rucio` server signs in automatically with the
  shared read-only `eicread` account, and the assistant reads files over `root://` in place.
* Have learners run `eic-mcp up` once ahead of time — it confirms their image is recent enough to
  ship the servers (`./eic-shell --upgrade` if not); starting takes seconds.
* The Episode 3 exercise pins a campaign (currently `26.04.1`). Campaigns retire — run the
  campaign-listing prompt from Episode 3 beforehand and bump the version in the exercise if
  production has moved on.

## Timing and pitfalls

* Total ≈ 2 h 45 m teaching + 1.5 h exercises (a full day with breaks). Episode 3 is the longest; budget time for
  upgrading stale eic-shell images (`./eic-shell --upgrade` downloads gigabytes) and connecting
  opencode to a model.
* **Common snag:** the assistant stays in "one-shot" mode and only prints code. Have learners
  confirm **Agent/edit mode** in the Setup page's "Check it works" exercise.
* **Servers not connected:** if `/mcp` shows nothing, check `eic-mcp status` and that
  `opencode.jsonc` (generate it with `eic-mcp config opencode`) is in the directory where
  `opencode` was launched.
* **Statistics:** peak clarity scales with how many `root://` files the assistant processes — a
  few files show a modest excess; tens of files give a clean fit. Set expectations accordingly.
* **macOS learners:** the classic missed Setup step is port publishing — `/mcp` finds nothing on
  the Mac when `./eic-shell` was started without `DOCKER_OPTIONS="$(./eic-shell -- eic-mcp docker-args)"`.
* **Free-tier throttling:** at busy hours the free hosted models can take minutes per agent turn
  (the MCP tool context makes each request large). If the session drags, switch the class to
  another free model in the opencode picker, or keep one paid key as backup.
* **Store outage:** if rucio queries work but all xrootd/uproot file access times out, the
  XRootD store is likely down — verify with
  `xrdfs root://epicxrd1.sdcc.bnl.gov:1095 ls /eic/EPIC/RECO` before the session, and have a
  fallback ready (Episodes 1–2 material, or a locally cached file). BNL disk serves campaigns
  25.12.0 onward (the `eic-mcp` default); the JLab store (`root://dtn-eic.jlab.org`,
  `/volatile/eic/EPIC`) has campaigns up to 25.10.x.

## Verifying your own setup

Start the servers (`eic-mcp up`), launch `opencode`, run `/mcp` to confirm the three servers, and
ask it to histogram a branch of a discovered `root://` file. The `extras/` examples reproduce the
same peak in uproot, RDataFrame, TTreeReader, and PODIO.

## Currency of the market table

The Setup page's assistant table dates quickly. Pricing and free tiers change often —
check current vendor docs before teaching, and update the table. The *MCP* portability message is
the stable part.
