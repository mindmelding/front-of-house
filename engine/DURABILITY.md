---
id: engine-durability
type: process
status: active
confidence: high
last_reviewed: 2026-09-17
---

# Durability: the one rule that decides whether any of this still runs

Learned expensively. Twenty-two scheduled agents were built over two days in May 2026 as in-session routines. They fired for five days and then never again, silently, because the routine mechanism only fires while a session is open. Over the same four months, on the same machine, every automation still alive was a `launchd` job. It was never a discipline problem.

## The rule

**A scheduled job runs from the operating system's scheduler, or it does not exist.**

`launchd` on macOS, `cron` or `systemd` timers on Linux, Task Scheduler on Windows. Never an agent host's in-session routine, whatever it promises.

## The second half

Durable scheduling is necessary and not sufficient. A scheduled job can exit non-zero for months without anyone noticing. So every scheduled thing needs two properties:

1. **It runs without a session open.**
2. **It tells you when it stops.** The sweep writes `overlay/state/heartbeat.json` at start and end; the SessionStart hook reads it and prints `SWEEP STALE` or `SWEEP DID NOT FINISH` the next morning. A job that cannot report its own death is a job that is already dead.

## Checklist before calling any scheduled thing done

- [ ] Scheduled by the OS scheduler, not a host routine.
- [ ] `launchctl list | grep <label>` (or equivalent) shows it loaded.
- [ ] Ran once on its own schedule, unattended, and produced output.
- [ ] Failure is visible without going to look (the heartbeat line in the hook).
- [ ] No placeholder left in the config. Search for `REPLACE_ME` before loading.
- [ ] Secrets come from a file the scheduler can read, not from a shell that only exists in your terminal. For the sweep that file is `overlay/secrets.env` (gitignored), sourced by `scripts/sweep.sh`; `overlay/mcp.json` references it as `${MOONBASE_MCP_KEY}` (Claude Code expands `${VAR}`, not `${env:VAR}`). The first hand run on 2026-09-17 failed for exactly this reason and reported PARTIAL instead of pretending.

## Templates

`ops/launchd.template.plist` and `scripts/sweep.sh`. Copy the shape of a job already proven on the machine rather than writing one from scratch.

## Build it, use it, trust it, then schedule it

Skipping to scheduling is what produced twenty-two jobs nothing dispatched. Run the sweep by hand once. Read its output. Run it by hand again the next day. Then schedule it.
