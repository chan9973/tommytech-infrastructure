---
name: bug-fixing-workflow
description: "Systematic approach to finding and fixing edge-case bugs in test failures with pytest"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [debugging, testing, pytest, bug-fixing, tdd]
    related_skills: [test-driven-development, systematic-debugging]
---

# Bug-Fixing Workflow for Test Failures

## Overview

A systematic approach to audit repositories, find edge-case bugs revealed by failing tests, fix them, and run tests until all pass.

## When to Use

- Tests are failing in your repository
- You need to audit code for bugs
- Refactoring legacy code with test coverage
- Quality assurance for code changes

## The Five-Phase Workflow

### Phase 1: Repository Discovery

1. **Identify project structure**
   - Look for `README.md`, `pyproject.toml`, `setup.py`
   - Find source directories (`src/`, `lib/`)
   - Locate test directories (`tests/`, `test/`)

2. **Understand the test framework**
   ```bash
   find . -name "test_*.py" -o -name "*_test.py"
   pytest --collect-only  # See what tests exist
   ```

3. **Explore source code**
   - Read source files referenced in tests
   - Understand class/module structure
   - Identify potential edge cases

### Phase 2: Test Execution & Analysis

4. **Run initial test suite**
   ```bash
   pytest tests/ -v --tb=short
   ```

5. **Analyze failures**
   - Record test names and failure types
   - Examine stack traces
   - Identify root causes

### Phase 3: Bug Identification

6. **Common bug patterns to look for**

| Pattern | Symptom | Fix |
|---------|---------|-----|
| Incorrect split | Data lost after delimiter | Use `split('=', 1)` |
| Missing directory creation | FileNotFoundError | Use `os.makedirs(exist_ok=True)` |
| Boolean strings | 'true' stays string | Check `.lower() in ('true', 'false')` |
| List detection | Comma values not lists | Smart split based on content |
| Type conversion | Wrong type parsed | Try int→float→str with fallback |
| None handling | TypeError on None input | Check before operation |
| Permission errors | Access denied | Use user-writable temp dirs |
| Unicode handling | Comma splits unicode | Only split if neither side is number |

### Phase 4: Bug Fixing

7. **Fix bugs systematically**
   - Fix one bug at a time
   - Run tests after each fix
   - Document changes

8. **Verify with tests**
   ```bash
   pytest tests/ -v  # All should pass
   ```

### Phase 5: Verification Checklist

- [ ] All tests pass (0 failures)
- [ ] No new warnings or errors
- [ ] Edge cases handled (empty, unicode, special chars)
- [ ] Error messages are informative
- [ ] Type conversions are robust

## Detailed Bug Patterns

### Bug 1: Value with Equals Sign
- **Problem**: `split('=')` on `query=SELECT * FROM users WHERE id=1` loses `=1`
- **Fix**: Use `split('=', 1)` to preserve rest of value

### Bug 2: Directory Creation
- **Problem**: `open(filepath, 'w')` fails if parent directory doesn't exist
- **Fix**: `os.makedirs(os.path.dirname(filepath), exist_ok=True)` before open

### Bug 3: Boolean Parsing
- **Problem**: String `'true'` not converted to boolean `True`
- **Fix**: Check `value.lower() in ('true', 'false')` and return appropriate bool

### Bug 4: List Detection Heuristic
- **Problem**: Comma in unicode text splits incorrectly
- **Fix**: Only split on comma if neither side is a valid number

### Bug 5: String Processing Edge Cases
- **Problem**: Whitespace and empty strings in split results
- **Fix**: Strip whitespace first, then filter empty strings: `[w for w in text.split(' ') if w]`

### Bug 6: None Input Handling
- **Problem**: Calling `len(None)` raises TypeError
- **Fix**: Check for None at the start and raise meaningful error

### Bug 7: Temp File Permissions
- **Problem**: Permission denied writing to system temp directory
- **Fix**: Use user-writable directories: `os.path.join(tempfile.gettempdir(), 'user_cache')`

## Verification

Before completing:
- All tests pass with `pytest tests/ -v`
- No regression in related functionality
- Code is documented with comments explaining fixes