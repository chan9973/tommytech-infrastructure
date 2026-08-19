# Obsidian Auto-Ingest Runner - Runbook

## Purpose
Periodically discovers `.tmp` artifacts in the vault workspace, routes them through `obsidian-ingest.py`, and maintains a deterministic audit trail in `obsidian-cron.log`.

## Directory Hierarchy
```
E:\tommy vault\tommy vault\Read & Write\
├── .hermes_cron\
│   ├── obsidian-cron.py              # Core ingestion loop
│   ├── run_obsidian_cron.bat         # Windows batch entrypoint
│   ├── quick-run.sh                  # Quick one-off invocation
│   └── obsidian-cron.log             # Append-only execution log
└── (vault content / Scripts/obsidian-ingest.py external)

```

## Invocation Modes

### One-off scan & process
```bat
python "E:/tommy vault/tommy vault/Read & Write/.hermes_cron/obsidian-cron.py" --verbose
```

### Infinite loop (every 60s)
```bat
while true; do python "E:/tommy vault/tommy vault/Read & Write/.hermes_cron/obsidian-cron.py"; done
```

### Background daemon (Unix/Linux)
```bash
daemonize; python obsidian-cron.py --daemon --interval 60
```

## Logging Specification
- Destination: `obsidian-cron.log` (path-resolved absolute)
- Format: `ISO8601Timestamputile8s-level-message`
- Exits cleanly on "UNCHANGED" (no artifacts found)

## Environment Variables
```
BASE_DIR   Optional override for vault root (default: "E:/tommy vault/tommy vault/Read & Write")
```

## Safety Checks (Built-in)
- `.tmp` files only (via filename suffix)
- Size threshold: < 100KB
- Freshness threshold: modified < 60s ago
- Fails fast on unknown paths
- Non-fatal ingest/delete errors are logged but do not crash
- `UNCHANGED` exit (code 0) when scan returns empty set

## Maintenance Notes
- Review `obsidian-cron.log` weekly for back-to-back CRITICAL entries
- Prune old `.tmp` artifacts manually if they appear outside cron windows
- Keep Python stdlib at minimum; no third-party deps

Tommy Chan — last reviewed: 19 Aug 2026 (CRON: auto-refresh)