---
name: diff-minimality
description: Simplify an implementation or proposed diff while preserving its required behavior. Use before implementation to choose a smaller solution, when asked to simplify code, or before publishing code changes to a PR. Remove unnecessary structure and reuse existing code without weakening correctness or tests.
---

# Simplify the required change

Optimize for less conceptual complexity and a reviewable diff. Fewer lines alone do not justify losing clarity, domain distinctions, or guarantees.

## 1. Pin the contract and scope

Identify the accepted request or plan and observable behavior that must remain. Read repository instructions and inspect local changes before editing. For a PR, use its actual base; a stacked PR uses its parent branch. Include staged, unstaged, and relevant untracked changes when simplifying work in progress.

If the requested contract is ambiguous, use existing behavior and tests as the preservation baseline; ask only when a simplification would require choosing new behavior.

## 2. Search before adding structure

Inspect comparable implementation and test files in the repository before choosing a pattern. Follow their directory structure, naming, factories, helpers, mocking conventions, and test level, subject to documented repository rules. Introduce a different pattern only when the existing one cannot meet the current need; explain that limitation.

Before implementation, or for each candidate simplification, answer in order:

1. Does this code need to exist to meet the contract?
2. Does an existing module, helper, standard library, or dependency already do it?
3. Can the change stay in an existing function without hiding responsibilities?
4. Does a new abstraction reduce concepts the caller needs to understand, or just move lines?

Prefer deleting unused structure and speculative configuration. Inline wrappers that add no meaningful boundary. Reuse existing helpers only when their semantics match. Similar syntax alone does not establish shared domain meaning.

## 3. Simplify within the contract

Apply justified changes inside the requested scope. Preserve public behavior, error semantics, authorization, atomicity, idempotency, observability, and distinctions such as absent versus zero when they matter.

Apply minimality to tests as well as implementation:

1. For each new test or candidate removal, identify the distinct failure it detects. Compare with existing coverage; consolidate tests only when another retained test detects the same failure under the same conditions. Shared setup or execution of the same code does not establish redundancy: different inputs, boundaries, and integration paths may protect different behavior.
2. Test relevant observable behavior. Avoid tests that merely mirror the implementation, assert internal details without a contract of their own, or recheck a framework guarantee. Before removing a test on those grounds, verify that it is not protecting application configuration, integration, or a known regression.
3. Retain tests that protect distinct behavior. Reduce duplicated setup only when intent stays clear; do not introduce generic fixtures or abstractions merely to reduce line count. For a removal or consolidation, identify the retained coverage that protects the required behavior.

For money, authentication, ledgers, or other correctness-sensitive code, trace the protected invariant before removing a branch or abstraction. A simplification request does not authorize changing that invariant. Existing approval for an intentional behavior change counts.

When invoked to assess a proposal, return the simpler approach without editing source. When invoked to simplify an implementation, make the changes. Do not expand into unrelated cleanup.

## 4. Verify and hand back

Run checks appropriate to the affected behavior and required repository checks. Report what actually ran, its result, and any limitation. Read the final diff for unrelated edits and accidental loss of behavior.

Return what was removed or simplified, why behavior is preserved, and what remains necessary. If no useful simplification exists, explain that briefly; do not manufacture a change to satisfy the skill.

When this is part of preparing a PR, return control to that workflow after verification. Commit or publish only as authorized by the surrounding task. Any repository-installed hook remains a local integration: follow its documented procedure where applicable, without making this skill depend on one hook or provider.
