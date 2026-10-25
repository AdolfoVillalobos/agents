# Posting the drafts to GitHub

Read this only after the user has authorized publishing, approving, or requesting changes on a GitHub pull request.

Send one review so the author gets one notification. Put inline comments in that review. A summary-only review command does not carry line comments.

Use the pull request head SHA as `commit_id`. Each comment needs `path`, `line`, and `side`:

- `RIGHT` for an added or context line on the new file.
- `LEFT` for a deleted line on the old file.
- `start_line` and `start_side` when the comment covers a range. `line` and `side` are the last line.

The line must appear in the diff. `position` is a legacy hunk index. Use `line` and `side`.

```bash
gh api repos/OWNER/REPO/pulls/N/reviews --method POST --input review.json
```

`review.json` has `commit_id`, `event` (`APPROVE`, `COMMENT`, or `REQUEST_CHANGES`), `body`, and `comments`. `body` is required for `COMMENT` and `REQUEST_CHANGES`. Map the summary verdict to that event. A suggestion fence inside a comment body uses the language tag `suggestion` and replaces the anchored lines.

Prefer this single review call. Treat a separate comment-creation call that returns an error as a failed post, and report the error instead of claiming the comments landed.

Requesting changes blocks merge only when branch protection gives that reviewer's request that effect. Say which event you submitted and the head SHA you used.
