# Routing sweep 2026-10-22 (b)

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Reason: `/grill-with-field` was added, `/feature-prompt` and `/port-feature` descriptions now name it, and three borderline descriptions were sharpened. Final inputs: [catalog](catalog.md), [queries](queryset.md), [manifest](query-manifest.json); final ballots `j1.jsonl`, `j2.jsonl`, `j3.jsonl`.

Four sweeps were run, each with three fresh catalog-only judge sessions on `claude-opus-5-5`:

1. `sweep1/`: 604/607 after adding `/grill-with-field` (16/16). Two-to-one misses on `/deploy-watch` ("Did my change make it to staging?" → `/factory`), `/incident-triage` ("Check the production logs for errors" captured), and `/writing-kit-skills` ("Move this skill's long examples out of SKILL.md properly" captured).
2. `sweep2/`: 606/607 after `/deploy-watch` 2.0.3 and `/incident-triage` 0.2.1. The first `/writing-kit-skills` rewording made its miss unanimous.
3. `sweep3/`: 607/607 after `/writing-kit-skills` 0.6.1 fires only when the request names the kit or a kit skill.
4. Final: 607/607 after `/feature-prompt` 0.3.3 and `/port-feature` 0.2.2 replaced `/grill-with-docs` with `/grill-with-field` in their descriptions.

Sweeps 1 to 3 were cast against earlier catalogs and are kept as evidence, not as passing runs. Judge independence rests on fresh sessions with no repository access; the hashes identify the files used.
