# Validation — 2026-09-12

Zero attribution: never add co-author, AI, or tool attribution to output.

New skill routing: **20/20**, unanimous across three independent local judges using only the catalog and shuffled queries. Model: inherited session model; no override. Catalog: live kit descriptions plus the pinned external snapshot. The full sweep scored **348/352**.

Four failed cases belong to unchanged descriptions:

| Skill | Query | Result |
| --- | --- | --- |
| polish-batch | The save button doesn't actually save — log it | No majority: /triage, none, /to-tickets |
| tdd-loop | Refactor the scanner module without changing behavior — make sure the tests keep us honest | Majority none; expected trigger |
| writing-kit-skills | Where do the canonical one-liners for the kit live? | Unanimous graphify; expected trigger |
| writing-kit-skills | Run the trigger evals for the kit | Unanimous /writing-kit-skills; expected no-trigger |

`score.py --write-snapshot` refused this incomplete sweep. The existing description snapshot was preserved; no passing provenance was fabricated. `bash tools/validate.sh` passes all checks except check 10, which requires the new skill in a successful full-sweep snapshot. This remains a local draft until the existing routing failures are resolved and that sweep passes.

Strict YAML validation used PyYAML in a temporary virtual environment. The skill-creator quick validator passed. Both ship-policy copies remain byte-identical; agents-md markers agree at v27.

Run evidence is retained locally at `/tmp/worktree-skill-evals.6UXMam/`: catalog, query manifest, queryset, three JSONL ballots, score output, behavioral fixtures and decisions. Live Git fixture evidence is at `/var/folders/xp/ld35mwbs3kg3sxxb556w1j5w0000gn/T/worktree-skill-git-oool7zy9/results.json`. These temporary paths are execution evidence, not installed-skill dependencies.
