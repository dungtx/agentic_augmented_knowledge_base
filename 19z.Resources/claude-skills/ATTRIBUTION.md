# Vendored skills — attribution

The skill directories alongside this file (`a11y-debugging`, `chrome-devtools`,
`chrome-devtools-cli`, `debug-optimize-lcp`, `memory-leak-debugging`,
`troubleshooting`) are vendored from the official Chrome DevTools MCP plugin:

- Source: https://github.com/ChromeDevTools/chrome-devtools-mcp (skills/), v1.2.0
- License: Apache-2.0 (see LICENSE-chrome-devtools-mcp)

Why vendored instead of installing the `chrome-devtools-mcp` plugin: that plugin
ships its own MCP server, which duplicates the chrome-devtools server already
provided by the `ecc` plugin (two identical servers -> duplicate tools, possible
two Chrome instances, agentic tool-selection ambiguity). The skills reference
chrome-devtools tools by capability (no hardcoded tool IDs), so they drive ecc's
single server unchanged. Vendoring keeps the debugging skills while avoiding the
redundant server -- and survives reinstalls (no cached-plugin edits required).

To sync upstream improvements, re-copy skills/ from the upstream repo at the
pinned version and update this note.
