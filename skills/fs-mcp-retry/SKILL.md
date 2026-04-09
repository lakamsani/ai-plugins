---
name: fs-mcp-retry
description: Retry a request against a configured MCP alias after refreshing OAuth tokens from ~/.mcp-auth when the first attempt fails with an auth error.
---

# FS MCP Retry

Use this skill when a request should be sent through an MCP alias and retried once after an OAuth token refresh.

This is intended for hosts that can:
- call MCP tools bound to a configured alias
- run a local helper script
- retry the original request after a failed auth attempt

## Inputs

Treat the first token as the MCP alias. Treat the remaining text as the request to send through that alias.

Example:

```text
vamsee-fs-remote fetch tickets
```

## Workflow

1. Parse the first token as the MCP alias.
2. Treat the remaining text as the query.
3. Resolve the alias from the local MCP config.
4. Infer the tool namespace as `mcp__<alias with '-' replaced by '_'>__*`.
5. Execute the request once.
6. If the request fails because of authentication or expired tokens, run:

```bash
python3 scripts/refresh_mcp_oauth.py <alias> --force
```

7. Retry the original request once.
8. Report whether a refresh was needed.

## Rules

- Do not guess an alias that is not configured locally.
- If the alias is missing, ask for it.
- If the query is empty, ask what to do with that alias.
- Retry at most once.
- Surface refresh failures directly.

## Portability

The helper script defaults to Codex locations:
- config: `~/.codex/config.toml`
- auth cache: `~/.mcp-auth`

Override these when a different host stores MCP config elsewhere:

```bash
python3 scripts/refresh_mcp_oauth.py <alias> --force --config /path/to/config.toml --auth-root /path/to/.mcp-auth
```
