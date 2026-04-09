# ai-plugins

A marketplace of AI agent skills and plugins for Claude Code and other AI coding agents.

## Install Skills

```bash
# Install all skills from this repo
npx skills add lakamsani/ai-plugins

# Install a specific skill
npx skills add https://github.com/lakamsani/ai-plugins/tree/main/skills/<skill-name>

# Install globally (available in all projects)
npx skills add -g lakamsani/ai-plugins
```

## Available Skills

_No skills published yet._

## Repo Layout

```
ai-plugins/
├── skills/                    # Primary skills directory (npx skills scans here)
│   └── <skill-name>/
│       ├── SKILL.md           # Required: YAML frontmatter + instructions
│       ├── scripts/           # Optional: executable code
│       ├── references/        # Optional: additional docs
│       └── assets/            # Optional: templates, data files
├── .claude-plugin/
│   └── marketplace.json       # Claude Code plugin marketplace manifest
├── .claude/
│   └── skills/                # Claude-native skills path
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
