---
title: "Generative AI as an agentic research tool"
teaching: 15
exercises: 5
---

<style>
/* Mermaid: force diagram label text dark so it stays readable on the
   light node fills in BOTH light and dark mode. The Carpentries dark
   theme sets `p`/`li` color and darkens `pre` backgrounds, which would
   otherwise turn mermaid's label text light (invisible on light nodes)
   and the diagram surface dark. We override both, with !important to
   beat the theme rules and mermaid's own inline styles. */
.mermaid { background: transparent !important; }
/* Hide the Workbench "Diagram source code" spoiler under each diagram */
.mermaid-img-wrapper details { display: none !important; }
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
pre.ai-prompt, pre.ai-prompt code {
  white-space: pre-wrap;       /* wrap long prompts onto many lines */
  overflow-wrap: anywhere;
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

- How does an agentic assistant differ from a chat model?
- What are the parts of an LLM "harness"?
- How do we get trustworthy results from a stochastic model?

:::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::: objectives

- Trace one pass of the agent loop for a physics task, naming what enters the context at each step.
- Draft acceptance criteria precise enough that a grader — human or agent — can apply them.
- Tell a tool from a skill.

:::::::::::::::::::::::::::::::::::::::::::::

## The bottleneck is rarely the physics

In a typical analysis the physics steps are few: select a final state, build an observable, fit a
signal. Most of the time goes into the software around them: finding datasets, learning the data
model, getting branch names and units right, and iterating on plotting and analysis code. LLMs can
reduce this work, but only if their results can be checked. Later episodes apply this to the decay
$\Lambda^0 \to p\,\pi^-$.

## Two modes of use

A **chat completion** is a single request: a prompt goes in, text comes out. If the text is code,
you run it, read the error, and paste it back by hand. The model never observes your
data or the result of running anything.

An **agentic loop** runs the same model inside a control structure that lets it act. The model
proposes an action, an external **tool** carries it out, the result is added to the context, and
the model is called again, until a stopping condition is met. The model then works from the actual
state of your files and the output of real computations, not only from its training.

In this lesson "generative AI" means an LLM-based coding assistant used in this agentic mode.
Machine learning for reconstruction or particle identification is not covered.

## The agent loop

The model calls a tool, looks at what came back, and decides whether it is done.

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'fontSize':'15px','lineColor':'#94a3b8','edgeLabelBackground':'#e2e8f0','clusterBkg':'#1f293720','clusterBorder':'#94a3b8','titleColor':'#94a3b8'}}}%%
flowchart TD
    accTitle: {The agent loop}
    accDescr: {The agent loop}
    Q["task"]:::user --> M["model"]:::core
    M -->|"tool call"| T["tools<br/>read files · run code · query "]:::tool
    T -->|"result appended to context"| D{"task<br/>complete?"}:::core
    D -->|"no"| M
    D -->|"yes"| R["result + provenance"]:::out
    classDef core fill:#e7efff,stroke:#4c6ef5,stroke-width:1.5px,color:#10204a;
    classDef tool fill:#e6f7ed,stroke:#2f9e44,stroke-width:1.5px,color:#0b3d1f;
    classDef out fill:#f3e8ff,stroke:#7048e8,stroke-width:1.5px,color:#2e1065;
    classDef user fill:#f1f3f5,stroke:#868e96,stroke-width:1.5px,color:#212529;
```

The model together with the software that runs this cycle is called a **harness**. It has four parts:

* **Model**: reasoning and code generation. The provider and model can be swapped; they are not
  part of the method.
* **Context**: everything the model sees in a step: instructions, files, earlier turns, tool
  outputs. Its size is limited (the *context window*).
* **Tools**: operations the model may call. Tools are the only way the model can change anything
  outside itself.
* **Control loop**: repeats *propose → execute → observe* until the task is done. This is what
  separates an agent from a chatbot.

### Extending the harness

Current assistants add a few standard extension points to this core.

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'fontSize':'15px','lineColor':'#94a3b8','edgeLabelBackground':'#e2e8f0','clusterBkg':'#1f293720','clusterBorder':'#94a3b8','titleColor':'#94a3b8'}}}%%
flowchart TB
    accTitle: {AI agent harness}
    accDescr: {AI agent harness}
    MCP["MCP servers<br/>external tools & data"]:::tool --> H
    SUB["subagents<br/>specialized, isolated context"]:::tool --> H
    HOOKS["hooks<br/>lifecycle automation"]:::tool --> H
    MON["monitors<br/>watch & react"]:::tool --> H
    H(["harness core<br/>model + context + tools + loop"]):::core
    classDef core fill:#e7efff,stroke:#4c6ef5,stroke-width:1.5px,color:#10204a;
    classDef tool fill:#e6f7ed,stroke:#2f9e44,stroke-width:1.5px,color:#0b3d1f;
```
This lesson uses two ways to extend a harness:
* **MCP servers**: tools in a standard form that works with any assistant. This is how the
  assistant gets physics tools ([Episode 3](03-mcp-servers.md)).
* **Skills**: versioned *procedures* (a `SKILL.md`) loaded when a request matches
  ([Episode 4](04-skills.md)). A tool is a capability; a skill is a recipe.

Assistants also offer subagents (a separate assistant for a sub-task), hooks (scripts run at fixed
moments, e.g. after every edit), and monitors (watch a background job).

## The verification loop

An agent stops when it decides the task is complete. An LLM is stochastic: the same prompt
can give different outputs, and a confident answer is not evidence of a correct one. A second loop
around the first handles this. A **grader** checks the agent's result against explicit acceptance
criteria, and a failure goes back to the agent as feedback for another attempt.

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'fontSize':'15px','lineColor':'#94a3b8','edgeLabelBackground':'#e2e8f0','clusterBkg':'#1f293720','clusterBorder':'#94a3b8','titleColor':'#94a3b8'}}}%%
flowchart TD
    accTitle: {The verification loop}
    accDescr: {The verification loop}
    A["agent loop"]:::core -->|"draft result"| G["grader<br/>explicit success criteria"]:::tool
    G --> P{"pass?"}:::core
    P -->|"no — feedback into context"| A
    P -->|"yes"| R["accepted result"]:::out
    classDef core fill:#e7efff,stroke:#4c6ef5,stroke-width:1.5px,color:#10204a;
    classDef tool fill:#e6f7ed,stroke:#2f9e44,stroke-width:1.5px,color:#0b3d1f;
    classDef out fill:#f3e8ff,stroke:#7048e8,stroke-width:1.5px,color:#2e1065;
```

Treat every model output as a **hypothesis** and accept it only after checking it against something
external: the data, a fit statistic, a known physical value, or an independent implementation.
Prefer tools that return small quantities you can inspect (counts, bin edges, fit parameters), and
keep a record of what was run.

::::::::::::::::::::::::::::::::::::::::::::: challenge

## Exercise: acceptance criteria (≈ 5 min)

An assistant reports "the Λ⁰ peak was fitted successfully". Write three or four checks the fit
must pass before you accept it. Each must be a comparison a script could evaluate.

::::::::::::::: solution

* $|\mu - 1.115683\,\mathrm{GeV}| < 5\,\mathrm{MeV}$.
* $\sigma$ of a few MeV, the detector resolution.
* $\chi^2/\mathrm{ndf}$ of order 1.
* Enough entries in the fit window for the fit to mean anything.

"The fit looks good" is not a criterion. In [Episode 4](04-skills.md) these checks go into the
lambda-fit skill; an agent that fails them must report the failure instead of a result.

:::::::::::::::

:::::::::::::::::::::::::::::::::::::::::::::

## Outer loops

Two more loops can wrap these. In an **operation loop** an event (a schedule, a finished
production job, a new pull request) starts the agent and its verified output updates a report or a
documentation page; [Episode 6](06-eic-mcp-servers.md) shows ePIC examples. In an **improvement
loop** you read what the agent actually did and change the harness: clarify `AGENTS.md`, tighten a
skill's success criteria, add a missing tool.

A person decides at each level: approving a sensitive tool call, signing off a graded result,
reviewing what runs unattended, and choosing which harness changes to keep.

::::::::::::::::::::::::::::::::::::::::::::: keypoints

- An agentic assistant runs tools and reads their output; a chat model only returns text.
- Treat every result as a hypothesis and check it against explicit criteria before you accept it.
- A tool is a capability; a skill is a recipe.

:::::::::::::::::::::::::::::::::::::::::::::

<small>The loop schematics are adapted from
[*The Art of Loop Engineering*](https://www.langchain.com/blog/the-art-of-loop-engineering).</small>
