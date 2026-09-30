---
title: Setup
---

eic-shell contains everything this lesson needs: the three MCP servers (uproot, xrootd, rucio),
the `eic-mcp` command that starts them, and the `opencode` assistant. You need no grid certificate
and download no data: `rucio` is already signed in to the shared read-only `eicread` account.

::::::::::::::::::::::::::::::::::::::::::::: checklist

## Quick checklist

* [ ] **eic-shell** is up to date (`./eic-shell --upgrade`).
* [ ] Inside eic-shell, **`eic-mcp up`** starts three servers and **`opencode`** opens.

:::::::::::::::::::::::::::::::::::::::::::::

## 1. eic-shell

See the [environment setup guide](https://eic.github.io/tutorial-setting-up-environment/) if you
do not have eic-shell yet. Then, in the folder with `./eic-shell`:

```bash
cd ~/eic                  # yours may differ
./eic-shell --upgrade
```

## 2. Start the servers and the assistant

```bash
./eic-shell
mkdir -p lambda && cd lambda     # a working directory for the analysis
eic-mcp up                       # uproot, xrootd, rucio on 127.0.0.1:9101-9103
eic-mcp config opencode          # writes opencode.jsonc here
opencode
```

In opencode, `/mcp` should list `uproot`, `xrootd`, and `rucio` as connected. The free hosted
models need no login. If `eic-mcp` or `opencode` is not found, exit eic-shell, return to the folder
containing the launcher, run `./eic-shell --upgrade`, and start eic-shell again.

On macOS, eic-shell is a Docker container: the servers stop when you leave it, and its home
(`/root`) is wiped, so opencode forgets its settings. Keep your work in the eic-shell folder.

::::::::::::::::::::::::::::::::::::::::::::: callout

## Check it works

In an empty directory, ask: *"Create hello.py that prints the PDG Λ⁰ baryon mass in GeV, then run
it."* The assistant should write the file and run it, printing `1.115683`. If it only shows the
code, switch it to agent (build) mode.

:::::::::::::::::::::::::::::::::::::::::::::

## Other assistants

![](fig/one-ring.svg){alt='gold ring engraved with the words EIC' width='160px'}

**One assistant to rule them all?** Any **agentic** assistant — one that can
read/write your files and run commands, not just emit text — works, and MCP works with any.

| Tool | Interface | Free access |
| --- | --- | --- |
| [opencode](https://opencode.ai) | terminal | open source (MIT); free hosted models (no key), bring your own key, or a local model |
| [GitHub Copilot](https://github.com/features/copilot) | [VS Code](https://code.visualstudio.com/), CLI | free tier; free Pro for verified students/educators/OSS maintainers |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | terminal | open source; free tier with a personal Google account |
| [Codex](https://developers.openai.com/codex) | terminal, IDE | included with ChatGPT plans |
| [Claude Code](https://claude.com/claude-code) | terminal, IDE | included with Claude plans |
| [Cursor](https://cursor.com/) | dedicated editor | free tier |
| [Cline](https://cline.bot/) / [Continue](https://continue.dev/) | VS Code extensions | open source; bring your own key |

eic-shell also has `claude` and `copilot`: run `eic-mcp config claude` (or `copilot`), then start
it. The first login prints a code to paste in a browser, so it works over SSH.

::::::::::::::::::::::::::::::::::::::::::::: callout

## Assistant outside eic-shell

The servers must run in eic-shell, but the client can run on your machine. Keep `eic-mcp up`
running and put the client config in the directory where you start the client.

* **Linux, WSL:** apptainer shares the host network. Run `eic-mcp config <client>` there.
* **macOS:** publish the ports once, restart `./eic-shell`, and download the example config
  (`eic-mcp` does not run on the Mac itself):

  ```bash
  cd ~/eic
  grep -q 9101 eic-shell || sed -i '' 's|^docker run |docker run -p 127.0.0.1:9101-9103:9101-9103 |' eic-shell
  curl -fsSLO https://raw.githubusercontent.com/eic/tutorial-mcp/main/files/mcp-config/opencode.jsonc   # in your work directory
  ```

:::::::::::::::::::::::::::::::::::::::::::::
