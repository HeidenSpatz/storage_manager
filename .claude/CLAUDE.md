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

**Commit Message Structure:**
```
Brief imperative description
```

**Don't add this:**
  🤖 Generated with [Claude Code](https://claude.com/claude-code)

  Co-Authored-By: Claude <noreply@anthropic.com>"&& git status


