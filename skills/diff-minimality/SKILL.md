---
name: diff-minimality
description: Simplify an implementation against its accepted plan. Apply before writing code and always before creating a draft PR or publishing further code changes to it.
---

## Diff minimality (non-negotiable)
- Prefer delete over abstract. Prefer one function over a new package.
- Do not add files, types, interfaces, factories, or “future-proof” layers that the task does not require.
- If an existing helper/module already does it, reuse it. Search first.
- Maximum blast radius: only files required by the accepted plan.
- After implementation, run a simplification pass: "what can we delete and still pass tests?"
- Never expand scope to "while we're here".

## YAGNI ladder (answer before writing code)
1. Does this need to exist at all?
2. Does it already exist in this repo?
3. Can the stdlib / existing dependency do it?
4. Can it be a 10-line change in an existing function?
5. Only then write new code. Smallest implementation that passes the verification.

## Payments / correctness
- No new abstraction around money, idempotency, auth, or ledger without an explicit human "yes" in the plan. Existing approval in the conversation counts.
- Fail closed. Do not swallow errors. Do not "fix" tests by rewriting assertions to match new behavior unless the plan says the behavior changed.
- Preserve observable distinctions such as no deduction (`nil`) versus a free deduction (`0`), atomicity, idempotency, alerts and invoice periods.

## Before publishing
1. Identify the accepted plan and the PR's actual base. For a stacked PR, review against its parent branch, not the whole stack against main.
2. Read `git diff BASE...HEAD` and the changed files. Identify deletions, existing helpers and redundant test setup; retain tests that protect distinct behavior. Do not invent an abstraction to reduce line count.
3. Apply necessary simplifications and run the relevant checks. Commit the final changes. In repositories with `.agents/hooks/diff-minimality.py` installed, record the review with `python3 .agents/hooks/diff-minimality.py --record BASE --summary "What was removed or why it is necessary; checks run"`. Record only after completing the review, never just to bypass the hook.
4. Create the PR with `gh pr create --draft --base BASE` from its branch's working directory. Use the same base ref in both commands. Repeat the review if the head or base changes.

Where installed, the command hook checks the review record before `gh pr create`; it does not perform the semantic review or prove code correctness. The agent performs this skill. The same review applies when another tool publishes a PR or when an existing PR is updated.
