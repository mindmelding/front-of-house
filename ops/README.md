# ops

Durable scheduling for the engine. `launchd.template.plist` runs `scripts/sweep.sh` every weekday at 07:00. Install instructions are in the file's header; the rule and the checklist are in `engine/DURABILITY.md`. For Linux, the equivalent is a cron line: `0 7 * * 1-5 /path/to/front-of-house/scripts/sweep.sh`.
