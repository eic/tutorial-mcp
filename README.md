# Generative AI for Physics Analysis (ePIC tutorial)

A **tool-agnostic** lesson that teaches researchers to use generative AI — AI coding assistants,
**MCP servers**, *skills*, and *agents* — for a real ePIC physics analysis: reconstructing the
decay **Λ⁰ → p + π⁻** and fitting its invariant-mass peak at 1.115683 GeV.

It is built with [The Carpentries Workbench][workbench].

## What's here

| Path | Contents |
| --- | --- |
| `episodes/` | The lesson. **01–03 are the hands-on core** (harness concept; the physics; MCP servers). **04–06 extend it** (Skills; the end-to-end run; the EIC MCP and AI-infrastructure catalogue). |
| `learners/` | `setup.md`, the glossary (`reference.md`), and reference pages: `about-the-physics.md` (Λ deep-dive), `analysis-approaches.md` (the same analysis in uproot/RDataFrame/TTreeReader/PODIO), and `discuss.md`. |
| `instructors/` | `instructor-notes.md` (scope, timing, pitfalls). |
| `files/mcp-config/` | Committed examples of the configs `eic-mcp config` generates (opencode, VS Code/Copilot), plus a hand-written Copilot-CLI example. |
| `files/skills/` | Example `AGENTS.md`, bridge files, and the `lambda-fit` skill. |
| `extras/` | Stand-alone worked examples (uproot / RDataFrame / TTreeReader / PODIO). |
| `episodes/fig/` | Figures embedded in the lesson. |

## The physics, in one line

Pair every reconstructed proton (PDG `2212`) with every π⁻ (PDG `-211`), compute the invariant
mass `m = √((E_p+E_π)² − |p_p+p_π|²)`, and a Λ⁰ peak rises at 1.115683 GeV over a combinatorial
background. Students reconstruct it themselves by driving the MCP tools from natural-language
prompts — the lesson includes no analysis code or data.

## Build and preview locally

This lesson uses [The Carpentries Workbench][workbench] (the `sandpaper`/`pegboard`/`varnish` R
packages — no Ruby/Jekyll). In an R session:

```r
# one-time install
install.packages("sandpaper", repos = c("https://carpentries.r-universe.dev/", getOption("repos")))

sandpaper::serve()            # build and live-preview at http://localhost:4321
sandpaper::validate_lesson()  # check episode formatting and internal links
```

See the [Workbench documentation][workbench] for details.

## Data

The lesson includes no data. Inside eic-shell the assistant **finds** a dataset with the
`rucio` tools, **verifies** the files with `xrootd`, and **reads** a `root://` URL in place with
`uproot` — no download, and no credentials (the shared read-only `eicread` account is built in).

## Verify it works

Start the servers (`eic-mcp up`), launch `opencode`, and run `/mcp` — `uproot`, `xrootd`, and
`rucio` should be connected. Then work through [Episode 3](episodes/03-mcp-servers.md).

## License

Instructional material is [CC-BY 4.0](LICENSE.md); code is MIT. See [LICENSE.md](LICENSE.md).

## Acknowledgements

Built for an ePIC generative-AI workshop. Uses the ePIC
[`uproot-mcp-server`](https://github.com/eic/uproot-mcp-server),
[`xrootd-mcp-server`](https://github.com/eic/xrootd-mcp-server), and
[`rucio-eic-mcp-server`](https://github.com/eic/rucio-eic-mcp-server).

[workbench]: https://carpentries.github.io/sandpaper-docs/
