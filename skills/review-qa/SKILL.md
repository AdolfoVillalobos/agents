---
name: review-qa
description: Hunt production defects introduced by a PR or working diff by tracing affected flows end to end and running focused checks. Use for QA, regression, retry, concurrency, or authorization review; reports findings by default.
---

# Review behavior end to end

Find reachable failures introduced by the selected change. Prefer one demonstrated bug over a list of hypothetical weaknesses.

First read the [shared review protocol](../code-review/references/review-protocol.md). It defines scope selection, evidence, severity, and reporting for this pass. Resolve that path relative to this skill, not the repository being reviewed.

## Trace before reporting

For each affected flow, follow the entry point through callers, services, persistence, and external effects. Build a compact map of the boundaries that actually exist: authentication and authorization, state writes, idempotency/replay, external I/O, failure handling, and observability. Account for each changed file, including tests and configuration; mark unrelated bug classes inapplicable rather than manufacturing checks.

Check reachable failure scenarios:

- Incorrect state transitions, empty or boundary inputs, lost updates, and incompatible return/error contracts.
- Partial success, effects that survive a failed transaction, retries that repeat a non-idempotent action, and concurrent check-then-act sequences. Look for existing transactions, unique constraints, locks, and downstream deduplication before reporting a gap.
- Time zones, date boundaries, ordering, and serialization when the changed behavior depends on them.
- Cross-user or cross-tenant access, injection, secrets in logs, or attacker-controlled external requests. Show the input-to-impact path. Missing validation, rate limiting, or a security mechanism alone is not a vulnerability; a concrete introduced exploit remains in scope.
- Swallowed failures or lost correlation that make a reachable incident undetectable or unrecoverable. State the operational consequence rather than requesting a metric by default.

When the flow handles payments or ledgers, read the [payment invariants](../code-review/references/payment-invariants.md). Derive the actual money representation and guarantees from this repository.

## Verify the suspected failure

Find the repository's documented test commands and run the smallest relevant checks when the environment permits. Trace what their assertions prove: can the test still pass when the claimed invariant is broken? Check whether mocks remove the failing boundary or assertions mirror the new implementation. Report a coverage gap only with the distinct failure it leaves undetected; do not request test counts or duplicate existing coverage.

Use a focused reproduction when it can distinguish the bug from its strongest counterargument. Keep experimental files in a disposable location and use local fixtures or sandbox services. Review does not authorize production writes, real charges, or sending notifications. If a check cannot run, record why and use code evidence where sufficient; do not claim executed behavior.

For each blocker or major finding, supply numbered reproduction steps with expected versus actual behavior, or a precise code-only trace that establishes the failure. Passing tests and confidence scores do not replace that explanation.

## Deliver the QA pass

Use the shared report format and add a short **Flujos recorridos** section containing the actual flow map. Separate executed checks from code tracing, including important paths not exercised.

Report only by default. If the user explicitly requests fixes (including `--fix`), first establish the failure, then make the smallest correction and rerun the relevant check. Preserve unrelated work and report the final diff separately from the original findings; this does not authorize committing or publishing.
