# Generative AI for Physics Analysis (ePIC tutorial)

A lesson on using an AI coding assistant with MCP tool servers for an ePIC analysis: find a
dataset, read it, and fit the Λ⁰ → p π⁻ invariant-mass peak at 1.1157 GeV. Everything runs in
eic-shell, which includes the servers and the `opencode` assistant. No data download or
credentials are needed.

## Contents

| Path | Contents |
| --- | --- |
| `episodes/` | The six episodes |
| `learners/` | Setup page and glossary |
| `instructors/` | Instructor notes |
| `files/` | Example assistant configs, `AGENTS.md`, and the `lambda-fit` skill |
| `extras/` | The same analysis without MCP (uproot, RDataFrame, TTreeReader, PODIO) |

## Try it

Inside eic-shell:

```bash
eic-mcp up
eic-mcp config opencode
opencode
```

`/mcp` in opencode should list `uproot`, `xrootd`, and `rucio`. Then follow the episodes.

## Build the site

The lesson uses [The Carpentries Workbench][workbench]. With Docker, run `make preview` and then
`make serve`. With R, run `sandpaper::serve()`.

## License

Lesson text is [CC-BY 4.0](LICENSE.md); code is MIT.

[workbench]: https://carpentries.github.io/sandpaper-docs/
