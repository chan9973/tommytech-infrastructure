# Bug Pattern Reference

## From Music Player Development Session (2026-08-17)

### File: yt_downloader.py - Permission Error

**Error:**
```
[Errno 13] Permission denied: 'C:\Users\tommy\AppData\Local\Temp\tmpwqrxxm8q.wav'
```

**Root Cause:**
- `tempfile.gettempdir()` returns system temp directory with restricted permissions
- Application cannot write to `C:\Users\tommy\AppData\Local\Temp\`

**Fix:**
```python
# Use user-writable directory instead
temp_dir = os.path.join(os.path.expanduser("~"), "Downloads", "temp_cache")
os.makedirs(temp_dir, exist_ok=True)
temp_file = stream.download(output_path=temp_dir, filename="temp_audio")
```

### File: processor.py - String Processing

**Test Failure:**
```
test_filters_empty_words FAILED
assert '' not in ['hello', '', '', '', 'world']
```

**Root Cause:**
- `text.split(' ')` on "hello world" with multiple spaces creates empty strings
- No filtering of empty strings from result

**Fix:**
```python
# Filter empty strings from split
words = [w for w in text.split(' ') if w]
```

**Also needed:**
```python
# Handle None input
if text is None:
    raise TypeError("Input cannot be None")

# Strip whitespace first
text = text.strip()
```

### File: legacy_parser.py - Value with Equals Sign

**Test Failure:**
```
test_parse_value_with_equals_sign FAILED
{'query': 'SELECT * FROM users WHERE id'} != {'query': 'SELECT * FROM users WHERE id=1'}
```

**Root Cause:**
- `line.split('=')` breaks on ALL `=` signs, not just the first
- Value `SELECT * FROM users WHERE id=1` becomes `SELECT * FROM users WHERE id`

**Fix:**
```python
# Split on first '=' only
parts = line.split('=', 1)
key = parts[0].strip()
value = parts[1].strip() if len(parts) > 1 else ''
```

## Common Pytest Issues

### Test passes immediately = testing wrong thing
```
# BAD - This test passes without implementing
result = SimpleCalculator.add(5, 3)
assert result == 8  # Implementation already correct

# GOOD - Test catches wrong implementation
result = SimpleCalculator.subtract(3, 10)
assert result == -7  # Catches sign bug
```

### Use test-specific temp directories
```python
import tempfile
import os

def test_file_operations():
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test.txt")
        # ... test file operations
        # Auto-cleaned up
```

## Debug Commands Used

```bash
# Run specific test
pytest tests/test_module.py::test_name -v

# Run all tests
pytest tests/ -v

# Check for syntax errors
python -m py_compile file.py

# Check file exists
os.path.exists(filepath)
```