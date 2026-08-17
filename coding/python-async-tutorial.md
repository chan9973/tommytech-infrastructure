---
created: 2026-08-15T12:05:00+08:00
tags: [async, python, testing]
---

# Async Python Tutorial

## What is Async/Await?

Async allows non-blocking I/O operations like network requests or file reads. This improves performance when doing multiple concurrent tasks.

## Basic Example

```python
import asyncio

async def fetch_data(url):
    # Simulate async operation (in real code: aiohttp.get(url))
    await asyncio.sleep(1)  # 1 second delay
    return "Success!"

async def main():
    # Run multiple tasks concurrently
    results = await asyncio.gather(
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3")
    )
    print(results)  # ['Success!', 'Success!', 'Success!']

asyncio.run(main())
```

## When to Use Async

- ✅ Multiple independent operations (network, file I/O)
- ⚠️ CPU-bound tasks don't benefit from async
- ❌ Synchronous code blocks the event loop (avoid in async functions)

See: [[deep-learning-fundamentals]] for research on performance optimization techniques.
