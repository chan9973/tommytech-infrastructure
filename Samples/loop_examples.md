# /loop Command - Practical Examples

The `/loop` feature (via `cronjob`) creates scheduled background tasks that run automatically. Use it for:
- Monitoring web content changes
- Watching system metrics
- Periodic data collection
- Automated reminders & checks

---

## Example 1: Monitor Website Price Changes

Monitor Amazon price drops for your products every 30 minutes.

```python
# Task: Monitor Amazon prices for paper towels, check every 30 minutes
cronjob(action='create', schedule='30m', prompt='Check current prices on Amazon for "paper towels". If any product drops below $8.99, send a notification with the product link.')
```

**What happens:**
- Runs every 30 minutes indefinitely
- Browses Amazon, searches for paper towels
- Compares prices against your threshold
- Sends alerts when price drops occur

---

## Example 2: Daily System Health Check

Run a health diagnostic on your computer daily at 8 AM.

```python
# Task: Daily system health report at 8:00 AM
cronjob(
    action='create', 
    schedule='0 8 * * *',  # Daily at 8 AM
    prompt='Check CPU, RAM, and disk usage. Display open processes running for >2 hours. Summarize available disk space and warn if below 20%.'
)
```

**Schedule options:**
- `'30m'` = Every 30 minutes
- `'every 2h'` = Every 2 hours
- `'0 9 * * *'` = Daily at 9:00 AM
- ISO timestamp: `'2026-12-25T10:00:00'` = One-time execution

---

## Example 3: Monitor GitHub Repository for New Commits

Watch your repository and notify when someone pushes code.

```python
# Task: Monitor GitHub repo for new commits every hour
cronjob(
    action='create',
    schedule='every 1h',
    prompt='Check GitHub repository for new commits, pull requests, or issues. If any are created since last check, list them with links.'
)
```

---

## Example 4: Stock Price Tracker

Monitor stock prices and alert on movements.

```python
# Task: Track stock prices, run every 15 minutes
cronjob(
    action='create',
    schedule='15m',
    prompt='Check current prices for TSLA, AAPL, and NVDA. If any moves more than 2% from previous check, highlight and explain potential reasons.'
)
```

---

## Example 5: Research Paper Discovery

Find new papers in your research area every hour.

```python
# Task: Monitor arXiv for new papers hourly
cronjob(
    action='create',
    schedule='every hour',
    prompt='Search arXiv for new papers in "machine learning" and "reinforcement learning". Summarize the top 5 most cited or relevant papers found since last run.'
)
```

---

## Example 6: Email Inbox Triage

Process important emails first thing each morning.

```python
# Task: Daily email triage at 9 AM
cronjob(
    action='create',
    schedule='0 9 * * *',
    prompt='Check Gmail for unread messages from boss or deadlines. Draft quick replies to urgent items, flag those needing attention over weekend.'
)
```

---

## Example 7: Social Media Content Monitor

Track social media mentions every hour.

```python
# Task: Monitor Twitter/X mentions hourly
cronjob(
    action='create',
    schedule='every hour',
    prompt='Search Twitter for mentions of "Hermes Agent" and "AI automation". Summarize sentiment (positive/negative) and share any viral threads.'
)
```

---

## Example 8: One-Time Task with Specific Deadline

Run a specific check just once at a future time.

```python
# Task: Generate monthly report on the 1st at 9 AM
cronjob(
    action='create',
    schedule='0 9 1 * *',  # Monthly, 1st day at 9 AM
    prompt='Generate monthly productivity summary: tasks completed, time spent, most productive hours. Export to PDF and email to boss.'
)
```

---

## Quick Reference for Schedules

| Schedule | Meaning |
|----------|---------|
| `'30m'` | Every 30 minutes |
| `'every hour'` | Hourly |
| `'every 2h'` | Every 2 hours |
| `'0 9 * * *'` | Daily at 9:00 AM |
| `'0 12 * * *'` | Daily at noon |
| ISO timestamp `'2026-12-25T10:00:00'` | One-time run |

---

## Best Practices

✅ **DO:**
- Start with longer intervals (every hour/day) before going frequent
- Make prompts self-contained (tasks run without context)
- Include clear action items in the prompt
- Set deadlines or time ranges when relevant

❌ **DON'T:**
- Run too frequently (every 1-2 minutes wastes resources)
- Make prompts depend on live variables (use current data)
- Forget to cancel tasks you no longer need
- Use for tasks requiring interactive input

---

## Managing Your Loop Tasks

**List all active loops:**
```python
cronjob(action='list')
```

**Update an existing loop:**
```python
# Find your job_id first with cronjob(list)
cronjob(action='update', job_id='<your_job_id>', schedule='15m')
```

**Pause a running loop:**
```python
cronjob(action='pause', job_id='<your_job_id>')
```

**Stop completely:**
```python
cronjob(action='remove', job_id='<your_job_id>')
```

---

## Pro Tips

1. **Combine with skills**: Attach domain-specific skills for smarter checks
   ```python
   cronjob(
       action='create',
       schedule='hourly',
       prompt='Monitor system performance using terminal commands: check disk, ram, cpu via psutil. Alert if disk <20% or RAM >80%.',
       skills=['terminal']
   )
   ```

2. **Chain tasks**: Let one loop trigger another
   - Loop A collects data
   - Loop B processes reports

3. **Use workspace paths**: Save results to organized folders
   ```python
   # Task saves output to ~/workspace/reports/daily-check.txt
   cronjob(
       action='create',
       schedule='daily',
       prompt='Run health diagnostics and save full report to ~/workspace/reports/health-summary-{{date}}.txt'
   )
   ```

---

Need help customizing a specific use case? Ask: **"Create a loop for monitoring [your task]"**
