---
name: hermes-tweet
description: >
  Use Hermes Tweet to install, validate, and safely route Hermes Agent X/Twitter
  explore, read, and explicit action workflows. Use when a Hermes Agent session
  needs social context, authenticated account reads, or guarded account actions.
license: MIT
metadata:
  author: Xquik-dev
  version: "0.1.6"
  repository: "https://github.com/Xquik-dev/hermes-tweet"
---

# Hermes Tweet

Hermes Tweet is a Hermes Agent plugin for X/Twitter workflows. Use it when the
user wants Hermes Agent to explore public X/Twitter routes, read authenticated
account data, or perform explicitly approved account actions.

## When to Use

Activate when:

- The user asks to add X/Twitter capabilities to Hermes Agent.
- A Hermes Agent workflow needs tweet exploration, account reads, search, or
  social monitoring.
- The user explicitly asks for posting, replying, liking, following, or other
  account-changing actions through Hermes Agent.

Do not use this skill for generic social-media automation outside Hermes Agent.

## Setup

Install the plugin from the source repository:

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

Configure `XQUIK_API_KEY` in the local Hermes runtime environment before using
authenticated read tools. Enable action tools only for sessions where the user
intentionally sets:

```bash
HERMES_TWEET_ENABLE_ACTIONS=true
```

Never ask the user to paste API keys, cookies, tokens, or private account data
into chat, issues, docs, or pull requests.

## Workflow

1. Confirm the plugin is installed:

```bash
hermes plugins list
hermes tools list
```

2. Use `tweet_explore` first. It maps available routes and works without
   credentials.
3. Use `tweet_read` only after `XQUIK_API_KEY` is configured.
4. Use `tweet_action` only after the user approves the exact account-changing
   operation and `HERMES_TWEET_ENABLE_ACTIONS=true` is set.
5. Summarize results with source links, timestamps, and any setup blockers.

## Safety Rules

- Keep action workflows off for research-only sessions.
- Do not pass credentials or private account data as tool arguments.
- Do not guess live account state, metrics, or trend data.
- Do not retry writes after authentication or permission failures.
- Resolve the relevant route with `tweet_explore` before calling read or action
  tools.

## Verification

Expected baseline:

- `tweet_explore` is available without credentials.
- `tweet_read` appears only when `XQUIK_API_KEY` is configured.
- `tweet_action` appears only when `XQUIK_API_KEY` is configured and
  `HERMES_TWEET_ENABLE_ACTIONS=true`.

References:

- Repository: <https://github.com/Xquik-dev/hermes-tweet>
- Package: <https://pypi.org/project/hermes-tweet/>
- Hermes Agent: <https://github.com/NousResearch/hermes-agent>
