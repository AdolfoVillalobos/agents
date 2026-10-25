---
name: code-review
description: Review a PR, branch, or working diff adversarially against its intent and repository conventions. Look for concrete failure cases, challenge each candidate finding against the surrounding code, and report supported defects separately from design suggestions. Use for PR reviews, second opinions, or requests to challenge an implementation.
---

# Adversarial code review

Try to falsify the implementation's claims, then try to falsify your own findings. Adversarial describes the investigation; comments to the author stay respectful and concrete. A review with no supported defects is a valid result.

## 1. Establish the review scope

Read the user's request, the repository's agent instructions, and its contribution and coding standards. Inspect Git status before choosing the comparison.

- For a PR, obtain its actual base and head from PR metadata. A stacked PR uses its parent branch.
- For branch changes, resolve the supplied base and head to commits and compare `git diff BASE...HEAD`. Infer a missing base from repository/PR evidence; ask only if materially different plausible bases remain.
- For work in progress, include the requested committed diff plus staged and unstaged changes; inspect relevant untracked files separately. Do not label a HEAD-only comparison a working-tree review.

Record the comparison, resolved commits, and any included local changes. An invalid ref needs correction. An empty selected diff means there is nothing to review in that scope.

Read the PR description and linked issue/spec through available tools, or use the supplied text. If intent remains unavailable, state the assumption and continue reviewing correctness; mark spec coverage as unverified. Missing issue-tracker setup alone is not a defect in the code.

## 2. Investigate independently

Use these passes. If independent agents are available and permitted, give them the same pinned scope and distinct passes. Otherwise perform the passes sequentially; do not claim independent reviewers ran.

1. **Intent and design.** Trace requirements to implementation. Challenge the chosen location, omitted user flows, compatibility, and additions outside scope. Search for an existing flow that already solves the problem.
2. **Correctness.** Read changed code and relevant callers, callees, persistence constraints, and tests. Construct concrete counterexamples: empty input, boundary values, retries, concurrent execution, partial failures, and authorization boundaries where applicable. For stateful code, trace which effects persist after failure.
3. **Maintainability and standards.** Check documented rules, unclear names, duplicated knowledge, unnecessary abstractions, and complexity that obscures behavior. Explain the practical cost of a design suggestion. A smell is a hypothesis, not proof that an abstraction or rewrite is needed. Leave formatting enforced by tooling to that tooling.

Prioritize serious design issues without allowing them to hide independently actionable correctness or security defects. Use focused tests or reproductions when they distinguish a real bug from a plausible story. Inspect beyond the diff before deciding a guard, constraint, or test is absent.

## 3. Challenge candidate findings

For each candidate, record the changed location, realistic trigger, observed or traced consequence, and evidence. Search for its strongest counterargument: an upstream guard, database constraint, transaction, framework behavior, documented invariant, or test that disproves it.

Retain a defect only when evidence survives that challenge. Distinguish a reproduced failure from a failure inferred through code. Move unresolved possibilities to a short questions section when they materially affect confidence; do not present them as confirmed bugs.

Deduplicate findings across passes. Recheck locations against the reviewed revision. If the target moved, identify what changed and review the affected scope before claiming the report applies to the new revision.

## 4. Deliver one complete review

Lead with supported defects, ordered by severity. Label each with its lens (intent, correctness, or standards), `file:line`, triggering scenario, consequence, evidence, and a concrete fix direction. Cite the requirement or repository rule when claiming a violation.

- **Blocking:** a demonstrated or well-supported defect that should prevent merge. Explain the severity in terms of impact and reachable conditions.
- **Suggestion:** a design or maintainability improvement with a concrete benefit; distinguish it from required correctness work.
- **Question:** missing information that prevents resolving an important concern.

Keep comments in the user's/team's language and discuss the code rather than the author. Prefer one comment for a recurring root cause. Omit speculative nits and forced praise.

Close with the reviewed base/head, checks actually run and their results, important coverage gaps, and a recommendation: request changes, approve with suggestions, or no blocking findings within the inspected scope. If there are no findings, say so without claiming the code is bug-free.

Deliver review comments as drafts. Post comments, submit approval/request-changes, or modify source only when the user authorized that action; existing session authorization counts.
