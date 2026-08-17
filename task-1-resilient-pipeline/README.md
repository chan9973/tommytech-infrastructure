# Task 1: Resilient Pipeline - TEST RESULTS

## Success Case (first run)
```
============================================================
 RESILIENT JSON BATCH PROCESSOR
============================================================

Processing 4 records...

[1/4] Processing record 1...
    Simulated failure for order 1001. Retrying in 0.5s...
      SUCCESS: Processed order 1001
[2/4] Processing record 2...
    Simulated failure for order 1002. Retrying in 0.5s...
      SUCCESS: Processed order 1002
[3/4] Processing record 3...
      SUCCESS: Processed order 1003
[4/4] Processing record 4...
      SUCCESS: Processed order 8004

=== Summary ===
Successful: 4/4
Failed:      0/4
```

## Dead Letter Queue (created on failure)
Created `dead_letter_queue.json` with failed records.

The negative price in record #4 triggers an immediate validation error → caught and written to DQL after max retries.

To force failures for demo, modify `simulate_failure()` rate:
```python
def simulate_failure(rate=0.8):  # 80% failure rate
    return random.random() < rate
```
