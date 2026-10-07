---
name: review-readiness
description: Assess whether a PR solves the intended problem and is ready to merge and deploy. Use for a staff-level pass on scope, rollout, migrations, compatibility, operability, and behavioral evidence, rather than another line-by-line bug hunt.
---

# Review merge and deployment readiness

Determine whether the change is the right solution and can be shipped under the stated conditions. Read the code and operational context needed to support that decision; existing reviews are evidence to verify, not authority to repeat.

First read the [shared review protocol](../code-review/references/review-protocol.md). It defines scope selection, evidence, severity, and reporting for this pass. Resolve that path relative to this skill, not the repository being reviewed.

## Assess the change as a whole

1. **Problem and scope.** Map the stated intent to implemented behavior. Identify a missed requirement or unrelated expansion with evidence. If intent is missing, distinguish unverifiable product fit from defects you can establish independently.
2. **Affected behavior.** Trace which users, tenants, services, jobs, stored data, and public contracts can change. Check feature-flag defaults and the paths they actually gate. Read the [payment invariants](../code-review/references/payment-invariants.md) when money or payment processing is affected.
3. **Rollout and compatibility.** Walk the actual deployment order and mixed-version period. Inspect migrations, backfills, dual writes, event consumers, and public payloads where applicable. Establish whether an older binary can run against the new data. Propose flags or staged rollout only when they mitigate an identified risk; a flag does not undo a schema change or external side effect.
4. **Operation and recovery.** Check how the affected failure is detected and recovered: retries, poison messages, replay, alerts, or runbooks as relevant. State the concrete missing capability; avoid a generic observability checklist for a low-risk change.
5. **Evidence and reviewability.** Assess whether verification protects the changed behavior, including contract, concurrency, replay, or timezone boundaries only when relevant. A test suite that passes without exercising the disputed boundary leaves that boundary unverified. Review the PR description for the context a reviewer cannot obtain readily from the diff or CI.

Escalate supported merge risks, not prose quality by itself. Missing intent or rollout information can become a blocking question when a specific safety decision cannot be made without it; explain which decision. Do not classify an inadequate description automatically as a major code defect.

## Deliver a decision

Use the shared report format, then add:

- **Decisión de entrega:** ship, ship behind a verified flag, split the PR, or do not ship, expressed in the report's language with the concrete reason or condition. If essential evidence is unavailable, say the decision is pending that evidence rather than declaring the change safe.
- **Foco humano:** up to three specific unresolved decisions or high-impact locations requiring human review. Omit this when no such item was identified.
- **Descripción propuesta:** only when the current body lacks material context, draft a concise replacement using the rules below. Do not update the remote PR as part of review alone.

This pass does not certify exhaustive bug coverage or authorize a merge/deployment. Keep any concrete bug discovered, but avoid repeating a complete QA pass unless requested.

## Drafting a replacement description

Read [the create-pr writing rules](../create-pr/SKILL.md) only when drafting a replacement body; apply its language, length, issue-reference, attribution, and behavioral-test rules as writing guidance. Do not execute its branch, commit, approval, or publication workflow. That sibling skill is part of this collection.

Include material rollout or rollback considerations only when they affect review. Preserve uncertainty: a proposed test or rollout check is not completed evidence.
