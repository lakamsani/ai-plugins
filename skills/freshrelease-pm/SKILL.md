---
name: freshrelease-pm
description: >
  Freshrelease project management — filter and manage tasks, track sprints and epics,
  get epic insights, manage test cases and test runs, search users, create bugs.
  Use when the user asks about sprints, epics, tasks, stories, bugs, test cases,
  or Freshrelease project tracking.
license: MIT
compatibility: Requires Freshrelease MCP server (freshrelease)
metadata:
  author: lakamsani
  version: "1.0"
  category: project-management
allowed-tools: Bash Read Write
---

# Freshrelease Project Management

Manage engineering work items, sprints, epics, and QA workflows via the Freshrelease MCP integration.

## When to Use

Activate when the user mentions:
- Sprints, sprint planning, sprint velocity, current sprint
- Epics, epic progress, epic insights
- Tasks, stories, bugs, issues, work items
- Test cases, test runs, QA, test coverage
- Freshrelease, project tracking, backlog
- ICS (Initiative Commitment Sheet), delivery tracking

## Available Operations

### Tasks & Issues
- `fr_filter_tasks` — Filter tasks by status, assignee, sprint, epic, tags, type
- `fr_get_all_tasks` — List all tasks in a subproject
- `fr_get_task` — Get full task details by key or ID
- `fr_create_bug` — File a new bug with title, description, priority
- `get_task_default_and_custom_fields` — Get available fields for task creation
- `fr_get_issue_form_fields` — Get form fields for a specific issue type
- `fr_get_all_issue_type_form_fields` — Get form fields for all issue types
- `add_notes_or_comment_in_issue` — Add comments to tasks

### Sprints
- `fr_get_current_subproject_sprint` — Get the active sprint
- `fr_get_sprint_by_name` — Look up a sprint by name

### Epics & Releases
- `fr_get_epic_insights` — Get epic progress, completion %, story breakdown
- `fr_get_release_by_name` — Look up a release by name
- `fr_get_tag_by_name` — Look up a tag by name

### Test Management
- `fr_list_testcases` — List all test cases
- `fr_get_testcase` — Get test case details
- `fr_get_testcases_by_section` — Get test cases grouped by section
- `fr_get_testcase_form_fields` — Get fields for creating test cases
- `fr_add_testcases_to_testrun` — Add test cases to a test run
- `fr_get_testrun_summary` — Get test run results summary
- `fr_link_testcase_issues` — Link test cases to issues
- `fr_testcase_filter_summary` — Filter and summarize test cases

### Project & Users
- `fr_get_project` — Get project details
- `get_subproject_id_by_name` — Resolve subproject name to ID
- `fr_search_users` — Search for team members

### Cache
- `fr_clear_all_caches` — Clear all cached data
- `fr_clear_filter_cache` — Clear filter cache only

## Tips
- Use `get_subproject_id_by_name` first when working with a specific subproject
- `fr_get_epic_insights` is the best way to get delivery progress for leadership reporting
- Always use `fr_filter_tasks` with specific filters rather than `fr_get_all_tasks` for large projects
