---
name: create-pr
description: Prepare or create a pull request that a reviewer can understand without the conversation. Use when asked to open a PR, prepare a draft PR, write or improve its title and description, or update a PR after its scope changes. Ground the explanation in the final diff and actual validation.
---

# Create an understandable PR

## 1. Identify the final change

Read the user request, repository instructions, PR template, and Git status. Establish the repository, branch, actual target base, and whether this is a new PR or an update. A stacked PR targets its parent branch.

Read the diff and relevant surrounding code. Include local changes when preparing work that is not yet committed. Separate the trigger/problem, previous behavior, resulting behavior, and reason for the approach. Resolve uncertainty from the code and issue before asking the user.

## 2. Prepare the implementation when requested

For a request to create/publish a PR, complete authorized implementation work and relevant checks. Use `diff-minimality` if it is available; otherwise inspect for unnecessary structure and unrelated edits while preserving required behavior. Re-read the final diff after any simplification.

For a request only to write/edit a title or description, inspect and draft without changing source, committing, pushing, or opening a PR.

## 3. Write for someone outside the conversation

Follow the repository template and language. Otherwise use a short title naming the concrete behavior and a description proportional to the change:

1. State the problem and the resulting behavior. Use a trigger and before/after example when it helps.
2. Explain implementation choices only when they help a reviewer assess correctness or tradeoffs.
3. Give validation actually performed and its results. State checks that failed or could not run and why.
4. Include rollout steps, compatibility concerns, or material limitations only when relevant.

A small change often needs one or two paragraphs plus validation. Avoid chronological accounts, abandoned approaches, unsupported claims, and lists of files that merely repeat the diff. Rewrite the title and body around the final implementation when scope changes. Link the originating issue when known; claim it is closed only when the completed scope warrants it.

Example:

> **Prevent duplicate refund fees on retries**
>
> Retrying a completed refund could create a second fee. Fee creation now reuses the existing fee for that refund, so repeated processing leaves the billed amount unchanged.
>
> Validation: the focused retry regression test passes. The full suite was not run.

The example illustrates structure, not facts to copy into another PR.

## 4. Complete the requested delivery

For a writing-only request, return the title and body. For an authorized creation/update request, use the available PR integration and the verified base, defaulting a new PR to draft unless the user or repository specifies otherwise. Inspect and commit only intended changes when needed; preserve unrelated local work. Push the selected branch normally when required and authorized by the PR creation task.

Pass multiline descriptions as structured tool text or an exact UTF-8 body file. With a CLI, use its body-file option where available; treat shell command strings as code and avoid interpolating prose into executable commands.

After publishing, verify the returned PR URL, base, head, title, and body. Report the link and validation outcome. If authentication, permissions, or repository policy prevent publication, keep the finished title/body available and identify the exact blocked action. Existing authorization in the conversation counts; do not ask again solely because this workflow reaches publication.
