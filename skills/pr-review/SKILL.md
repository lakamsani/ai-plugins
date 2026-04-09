---
name: pr-review
description: >
  Structured pull request code review — checks for security vulnerabilities, performance issues,
  correctness bugs, test coverage gaps, and style consistency. Use when the user asks to review
  a PR, review code changes, check a diff, or do a code review.
license: MIT
metadata:
  author: lakamsani
  version: "1.0"
  category: code-quality
allowed-tools: Bash(git:*) Bash(gh:*) Read Grep Glob
---

# Pull Request Review

Perform a structured, thorough code review on pull request changes.

## When to Use

Activate when the user mentions:
- Review a PR, review this pull request
- Check my changes, review my code, look at this diff
- Code review, security review, performance review

## Review Process

### 1. Gather Context
```bash
# Get PR details
gh pr view <number> --json title,body,files,commits,additions,deletions

# Get the diff
gh pr diff <number>

# Check CI status
gh pr checks <number>
```

### 2. Review Checklist

For each changed file, evaluate:

**Security**
- [ ] No secrets, keys, or credentials in code
- [ ] Input validation at system boundaries
- [ ] No SQL injection, XSS, command injection vectors
- [ ] Auth/authz checks in place for new endpoints

**Correctness**
- [ ] Logic handles edge cases (nil, empty, overflow)
- [ ] Error handling is appropriate (not swallowed)
- [ ] Concurrency safety (races, deadlocks)
- [ ] Database migrations are reversible and safe

**Performance**
- [ ] No N+1 queries or unbounded fetches
- [ ] Appropriate indexing for new queries
- [ ] No unnecessary allocations in hot paths

**Tests**
- [ ] New behavior has test coverage
- [ ] Edge cases are tested
- [ ] Tests are deterministic (no flaky timing)

**Style**
- [ ] Consistent with surrounding code
- [ ] No unnecessary refactoring mixed with feature work
- [ ] Clear naming, no magic numbers

### 3. Report Format

Present findings as:
```
## PR Review: <title>

### Summary
<1-2 sentence overview>

### Issues Found
- **[CRITICAL]** description (file:line)
- **[WARNING]** description (file:line)
- **[NIT]** description (file:line)

### Looks Good
- <positive callouts>

### Verdict
APPROVE / REQUEST_CHANGES / COMMENT
```

## Tips
- Focus on substantive issues, not style nitpicks
- If the PR is too large (>500 lines), suggest splitting it
- Always check the test changes alongside the implementation
