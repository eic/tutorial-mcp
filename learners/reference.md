---
title: 'Reference'
---

## Glossary

agent
:   A language model operated in a control loop where it may invoke tools, observe their output,
    and decide subsequent actions, in contrast to a single chat completion.

agentic loop
:   The control structure *propose action → execute tool → append observation → re-invoke model*,
    repeated until a stopping condition. It enables self-verification against ground truth.

AGENTS.md
:   A plain-Markdown file giving an assistant always-on project context (environment, data model,
    conventions, definition of done). Read automatically by many clients; equivalent to a
    `copilot-instructions.md`, `.cursorrules`, or "custom instructions" elsewhere.

branching fraction
:   The probability that a particle decays through a particular channel. For Λ⁰ → p π⁻ it is ≈ 63.9%.

combinatorial background
:   The smooth, non-peaking distribution from pairing tracks that did not originate from a common
    parent. It is separated from signal by a fit, not removed by selection alone.

context (context window)
:   The bounded set of tokens a model attends to in a step: system instructions, files, prior
    turns, and tool outputs. Managing its contents is "context engineering."

EDM4eic
:   The ePIC event data model, an EIC extension of EDM4hep generated with PODIO. Reconstructed
    output is stored in an `events` tree whose branches are per-event collections (e.g.
    `ReconstructedChargedParticles`, `MCParticles`).

harness
:   A model together with the machinery that makes it operational: model, context, tools, and the
    control loop. The method of this lesson is independent of which model fills the first slot.

invariant mass
:   The Lorentz-invariant combination $m = \sqrt{(\Sigma E)^2 - |\Sigma \vec{p}|^2}$ of a set of
    four-momenta. For the daughters of a real decay it equals the parent mass.

JSON-RPC
:   A lightweight remote-procedure-call protocol using JSON messages. MCP is built on JSON-RPC 2.0.

LLM (large language model)
:   The generative model performing reasoning and code synthesis at the centre of a harness.

MCP (Model Context Protocol)
:   An open client–server standard for exposing tools, resources, and prompts to language-model
    clients, so one tool implementation serves many assistants. See <https://modelcontextprotocol.io>.

MCP server
:   A program that advertises MCP tools/resources to clients over stdio or HTTP. Here, the
    `uproot-mcp-server` provides ROOT/EDM4eic analysis tools.

PODIO
:   The event-data-model toolkit (AIDASoft) that generates the I/O code behind EDM4hep/EDM4eic. Its
    files are readable by PODIO, ROOT (RDataFrame, TTreeReader), and uproot.

reconstruction
:   The inference of particle four-momenta and identities from detector signals. Outputs such as
    `ReconstructedChargedParticles.PDG` are estimates, not truth.

SKILL.md
:   The specification file of a *skill*: YAML frontmatter (`name`, `description`) plus a body giving
    applicability, inputs, steps, and success criteria. Loaded on demand when a request matches the
    description.

skill
:   A versioned procedure: a directory containing a `SKILL.md` that orchestrates the MCP tools
    toward a defined result. Where a tool is a capability, a skill composes capabilities.

stdio transport
:   The MCP transport in which the client launches the server as a subprocess and exchanges JSON-RPC
    on standard input/output. This lesson instead uses the **streamable HTTP** transport: the servers
    run inside eic-shell (`eic-mcp up`) and the client connects over `http://127.0.0.1:910x/mcp`.

tool
:   An operation the model may invoke through a typed interface (name, arguments, return schema). The
    only channel by which an agent affects the outside world.

uproot
:   A pure-Python ROOT I/O library, used by the tool server to read EDM4eic files and return compact
    JSON without a ROOT installation.

V0
:   A neutral particle reconstructed from two oppositely charged tracks at a displaced vertex (e.g.
    Λ⁰ → p π⁻, K⁰ₛ → π⁺π⁻); the canonical invariant-mass measurement.

yield
:   The number of signal candidates, obtained by integrating the fitted signal component, not by a
    raw bin count.
