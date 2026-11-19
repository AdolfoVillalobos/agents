---
name: find-refactors
description: Find refactors worth doing in a codebase area, ranked by the future change each one makes cheaper, and verify each candidate adversarially before recommending it. Use when asked to find refactor opportunities, improve the design of a set of modules or engines, pick refactors for a batch of PRs, or audit an area for dependency, duplication or boundary problems. Produces evidence-backed refactor cards and a discard list; it does not edit code or open PRs.
---

# Find refactors worth doing

A refactor is worth doing when it makes a change the team will actually make cheaper. Every candidate you report names that change. Discard a candidate when you cannot name it.

This skill finds and verifies candidates. It changes no code. The caller decides which cards become PRs.

## Inputs

- **Scope:** directories, packages or engines to analyse, and their test directories.
- **Window:** history used to measure churn (default: 90 days).
- **Limit:** how many refactors to return (default: 5). Return fewer when fewer qualify. Never pad the list.
- **Exclusions:** paths or change types that are out of scope (generated files, migrations, schema, public API, state machines).

If the repository has a reference for this skill in [references/](references/), read it before starting. It lists that repository's boundary tool, conventions and known traps. Resolve that path relative to this skill.

## What counts

A good refactor does at least one of these, and you can show it in code:

1. **Inverts a dependency in the wrong direction.** A domain module reaches into a provider's or another module's internals. The fix uses or exposes a public interface, or lets the consumer own an interface that the other side implements.
2. **Gives a rule one owner.** The same decision (country, provider, status, code mapping) is written in several files. The fix moves it to the object that owns the data: an enum with per-value data, or an interface with one adapter per variant.
3. **Deepens a module.** A module whose interface is as large as its implementation, or that only forwards arguments. The fix deletes it or hides more behaviour behind a smaller interface.
4. **Makes invalid states unrepresentable.** Untyped hashes or loose primitives cross module boundaries. The fix introduces a typed value object.
5. **Separates decision from effect.** Business rules live inside a lock, a job, a controller or a callback, and can only be tested with the database. The fix extracts the decision as a pure function and leaves the effect where it is.
6. **Moves a seam to where tests need it.** Tests stub many internals or every instance of a class. The fix exposes the dependency so tests replace it at the boundary.

Propose a design pattern only when the code already has a second real case for it. A pattern for one imagined case goes to discards.

These do **not** count toward the limit: deleting comments, renaming for style, test-helper swaps, splitting assertions, formatting. Mention them in one line at the end, grouped by module, as candidates for a single chore PR.

## Process

### 1. Collect signals

Run each source below over the scope. Each gives its own evidence. Exclude tests, generated files and migrations from the counts.

**Hotspots** (churn × size). Large files that change often are where a refactor pays back.

```bash
git log --since="<window>" --no-merges --name-only --format= -- <scope paths> \
  | grep -v -e '<exclusion pattern>' | sort | uniq -c \
  | while read n f; do [ -f "$f" ] && l=$(wc -l < "$f") && echo "$((n * l)) $n $l $f"; done \
  | sort -rn | head -20
```

**Change coupling.** Pairs of files in different modules that change in the same commit three or more times. They show knowledge split across a boundary.

```bash
git log --since="<window>" --no-merges --name-only --format='format:@@' -- <scope paths> \
  | grep -v -e '<exclusion pattern>' \
  | awk '/^@@$/{n=0; split("",f); next} NF{f[++n]=$0; for(i=1;i<n;i++){a=f[i]; b=$0; if(a>b){t=a; a=b; b=t} c[a" "b]++}} END{for(k in c) if(c[k]>=3) print c[k], k}' \
  | sort -rn | head -30
```

Keep the pairs whose two files belong to different modules.

**Boundary violations.** The repository's dependency checker and its recorded exceptions (the reference names them). Each exception is a candidate for rule 1. The checker proves the fix.

**Repeated decisions.** Search the scope for the same branch written in several files: `case` or `if` over country, provider, status or mode, and duplicated code-to-value maps. Count the files per decision.

**Shallow modules and untyped data.** In the hotspot files, look for public classes that only forward to another class, and for hashes passed between commands or modules.

### 2. Shortlist and read

Take the top 15 hotspots, every coupled pair, and every repeated decision found in three or more files. Read each one fully, with its callers and tests. Drop what turns out to be intentional or already covered by an existing abstraction.

If the scope's history links commits to pull requests or issues, read the description and discussion of the ones that touched the candidate. A design that a reviewer already discussed and accepted is not a defect unless the cost has since become visible.

### 3. Write a card per candidate

```markdown
### <short title>
- Problem: `<file:line>`. <What is wrong, in one sentence.> Rule: <number and name from "What counts">.
- Evidence: <hotspot numbers, coupling count, violation count, or files repeating the decision>.
- Interface before: <real signatures>.
- Interface after: <proposed signatures>.
- Callers: <count>, listed with `file:line` (from a repository-wide search, not only the scope).
- Change it makes cheaper: <link to a recent PR that had to touch N places for this reason, or an open issue>.
- Coverage: <specs that exercise the touched code, and what they miss>.
- PR plan: <ordered list. The first PR adds characterization tests when coverage is missing. Each later PR preserves behaviour and passes the existing tests unchanged.>
- Risk: low | medium | high (see below).
- Effort: S | M | L.
```

Every field holds something you read or ran. Write "unknown" instead of guessing.

### 4. Verify adversarially

Give each card, with the code it cites, to a fresh agent that has not seen your reasoning. Its job is to refute the card. It checks:

- Is the current behaviour intentional, according to the history and discussion?
- Does an existing public interface or helper already solve it?
- Are there callers the card missed?
- Does the "after" interface change behaviour for any caller, including error types, nil handling, transactions and ordering?
- Is the "change it makes cheaper" real, or reconstructed after the fact?

If parallel agents are unavailable, do the same pass yourself sequentially, after finishing all cards, rereading the code from scratch. Keep a card only if the refutation fails. Record the refutation's outcome on the card in one line.

### 5. Classify risk and rank

Risk depends on the technique, not on how small the change looks:

- **Low:** behaviour-preserving changes inside one module, or a dependency fix that the boundary checker verifies, with tests covering the touched paths.
- **Medium:** signature changes with several callers, or logic moving between classes, when the PR plan splits it into steps that each preserve behaviour.
- **High:** touches a public API, persisted data, a state machine, money movement, or callbacks with side effects. Report it, but mark it ineligible.

Rank eligible cards by value (hotspot weight plus the change it makes cheaper), then risk, then effort. Prefer three cards with a solid PR plan over five small ones.

## Output

1. Ranked cards, at most the limit.
2. Discards, one line each with the reason: intentional, refuted, high risk, no future change named, pattern without a second case.
3. One line with the chore candidates, if any.

Do not edit files, create branches or open PRs.
