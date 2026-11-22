# Frozen invariants for slop removal

Read this when the scoped diff touches money, payments, ledgers, webhooks, idempotency, authorization, or public contracts.

Do not modify, inline, or delete logic whose job is any of the following. If cleanup would require touching it, stop and report. You may *report* a violation the diff introduces; you may not "simplify" it away.

Derive the repository's actual representation and guarantees first. This list says what cleanup must not weaken; it does not prescribe a replacement architecture.

- **Money:** amounts in integer minor units or a decimal with an explicit scale; currency travels with the amount; no floats; explicit rounding. Currencies differ in minor units: CLP has 0 decimal places, so do not assume 2.
- **Idempotency:** every externally triggered mutation (API POST, webhook, retryable job) has a key that covers the whole side effect; replays return the same result; a unique constraint backs it in the database.
- **Tenant scope:** every query and mutation is scoped to the organization or account; no lookup by global id alone.
- **State machines:** explicit guarded transitions; terminal states immutable; concurrent transitions use a lock or compare-and-set.
- **Reconciliation and ledger:** every money movement has an external reference; entries balance; corrections are reversing entries, never an update or delete of a movement.
- **External I/O:** timeouts; retries with backoff only on idempotent calls; an outbox for "database write + emit event"; a timeout is not a failure.
- **Time:** instants in UTC; business dates in the business timezone.
- **Data and contracts:** no PII, secrets, or account numbers in logs; migrations stay backward compatible; do not rename API, webhook, or event contracts as cleanup.
