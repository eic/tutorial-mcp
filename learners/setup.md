---
title: Setup
---

This lesson runs entirely inside **eic-shell**, the ePIC software container. You
only need two things: eic-shell and a free AI assistant. No Docker, no grid
certificate, no data download — the MCP tool servers reuse the container's own
`uproot`, `xrdfs`, and `rucio` (already logged in to the shared read-only
`eicread` account).

::::::::::::::::::::::::::::::::::::::::::::: checklist

## Quick checklist

* [ ] **eic-shell** installed and working (`./eic-shell` drops you into the container).
* [ ] **opencode** installed and connected to a free model (Episode 2).
* [ ] The three EIC MCP servers built and running (`eic-mcp up`, Episode 3).

:::::::::::::::::::::::::::::::::::::::::::::

## 1. eic-shell

The ePIC environment ships everything the tool servers need. If you don't have
it yet, follow the ePIC
[setup guide](https://eic.github.io/tutorial-setting-up-environment/), then:

```bash
./eic-shell
```

Everything below runs **inside** that shell.

## 2. An AI assistant — opencode

We use [opencode](https://opencode.ai), a free, open-source terminal assistant
with native MCP support. Install it and connect a free model (full walkthrough
in [Episode 2](../episodes/02-your-ai-coding-setup.md)):

```bash
curl -fsSL https://opencode.ai/install | bash
opencode auth login          # pick Google Gemini (free tier), GitHub Models, or a local Ollama model
```

## 3. The EIC MCP servers

This lesson's repository ships a small launcher, `bin/eic-mcp`, that builds and
runs the three servers inside eic-shell. Build them once:

```bash
eic-mcp setup
```

You start and stop them per session in [Episode 3](../episodes/03-mcp-servers.md)
with `eic-mcp up` / `eic-mcp down`. The matching opencode configuration lives in
[`files/mcp-config/opencode.jsonc`](../files/mcp-config/opencode.jsonc).

::::::::::::::::::::::::::::::::::::::::::::: callout

## No credentials, no data download

The `rucio` server signs in automatically with the shared, read-only `eicread`
account baked into eic-shell — the same one the `rucio` command line uses. You
never enter a password or a grid proxy, and you never download a dataset: the
assistant reads ROOT files in place over `root://`.

:::::::::::::::::::::::::::::::::::::::::::::
