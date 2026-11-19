# fintoc-rails

Read this when the repository is `fintoc-com/fintoc-rails`. The repository's `AGENTS.md` is the source of truth for conventions. This file only adds what the refactor search needs.

## Scope and exclusions

- Modules are engines under `engines/<name>/`. Ownership lives in each `package.yml` (`ownership`). Specs live in `spec/engines/<name>/`.
- Exclusion pattern for the signal commands: `-e '/spec/' -e '_spec\.rb$' -e '\.rbi$' -e '/db/' -e 'README'`.
- PRs land as squash commits, one per PR. The PR number is in the commit subject, so `gh pr view <number>` gives description and discussion.

## Boundary checker

- Packwerk: `make packwerk`. Recorded exceptions are in `engines/<name>/package_todo.yml`. Each entry is a rule-1 candidate.
- The fix uses an existing `X::Public::*` constant, or exposes a new public service, `T::Struct`, `T::Enum` or error class in the target engine and lists it in that engine's `README.md`. Read the `engine-public-interface` skill in the repository before proposing one.
- Never propose aliasing an internal constant under `Public`, or adding entries to `package_todo.yml`.

## Known patterns to propose

- Provider adapters behind a domain interface: `Compliance::Verifications::Provider` with its `::Trebol` adapter.
- Per-value data on a `T::Enum` with `case self` and `T.absurd`, or a frozen lookup with a spec over `.values` past about seven values.
- Lifecycle rules belong to the AASM machine, not to enums. Changing a machine is high risk.
- Product gating goes through the engine's `ProductPolicy`, called at each entry point.

## Repeated decisions worth searching

- `cl_payment?`, `mx_payment?`, `country ==`, `currency ==`, `mode ==` and `live?`/`test?` branches.
- `case` over provider names or provider status codes outside the provider's own engine.

## Risk notes

- Anything touching `amount_cents`, currency, ledger entries, refunds or chargebacks is high risk.
- `after_*_commit` callbacks and jobs enqueued from them are high risk.
- Public API serializers, rswag specs under `spec/requests/api/` and webhooks are public API.
