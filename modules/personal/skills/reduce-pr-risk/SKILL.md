---
name: reduce-pr-risk
description: Read a PR's tracker issue, description, and diff, estimate which risk axes make it risky, and propose concrete alternatives that lower that risk without over-engineering. Use when the user asks how to lower a PR's risk level, make it pass AI-only review, split it, or what to change before opening or after a high risk verdict.
---

# Reduce PR risk

Explain why a pull request is risky and what would make it less risky. The output is advice: never edit the code, push, or update the remote PR or issue unless the user asks.

Read the [risk axes reference](references/risk-axes.md) before scoring. Resolve that path relative to this skill.

## 1. Gather the three inputs

1. **PR.** Identify it from the user's link, number, or the current branch. Read title, body, base, and the full diff with the repository host's CLI or API (for GitHub: `gh pr view --json title,body,baseRefName,headRefName,files` and `gh pr diff`). Before a PR exists, use the branch diff against its real base and whatever draft description the user has.
2. **Issue.** Find the linked tracker issue from the PR body, branch name, or title prefix, and read it with the available tracker integration. It states the intended scope, so it tells you which parts of the diff were asked for.
3. **Surrounding code.** Read beyond the diff where a score depends on it: consumers of a changed contract, whether a flag exists and defaults off, existing tests that pin the behavior, and the `git log` of touched paths for reverts or repeated fixes.

If an input is unavailable, continue and name the gap. A missing issue lowers confidence in scope judgments; it is not itself a risk finding.

## 2. Score each axis

For each of the six axes in the reference, give `low`, `mid`, or `high` with the specific signal that decides it, citing `file:line` or the description sentence. Then name the one or two axes that drive the overall level, using the reference's combination rule.

This is an estimate of what an external risk engine might conclude, not its verdict. If the user has the engine's actual reasons, use them as the starting point and check them against the code.

## 3. Propose alternatives

Propose only alternatives that lower a driving axis. For each one state:

- **What to do**, concretely: which files move to which PR, which flag guards which call, which test pins which rule, which sentence the description needs.
- **Which axis it lowers** and why the new level follows from the reference.
- **Cost**: extra PRs, review context lost, UX or delivery delay.

Prefer, in order: evidence that is missing but cheap (a test that fails on the changed case, a description that explains the mechanism, a visible flag); then separating unrelated or mechanical changes; then a dependency-ordered split; then making an irreversible effect reversible. A split is valid only if each PR stands alone in production with no effect and still makes sense to review.

Say plainly when the risk is inherent. A change that moves money or has an irreversible external effect stays high; the useful advice is to keep that sensitive part small, explicit, and well tested, and to send it to human review. Do not propose splits, flags, or guards whose main purpose is lowering the score.

## 4. Report

Write in the user's language. Lead with the recommendation, then:

1. **Estimated level** and the driving axes, one line each with the signal.
2. **Alternatives**, ranked by risk reduced per unit of cost. For a split, list the PRs in merge order with one line of content each.
3. **What not to do**: only when a tempting option would over-engineer, hurt UX, or fragment context.
4. **Gaps**: inputs you could not read.

Keep it short enough to act on. Skip axes that are clearly `low` after one line.
