# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Date:** 2025-11-19
**Version:** 1.1
**Author:** uweli

## Guide References

See `.claude/guides/` for detailed guidance:
- **GUIDE_DOCS.md** - Documentation standards and file structure
- **GUIDE_PROJECT.md** - Project principles and token efficiency
- **GUIDE_TODO.md** - Todo file naming, structure, and writing standards

## Project Overview

Storage Manager - A custom application for managing food inventory, recipes, and meal planning.

## Project Principles

### Token Efficiency
- Keep files and file lengths minimal
- Every element has a cost - maintain only what's essential
- **Archive folder:** Non-essential materials go to `/archive`. Ignore this folder unless explicitly requested
- **Completed todos:** Finished todo files go to `/todo/done`. Ignore this folder to focus on active tasks

### Version Control
- Project uses Git version control
- SQLite databases (`data/*.db`) and application data are excluded from Git
- All source code, config templates, and documentation are tracked

### Git Commit Guidelines

**Commit Categories:**
- `[CODE]` - Implementation work (src/, main.py, tests/)
- `[CONCEPT]` - Design and architecture (requirements/, specs/, config/, templates/)
- `[DOC]` - Documentation (docs/, README updates)
- `[SETUP]` - Environment and tooling (requirements.txt, pyproject.toml, .venv setup, package installation)
- `[CLAUDE]` - Claude Code configuration (.claude/agents/, .claude/guides/, .claude/audit/, CLAUDE.md)
- `[ORGA]` - Project organization (todo/, file restructuring, .gitignore)

**Categorization Rules:**
- `src/`, `main.py`, `tests/` → `[CODE]`
- `requirements/`, `specs/`, `config/`, `templates/` → `[CONCEPT]`
- `docs/`, README files → `[DOC]`
- `requirements.txt`, `requirements-dev.txt`, `pyproject.toml`, package setup → `[SETUP]`
- `.claude/agents/`, `.claude/guides/`, `.claude/audit/`, `CLAUDE.md` → `[CLAUDE]`
- `todo/`, `.gitignore`, directory restructuring → `[ORGA]`
- Mixed changes → Prefer separate commits; if not feasible, use dominant category

**Commit Message Structure:**
```
[CATEGORY] Brief imperative description
```

**Don't add this:**
  🤖 Generated with [Claude Code](https://claude.com/claude-code)

  Co-Authored-By: Claude <noreply@anthropic.com>"&& git status

**Examples:**
- `[CODE] Implement product inventory manager`
- `[CONCEPT] Define unit conversion system for measurements`
- `[DOC] Add API documentation for recipe scaling`
- `[SETUP] Add pytest and coverage configuration`
- `[CLAUDE] Add project-context-auditor agent configuration`
- `[ORGA] Move completed todos to done directory`

