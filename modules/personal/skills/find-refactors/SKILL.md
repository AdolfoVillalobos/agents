---
name: find-refactors
description: Find refactors worth doing in a codebase area, in both recently changed and legacy code, by building a long list of candidates, investigating the most promising ones in depth, verifying each adversarially, and selecting the N best. Use when asked to find refactor opportunities, improve the design of a set of modules or engines, pick refactors for a batch of PRs, or audit an area for dependency, duplication, boundary or legacy problems. Produces evidence-backed refactor cards, a selection and a discard list; it does not edit code or open PRs.
---

# Find refactors worth doing

A refactor is worth doing when it makes a change the team will actually make cheaper, or removes a hazard the team keeps paying for. Every candidate you select names that change or that hazard. Discard a candidate when you cannot name either.

The work is a funnel: a wide long list from cheap signals, a deep investigation of the most promising candidates, and a selection of the best N. This skill changes no code. The caller decides which selected cards become PRs.

## Inputs

- **Scope:** directories, packages or engines to analyse, and their test directories.
- **Recent window:** history used to measure current churn (default: 90 days).
- **Long window:** history used to find legacy code (default: 2 years, or the full history if shorter).
- **Investigate:** how many candidates get a full investigation (default: 15).
- **Select:** how many refactors to return (default: 5). Return fewer when fewer qualify. Never pad the selection.
- **Exclusions:** paths or change types that are out of scope (generated files, migrations, schema, public API, state machines).

If the repository has a reference for this skill in [references/](references/), read it before starting. It lists that repository's boundary tool, legacy markers, conventions and known traps. Resolve that path relative to this skill.

## What counts

A good refactor does at least one of these, and you can show it in code:

1. **Inverts a dependency in the wrong direction.** A domain module reaches into a provider's or another module's internals. The fix uses or exposes a public interface, or lets the consumer own an interface that the other side implements.
2. **Gives a rule one owner.** The same decision (country, provider, status, code mapping) is written in several files. The fix moves it to the object that owns the data: an enum with per-value data, or an interface with one adapter per variant.
3. **Deepens a module.** A module whose interface is as large as its implementation, or that only forwards arguments. The fix deletes it or hides more behaviour behind a smaller interface.
4. **Makes invalid states unrepresentable.** Untyped hashes or loose primitives cross module boundaries, or a file opts out of the type checker. The fix introduces a typed value object or raises the file's type level.
5. **Separates decision from effect.** Business rules live inside a lock, a job, a controller or a callback, and can only be tested with the database. The fix extracts the decision as a pure function and leaves the effect where it is.
6. **Moves a seam to where tests need it.** Tests stub many internals or every instance of a class, or the class has no test of its own. The fix exposes the dependency so tests replace it at the boundary, starting with characterization tests.

Propose a design pattern only when the code already has a second real case for it. A pattern for one imagined case goes to discards.

These do **not** count toward the selection: deleting comments, renaming for style, test-helper swaps, splitting assertions, formatting. Mention them in one line at the end, grouped by module, as candidates for a single chore PR.

## Value: recent code and legacy code

Recent code shows its value through churn: it changes often, so a refactor pays back on the next change.

Legacy code changes little, so churn undervalues it. A legacy candidate qualifies when at least one of these holds, with evidence:

- **Planned work will touch it.** An open issue, project or roadmap item changes this area. Link it.
- **It produces incidents.** Recurring production errors, support tickets or manual fixes trace back to it. Link or count them.
- **Many things depend on it.** Callers across modules, so its shape leaks into new code. Count the callers.
- **It is the copy new code imitates.** Recent changes elsewhere repeat its pattern. Cite one.

Legacy code that nobody touches, nobody calls from new code and causes no incidents is not worth refactoring. Discard it with that reason.

## Process

### 1. Long list (wide and cheap)

Run every source below over the scope. Exclude tests, generated files and migrations from the counts. Write each candidate as one line: file or pair, signal, number. Aim for 30 to 50 lines. Do not read code in depth yet.

**Recent hotspots** (recent window, churn × size).

```bash
git log --since="<window>" --no-merges --name-only --format= -- <scope paths> \
  | grep -v -e '<exclusion pattern>' | sort | uniq -c \
  | while read n f; do [ -f "$f" ] && l=$(wc -l < "$f") && echo "$((n * l)) $n $l $f"; done \
  | sort -rn | head -20
```

**Long-term hotspots.** The same command over the long window. Files high here but low in the recent list are legacy that used to hurt and may still.

**Legacy markers.** Large non-test files that carry the repository's legacy markers (the reference lists them, for example a weak type-checker level, linter disables, or patterns the conventions say not to copy), sorted by size. Add classes with no test file of their own.

**Change coupling.** Pairs of files in different modules that change in the same commit three or more times, over both windows.

```bash
git log --since="<window>" --no-merges --name-only --format='format:@@' -- <scope paths> \
  | grep -v -e '<exclusion pattern>' \
  | awk '/^@@$/{n=0; split("",f); next} NF{f[++n]=$0; for(i=1;i<n;i++){a=f[i]; b=$0; if(a>b){t=a; a=b; b=t} c[a" "b]++}} END{for(k in c) if(c[k]>=3) print c[k], k}' \
  | sort -rn | head -30
```

Keep the pairs whose two files belong to different modules.

**Boundary violations.** The repository's dependency checker and its recorded exceptions (the reference names them).

**Repeated decisions.** The same branch written in several files: `case` or `if` over country, provider, status or mode, and duplicated code-to-value maps. Count the files per decision.

**Pain from outside the code.** Open issues, projects and recurring production errors that name files or modules in scope. They supply the value for legacy candidates.

### 2. Shortlist

Score each long-list line from the signals alone: strength of the signal, value evidence (churn, planned work, incidents, callers), and whether a rule from "What counts" plausibly applies. Pick the top candidates up to the **Investigate** count.

Keep the shortlist mixed. At least a third of it is legacy (low recent churn) when legacy candidates with value evidence exist, so recent hotspots do not crowd them out. Spread it across modules when the signals allow.

### 3. Investigate each shortlisted candidate

Investigate candidates independently: one fresh agent per candidate when parallel agents are available, otherwise one at a time. Each investigation reads the code fully, with its callers and tests, reads the history and discussion of the commits that touched it, and writes a card:

```markdown
### <short title>
- Kind: recent | legacy.
- Problem: `<file:line>`. <What is wrong, in one sentence.> Rule: <number and name from "What counts">.
- Evidence: <hotspot numbers, coupling count, violation count, legacy markers, or files repeating the decision>.
- Value: <the change it makes cheaper or the hazard it removes, with a link or count>.
- Interface before: <real signatures>.
- Interface after: <proposed signatures>.
- Callers: <count>, listed with `file:line` (from a repository-wide search, not only the scope).
- Coverage: <specs that exercise the touched code, and what they miss>.
- PR plan: <ordered list. The first PR adds characterization tests when coverage is missing. Each later PR preserves behaviour and passes the existing tests unchanged.>
- Files touched: <list, used to detect overlap at selection>.
- Risk: low | medium | high (see below).
- Effort: S | M | L.
```

Every field holds something read or run. Write "unknown" instead of guessing. An investigation that finds the candidate intentional, already solved, or without value ends with a one-line discard instead of a card.

### 4. Verify adversarially

Give each card, with the code it cites, to a fresh agent that has not seen the investigation. Its job is to refute the card. It checks:

- Is the current behaviour intentional, according to the history and discussion?
- Does an existing public interface or helper already solve it?
- Are there callers the card missed?
- Does the "after" interface change behaviour for any caller, including error types, nil handling, transactions and ordering?
- Is the value real, or reconstructed after the fact?

If parallel agents are unavailable, do the same pass yourself after finishing all cards, rereading the code from scratch. Keep a card only if the refutation fails. Record the outcome on the card in one line.

### 5. Classify risk

Risk depends on the technique, not on how small the change looks:

- **Low:** behaviour-preserving changes inside one module, or a dependency fix that the boundary checker verifies, with tests covering the touched paths.
- **Medium:** signature changes with several callers, or logic moving between classes, when the PR plan splits it into steps that each preserve behaviour.
- **High:** touches a public API, persisted data, a state machine, money movement, or callbacks with side effects. Report it, but mark it ineligible.

### 6. Select N

From the surviving eligible cards, select up to **Select**:

1. Rank by value, then risk, then effort.
2. Walk the ranking and skip a card whose files overlap a card already selected, so the PRs do not conflict. Note the skipped card as "next batch".
3. Keep recent and legacy cards both represented when both have eligible cards.
4. Prefer a card with a solid multi-PR plan over two small cards.

## Output

1. **Selection:** the selected cards, in order.
2. **Investigated, not selected:** the other surviving cards, one line each with why (ranked lower, overlaps, ineligible risk). They are the next batch.
3. **Discards:** one line each with the reason: intentional, refuted, high risk, no value, pattern without a second case.
4. **Long list:** the full list from step 1, one line each, marking which entries were shortlisted.
5. One line with the chore candidates, if any.

Do not edit files, create branches or open PRs.
