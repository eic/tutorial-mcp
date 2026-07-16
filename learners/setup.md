---
title: Setup
---

The tool **servers** run inside **eic-shell**; your **assistant** runs where you normally work.
Install an AI assistant (this tutorial will use `opencode`), get `eic-mcp`, and one command starts
the tool servers. Nothing else — no grid certificate, no data download — the MCP servers reuse
eic-shell's own `uproot`, `xrdfs`, and `rucio` (already logged in to the shared read-only `eicread`
account).

::::::::::::::::::::::::::::::::::::::::::::: checklist

## Quick checklist

* [ ] **eic-shell** working (`./eic-shell` drops you into the container).
* [ ] One **AI assistant** installed (e.g. `opencode`).
* [ ] **`eic-mcp`** on your `PATH`, **`~/tutorial-mcp`** cloned (two `git clone`s).
* [ ] **`eic-mcp up`** starts the three MCP servers (the first run bootstraps them automatically).

:::::::::::::::::::::::::::::::::::::::::::::

## 1. eic-shell

Make sure `./eic-shell` drops you into the container. (See
[environment setup guide](https://eic.github.io/tutorial-setting-up-environment/).)

## 2. Choose an AI assistant

![](fig/one-ring.svg){alt='gold ring engraved with the words EIC' width='160px'}

**One assistant to rule them all?** Any **agentic** assistant — one that can
read/write your files and run commands, not just emit text — works, and MCP works with any.
This tutorial is based on [opencode](https://opencode.ai).

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

This lesson uses **[opencode](https://opencode.ai)**:

```bash
curl -fsSL https://opencode.ai/install | bash
```

The free hosted models work out of the box without any login. Run it on your own machine, not
inside `eic-shell`.

If you prefer an editor — try [VS Code](https://code.visualstudio.com/) plus the
[GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) and
[Copilot Chat](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) extensions
(sign in with GitHub — students/educators get Pro free — and use **Agent** mode), or
[Cursor](https://cursor.com/).

::::::::::::::::::::::::::::::::::::::::::::: callout

## Not allowed to install anything?

eic-shell already has two assistants: **Claude Code** (`claude`) and the **GitHub Copilot CLI**
(`copilot`). Run one *inside* the container, alongside the servers (step 4):

```bash
eic-mcp config claude    # writes .mcp.json here  (copilot: eic-mcp config copilot)
claude                   # or: copilot
```

One browser login the first time; it prints a code to paste, so it works over SSH.

:::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::: callout

## Check it works

Open an empty folder in your assistant and ask: *"Create hello.py that prints the PDG Λ⁰ baryon mass
in GeV, then run it."* It should **write** the file and **run** it, printing `1.115683`. If it only
shows code, switch on agent/edit mode — executing, not suggesting, is what is needed.

:::::::::::::::::::::::::::::::::::::::::::::

## 4. Start the MCP servers — `eic-mcp up`

**This step is temporary**: `eic-mcp` and the servers are becoming part of eic-shell itself. Once
the image ships them there are no extra steps — no clone, no PATH line — and the commands stay
exactly the same. Until then, clone the launcher — and this lesson's repository, whose example
files Episodes 4–5 use — into your home directory (or workdir):

```bash
git clone https://github.com/eic/eic-mcp ~/eic-mcp
git clone https://github.com/eic/tutorial-mcp ~/tutorial-mcp
echo 'export PATH="$HOME/eic-mcp/bin:$HOME/.opencode/bin:$PATH"' >> ~/.bashrc && . ~/.bashrc
```

It runs the three servers (uproot, xrootd, rucio) inside eic-shell:

```bash
cd ~/eic && eic-mcp up    # first run from your eic-shell folder — it remembers the image
```

::::::::::::::::::::::::::::::::::::::::::::: callout

## macOS: two extra steps

On a Mac, `eic-shell` is Docker: it publishes no ports and does not share your home. Clone the
launcher **next to `./eic-shell`** instead, and publish the server ports once:

```bash
cd ~/eic                                    # the folder with ./eic-shell (yours may differ)
git clone https://github.com/eic/eic-mcp
grep -q 9101 eic-shell || sed -i '' "s|^docker run |docker run -p 127.0.0.1:9101-9104:9101-9104 -v $PWD/eic-mcp/bin/eic-mcp:/usr/local/bin/eic-mcp:ro |" eic-shell
grep 'docker run' eic-shell                 # must now show the -p and -v flags
./eic-shell
```

That one edit publishes the ports **and** puts `eic-mcp` on the container's `PATH` for good, so
inside eic-shell there is nothing to export — just:

```bash
eic-mcp up
```

Leave this window open: the container — and the servers inside it — only live while `./eic-shell`
runs. Your assistant stays **on the Mac**, in a second terminal; copy the ready-made config into the
directory where you launch `opencode`:

```bash
cp ~/tutorial-mcp/files/mcp-config/opencode.jsonc .
```

:::::::::::::::::::::::::::::::::::::::::::::

If your eic_xl image already ships the servers, they just start; otherwise the **first** run
bootstraps them automatically (a one-time clone and build, a few minutes). Every later `eic-mcp up`
starts in seconds. You start and stop the servers per session in
[Episode 3](../episodes/03-mcp-servers.md) with `eic-mcp up` / `eic-mcp down`;
`eic-mcp config opencode` writes the client config for you (Episode 3).

::::::::::::::::::::::::::::::::::::::::::::: callout

## No credentials, no data download

The `rucio` server signs in automatically with the shared, read-only `eicread` account baked into
eic-shell — the same one the `rucio` command line uses. You never enter a password
and you never download a dataset: the assistant reads ROOT files in place over `root://`.

:::::::::::::::::::::::::::::::::::::::::::::
