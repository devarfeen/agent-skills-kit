# Authoring review

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Load when auditing an existing skill or fixing an observed instruction failure.

### Form follows the failure

Classify the observed failure before writing the fix. Knows the rule, skips it under pressure → prohibition, its replacement, one-clause why. Right behavior, wrong output shape → a positive recipe: the output's parts, in order; prohibition lists invite negotiation. Omits a required element → a required slot in the template it fills. Condition-dependent → a conditional on an observable predicate. Never append nuance ("unless it matters") or exemption clauses; restructure so the rule cannot reach the exempt case.

## Failure modes to hunt

**Sediment** — layers that settle because adding feels safe; prune on every edit. **Sprawl** — over budget even when every line is live; cure by disclosure to `references/`, not by thinning safety language. **Duplication** — the same meaning twice in one file (description↔body, rules↔checklist); keep one. **No-op** — a line the agent already obeys by default; delete the sentence, don't trim it. **Speculative rule** — a line added for a failure no run, transcript, or behavior case has shown; name the observed failure in the change or drop it — zero additions is a valid audit result. **Cache** — text restating what one lookup answers (a script name, a flag list, a directory layout); it goes stale silently. Keep what looking cannot find: the convention, the reason, the gotcha. **Phantom tooling** — documented commands or pointers that don't hold: a flag absent from the script's `--help`, a reference committed as placeholder scaffolding. If scripts ever land, flag↔`--help` parity becomes a validator check.
