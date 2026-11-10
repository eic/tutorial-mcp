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
* [ ] The assistant can list the campaigns on the data store.

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
models need no login. The servers stop when you leave eic-shell: keep that shell open.

On macOS the container's home (`/root`) is wiped on exit: keep your work in the eic-shell folder.

::::::::::::::::::::::::::::::::::::::::::::: callout

## Check it works

Ask: *"Create hello.py that prints the PDG Λ⁰ baryon mass in GeV, then run it."* The assistant
should write the file and run it, printing `1.115683`. If it only shows the code, switch it to
agent (build) mode.

Then ask: *"Use the xrootd tools to list /eic/EPIC/RECO."* The answer should be a list of campaign
versions (`26.04.1`, …). This checks the servers and the data store.

:::::::::::::::::::::::::::::::::::::::::::::

## Other assistants

![](fig/one-ring.svg){alt='gold ring engraved with the words EIC' width='160px'}

**One assistant to rule them all?** Any **agentic** assistant — one that can
read/write your files and run commands, not just emit text — works, and MCP works with any.

| Tool | Interface | Free access |
| --- | --- | --- |
| [opencode](https://opencode.ai) | terminal | free hosted models, an API key, or a local model |
| [GitHub Copilot](https://github.com/features/copilot) | [VS Code](https://code.visualstudio.com/), CLI | free tier; free Pro for students and educators |
| [Antigravity](https://antigravity.google/) | terminal (`agy`), IDE | free preview; replaces Gemini CLI |
| [Codex](https://developers.openai.com/codex) | terminal, IDE | paid ChatGPT plans |
| [Claude Code](https://claude.com/claude-code) | terminal, IDE | Claude plans |
| [Cursor](https://cursor.com/) | dedicated editor | free tier |
| [Cline](https://cline.bot/) | VS Code extensions | needs an API key |

eic-shell also has `claude` and `copilot`: run `eic-mcp config claude` (or `copilot`), then start
it.

::::::::::::::::::::::::::::::::::::::::::::: callout

## Assistant outside eic-shell

The servers must run in eic-shell, but the client can run on your machine, started in the
directory that holds its config file.

* **Linux, WSL:** apptainer shares the host network and your home directory. Run
  `eic-mcp config <client>` inside eic-shell, in the directory where you will start the client.
* **macOS:** start eic-shell with the server ports published, run `eic-mcp up` in it, and
  download the client config on the Mac (`eic-mcp` does not run on the Mac itself):

  ```bash
  DOCKER_OPTIONS="$(./eic-shell -- eic-mcp docker-args)" ./eic-shell
  ```

  ```bash
           # on Mac: the directory where you will launch opencode
  curl -fsSLO https://raw.githubusercontent.com/eic/tutorial-mcp/main/files/mcp-config/opencode.jsonc
  ```

:::::::::::::::::::::::::::::::::::::::::::::
