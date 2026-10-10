---
name: create-pr
description: Open a pull request with a concise review format — draft, self-assigned, English title and Spanish body by default, an issue ID prefix, the issue tracker's suggested branch when available, and a body under 120 words that signposts the diff instead of summarizing it. Use when the user asks to create/open/raise a PR, says "PR this", "abre un PR", "subamos el PR", or runs `/create-pr`.
---

# Create PR

Treat any arguments the user passed as extra context about the change, and use them to enrich the body. They never replace reading the diff.

PR descriptions and commit messages must contain only relevant change information, with no acknowledgments or attribution to an LLM provider, model, or coding agent. Omit generated-by footers, promotional signatures, and AI `Co-authored-by` trailers, including those copied from templates or added by default tooling. Preserve genuine human authorship trailers.

## Git context

Inspect Git status, the current branch, and any existing PR before changing branches. Default base branch is `main`; use a different one when the user names it or an existing/stacked PR has a verified different base.

```sh
git branch --show-current
git diff {base}...HEAD      # current changes
git log {base}..HEAD --oneline    # recent commits on this branch
```

## Issue and branch

1. **Resolve the issue.** Use the issue supplied by the user or extract its ID from the current branch and uppercase it. Resolve conflicting IDs before proceeding. If neither is available, ask for the ID or use the issue-tracker integration to find/create the intended issue.
2. **Read the issue and its suggested branch.** Fetch the issue context and the exact suggested Git branch name through the available integration. Use that returned name whenever possible; do not invent a translation or reconstruct it from the title. For Linear conventions, read [references/fintoc.md](references/fintoc.md#linear-y-ramas).
3. **Choose the branch without losing work.** For new work, create the suggested branch if it is free. For local unpublished work, use that name when the workspace allows renaming. Preserve an existing PR's head or a branch whose name is fixed by the user/workspace; identify that exception and associate the issue through the PR title. Check local and remote branches before selecting a name; an existing branch is reusable only when it belongs to this same work. Preserve local changes and obey existing restrictions on branch operations.
4. **Support several PRs for one issue.** If the suggested branch already belongs to another PR or completed work, create a distinct branch by appending a short scope suffix to the suggested name, keeping the same issue ID. Link the additional PR to that same issue; do not create a duplicate issue just because it has several PRs. A request to update an existing PR keeps its branch.
5. **Handle unavailable integration explicitly.** If the suggested name cannot be retrieved, use one supplied by the user or retain the current branch and put the known issue ID in the PR title. State that the suggested name or linkage could not be verified; do not invent either.

Resolve the issue and branch before making the planned commits.

## Commits

Each commit should answer one question for the reviewer. The sequence explains the final solution, not the chronology of attempts.

1. **Plan the sequence before committing.** Draft the commit titles in order, from the problem to the solution. Put prerequisites before the changes that depend on them.
2. **Group by purpose, not by file or layer.** Keep a behavior change and its tests together. Separate preparation or refactoring only when it makes the following change easier to understand.
3. **Make each commit coherent on its own.** Give it one main intention and keep relevant checks passing at each step. A small change may need only one commit; avoid splitting a single idea across diffs the reviewer must reconstruct.
4. **Explain intent in the message.** The title states what the commit achieves. Use the body when needed to explain why it is necessary or a decision the diff cannot explain. Replace vague titles such as `fix`, `updates`, or `address feedback` with the concrete outcome.
5. **Review the complete history before publishing.** Read the titles in order, then each diff. Fold corrections to mistakes introduced in the same branch into the relevant commit and remove intermediate changes later undone. Preserve existing commits when they already tell a clear story. History edits must preserve the intended final diff and unrelated work; follow the repository's rules and existing authorization for rewriting shared history.

For a concrete sequence, read the [commit narrative example](references/fintoc.md#ejemplo-de-narrativa-de-commits). Use it as an illustration, not a required number of commits or a fixed layer order.

## Pull request

Use the available pull-request integration. Create the PR as a draft and assign the authenticated user. Write the PR title IN ENGLISH and the description IN SPANISH BY DEFAULT, including Spanish section headings, regardless of the conversation, branch, commit, or template language. Apply an explicit language override only to the part the user names. A request for the whole PR in another language applies to both title and body. Keep issue IDs, code identifiers, commands, and product names unchanged.

**Before creating the PR:** show the user the proposed title and body, then ask:

1. **Ok** — proceed with creation
2. **Shorter** — cut it down further
3. **Missing something** — a section needs more detail

Only create the PR after the user selects "Ok".

### Title

Brief, starts with the issue ID in brackets, and names the action and affected object or concrete effect in English by default. Omit vague introductions and merge-bot prefixes.

### Body

Read the PR template at `.github/pull_request_template.md` for the section structure. Preserve its structure and translate headings into Spanish unless the user explicitly requests another body language.

Prefer first-person singular from the PR author's perspective when describing changes or checks supported by the diff and session evidence, such as "Agregué", "Corregí", or "Verifiqué". Omit an unnecessary "yo". Keep problem statements and system behavior impersonal when that reads more naturally. Do not invent personal observations, manual testing, or shared authorship to force first person.

Use plain punctuation in PR titles and descriptions. Do not use semicolons (`;`), double hyphens (`--`), or em/en dashes as prose separators. Prefer short sentences with periods or commas, and use a colon only when needed. Preserve literal code, identifiers, command flags such as `--dry-run`, URLs, and Markdown syntax. This rule changes prose punctuation, not technical syntax.

Keep issue references exclusively in the PR title and branch. The description must contain no Linear/issue-tracker URLs or issue IDs, whether linked, plain text, parenthetical, or hidden in Markdown link definitions. If copied context ends with an issue reference in parentheses, remove that entire reference and the empty parentheses; retain only the explanation of the problem. Apply this to every section, including Contexto, even when the reference comes from the issue or PR template.

The body is a signpost, not a summary: it tells the reviewer what to expect and then gets out of the way. **The diff carries the detail.** Assume the reviewer has no project context, but trust them to read code — do not pre-explain what they are about to read.

**Length budget: the whole body is at most 120 words. Aim for 80 or fewer; this is a ceiling, not a quota.** Count before showing it to the user; if it is over, cut — don't reflow. Keep the shortest text that explains the problem, change, and any consideration needed to review it. Extra background belongs in the issue; do not automatically post extra comments to fit the budget.

**Per section:**

- **Contexto** — usually one sentence, at most two: name the concrete need or failure and why it matters. No paragraph breaks, no design rationale, no history of how you got there.
- **¿Qué hay de nuevo?** — usually 1-3 `- [x]` items, up to 5 only for distinct changes, **one line each, 15 words max**. State one concrete change or effect per item, naming a code identifier only when it helps locate the change. One useful bullet is enough for a small fix. Never justify the change inside the item, never wrap onto continuation lines.
- **Pruebas** — focus on the big picture: the user flow, business behavior, or important risk that was validated, and its outcome. In one or two lines, explain what confidence the verification adds, whether manual or automated. Omit test counts, test-file/case inventories, and routine results such as Sorbet, rubyfmt, lint, or "unit tests pass": the diff and CI already expose those details. Include only information that helps the reviewer assess the change; omit the section when it adds nothing. Ground every claim in checks actually performed and state a material validation gap when it affects confidence. This rule governs the PR description; still run the checks required for the change.
- **Consideraciones** — only what changes what the reviewer must do or know: stacked PR base, frontend coordination required, a non-obvious tradeoff, a scope limit, a concrete uncertainty to review, or a backwards-incompatible change. For preparatory work, say what this PR enables and what remains for the next one in a single sentence. Max 2 one-liners. If there's nothing, write `NA` or drop the section.
- **Reversión** — omit unless rollback is more than reverting the PR (data migration, cutover flip).

**Never include:** internal jargon (milestone names like `M0`/`M1`, codenames, acronyms), file-by-file walkthroughs, or restated code.

Read the [Fintoc writing examples](references/fintoc.md#ejemplos-de-redacción) before drafting. The [study of 50 PRs](references/npcastro-pr-writing.md) documents the evidence behind the brevity rules; the rules above remain authoritative where author habits differ from the user's preferences.

## Verify delivery

Before creating or amending commits, check their messages against the attribution rule above. Before showing the proposed PR text and again before publishing, check title/body language, natural first-person wording, and prose punctuation, then check the complete description against the attribution and issue-reference rules above. Remove any remaining reference and recheck; do not merely turn a Markdown link into a plain issue ID. Associate the PR through its branch, title, or the tracker's PR-linking capability instead. This restriction applies to the PR description, not to the association stored on the issue.

After creation or update, verify the published title, body, base, and head, including language, voice, punctuation, and the body's attribution and issue-reference rules. Check the issue's linked PRs when the integration is available, including for an additional PR on the same issue. Report unverified linkage as unverified; a branch name alone is not proof that the integration completed the association. Return the PR URL.
