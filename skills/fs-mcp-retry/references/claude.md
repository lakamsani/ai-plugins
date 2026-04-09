# Multi-Host Integration Notes

## Claude Code

```bash
claude plugin marketplace add lakamsani/ai-plugins
claude plugin install fs-mcp-retry@ai-plugins
```

After installing, run `/reload-plugins` to activate. The skill fires automatically when an MCP tool call fails with an auth/token error.

## Gemini CLI

Gemini reads MCP servers from `~/.gemini/settings.json` under the `mcpServers` key. The refresh script auto-detects this as the first config to check.

## Config Discovery Order

The script checks for configs in this order (first match wins):
1. `~/.claude.json` (JSON, `mcpServers`) — **used when running from Claude Code**
2. `~/.gemini/settings.json` (JSON, `mcpServers`)
3. `~/.codex/config.toml` (TOML, `mcp_servers`)

Override with `--config /path/to/config.json` for any other location.

## Token Storage

All hosts share `~/.mcp-auth/` for OAuth token bundles (managed by `mcp-remote`). The refresh script updates tokens in place so they're immediately available to any host.

## Expected Host Capabilities

The host should be able to:
- Invoke MCP tools for a configured alias
- Run `python3 skills/fs-mcp-retry/scripts/refresh_mcp_oauth.py <alias> --force`
- Retry the original MCP request once
