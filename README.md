# ai-plugins

A marketplace of AI agent skills and plugins for Claude Code and other AI coding agents.

## Install Skills

```bash
# Install all skills from this repo
npx skills add lakamsani/ai-plugins

# Install a specific skill
npx skills add https://github.com/lakamsani/ai-plugins/tree/main/skills/freshservice-ops

# Install globally (available in all projects)
npx skills add -g lakamsani/ai-plugins
```

## Available Skills

| Skill | Description |
|-------|-------------|
| [freshservice-ops](skills/freshservice-ops/) | Freshservice ticket, asset, and service catalog operations via MCP |
| [freshrelease-pm](skills/freshrelease-pm/) | Freshrelease project management — sprints, epics, tasks, and test cases |
| [databricks-analytics](skills/databricks-analytics/) | Query and explore Databricks warehouses via Baikal MCP |
| [pr-review](skills/pr-review/) | Structured pull request review with security, performance, and correctness checks |
| [mcp-builder](skills/mcp-builder/) | Scaffold and test new MCP server integrations |

## Repo Layout

```
ai-plugins/
├── skills/                    # Primary skills directory (npx skills scans here)
│   ├── freshservice-ops/
│   │   └── SKILL.md
│   ├── freshrelease-pm/
│   │   └── SKILL.md
│   ├── databricks-analytics/
│   │   └── SKILL.md
│   ├── pr-review/
│   │   └── SKILL.md
│   └── mcp-builder/
│       ├── SKILL.md
│       └── references/
├── .claude-plugin/
│   └── marketplace.json       # Claude Code plugin marketplace manifest
├── .claude/
│   └── skills/                # Claude-native skills path (symlink targets)
├── .agents/
│   └── skills/                # Agent-agnostic canonical path
└── README.md
```

## Creating a New Skill

1. Create a directory under `skills/` with a lowercase hyphenated name
2. Add a `SKILL.md` with YAML frontmatter (`name` and `description` required)
3. Optionally add `scripts/`, `references/`, and `assets/` subdirectories
4. Validate: the `name` field must match the directory name

See the [Agent Skills Specification](https://github.com/agentskills/agentskills) for full details.

## Compatibility

Works with any agent that supports the [Agent Skills spec](https://agentskills.io):
- Claude Code
- Cursor
- Windsurf
- Cline
- And many more

## License

MIT
