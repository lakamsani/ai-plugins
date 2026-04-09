# ai-plugins

A marketplace of AI agent skills and plugins. Built for [Claude Code](https://claude.com/product/claude-code), also compatible with any agent that supports the [Agent Skills spec](https://agentskills.io).

## Getting Started

### Claude Code

```bash
# Add this repo as a plugin marketplace
claude plugin marketplace add lakamsani/ai-plugins

# List available plugins
claude plugin marketplace list

# Install a specific plugin
claude plugin install fs-mcp-retry@ai-plugins
```

Once installed, skills activate automatically when relevant. Slash commands (if any) become available in your session.

### Agent Skills (`npx skills`)

```bash
# Install all skills from this repo
npx skills add lakamsani/ai-plugins

# Install a specific skill
npx skills add https://github.com/lakamsani/ai-plugins/tree/main/skills/fs-mcp-retry

# Install globally (available in all projects)
npx skills add -g lakamsani/ai-plugins
```

## Available Plugins

| Plugin | Description |
|--------|-------------|
| **[fs-mcp-retry](./skills/fs-mcp-retry)** | Retry MCP requests after refreshing OAuth tokens from `~/.mcp-auth`. |

## How Plugins Work

Every plugin follows the same structure:

```
plugin-name/
├── SKILL.md           # Required: YAML frontmatter + agent instructions
├── scripts/           # Optional: executable helpers
├── references/        # Optional: additional docs the agent reads on demand
└── assets/            # Optional: templates, data files
```

- **Skills** encode domain expertise and step-by-step workflows. The agent draws on them automatically when relevant.
- **Scripts** are executable helpers that skills can invoke (e.g., token refresh, API calls).
- **References** provide deeper context loaded on demand, keeping the main skill file concise.

Everything is file-based — markdown, JSON, and scripts. No build steps, no infrastructure.

## Repo Layout

```
ai-plugins/
├── skills/                        # Primary skills directory
│   └── fs-mcp-retry/
│       ├── SKILL.md
│       ├── scripts/
│       │   └── refresh_mcp_oauth.py
│       └── references/
│           └── claude.md
├── .claude-plugin/
│   └── marketplace.json           # Claude Code plugin marketplace manifest
├── .claude/skills/                # Claude-native skills install target
├── .agents/skills/                # Agent-agnostic install target
├── LICENSE
└── README.md
```

## Creating a New Plugin

1. Create a directory under `skills/` with a lowercase hyphenated name
2. Add a `SKILL.md` with YAML frontmatter:

   ```yaml
   ---
   name: my-plugin-name        # Must match directory name
   description: >
     What this plugin does and when to use it.
     Include trigger keywords so the agent knows when to activate.
   license: MIT
   metadata:
     author: lakamsani
     version: "1.0"
   ---
   ```

3. Write agent instructions in the markdown body (keep under 500 lines)
4. Optionally add `scripts/`, `references/`, and `assets/` subdirectories
5. Register the plugin in `.claude-plugin/marketplace.json`:

   ```json
   {
     "name": "my-plugin-name",
     "description": "Short description.",
     "source": "./skills/my-plugin-name"
   }
   ```

6. Update this README's **Available Plugins** table

See the [Agent Skills Specification](https://github.com/agentskills/agentskills) for the full spec.

## Included Plugins

### `fs-mcp-retry`

Host-agnostic retry workflow for remote MCP servers that use OAuth token bundles under `~/.mcp-auth`.

```text
skills/fs-mcp-retry/
├── SKILL.md
├── scripts/
│   └── refresh_mcp_oauth.py
└── references/
    └── claude.md
```

The helper script is portable across hosts because it accepts explicit config overrides:

```bash
python3 skills/fs-mcp-retry/scripts/refresh_mcp_oauth.py <alias> --force \
  --config /path/to/config.toml \
  --auth-root /path/to/.mcp-auth
```

## Compatibility

| Agent | Install method |
|-------|---------------|
| Claude Code | `claude plugin marketplace add lakamsani/ai-plugins` |
| Cursor | `npx skills add lakamsani/ai-plugins` |
| Windsurf | `npx skills add lakamsani/ai-plugins` |
| Cline | `npx skills add lakamsani/ai-plugins` |

## License

MIT
