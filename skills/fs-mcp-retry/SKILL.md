---
name: fs-mcp-retry
description: >
  Retry a request against a configured MCP alias after refreshing OAuth tokens from ~/.mcp-auth.
  Supports Gemini CLI (~/.gemini/settings.json), Claude Code, and Codex (~/.codex/config.toml).
  Use when an MCP tool call fails with an auth or expired token error.
---

# FS MCP Retry

Retry MCP requests after automatically refreshing expired OAuth tokens. Works across multiple AI agent hosts.

## When to Use

Activate when:
- An MCP tool call fails with an authentication or expired token error
- The user asks to refresh OAuth tokens for an MCP alias
- The user asks to retry a failed MCP request

## Supported Hosts

| Host | Config location | Format |
|------|----------------|--------|
| Claude Code | `~/.claude.json` | JSON — `mcpServers` |
| Gemini CLI | `~/.gemini/settings.json` | JSON — `mcpServers` |
| Codex | `~/.codex/config.toml` | TOML — `mcp_servers` |

The script auto-detects by checking configs in the order above (first match wins). Pass `--config` to override.

## Workflow

1. Parse the first token as the MCP alias.
2. Treat the remaining text as the query.
3. Resolve the alias from the local MCP config (auto-detected or specified).
4. Infer the tool namespace as `mcp__<alias with '-' replaced by '_'>__*`.
5. Execute the request once.
6. If the request fails because of authentication or expired tokens, run:

```bash
python3 skills/fs-mcp-retry/scripts/refresh_mcp_oauth.py <alias> --force
```

7. Retry the original request once.
8. Report whether a refresh was needed.

## Usage Examples

### Auto-detect config (tries ~/.claude.json, ~/.gemini/settings.json, ~/.codex/config.toml)
```bash
python3 skills/fs-mcp-retry/scripts/refresh_mcp_oauth.py vamsee-fs-mcp-remote --force
```

### Gemini CLI (explicit)
```bash
python3 skills/fs-mcp-retry/scripts/refresh_mcp_oauth.py fs-remote --force \
  --config ~/.gemini/settings.json
```

### Codex (explicit)
```bash
python3 skills/fs-mcp-retry/scripts/refresh_mcp_oauth.py vamsee-fs-remote --force \
  --config ~/.codex/config.toml
```

### Claude Code

Claude Code users install this as a plugin:

```bash
claude plugin marketplace add lakamsani/ai-plugins
claude plugin install fs-mcp-retry@ai-plugins
```

Once installed, the skill activates automatically when an MCP tool call fails with an auth error. Claude Code will run the refresh script and retry the request.

To manually trigger from within a Claude Code session, describe the MCP alias and the failed request — the skill instructions guide the agent through the retry workflow.

## Rules

- Do not guess an alias that is not configured locally.
- If the alias is missing, ask for it.
- If the query is empty, ask what to do with that alias.
- Retry at most once.
- Surface refresh failures directly.

## Config Override

```bash
python3 skills/fs-mcp-retry/scripts/refresh_mcp_oauth.py <alias> --force \
  --config /path/to/config.json \
  --auth-root /path/to/.mcp-auth
```
