---
name: review-comments
description: Turn an existing review into paste-ready line comments. Use when the user wants comments to paste, Conventional Comments, suggestion blocks, or diff line anchors, including "comentarios para pegar" or "draft the comments". Format findings already in hand. Investigate with code-review or a named pass only when no findings exist yet. Publish only after the user authorizes that action.
---

# Review comments

Write the comments a reviewer can paste. Design, defect hunting, and the ship decision stay in `code-review`, `review-design`, `review-qa`, and `review-readiness`. This skill formats surviving findings and leaves them as drafts.

## 1. Start from findings

Use the review already in the conversation when it covers the same scope. Quote its base, head, and local changes.

When no such review exists, read the [shared protocol](../code-review/references/review-protocol.md) and complete one investigation before drafting:

- A general review follows [code-review](../code-review/SKILL.md).
- A request for design, behavior, or merge readiness follows `review-design`, `review-qa`, or `review-readiness`.
- A request for every pass runs design, then QA, then readiness, on the same pinned scope.

Stop when that report is finished. Draft here. Keep one finding per root cause.

Every comment below traces to a finding that report kept. An empty report produces a summary and no line comments.

## 2. Label each comment

Use [Conventional Comments](https://conventionalcomments.org/): a label, an optional decoration, and a subject. The label states whether the comment blocks merge.

| Finding from the report | Label | Blocks |
| --- | --- | --- |
| `blocker`, `major`, or a blocking defect | `issue (blocking)` | Yes |
| `minor`, or a non-blocking design note | `suggestion (non-blocking)` | No |
| `nit` grounded in a written rule | `nitpick (non-blocking)` | No |
| Question the report marks as blocking | `question (blocking)` | Yes |
| Any other material question | `question (non-blocking)` | No |
| Specific, earned reinforcement | `praise` | No |

Write `praise` only for a concrete property of this change. Leave it out when nothing qualifies.

Keep at most three `nitpick` comments. Put any further nits on the clearest example and list the other locations in that same comment.

A blocking comment names the reachable failure, why it matters, and the smallest fix. A non-blocking alternative is an option with its trade-off, written as if the author may already have considered it. Talk about the code.

## 3. Anchor the line

Attach each comment to a line that appears in the reviewed diff.

For a unified diff, start at the new-file number in `@@ -oldStart,oldCount +newStart,newCount @@`. Count `+` lines and context lines toward the new file. Count `-` lines only toward the old file.

- Added or context line: `path:line` on the new side.
- Deleted line: `path:line` on the old side.
- A range covers contiguous lines of that same side.

When the right line is outside the diff, anchor the nearest changed line and say where the problem actually is. Check every anchor against the diff before delivering. A comment with no diff line belongs in the summary.

## 4. Write the paste block and the private note

Write paste blocks in the language of the PR title and body. Write private notes in the user's language. Apply an explicit language request only to the part the user names.

Paste block:

```text
**issue (blocking):** What happens, why it matters, and what to change.
```

Add a `suggestion` fence only when those lines replace the anchored lines exactly and the author could accept them unchanged. Keep the reason above the fence. Leave design disagreements in prose.

```suggestion
exact replacement of the anchored lines
```

Under each paste block, add a private note the author does not receive: the concrete scenario, the evidence, and the smallest fix. Mark executed checks and traces separately.

## 5. Close with one summary

Lead with the suggested verdict and the reviewed base and head:

- **Request changes** when any comment blocks, including a blocking question.
- **Comment** when the review is partial and the report does not yet support approval or a request for changes.
- **Approve with comments** when every comment is non-blocking.
- **No blocking findings** when there is nothing to paste. Skip praise and skip an empty comment list.

Then list blocking comments with `path:line`, group the non-blocking ones, and keep questions. One legend for the labels used, placed once in this summary.

## 6. Hand back drafts

Return the drafts in the conversation. Publishing, approving, or requesting changes waits until the user authorizes that action. Existing authorization counts.

When that authorization names GitHub, read [GitHub posting](references/github-posting.md) and send one review that contains the inline comments. Record the head commit you commented on.

Worked comments are in [examples](references/examples.md).
