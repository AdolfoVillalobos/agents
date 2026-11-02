---
name: reduce-pr-risk
description: Read a PR's tracker issue, description, and diff, estimate which risk axes make it risky, and propose concrete alternatives that lower that risk without over-engineering. Use when the user asks how to lower a PR's risk level, make it pass AI-only review, split it, or what to change before opening or after a high risk verdict.
---

# Reduce PR risk

Explain why a pull request is risky and what would make it less risky. The output is advice: never edit the code, push, or update the remote PR or issue unless the user asks.

Read the [risk axes reference](references/risk-axes.md) before scoring. Resolve that path relative to this skill. It is a snapshot of the risk engine's rules; when the engine's repository is readable, prefer the current rule files it lists.

## 1. Gather the three inputs

1. **PR.** Identify it from the user's link, number, or the current branch. Read title, body, base, and the full diff with the repository host's CLI or API (for GitHub: `gh pr view --json title,body,baseRefName,headRefName,files` and `gh pr diff`). Before a PR exists, use the branch diff against its real base and whatever draft description the user has.
2. **Issue.** Find the linked tracker issue from the PR body, branch name, or title prefix, and read it with the available tracker integration. It states the intended scope, so it tells you which parts of the diff were asked for.
3. **Surrounding code.** Read beyond the diff where a score depends on it: consumers of a changed contract, whether a flag exists and defaults off, existing tests that pin the behavior, and the `git log` of touched paths for reverts or repeated fixes.

If an input is unavailable, continue and name the gap. A missing issue lowers confidence in scope judgments; it is not itself a risk finding.

## 2. Score each axis

For each of the six axes in the reference, give the level and its rubric reason id (for example `high` `sensitive_or_broad_consequence`), the signals that decide it, and the evidence, citing `file:line` or the description sentence. Apply the axis's own rules: judge the effect introduced rather than the domain, discount tests edited only to match new output, and judge `path_track_record` only from the history of the touched paths.

Then compute the suggested level with the reference's deterministic rule, showing impact, likelihood, and any adjustment or floor. Name the axes that drive it.

This is an estimate of what an external risk engine might conclude, not its verdict. If the user has the engine's actual reasons, use them as the starting point and check them against the code.

## 3. Propose alternatives

Propose only alternatives that lower a driving axis. For each one state:

- **What to do**, concretely: which files move to which PR, which flag guards which call, which test pins which rule, which sentence the description needs.
- **Which axis it lowers**, to which level, and the `support_reason` or signal whose conditions it would satisfy. State each condition the change must make visible, such as the flag read in the diff.
- **Effect on the suggested level**, recomputed with the deterministic rule. If lowering the axis does not change the result, say so and do not lead with it.
- **Cost**: extra PRs, review context lost, UX or delivery delay.

Use the rule to find the lever. With `blast_radius` at `high`, only lowering `blast_radius` itself or the `-1` adjustment (every likelihood axis, `detectability`, and `reversibility` at `low`) leaves `high`. At impact `mid`, the likelihood axes decide. A `detectability` at `high` costs a level whenever impact is not `low`.

Among alternatives that move the result, prefer, in order: evidence that is missing but cheap (a test that fails on the changed case, a description that explains the mechanism, a visible flag); then separating unrelated or mechanical changes; then a dependency-ordered split; then making an irreversible effect reversible. A split is valid only if each PR stands alone in production with no effect and still makes sense to review.

Say plainly when the risk is inherent. A change that moves money or has an irreversible external effect stays high; the useful advice is to keep that sensitive part small, explicit, and well tested, and to send it to human review. Do not propose splits, flags, or guards whose main purpose is lowering the score.

## 4. Report

Write in the user's language. Lead with the recommendation, then:

1. **Estimated level**: the suggested level with impact and likelihood, then the driving axes, one line each with reason id and signal.
2. **Alternatives**, ranked by risk reduced per unit of cost. For a split, list the PRs in merge order with one line of content each.
3. **What not to do**: only when a tempting option would over-engineer, hurt UX, or fragment context.
4. **Gaps**: inputs you could not read.

Keep it short enough to act on. Skip axes that are clearly `low` after one line.

## 5. Request a new risk review

The risk engine reviews a PR again only when a new commit reaches it. A change limited to the PR description does not trigger it. After the risk-lowering changes are in place, request the new review with an empty amend of the last commit and a force push:

```bash
git commit --amend --no-edit
git push --force-with-lease
```

Include these steps in the report whenever an alternative changes only the description. Run them only when the user asks: the force push rewrites the PR's head commit.
