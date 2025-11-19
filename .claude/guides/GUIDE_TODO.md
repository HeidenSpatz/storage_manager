# Todo File Guide

**Date:** 2025-11-16
**Version:** 1.0
**Author:** uweli

## Executive Summary

Defines the naming scheme, structure, and writing standards for todo files in the stock analysis project.

<br><br>

## Naming Scheme

**Format:**
```
<start_date>_<category>_<description>.md
```

**Components:**
- `start_date`: YYYY-MM-DD format
- `category`: CODE | CONCEPT | DOC | SETUP | CLAUDE | ORGA (matching commit categories)
- `description`: Brief snake_case description (2-4 words)

**Examples:**
- `2025-11-16_CODE_implement_metrics_calculator.md`
- `2025-11-16_CONCEPT_design_analysis_profiles.md`
- `2025-11-16_DOC_api_documentation.md`
- `2025-11-16_SETUP_install_dependencies.md`
- `2025-11-16_CLAUDE_context_audit_fixes.md`
- `2025-11-16_ORGA_restructure_directories.md`

<br><br>

## File Structure

Todo files must follow the documentation standards defined in `.claude/guides/GUIDE_DOCS.md`:
- Header with clear title
- Metadata (Date, Version, Author)
- Executive Summary (1-2 sentences)
- Sections with hierarchical headings
- `<br><br>` after major sections

<br><br>

## Todo Item Standards

**Writing Guidelines:**
- Use active verbs (Implement, Create, Add, Update, Fix, Refactor)
- Be specific and actionable
- Include file paths or function names where applicable
- Avoid vague descriptions (e.g., "work on metrics" → "Implement PE ratio calculation in metrics_calculator.py")

**Format:**
```markdown
## Tasks

- [ ] Implement data fetcher for Yahoo Finance API
- [ ] Add SQLite schema for prices table in data_acquisition.py
- [ ] Create unit tests for metrics calculations
- [ ] Update config.yaml with refresh_interval_days parameter
```

**Examples of Good vs Bad:**

❌ Bad:
- [ ] Fix the code
- [ ] Update metrics
- [ ] Work on database

✅ Good:
- [ ] Fix division by zero error in calculate_pe() at src/metrics_calculator.py:45
- [ ] Update PEG ratio calculation to use 5-year growth rate
- [ ] Add foreign key constraint between prices and fundamentals tables

<br><br>

## Location

Store todo files in `/todo` directory (excluded from Git via .gitignore).

<br><br>
