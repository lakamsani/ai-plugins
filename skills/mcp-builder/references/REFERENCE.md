# MCP Builder Reference

## MCP Protocol Basics

- Transport: stdio (local) or SSE/HTTP (remote)
- Message format: JSON-RPC 2.0
- Capabilities: tools, resources, prompts

## Tool Response Format

```json
{
  "content": [
    { "type": "text", "text": "string result" }
  ]
}
```

## Error Handling

Throw `McpError` with standard JSON-RPC error codes:
- `-32600` Invalid request
- `-32601` Method not found
- `-32602` Invalid params
- `-32603` Internal error

## Claude Code Integration

Add to `.claude/settings.json`:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["path/to/dist/index.js"],
      "env": {}
    }
  }
}
```
