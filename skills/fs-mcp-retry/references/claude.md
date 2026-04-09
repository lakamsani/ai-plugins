# Claude Packaging Notes

This repo packages `fs-mcp-retry` as an Agent Skills spec skill instead of a Codex-only plugin.

## Why

- Claude can consume repo-installed skills more directly than Codex plugin manifests.
- The reusable part of this package is the refresh helper script plus the workflow instructions.
- Codex-specific files such as `.codex-plugin/plugin.json` and command markdown are not portable to Claude.

## Expected Host Capabilities

The host should be able to:

- parse the first token as an MCP alias
- invoke MCP tools for that alias
- run `python3 skills/fs-mcp-retry/scripts/refresh_mcp_oauth.py <alias> --force`
- retry the original MCP request once

## Config Assumptions

By default the helper script uses:

- `~/.codex/config.toml`
- `~/.mcp-auth`

If Claude stores MCP config elsewhere, pass overrides:

```bash
python3 skills/fs-mcp-retry/scripts/refresh_mcp_oauth.py \
  vamsee-fs-remote \
  --force \
  --config /path/to/config.toml \
  --auth-root /path/to/.mcp-auth
```

## Suggested Claude Wrapper

Use a Claude command or local instruction that says:

1. Parse the first token as the MCP alias.
2. Execute the request once.
3. If the error indicates expired or invalid OAuth access, run the helper script.
4. Retry once.
5. Report whether a refresh was needed.
