---
title: Setup
---

Everything runs inside **eic-shell**. Install an AI assistant (this tutorial will use `opencode`), get `eic-mcp`, and
one command starts the tool servers. Nothing else — no grid certificate, no data download — the
MCP servers reuse the eic-shell own `uproot`, `xrdfs`, and `rucio` (already logged in to the
shared read-only `eicread` account).

::::::::::::::::::::::::::::::::::::::::::::: checklist

## Quick checklist

* [ ] **eic-shell** working (`./eic-shell` drops you into the container).
* [ ] One **AI assistant** installed (e.g. `opencode`).
* [ ] **`eic-mcp`** on your `PATH`, **`~/tutorial-mcp`** cloned (two `git clone`s).
* [ ] **`eic-mcp up`** starts the three MCP servers (the first run bootstraps them automatically).

:::::::::::::::::::::::::::::::::::::::::::::

## 1. eic-shell

Make sure `./eic-shell` drops you into the container —
everything below runs **inside** it. (See
[environment setup guide](https://eic.github.io/tutorial-setting-up-environment/).)

## 2. Choose an AI assistant

![](fig/one-ring.svg){alt='gold ring engraved with the words EIC' width='160px'}

**One assistant to rule them all?** Fortunately not: any **agentic** assistant — one that can
read/write your files and run commands, not just emit text — works, and MCP keeps you free to
switch. This tutorial is based on [opencode](https://opencode.ai).

| Tool | Interface | Free access |
| --- | --- | --- |
| [opencode](https://opencode.ai) | terminal | open source (MIT); free hosted models (no key), bring your own key, or a local model |
| [GitHub Copilot](https://github.com/features/copilot) | [VS Code](https://code.visualstudio.com/), CLI | free tier; free Pro for verified students/educators/OSS maintainers |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | terminal | open source; generous free tier with a personal Google account |
| [Codex](https://developers.openai.com/codex) | terminal, IDE | included with ChatGPT plans |
| [Claude Code](https://claude.com/claude-code) | terminal, IDE | included with Claude plans |
| [Cursor](https://cursor.com/) | dedicated editor | free tier |
| [Cline](https://cline.bot/) / [Continue](https://continue.dev/) | VS Code extensions | open source; bring your own key |

## 3. Install one

This lesson uses **[opencode](https://opencode.ai)** — terminal, native MCP, free models:

```bash
curl -fsSL https://opencode.ai/install | bash
```

The free hosted models work out of the box without any login.

Prefer an editor? Install [VS Code](https://code.visualstudio.com/) plus the
[GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) and
[Copilot Chat](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) extensions
(sign in with GitHub — students/educators get Pro free — and use **Agent** mode), or
[Cursor](https://cursor.com/).

::::::::::::::::::::::::::::::::::::::::::::: callout

## Check it works

Open an empty folder in your assistant and ask: *"Create hello.py that prints the PDG Λ⁰ baryon mass
in GeV, then run it."* It should **write** the file and **run** it, printing `1.115683`. If it only
shows code, switch on agent/edit mode — executing, not suggesting, is what is needed.

:::::::::::::::::::::::::::::::::::::::::::::

## 4. Start the MCP servers — `eic-mcp up`

The launcher lives in its own repository. Clone it — and this lesson's repository, whose example
files Episodes 4–5 use — into your home directory (or workdir), so every command in the lesson can be pasted
as-is:

```bash
git clone https://github.com/eic/eic-mcp ~/eic-mcp
git clone https://github.com/eic/tutorial-mcp ~/tutorial-mcp
export PATH="$HOME/eic-mcp/bin:$PATH"    # re-run in each new shell (eic-shell skips your profile)
```

It runs the three servers (uproot, xrootd, rucio) inside eic-shell:

```bash
eic-mcp up
```

If your eic_xl image already ships the servers, they just start; otherwise the **first** run
bootstraps them automatically (a one-time clone and build, a few minutes). Every later `eic-mcp up`
starts in seconds. You start and stop the servers per session in
[Episode 3](../episodes/03-mcp-servers.md) with `eic-mcp up` / `eic-mcp down`; point your assistant
at them with `eic-mcp config opencode` (see Episode 3).

::::::::::::::::::::::::::::::::::::::::::::: callout

## No credentials, no data download

The `rucio` server signs in automatically with the shared, read-only `eicread` account baked into
eic-shell — the same one the `rucio` command line uses. You never enter a password
and you never download a dataset: the assistant reads ROOT files in place over `root://`.

:::::::::::::::::::::::::::::::::::::::::::::
