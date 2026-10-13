# Comment examples

These show the paste block and the private note. They are illustrations, not extra findings.

## Blocking defect

Scope: `app/webhooks/refunds.py:41-47` on the new side writes a ledger row for every webhook and does not record the event id. The report kept this as a blocking defect.

Paste this:

> **issue (blocking):** A retried webhook writes a second ledger entry and the balance drifts. Dedupe on the event id with a unique constraint before inserting, and return the original result on replay.

Private note: Two `refund.succeeded` deliveries with the same id, about 200 ms apart, insert two movements. Evidence is the insert path and the absence of a uniqueness check in this diff. Smallest fix: conflict-do-nothing on the provider event id, then respond as a duplicate.

## Exact edit

Paste this, including the fence, because it replaces the anchored line exactly:

> **suggestion (non-blocking):** Dividing the minor-unit amount by 100 produces a float. Format it with the currency exponent this module already uses.
>
> ~~~~suggestion
> display_amount = format_minor_units(amount, currency)
> ~~~~

In a real comment the fence uses three backticks and the language tag `suggestion`. The tildes above only keep this example readable.

## Batched nit

> **nitpick (non-blocking):** `user_id` matches the rest of this module. Same mismatch at L12, L30, and L58.

## Question that does not block

> **question (non-blocking):** Would a single status with guarded transitions fit better than `is_paid` and `is_failed`, which can both be true? Happy to keep the flags if they are an explicit constraint.

No suggestion fence: the alternative is a design option, not an exact edit.
