---
title: Setup
---

The tool **servers** are installed in **eic-shell**, and you start them there with `eic-mcp up`.
Your **assistant** runs either on your own machine or inside the container. Install an assistant
(this tutorial uses `opencode`), then start the servers. You need no grid certificate and you
download no data: the MCP servers use eic-shell's own `uproot`, `xrdfs`, and `rucio`, which is
already logged in to the shared read-only `eicread` account.

::::::::::::::::::::::::::::::::::::::::::::: checklist

## Quick checklist

* [ ] **eic-shell** working; if `eic-mcp` is not found inside it, run `./eic-shell --upgrade`.
* [ ] One **AI assistant** installed (e.g. `opencode`), or use one already in eic-shell.
* [ ] **`~/tutorial-mcp`** cloned (this lesson's example files, used in Episodes 4–5).
* [ ] **`eic-mcp up`** run inside eic-shell starts the three MCP servers.

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

The free hosted models work without a login. You can also skip this step and use the `opencode`
that is installed in `eic-shell` (see step 4).

If you prefer an editor — try [VS Code](https://code.visualstudio.com/) plus the
[GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) and
[Copilot Chat](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) extensions
(sign in with GitHub — students/educators get Pro free — and use **Agent** mode), or
[Cursor](https://cursor.com/).

::::::::::::::::::::::::::::::::::::::::::::: callout

## Not allowed to install anything?

eic-shell already includes three assistants: `opencode`, `claude` (Claude Code), and `copilot`
(GitHub Copilot CLI). Run one inside the container, alongside the servers (step 4):

```bash
eic-mcp config opencode  # writes opencode.jsonc here  (claude: .mcp.json, copilot likewise)
opencode                 # or: claude, copilot
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

`eic-mcp` and the three servers are installed in eic-shell. First clone this lesson's repository;
Episodes 4–5 use its example files:

```bash
git clone https://github.com/eic/tutorial-mcp ~/tutorial-mcp
```

Then start the servers inside the container:

```bash
./eic-shell               # from your eic-shell folder
eic-mcp up                # starts uproot, xrootd, rucio on 127.0.0.1:9101-9103/mcp
```

Each server speaks MCP over streamable HTTP, so `eic-mcp` only starts and stops them. If
`eic-mcp` is not found, or `up` reports a missing server, update eic-shell with
`./eic-shell --upgrade` and try again.

### Where does the assistant run?

Pick one of two places:

1. **Inside eic-shell.** `opencode`, `claude`, and `copilot` are installed there. In the same
   shell where the servers run:

   ```bash
   eic-mcp config opencode && opencode
   ```

   `eic-mcp config opencode` writes `opencode.jsonc` in the current directory.

2. **On your own machine.** On Linux and Windows/WSL, Apptainer shares the host network, so the
   same `http://127.0.0.1:910x/mcp` URLs also work outside the container. Run
   `eic-mcp config opencode` in a directory you can reach from the host, or copy
   `~/tutorial-mcp/files/mcp-config/opencode.jsonc` there, then start your assistant in that
   directory. On macOS, read the next callout first.

::::::::::::::::::::::::::::::::::::::::::::: callout

## macOS: publish the server ports

On a Mac, `eic-shell` uses Docker, which publishes no ports by default. `eic-mcp docker-args`
prints the `docker run` flags that publish them; pass those flags in `DOCKER_OPTIONS`:

```bash
cd ~/eic                                    # the folder with ./eic-shell (yours may differ)
grep -q DOCKER_OPTIONS eic-shell || curl -L https://github.com/eic/eic-shell/raw/main/install.sh | bash
DOCKER_OPTIONS="$(./eic-shell -- eic-mcp docker-args)" ./eic-shell
```

The `grep` line reinstalls `eic-shell` if your copy is older than `DOCKER_OPTIONS`; you need it
only once. Then, inside eic-shell:

```bash
eic-mcp up
```

Leave this window open: the container — and the servers inside it — only live while `./eic-shell`
runs. Your assistant stays **on the Mac**, in a second terminal; copy the example config into the
directory where you launch `opencode`:

```bash
cp ~/tutorial-mcp/files/mcp-config/opencode.jsonc .
```

:::::::::::::::::::::::::::::::::::::::::::::

[Episode 3](../episodes/03-mcp-servers.md) covers the per-session workflow: `eic-mcp up`,
`eic-mcp down`, and `eic-mcp config opencode` to write your client config.

::::::::::::::::::::::::::::::::::::::::::::: callout

## No credentials, no data download

The `rucio` server signs in automatically with the shared, read-only `eicread` account baked into
eic-shell — the same one the `rucio` command line uses. You never enter a password
and you never download a dataset: the assistant reads ROOT files in place over `root://`.

:::::::::::::::::::::::::::::::::::::::::::::
