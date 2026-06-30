---
title: "Persisting instructions: AGENTS.md and SKILL.md"
teaching: 30
exercises: 20
---

::::::::::::::::::::::::::::::::::::::::::::: questions

- How do I give an assistant durable project context instead of re-explaining it each session?
- What is the difference between AGENTS.md and a SKILL.md, and when do I use each?
- How do I make every tool — even ones that ignore AGENTS.md — read the same rules?
- What does a usable SKILL.md for the Λ⁰ measurement actually contain?

:::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::: objectives

- Write an AGENTS.md that supplies always-on project context to any assistant.
- Use bridge files so a single AGENTS.md drives Claude Code, Copilot, opencode, and others.
- Write a SKILL.md that an assistant loads on demand to run the Λ⁰ fit.
- Encode explicit success criteria and provenance into a procedure so its output is auditable.

:::::::::::::::::::::::::::::::::::::::::::::

## Two ways to make instructions persistent

In Episode 3 you drove the assistant by typing requests. That works, but it does not scale: you
re-explain the data model, the conventions, and the procedure every session, and nothing stops two
runs from diverging. Two file-based mechanisms fix this, and they are complementary.

* **`AGENTS.md`** — always-on **context**. The assistant reads it automatically at the start of a
  session and treats it as background knowledge about the project: environment, data model,
  conventions, and what "done" means.
* **`SKILL.md`** — an on-demand **procedure**. It sits in a named skill directory and is loaded
  only when a request matches its description. It encodes a specific, repeatable workflow.

```mermaid
flowchart TD
    R["your project"] --> AG["AGENTS.md<br/>whole file always in context"]:::always
    R --> SK["skills/lambda-fit/SKILL.md<br/>only its description is indexed"]:::ondemand
    AG --> M(["model context"]):::core
    SK -. "body loaded only when a<br/>request matches its description" .-> M
    classDef always fill:#e6f7ed,stroke:#2f9e44,stroke-width:1.5px,color:#0b3d1f;
    classDef ondemand fill:#fff4e0,stroke:#f08c00,stroke-width:1.5px,color:#5c3b00;
    classDef core fill:#e7efff,stroke:#4c6ef5,stroke-width:1.5px,color:#10204a;
```

Roughly: `AGENTS.md` answers "what is this project and how do we work here?"; a `SKILL.md` answers
"how do I carry out *this specific task*?".

## AGENTS.md — project context

`AGENTS.md` is a plain-Markdown file at the root of your project (subdirectories may have their own,
which override the root for files beneath them). It is an emerging cross-tool convention: Claude
Code, opencode, and others read it automatically, and where a tool uses a different name (for
example a `CLAUDE.md` or "custom instructions"), the content transfers unchanged.

Keep it short and factual — it is loaded into context on every turn, so wasted words cost tokens.
A useful `AGENTS.md` for this analysis:

```markdown
# AGENTS.md — Lambda analysis project

## What this project does
Reconstruct Lambda0 -> p pi- in ePIC EDM4eic data and fit the invariant-mass
peak near 1.115683 GeV.

## Environment
- Everything runs inside eic-shell; the MCP servers are started with `eic-mcp up`.
- Data lives on the grid: find a DIS dataset with the `rucio` tools and read its
  root:// files in place with `uproot` — no download.

## Tools
- Use the `rucio` MCP server (list_dids, list_files, list_file_replicas) to locate
  a dataset and resolve its root:// URLs.
- Use the `xrootd` MCP server (check_file_exists, get_file_info) to verify a file.
- Use the `uproot` MCP server (get_file_structure, get_tree_info, histogram_branch,
  execute_kernel, execute_kernel_dataset) for all ROOT file access.
- Do NOT write bespoke file I/O; the servers already handle it.

## Data model
- Tree: events.  Collection: ReconstructedChargedParticles.
- Members: .PDG, .momentum.x, .momentum.y, .momentum.z   (momenta in GeV).
- PDG codes: proton 2212, pi- -211, antiproton -2212, pi+ 211.

## Physics constants (PDG)
- m(proton) = 0.9382720813 GeV, m(pi) = 0.13957061 GeV, m(Lambda) = 1.115683 GeV.

## Conventions
- Invariant mass over [1.05, 1.25] GeV, 200 bins.
- Fit a Gaussian + 2nd-order polynomial over [1.08, 1.16] GeV.
- Write results as JSON; save plots under output/.

## Definition of done
- Fitted peak within a few MeV of 1.115683 GeV and chi2/ndf of order 1.
- Always run the fit and check these before reporting a result.
```

Notice what it encodes: the schema (so the model never guesses branch names), the tool policy (use
the server, not hand-written I/O), the analysis conventions, and an explicit definition of done.

::::::::::::::::::::::::::::::::::::::::::::: callout

## Two rules for an AGENTS.md that helps rather than hurts

* **Keep it short.** It is loaded on every turn (see *context economy*, below), so a long file
  both costs tokens and dilutes the model's attention. Write only what the model cannot infer from
  the code itself.
* **Describe concepts, not file paths.** "The reconstructed tracks are in the
  `ReconstructedChargedParticles` collection" ages well; "the kernel is in `src/old/lambda_v2.py`"
  does not — paths move, and the model will then search confidently in the wrong place. State
  *what* things are and *how* you work, and let the tools locate the files.

:::::::::::::::::::::::::::::::::::::::::::::

## One source of truth: bridge files

There is a catch: not every tool reads `AGENTS.md`. Most modern ones do — opencode, Cursor, Codex,
Gemini CLI, Zed — but some look for their own filename and silently ignore it. Claude Code, for
instance, reads `CLAUDE.md`. If your project has only an `AGENTS.md`, such a tool runs with no
project context and gives you no warning.

The wrong fix is to copy your rules into a second file; two copies drift apart within a week. The
right fix follows one principle — **keep the standard in the centre and let each tool read from
it** — so the tool-specific file becomes a one-line *bridge* that points at `AGENTS.md` instead of
duplicating it.

`CLAUDE.md` (the `@` pulls the referenced file into Claude Code's context):

```markdown
@AGENTS.md
```

`.github/copilot-instructions.md` (GitHub Copilot):

```markdown
Follow the project rules in AGENTS.md.
```

Now every assistant a collaborator might run reads the same source of truth, maintained in one
place. Ready-made bridges are provided to copy: [`CLAUDE.md`](https://github.com/aprozo/tutorial-mcp/blob/main/files/skills/CLAUDE.md) and
[`copilot-instructions.md`](https://github.com/aprozo/tutorial-mcp/blob/main/files/skills/copilot-instructions.md).

## SKILL.md — a named procedure

A **skill** is a directory containing a `SKILL.md` that describes a repeatable procedure:

```bash
skills/
  lambda-fit/
    SKILL.md              specification: applicability, inputs, steps, success criteria
```

The procedure itself is carried out by driving the MCP tools (it builds the histogram with the
uproot kernel and fits the Gaussian + polynomial in the same sandbox), so the skill needs no
bundled scripts of its own.

The YAML frontmatter carries a `name` and a `description`. The `description` is load-bearing: the
client compares the user's request against it to decide whether to pull the skill into context, so
it should name the task explicitly. Crucially, **only the name and description stay in context at
all times** — the body of `SKILL.md` is read in *only when* the description matches the request. A
working `SKILL.md` for the Λ⁰ fit:

```markdown
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
1. Confirm the uproot MCP server is connected: get_file_structure on the input.
2. Build the proton-pion invariant-mass histogram with execute_kernel (one file)
   or execute_kernel_dataset (many files), tree_name 'events' and the
   ReconstructedChargedParticles momentum/PDG branches. For a large sample, cap
   the file count first.
3. Fit the histogram with a second execute_kernel call (Gaussian + 2nd-order
   polynomial over [1.08, 1.16] GeV; NumPy/awkward only, no imports).
4. Report mu, sigma, signal yield S, and chi2/ndf.

## Success criteria (check before reporting success)
- |mu - 1.115683 GeV| < 0.005 GeV.
- sigma in ~[0.001, 0.005] GeV (this is detector resolution, not natural width).
- chi2/ndf of order 1.
If any check fails, report the failure and the fit diagnostics, not a result.

## Provenance
List the tool calls and their parameters, and the dataset used (campaign and
file list), so the run can be reproduced.
```

::::::::::::::::::::::::::::::::::::::::::::: callout

## How clients load a skill

Claude Code reads skills from a `skills/` (or `.claude/skills/`) directory and loads one when a
request matches its `description`. Clients without a native skill mechanism reach the same end
by referencing the procedure from `AGENTS.md` or pasting it as instructions. The *form* — a
versioned, self-contained specification that drives the MCP tools — is portable even where the
loading mechanism is not.

:::::::::::::::::::::::::::::::::::::::::::::

Both example files are provided to copy: [`files/skills/AGENTS.md`](https://github.com/aprozo/tutorial-mcp/blob/main/files/skills/AGENTS.md) and
[`files/skills/lambda-fit/SKILL.md`](https://github.com/aprozo/tutorial-mcp/blob/main/files/skills/lambda-fit/SKILL.md).

## When to use which

| Question | Mechanism |
| --- | --- |
| "What is this project, and how do we work here?" | `AGENTS.md` (always loaded) |
| "How do I perform *this* specific task?" | a `SKILL.md` (loaded on demand) |
| "What must every result satisfy?" | success criteria — in both, but enforced by the skill |

The two work together: `AGENTS.md` sets standing context and conventions, and the skill executes a
procedure within that context.

::::::::::::::::::::::::::::::::::::::::::::: callout

## Why this is efficient: context economy

The context window is finite, and everything in it costs tokens on every turn. These two
mechanisms spend that budget very differently — which is the whole point of using them.

* **`AGENTS.md` is loaded in full, every turn.** It is *always-on* context, so it must stay short
  and high-signal: a page of conventions, not a manual. Every line you add is paid for on every
  request.
* **A skill loads progressively.** Only its `name` and one-line `description` are kept in context;
  the model reads the full `SKILL.md` body *only when* a request matches the description. So you can
  install dozens of skills — each a detailed procedure — and none of them occupies the context
  window until it is actually needed.

In short: put the small, always-relevant facts in `AGENTS.md`; put detailed, occasional procedures
in skills, where they stay out of the way until called. This *progressive disclosure* is what lets
the workflow scale without exhausting the context.

:::::::::::::::::::::::::::::::::::::::::::::

## Why the success criteria matter

A procedure that runs without human keystrokes still has to produce a defensible number. Writing
explicit acceptance tests into the skill — peak position, width, χ²/ndf — converts "the assistant
said it worked" into "the result passed stated, checkable conditions." Recording the tool calls and
the dataset makes the run reproducible and auditable. These are the same standards you would apply
to a result you computed by hand.

## Your project layout

Putting the pieces together, a project that behaves the same under any assistant looks like this:

```bash
lambda-analysis/
├── AGENTS.md                        # source of truth: context + conventions (write this)
├── CLAUDE.md                        # one line: @AGENTS.md  (bridge for Claude Code)
├── .github/
│   └── copilot-instructions.md      # points to AGENTS.md   (bridge for Copilot)
├── opencode.jsonc                   # MCP server connections (Episode 3)
└── skills/
    └── lambda-fit/
        └── SKILL.md                 # the procedure, loaded on demand
```

::::::::::::::::::::::::::::::::::::::::::::: callout

## The golden rule

Write each instruction once, in the shared, open format — `AGENTS.md` for context, `SKILL.md` for
procedures, `opencode.jsonc` for tool connections — then point any tool-specific file at it. Never keep
duplicate rule files. *Standards in the centre, tools at the edges:* this is what keeps the
workflow consistent as assistants come and go, and what lets a whole collaboration share one
vetted setup.

:::::::::::::::::::::::::::::::::::::::::::::

## Exercises

* Write a minimal `SKILL.md` for "summarise the contents of any EDM4eic file" that calls
  `get_file_structure` and `get_tree_info`.
* Extend the provenance section of `lambda-fit` so it also records the number of input files and the
  total number of candidate pairs.

The [next episode](05-end-to-end-agents.md) runs this skill end to end and scales it from one file
to the full sample.

::::::::::::::::::::::::::::::::::::::::::::: keypoints

- AGENTS.md is always-loaded project context; a SKILL.md is a named procedure loaded on demand.
- Keep one source of truth (AGENTS.md) and point tool-specific files (CLAUDE.md, copilot-instructions.md) at it — never maintain duplicates.
- A skill's frontmatter `description` is what the model matches against to decide when to load it.
- Encode inputs, steps, success criteria, and provenance so a result can be reproduced and audited.

:::::::::::::::::::::::::::::::::::::::::::::
