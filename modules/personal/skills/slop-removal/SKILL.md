---
name: slop-removal
description: >
  Detect and remove AI-generated code slop from a branch or worktree diff
  (duplicated/reinvented helpers, dead code, over-abstraction, defensive
  noise, verbose comments, inconsistent patterns, vacuous tests) while
  preserving behavior. Use after an agent coding session, before opening a
  PR, or when the user says "deslop", "remove slop", "limpia el slop",
  "simplify the diff", or runs /slop-removal. Not for feature work, typo
  fixes, or a dedicated bug hunt (use code-review). Default is
  report-first; apply only when the user asks.
---

# slop-removal

You clean AI slop introduced in the current change. You do not add features,
do not drive-by rewrite, and do not "fix" production behavior as a side
effect of cleanup. Under-removal is safer than over-removal.

Match the user's language. Keep code, commit subjects, and GitHub-facing
text in the language of the repo.

## Invocation

`/slop-removal [target] [--apply] [--repo]`

- `target`: omitted = current worktree diff (see scope below); or a path, PR
  number, or `base...HEAD`.
- `--apply`: after the plan, apply approved cleanups in small commits (or
  unstaged edits if the user said not to commit). Without this flag, **report
  only**.
- `--repo`: inventory the whole repository. Never auto-apply in this mode.

## Hard rules

1. **Behavior stays the same.** Cleanup changes *how* code is written, not
   *what* it does. A real bug is a finding, not a silent fix mixed into slop
   removal.
2. **Diff-scoped by default.** Do not touch files outside the scope. Do not
   reformat unrelated code. Do not rename public APIs, webhook fields, event
   names, or DB columns.
3. **The existing file is the style guide.** Match comment density, docstring
   use, error handling, and naming already in that file and its neighbors.
   Do not impose your own default style.
4. **When in doubt, leave it in.** Low confidence → list as `?`, do not apply.
5. **Never stage/unstage/force-push unless the user asked.** Do not
   `git restore --staged` work they already staged. Do not `git add -A`.
6. **Payments invariants are frozen.** When the diff touches money,
   payments, ledgers, webhooks, idempotency, authorization, or public
   contracts, read [frozen invariants](references/frozen-invariants.md)
   before proposing edits. Report a violation the diff introduces; never
   "simplify" it away.
7. **This is not a bug review.** After cleanup (or instead, if you find a
   P1 bug), recommend a second pass with a *different* reviewer or model,
   such as the `code-review` skill. Do not pretend the cleaner is the bug
   reviewer.

## Phase 0 — Scope and safety net

The default scope is everything the change adds on top of its base:
committed branch work plus staged, unstaged, and untracked files. Do not
stop at the first non-empty `git diff`; that hides the rest.

```bash
base=$(git merge-base origin/<base> HEAD)   # the PR base; a stacked PR uses its parent
git diff "$base"                            # committed + staged + unstaged
git ls-files --others --exclude-standard    # untracked files, read them too
```

If `target` is a PR and the forge CLI works, the PR diff is the source of
truth.

Then:

1. `git status` + the list of changed files. Note which ones look like
   money, webhooks, idempotency, authz, or public contracts.
2. Read repo guidance that applies to those paths: `AGENTS.md`,
   `CLAUDE.md`, `CONTRIBUTING.md`.
3. Read each changed file **in full** (not only the hunk) before proposing
   edits — comment density, error handling, helpers already in the module.
4. Run the **smallest relevant test subset** (no networked side effects, no
   shared-DB migrations). Record the command and the baseline. If the
   baseline is red, stop: slop-removal does not start on a red suite.
5. If the diff touches a [frozen invariant](references/frozen-invariants.md) and there is no characterizing
   test for that behavior, do not apply cleanup there. In `--apply` mode,
   either write a characterization test first (with the user's OK) or skip
   that file.

## Phase 1 — Deterministic scanners

Run only tools that are already in the repo or cheap to invoke (`npx`,
`pipx`). If a tool is missing, skip it and say so — do not invent findings.

Suggested map (adapt to the stack in front of you):

- Clones: `jscpd` (threshold in the same ballpark as 5+ meaningful lines)
  or PMD CPD, scoped to changed paths plus likely siblings.
- Dead code / unused exports: `knip` (JS/TS), `vulture` (Python),
  `deadcode` (Go). Treat reflection/plugin entrypoints as probable
  false positives.
- Patterns: repo Semgrep or `ast-grep` rules; empty `catch`/`except: pass`;
  tautological asserts; raw `as any` / `# type: ignore` added in the diff.
- Already-configured linters (`ruff`, ESLint, etc.): use their output, do
  not re-litigate what CI already enforces, and do not reformat the tree.
- Weak tests (optional, expensive): Stryker incremental or `mutmut` on
  *new* tests in the diff, or on a payments path the user named. A surviving
  mutant is evidence the test is theater.

Do not report a "finding" that is only a linter hit CI would catch, unless
you are about to remove the slop that triggered it.

## Phase 2 — Semantic review (four lenses)

Review the scoped diff with all four lenses. If parallel subagents are
available, give each one lens and merge the results; otherwise run the
lenses in sequence. Every finding needs a
`path:line` anchor and a short concrete scenario or snippet.

1. **Reuse.** Did the change reinvent a helper, policy, or type that already
   exists in this package or an obvious shared lib? Would a later bug-fix
   have to land in two places?
2. **Simplification / noise.** Code-restating comments; docstrings added to
   a file that does not use them; single-use variables that add no clarity;
   defensive null checks, type guards, or try/catch on *internal* trusted
   paths; redundant casts/annotations; deep nesting that early returns would
   fix; speculative fallbacks or abstractions with a single use.
3. **Dead code and consistency.** Unused functions, flags, branches, or
   files introduced by the diff; style that fights the surrounding file
   (`let` vs `const`, new naming scheme, drive-by refactors).
4. **Vacuous tests.** Empty tests, asserts that cannot fail, tests that only
   check a mock was called, huge setup with no exercise of the business
   rule, "verification theater." Especially on money / idempotency /
   tenant paths → P1, do not delete the test without replacing it with a
   real one.

Keep:

- The actual feature, including new helpers used more than once.
- Comments that explain *why* (business rule, workaround, security
  rationale: timing-safe compare, CSRF, sanitization).
- Defensive code at *real* system boundaries: user input, untrusted I/O,
  external APIs, webhook signatures.
- Existing abstractions that still earn their keep.

## Phase 3 — Report (always)

Write the report in the user's language, with this shape:

```
Alcance: <base...HEAD or staged/unstaged>, N archivos, +X / −Y
Scanners: <ran / skipped>
Tests baseline: <command, green/red>

Hallazgos
- [P1|P2|P3|?] path/file.ext:LINE — título corto
  Evidencia: …
  Propuesta: …
  Riesgo si se aplica: …
  Cómo verificar: …

No tocado: <invariants, doubts, out of scope>
```

Severity:

- **P1** — possible behavior change on a frozen invariant; swallowed error
  at a system boundary; vacuous test on a payments path. Never auto-apply.
  Escalate; this may belong to a bug review, not cleanup.
- **P2** — non-trivial duplication, reinvented helper, likely dead code,
  over-abstraction, vacuous tests elsewhere. Apply only after the user
  accepts the plan.
- **P3** — cosmetic slop (comments, single-use vars, redundant casts,
  internal defensive noise that is clearly unnecessary). May auto-apply
  only with `--apply` and a green suite.
- **?** — confidence too low.

Cap noise: group repeated nits; skip anything a formatter/linter already
owns; skip pre-existing slop unless it sits in a hunk you must touch.

If the user did not pass `--apply` and did not say "aplícalo", **stop
here**.

## Phase 4 — Apply (opt-in)

1. Re-state the plan in one short list. Apply P3 first, then accepted P2.
   Never apply P1 as cleanup.
2. Work in small thematic clusters, preferably separate commits if the user
   allows commits: comments/cosmetics; dead code; dedup/reuse; flattening
   an unneeded abstraction. One concern per commit.
3. After each cluster, re-run the Phase 0 test subset. On failure: revert
   that cluster, record it, do not weaken the test to silence it unless the
   plan already classified that test as vacuous *and* you replace it with a
   characterization of the real behavior.
4. Do not keep going if the cleanup diff is growing past the original
   feature diff, or if you would need to edit files outside scope to "make
   it neat."

## Phase 5 — Verify and hand off

- Tests: same subset, green. Mention anything you did not run.
- Recommend a *separate* bug review on the cleaned diff, with another
  model or reviewer (for example, the `code-review` skill).
- 10-second hand-off:

```
Cambió (N archivos, +X / −Y):
- path — qué se quitó o consolidó
Reusé: <helper canónico>
Mirar con atención: <path:line>
Test: <comando>
No tocado / pendiente: …
```

## Stop conditions (any one is enough)

- Baseline tests red, or a cluster leaves tests red and revert did not
  restore green.
- Cleanup would touch a frozen invariant or a public contract.
- No characterization test and the behavior is not obvious from types and
  call sites.
- Two helpers *might* be equivalent (money rounding, time, retries) but
  you cannot prove it.
- User asked for a report only.
- Scope is `--repo` (inventory, never a mass rewrite).

## Out of scope

Feature implementation, typo/bug-only tasks, writing new architecture,
rewriting tests to match a new design, prose deslop of docs or PR copy
(review PR descriptions, but do not treat them as this skill's job), and
posting comments to GitHub unless the user explicitly asks in this
conversation.
