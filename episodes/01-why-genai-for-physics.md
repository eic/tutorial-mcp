---
title: "Generative AI as an agentic research tool"
teaching: 40
exercises: 10
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

- How does an agentic, tool-using assistant differ from a conversational language model?
- What are the components of an LLM "harness", and why does each one matter for analysis work?
- How do modern assistants extend that core — MCP, subagents, LSP, hooks, monitors, plugins?
- How do we obtain trustworthy, reproducible results from a stochastic model?
- Why build the workflow on an open protocol rather than a single product?

:::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::: objectives

- Distinguish a one-shot chat completion from an agentic loop that observes and acts.
- Identify the four components of a harness: model, context, tools, and the control loop.
- Outline how the harness is extended: MCP tools, subagents, LSP, hooks, monitors, and plugins.
- Explain why verification against ground truth, not the model's confidence, establishes correctness.
- Justify an interoperability standard (MCP) as the basis for a portable, reproducible workflow.

:::::::::::::::::::::::::::::::::::::::::::::

## The bottleneck is rarely the physics

In a typical analysis the physics is modest: select a final state, build an observable, fit a
signal. Most effort goes into the software around it — locating datasets, decoding a data model,
getting branch names and units right, iterating on plotting and fitting code. LLMs compress this
overhead well, but only if they produce *checkable* results. Later episodes apply this to the decay
$\Lambda^0 \to p\,\pi^-$.

## Two modes of use

A **chat completion** is a single forward pass: prompt in, text out, exchange ends. If that text is
code, *you* execute it, inspect the error, and feed it back by hand. The model never observes your
data or the result of running anything.

An **agentic loop** wraps the same model in a control structure that lets it *act*: the model
proposes an action, an external **tool** carries it out, the result is appended to the context, and
the model is invoked again — until a stopping condition is met. In the loop the model is conditioned
on the actual state of your files and real computation output, not on its prior alone.

::::::::::::::::::::::::::::::::::::::::::::: callout

## Scope

Here, "generative AI" means an LLM-based coding assistant in this agentic mode — not machine
learning for reconstruction or particle identification. The object of study is the
*analysis-authoring* workflow.

:::::::::::::::::::::::::::::::::::::::::::::

## Anatomy of a harness

A model plus the machinery that makes it useful is a **harness**, with four components.

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'fontSize':'15px','lineColor':'#94a3b8','edgeLabelBackground':'#e2e8f0','clusterBkg':'#1f293720','clusterBorder':'#94a3b8','titleColor':'#94a3b8'}}}%%
flowchart TD
    U["Task specification"]:::user --> M
    C["Context window<br/>files · history · instructions"]:::core --> M["Model<br/>LLM: reasoning + generation"]:::core
    M -->|"proposes a typed tool call"| T["Tools<br/>read/write files · run code · query a server"]:::tool
    T -->|"observation appended to context"| C
    M -->|"stopping condition met"| R["Result + provenance"]:::out
    classDef core fill:#e7efff,stroke:#4c6ef5,stroke-width:1.5px,color:#10204a;
    classDef tool fill:#e6f7ed,stroke:#2f9e44,stroke-width:1.5px,color:#0b3d1f;
    classDef out fill:#f3e8ff,stroke:#7048e8,stroke-width:1.5px,color:#2e1065;
    classDef user fill:#f1f3f5,stroke:#868e96,stroke-width:1.5px,color:#212529;
```

* **Model** — reasoning and code generation. *Interchangeable*: provider and model are an
  implementation choice, not part of the method.
* **Context** — everything the model attends to in a step: system instructions, files, prior turns,
  tool outputs. Bounded by the *context window* (in tokens), so what is included, and when, is
  deliberate.
* **Tools** — operations the model may invoke, each with a typed interface (name, arguments, return
  schema). The only channel through which the model affects the outside world.
* **Control loop** — the policy that alternates *propose → execute → observe* until done. This
  distinguishes an agent from a chatbot.

::::::::::::::::::::::::::::::::::::::::::::: callout

## Why the loop is essential, not cosmetic

Feeding tool results back lets the assistant correct course against ground truth: read the actual
branch names rather than guessing, run a fit and read back its $\chi^2/\mathrm{ndf}$, refit if the peak is
misplaced. A single completion cannot, because it never observes a consequence of its actions.

:::::::::::::::::::::::::::::::::::::::::::::

## Extending the harness: the modern toolkit

Production assistants keep that small core and surround it with standard extension points. The
vocabulary recurs in every modern assistant's documentation.

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'fontSize':'15px','lineColor':'#94a3b8','edgeLabelBackground':'#e2e8f0','clusterBkg':'#1f293720','clusterBorder':'#94a3b8','titleColor':'#94a3b8'}}}%%
flowchart TB
    MCP["MCP servers<br/>external tools & data"]:::tool --> H
    SUB["subagents<br/>specialised, isolated context"]:::tool --> H
    LSP["LSP<br/>code intelligence"]:::tool --> H
    HOOKS["hooks<br/>lifecycle automation"]:::tool --> H
    MON["monitors<br/>watch & react"]:::tool --> H
    H(["harness core<br/>model + context + tools + loop"]):::core
    H -. "packaged & shared by" .-> PLUG["plugins<br/>bundle & share all of the above"]:::pkg
    classDef core fill:#e7efff,stroke:#4c6ef5,stroke-width:1.5px,color:#10204a;
    classDef tool fill:#e6f7ed,stroke:#2f9e44,stroke-width:1.5px,color:#0b3d1f;
    classDef pkg fill:#fff4e0,stroke:#f08c00,stroke-width:1.5px,color:#5c3b00;
```

* **MCP servers** — the *tools* layer, standardised. A server exposes tools, data, and prompts over
  the Model Context Protocol so one implementation works in any client. This is how we give the
  assistant physics capabilities ([Episode 3](03-mcp-servers.md)).
* **Subagents (agents)** — a separate assistant instance with its own context window, tools, and
  instructions, spawned for a sub-task. They isolate context and enable divide-and-conquer.
* **Skills** — packaged, versioned *procedures* (a `SKILL.md` plus scripts) loaded on demand when a
  request matches ([Episode 4](04-skills.md)). A tool is a capability; a skill is a recipe.
* **LSP (Language Server Protocol)** — the language servers behind editor autocomplete, giving real
  code intelligence: go-to-definition, references, types, and *compiler diagnostics*.
* **Hooks** — user scripts triggered on lifecycle events (before/after a tool call, on prompt
  submit, on session stop). They enforce policy deterministically — format after an edit, block a
  dangerous command, record a provenance log.
* **Monitors** — watch long-running background state (a build, a job queue, files) and react,
  notifying you or re-invoking the assistant when something finishes. They close the loop around work
  that outlives a single turn.
* **Plugins** — the *packaging* layer. A plugin bundles commands, subagents, skills, hooks, and MCP
  servers into one installable, versioned unit, so a collaboration shares a whole capability set at
  once.

| Component | What it adds to the core loop | In this tutorial |
| --- | --- | --- |
| MCP servers | external tools & data, client-agnostic | Episodes 3 & 5 (the uproot/xrootd servers) |
| Subagents | isolated, specialised helpers | discussed in Episode 5 |
| Skills | reusable, versioned procedures | Episode 4 (`SKILL.md`) |
| LSP | code intelligence & diagnostics | background (your editor) |
| Hooks | deterministic lifecycle automation | mentioned as best practice |
| Monitors | watch & react to background work | mentioned for long jobs |
| Plugins | bundle & share all of the above | the collaboration's distribution model |

::::::::::::::::::::::::::::::::::::::::::::: callout

## Plugins are how this becomes shareable

A *plugin* is a container for the other components — commands, subagents, skills, hooks, MCP
servers — so an entire workflow installs in one step. For a collaboration, that is the path from "I
configured my assistant" to "everyone runs the same vetted setup." See the Claude Code
[plugin components reference](https://code.claude.com/docs/en/plugins-reference#plugin-components-reference).

:::::::::::::::::::::::::::::::::::::::::::::

## Correctness comes from verification, not confidence

All this machinery serves one thing: results you can trust. That is hard, because an LLM is
stochastic — identical prompts can yield different outputs, and a confident answer is not evidence
of a correct one.

The discipline: treat every model output as a **hypothesis**, accepted only after checking it
against something external — the data, a fit statistic, a known physical value, or an independent
implementation. The agentic loop makes such checks cheap and automatic.

So favour tools that return compact, inspectable quantities — counts, edges, fit parameters — and
keep a record of what was run. Reproducibility and provenance are the criteria by which an automated
result earns trust.

::::::::::::::::::::::::::::::::::::::::::::: challenge

## Discussion: what does the loop buy you?

For the $\Lambda^0 \to p\,\pi^-$ analysis, identify two failure modes of a one-shot completion that an
agentic loop removes.

::::::::::::::: solution

1. **Hallucinated schema.** A one-shot model may emit a plausible but wrong branch name (for
   example `ReconstructedParticles.px` instead of `ReconstructedChargedParticles.momentum.x`). An
   agent can query the file and use the real names.
2. **Unvalidated fit.** A one-shot model cannot know whether its fit converged or where the peak
   landed. An agent can execute the fit, read $\mu$, $\sigma$, and $\chi^2/\mathrm{ndf}$, and iterate.

Both are the same principle: conditioning on observations beats conditioning on the prior.

:::::::::::::::

:::::::::::::::::::::::::::::::::::::::::::::

## Where this sits

Generative AI is already part of the research software ecosystem — code development and review,
navigating large codebases, searching technical documentation. The ePIC collaboration, which
produced the data used here, applies these tools in several such roles. This lesson is a
self-contained, low-cost entry point: with a free assistant and a single tool server you will carry
out a complete measurement on real ePIC data.

## Portability through an open protocol

The assistant market changes on a timescale of months, so we depend on a standard rather than a
product.

::::::::::::::::::::::::::::::::::::::::::::: callout

## One interface, many assistants

The **Model Context Protocol (MCP)** is an open standard for exposing tools to language-model
clients. A tool implemented once against MCP works in any compliant assistant — like a hardware bus
that decouples peripherals from hosts. In [Episode 3](03-mcp-servers.md) you connect the EIC tool
servers and see that any MCP-compliant client connects the same way, making the workflow
reproducible across environments.

:::::::::::::::::::::::::::::::::::::::::::::

The [next episode](02-your-ai-coding-setup.md) sets up a working assistant and states the physics
measurement precisely.

::::::::::::::::::::::::::::::::::::::::::::: keypoints

- A conversational model returns text; an agentic harness executes tools and conditions on their output.
- A harness has four parts: the model, the context window, a set of typed tools, and a control loop.
- Modern assistants extend the loop with MCP tools, subagents, LSP code intelligence, hooks, and monitors; plugins bundle these to share.
- LLM output is stochastic and must be treated as a hypothesis to be checked against data, fits, and known values.
- The agentic loop makes self-verification possible: the assistant can run the analysis and react to the result.
- Building on the open Model Context Protocol keeps tools portable across assistants and supports reproducibility.

:::::::::::::::::::::::::::::::::::::::::::::
