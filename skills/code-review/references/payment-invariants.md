# Payment and ledger review lens

Use only for flows that touch payments or ledger invariants. Discover the repository's money representation, state machine, and integration guarantees first; these questions do not prescribe a replacement architecture.

- **Amounts:** Trace units, currency, rounding, FX, and the authoritative amount through capture, partial capture, refund, and ledger entries as applicable. Preserve the repository's exact representation; do not propose converting integer minor units to decimals merely by preference. Show a concrete loss of precision or unit mismatch before reporting it.
- **Replay:** Identify the business operation deduplicated, the key's scope, and the durable mutation it covers. Follow duplicate and out-of-order webhooks through downstream effects. An absent header or local key is not proof of duplicate charging if another boundary enforces deduplication.
- **Partial failure:** Trace an external success followed by a timeout, process crash, or failed local write. Establish how retries reconcile that state and which effects survive rollback. A database transaction does not automatically roll back external effects.
- **Concurrency and ownership:** Check competing mutations against balance and ledger invariants, relevant uniqueness/locking constraints, and merchant/tenant authorization. Describe a reachable interleaving or access path instead of prescribing locks everywhere.
- **Time and recovery:** Check actual settlement windows and date/time conventions. Verify that failure can be detected and safely retried or reconciled, and that logs do not expose credentials or sensitive payment data.

Severity depends on the demonstrated impact and reachable conditions. Missing a preferred mechanism alone is not a blocker.
