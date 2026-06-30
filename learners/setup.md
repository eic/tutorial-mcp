---
title: Setup
---

This lesson runs inside **eic-shell**, the ePIC software container. Install an AI assistant (your
choice), then one command builds the tool servers. No Docker, no grid certificate, no data
download — the MCP servers reuse the container's own `uproot`, `xrdfs`, and `rucio` (already logged
in to the shared read-only `eicread` account).

::::::::::::::::::::::::::::::::::::::::::::: checklist

## Quick checklist

* [ ] **eic-shell** working (`./eic-shell` drops you into the container).
* [ ] One **AI assistant** installed and connected to a free model.
* [ ] **`eic-mcp setup`** run once (builds the three MCP servers).

:::::::::::::::::::::::::::::::::::::::::::::

## 1. eic-shell

If you don't have it yet, follow the ePIC
[setup guide](https://eic.github.io/tutorial-setting-up-environment/), then:

```bash
./eic-shell
```

Everything below runs **inside** that shell.

## 2. Choose an AI assistant

You need one. Any **agentic** assistant — one that can read/write your files and run commands, not
just emit text — works; the method is identical. This is a mid-2026 snapshot, so verify current
terms.

| Tool | Interface | Free access |
| --- | --- | --- |
| [opencode](https://opencode.ai) | terminal | open source (MIT); free hosted models (no key), bring your own key, or a local model |
| [GitHub Copilot](https://github.com/features/copilot) | [VS Code](https://code.visualstudio.com/), CLI | free tier; free Pro for verified students/educators/OSS maintainers |
| [Cursor](https://cursor.com/) | dedicated editor | free tier |
| [Cline](https://cline.bot/) / [Continue](https://continue.dev/) | VS Code extensions | open source; bring your own key |

::::::::::::::::::::::::::::::::::::::::::::: callout

## Two senses of "free"

**Open-source clients** ([opencode](https://opencode.ai), [Cline](https://cline.bot/),
[Continue](https://continue.dev/)) install free but bill per token — zero marginal cost only with a
local model (e.g. via [Ollama](https://ollama.com)). **Commercial free tiers**
([Copilot](https://github.com/features/copilot) Free, [Cursor](https://cursor.com/)) bundle a quota,
then meter. If an assistant only emits code to run by hand, enable its **agent**/**edit** mode.

:::::::::::::::::::::::::::::::::::::::::::::

## 3. Install one

This lesson uses **[opencode](https://opencode.ai)** — terminal, native MCP, free models:

```bash
curl -fsSL https://opencode.ai/install | bash
opencode auth login    # pick Google Gemini (free tier), GitHub Models, or a local Ollama model
```

Prefer an editor? Install [VS Code](https://code.visualstudio.com/) plus the
[GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) and
[Copilot Chat](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) extensions
(sign in with GitHub — students/educators get Pro free — and use **Agent** mode), or
[Cursor](https://cursor.com/).

::::::::::::::::::::::::::::::::::::::::::::: callout

## Check it works

Open an empty folder in your assistant and ask: *"Create hello.py that prints the PDG Λ⁰ baryon mass
in GeV, then run it."* It should **write** the file and **run** it, printing `1.115683`. If it only
shows code, switch on agent/edit mode — executing, not suggesting, is what this lesson relies on.

:::::::::::::::::::::::::::::::::::::::::::::

## 4. Build the MCP servers — `eic-mcp setup`

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
