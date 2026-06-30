---
title: Setup
---

This lesson runs entirely inside **eic-shell**, the ePIC software container. You install an AI
assistant yourself; one command then builds the tool servers. No Docker, no grid certificate, no
data download — the MCP servers reuse the container's own `uproot`, `xrdfs`, and `rucio` (already
logged in to the shared read-only `eicread` account).

::::::::::::::::::::::::::::::::::::::::::::: checklist

## Quick checklist

* [ ] **eic-shell** working (`./eic-shell` drops you into the container).
* [ ] An AI assistant installed and connected to a free model — you choose it (Episode 2).
* [ ] **`eic-mcp setup`** run once (clones + builds the three MCP servers).

:::::::::::::::::::::::::::::::::::::::::::::

## 1. eic-shell

If you don't have it yet, follow the ePIC
[setup guide](https://eic.github.io/tutorial-setting-up-environment/), then:

```bash
./eic-shell
```

Everything below runs **inside** that shell.

## 2. An AI assistant (your choice)

Install one agentic assistant and connect it to a free model. [Episode 2](../episodes/02-your-ai-coding-setup.md)
compares the options; this lesson uses [opencode](https://opencode.ai):

```bash
curl -fsSL https://opencode.ai/install | bash
opencode auth login    # pick Google Gemini (free tier), GitHub Models, or a local Ollama model
```

## 3. Build the MCP servers — `eic-mcp setup`

The lesson ships a launcher, `bin/eic-mcp`, that clones and builds the three servers (uproot,
xrootd, rucio) inside eic-shell. Run it once:

```bash
eic-mcp setup
```

The first run takes a few minutes. You start and stop the servers per session in
[Episode 3](../episodes/03-mcp-servers.md) with `eic-mcp up` / `eic-mcp down`; point your assistant
at them with [`files/mcp-config/opencode.jsonc`](../files/mcp-config/opencode.jsonc).

::::::::::::::::::::::::::::::::::::::::::::: callout

## No credentials, no data download

The `rucio` server signs in automatically with the shared, read-only `eicread` account baked into
eic-shell — the same one the `rucio` command line uses. You never enter a password or a grid proxy,
and you never download a dataset: the assistant reads ROOT files in place over `root://`.

:::::::::::::::::::::::::::::::::::::::::::::
