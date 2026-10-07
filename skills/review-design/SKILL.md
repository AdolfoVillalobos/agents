---
name: review-design
description: Review a diff's design, module boundaries, and simplicity against existing repository patterns. Use for an architecture or structure pass on a PR, including opportunities to delete unnecessary code. Reports suggestions without implementing them.
---

# Review design and structure

Assess whether the change solves today's problem with understandable boundaries and no unnecessary machinery. Focus on the changed design, rather than a general bug hunt or a repository-wide redesign.

First read the [shared review protocol](../code-review/references/review-protocol.md). It defines scope selection, evidence, severity, and reporting for this pass. Resolve that path relative to this skill, not the repository being reviewed.

## Investigate the design

Read the intent, surrounding code, callers, and comparable modules until you can explain where the responsibility belongs and which constraints it must preserve. Inspect tests for the contract they protect and the package's conventions.

Examine:

1. **Boundaries and cohesion.** Look for domain policy leaking into transport code, dependencies that create cycles, or unrelated responsibilities collected in a utility. Name the concrete cost to callers or future changes already required by this PR.
2. **Unnecessary structure.** Inspect new wrappers, configuration, flags, types, and indirection. A single caller is a reason to investigate, not proof of over-engineering: a boundary may protect an invariant or isolate external I/O.
3. **Duplicated policy.** Compare nontrivial rules with existing helpers. Reuse is justified by matching semantics, not similar syntax. Preserve distinct domain concepts even when their implementations look alike.
4. **Names, contracts, and scale.** Report names that misrepresent behavior, unnecessary public surface, or incompatible contracts. For complexity, queries, or memory concerns, cite a reachable path, realistic input volume, and the resulting cost; distinguish a measured regression from an estimate.
5. **Deletion and test simplicity.** Identify code added by the diff that has no required behavior. Before proposing removal of a flag, alternate path, or test, establish what still depends on it. Tests are redundant only when retained coverage catches the same failure under the same conditions; follow the repository's test structure and preserve distinct boundaries and integration paths.

For each candidate, look for an existing simpler implementation in the repository. Cite it if its semantics fit. Describe the smallest alternative and its trade-off in clarity, performance, or migration cost. If the proposed change merely expresses a preference, discard it.

Keep concrete correctness failures discovered during this pass, but do not claim an exhaustive correctness review. Read the [payment invariants](../code-review/references/payment-invariants.md) only when a proposed simplification touches money, ledger, or payment processing.

## Deliver the design pass

Use the shared report format. Distinguish required fixes from optional design improvements. Include deletion opportunities among the findings rather than repeating them in another checklist.

When useful, end with up to three changes worth making first, ordered by benefit. Use only supported findings; a clean design needs no invented improvement list. Generate no patches and leave source files unchanged.
