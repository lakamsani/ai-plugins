---
name: mcp-builder
description: >
  Scaffold, develop, and test MCP (Model Context Protocol) server integrations.
  Generates project boilerplate, tool definitions, and test harnesses for new MCP servers.
  Use when the user wants to create a new MCP server, add MCP tools, build an integration,
  or scaffold an MCP project.
license: MIT
compatibility: Requires Node.js 18+ or Python 3.10+
metadata:
  author: lakamsani
  version: "1.0"
  category: developer-tools
allowed-tools: Bash Read Write Edit Glob Grep
---

# MCP Builder

Scaffold and develop new MCP (Model Context Protocol) server integrations from scratch.

## When to Use

Activate when the user mentions:
- Create/build/scaffold a new MCP server
- Add tools to an MCP server
- MCP integration, Model Context Protocol
- Connect an API as an MCP server

## Scaffolding a New MCP Server

### TypeScript (Recommended)

Generate this structure:
```
my-mcp-server/
├── src/
│   ├── index.ts          # Server entry point
│   ├── tools/            # Tool implementations
│   │   └── example.ts
│   └── types.ts          # Shared types
├── package.json
├── tsconfig.json
└── README.md
```

**package.json essentials:**
```json
{
  "name": "@scope/my-mcp-server",
  "version": "0.1.0",
  "type": "module",
  "bin": { "my-mcp-server": "./dist/index.js" },
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0"
  }
}
```

**Server entry point pattern:**
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new McpServer({ name: "my-server", version: "0.1.0" });

server.tool("tool-name", "Description of what it does", {
  param1: { type: "string", description: "..." }
}, async ({ param1 }) => {
  // implementation
  return { content: [{ type: "text", text: JSON.stringify(result) }] };
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Python

Generate this structure:
```
my-mcp-server/
├── src/
│   └── my_mcp_server/
│       ├── __init__.py
│       ├── server.py     # Server entry point
│       └── tools/
│           └── example.py
├── pyproject.toml
└── README.md
```

## Adding a Tool

Each tool needs:
1. A unique name (lowercase, hyphenated)
2. A clear description (used by the AI to decide when to call it)
3. Input schema (JSON Schema for parameters)
4. Implementation that returns `content` array

## Testing

```bash
# Test with MCP Inspector
npx @modelcontextprotocol/inspector my-mcp-server

# Test stdio transport manually
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | node dist/index.js
```

## References

See `references/` for:
- MCP SDK API reference
- Transport protocol details
- Authentication patterns
