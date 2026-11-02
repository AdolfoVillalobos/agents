# Risk axes and how to lower them

Distilled from the description of Fintoc's PR risk engine (Dexter), shared by its author in Fintoc's engineering Slack on 2026-10-31. The engine's prompts and thresholds are not public; this reference records the axes, the combination rule, and the published advice, not the engine's implementation.

## Axes

| Axis | Low | Mid | High |
| --- | --- | --- | --- |
| **Blast radius**: who a plausible worst-case failure reaches | Developers only | One team, or the whole company | Customers or third parties. Touching money, personal data, auth, public contracts, or availability goes straight to high |
| **Reversibility**: effort to undo the effects | Revert, flag off, or down migration is enough | Derived data or state needs repair | External effects (money movement, emails), deletes, or source-of-truth writes that cannot be undone |
| **Detectability**: how fast and loudly a failure shows | Breaks build, boot, or deploy; raises; tests or alerts catch it | | Wrong value with a valid shape, silent fallback, swallowed error |
| **Change scope**: effective change, excluding generated files, tests, and docs | One unit with few consumers | | Several areas, shared contracts, cross-repo coupling |
| **Review burden**: knowledge needed to judge it wrong | Known pattern, mechanical, or explained by diff, description, and tests | | Domain rules, implicit rules, new architecture, concurrency, idempotency, cryptography |
| **Path track record**: history of touched files | No or ordinary history | | Reverts or production fixes above the repo's norm |

Combination: level ≈ impact × probability, adjusted by detectability. Impact is blast radius, plus reversibility when blast radius is not low. Probability is change scope, review burden, and path track record.

## Levers by axis

**Blast radius**
- Separate the sensitive part (money, financial records, auth, permissions, personal data, credentials, public contracts). Refactors, types, tests, UI, and logs go in earlier low-risk PRs; the sensitive PR stays small.
- Order independent PRs by dependency: refactor with behavior pinned by tests; then types, structure, schemas; then tested logic behind an off flag; then activation. Each merges before the next starts. The activation PR carries full context: what it enables, links to previous PRs, tests of the enabled flow.
- A flag that exists, is off, and is checked in the changed code bounds the reach and eases rollback.
- Adding a new validation or guard lowers risk, because failure leaves things as they were. Modifying an existing guard in the same PR loses that benefit.
- Limits that hold even if the code is wrong: amount caps, internal allowlists, test accounts, read-only access to data the audience already sees. Make them visible in code or description.
- Internal tools are low risk while only the team uses the output. They become risky when the output triggers an external effect without a human deciding (a payment, a customer approval, a reconciliation rule, a regulator report); make that step its own task.
- An unexpected bug or improvement found in a sensitive area gets its own issue and PR. Mixed in, it drags the whole PR to its level and hides the fix.

**Reversibility**
- A change that leaves no state of its own (UI, reads, unsaved computations) is reversible by revert. Say so in the description.
- Two-step migrations: add first (column, table, index) with code working on both schemas; drop or rename later. A `down` that loses no data is more reversible.
- Idempotent jobs and scripts can be fixed by rerunning them.
- A rollback section helps only when the code backs it. "Revert" does not roll back sent emails or moved money.
- Money movement or external effects that are irreversible are always high. The strategy is making them reversible (test mode, shadow write without effect, queue reviewed before execution), not making the PR smaller.

**Detectability**
- Reject invalid data (validation, constraint, type) instead of storing a valid-looking wrong value; log and report unexpected errors instead of silent fallbacks. The system must notice; the user need not see an error.
- Tests must exercise the changed case and fail if it is wrong. Updating a snapshot or expected value to match new output verifies nothing.
- A fix comes with a test that reproduces the bug.
- Complex or sensitive refactors need tests or types pinning prior behavior; if missing, add them in an earlier low-risk PR.
- Prompts, heuristics, and models need evals or tests that exercise the changed behavior.
- Show verification in the description: a screenshot, test-mode output, a request with its response.
- Backfills and scripts: run once, supervised, test mode first, result verifiable in the PR.

**Change scope**
- One PR, one unit of change. Bundling unrelated changes is the most common unnecessary escalation.
- Keep mechanical changes (rename, reformat, API change, adding types across files) separate and logic-free so they can be reviewed by sampling. One line of logic forces a full review.

**Review burden**
- The description explains context and mechanism so the change is understandable without knowing the module, and the code confirms it. "Implements DX-1234" explains nothing.
- Name the existing pattern the change follows and where it lives.
- Domain rules that need domain knowledge are pinned in tests named after the rule.
- Concurrency, idempotency, cache, numeric precision, and cryptography each need specialized reasoning; isolate them in small PRs where possible.

**Process**
- During planning, ask: does it touch a sensitive guarantee, leave state to repair, fail silently, handle credentials, need concurrency or idempotency? Split those parts so they are reviewed alone.
- PRs that grew during review rounds (pre-existing fixes, refactors) can often be split back out.
- When the engine's verdict is known, read which axis raised it; often it is a missing test or a flag not visible in code, and one commit with that evidence is faster than waiting for human review.

## Anti-patterns

- Splitting into PRs that make no sense alone: each needs more context and no one sees the whole behavior.
- Risk over-engineering: sacrificing UX for visibility, leaving giant PRs because they will be high anyway, or tiny PRs where the change loses its context. The goal is understanding the real risk, not gaming the score.
