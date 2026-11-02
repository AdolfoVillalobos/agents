# Risk axes and how to lower them

Snapshot of Fintoc's PR risk engine (Hermes, in the private repository `fintoc-com/dexter`), taken from `main` at `0593a7e` (risk config last changed in `46536d8`, 2026-10-27, rubric version 2). Sources:

- Axis rubrics: `engines/hermes/config/risk/axes/<axis>.yml`
- Signals: `engines/hermes/config/risk/signals/<axis>.yml`
- Combination rule: `engines/hermes/app/commands/hermes/risk/resolve_allowed_range_command.rb`
- Final verdict rules: `engines/hermes/app/services/hermes/risk/verdict_questions.rb`

**If you can read `fintoc-com/dexter`, read those files at its current `main` instead of this snapshot**: they are the source of truth and change over time. This file condenses them; ids are verbatim so a report can cite them.

## How the engine decides

1. **Signals.** For each signal predicate the engine decides present, absent, or unknown from cited evidence. A present signal points toward its guiding level; it does not set it. Unknown is uncertainty, never absence.
2. **Axes.** For each axis it picks a level and a rubric reason id, citing evidence. A `support_reason` justifies a lower level (`low` or `mid`) only when its conditions are met. Changes with no runtime effect in production (docs, comments, local or CI tooling that does not gate merges or deploys, test-only files) are `low:not_applicable` on every axis.
3. **Suggested level**, deterministic:
   - *Impact* = `blast_radius`; if it is not `low`, the max of `blast_radius` and `reversibility`.
   - *Likelihood* = max of `change_scope`, `review_burden`, `path_track_record`. Exception: if `change_scope` is the only likelihood axis at `mid` and both `detectability` and `reversibility` are `low`, likelihood counts as `low`.
   - Table (likelihood low / mid / high): impact `low` gives `low / low / mid`; impact `mid` gives `low / mid / mid`; impact `high` gives `high` always.
   - Adjustment, only when impact is not `low`: `detectability` `high` adds one level; impact `high` with likelihood `low`, `detectability` `low`, and `reversibility` `low` subtracts one (to `mid`).
   - Floor: `blast_radius` `high` and `reversibility` `high` together are always `high`.
4. **Final level.** A model picks within one level of the suggestion (only `low` if every axis is `low`), lowering only by citing what bounds the harm (prompt detection, simple way back, internal or bounded effect, or pinned observable behaviour) and raising only for risk the axes miss (for example, setting a pattern future code will copy). Uncertainty alone never raises it.
5. **Meaning.** `low` needs only the AI reviewer; `mid` any developer; `high` a maintainer of the repository or area.

Consequences for advice:

- `blast_radius` decides most outcomes. At `high`, the only way below `high` is the `-1` adjustment: every likelihood axis `low`, plus `detectability` and `reversibility` `low`. Lowering `blast_radius` itself through a support reason is usually the bigger lever.
- At impact `mid`, likelihood decides between `low` and `mid`: making `change_scope`, `review_burden`, and `path_track_record` `low` gets `low`.
- `detectability` `high` costs a level whenever impact is not `low`; moving it to `mid` or `low` removes that penalty.
- When impact is `low`, the result is `low` unless some likelihood axis is `high`.

## Axes

Each axis lists its question, the rubric reasons per level, the rules that most affect advice, the support reasons that lower it, and its signals by guiding level. All support reasons target `low` or `mid`.

### blast_radius

*If this change fails in the worst plausible way, what additional harm reaches whom, compared with the state before the change?*

- `low` `bounded_consequence`: only developers or one internal team, an annoyance or degraded capability, no sensitive guarantee.
- `mid` `bounded_user_impact`: customers, third parties, or company-wide operation see a bounded impact; a safeguard protecting production is weakened; or the outcome of a regulatory obligation changes, without breaking a sensitive guarantee.
- `high` `sensitive_or_broad_consequence`: a sensitive guarantee would break: money or financial records, tax data or reporting, who sees personal data or credentials and where they go, confidential information leaving our control, what customers, third parties, or cross-team internal roles are authorized to do, customer isolation, production availability or the ability to deploy or roll back, or a public contract.

Rules that matter for advice:

- Judge the effect introduced, not the domain the code lives in. Touching billing code is not enough; changing how much, to whom, when, or whether money moves is.
- A shared surface inherits the reach of its consumers.
- An internal tool reaches only its team until something outside the team acts on its output without a person deciding (customer approval, payout, reconciliation rule, regulatory report), or a defect would hide from the team what it must review.
- Adding a protection where there was none leaves the previous state when it fails; modifying an existing protection exposes what it protected. A protection that wrongly rejects valid operations is judged by what it blocks.
- A bound lowers the level only if it holds even when the change is wrong.
- For flags that are off, the consequences on activation are still assessed.

Support reasons:

- `internal_ops`: only internal tools or operations, with effects shown to stay bounded for internal consumers.
- `dev_only`: runs only in development and does not reach production behaviour.
- `additive_protection`: adds a protection where there was none, its failure leaves the previous state, and wrongly rejecting valid operations would not block a sensitive guarantee.
- `independent_bound`: a bound that does not depend on the change working (internal-only destination, test mode, read-only access to data its audience could already see, amount caps, an independent guard).
- `no_consumers_yet`: evidence shows nothing calls or loads the new code and this change does not wire it up. Finding no references alone is not enough.
- `observable_behaviour_preserved`: behaviour is preserved and types or tests in the evidence pin that what consumers observe stays equivalent. Tests edited only to match the new output do not count.
- `feature_flagged_off`: a flag that exists and is off gates every relevant effect, the flag read is visible, and the change does not turn it on or bypass it. A disabled per-customer or per-repository configuration record counts. Activation consequences are still assessed.

Signals:

- low: `developers_only`, `single_internal_team`, `optional_ci_or_reporting`, `new_optional_tool`, `observability_pipeline`, `cosmetic_only`, `internal_data_wrong`, `additive_protection`, `read_only_effect`, `test_mode_or_sandbox_only`, `internal_destination_only`, `independent_guard_exists`, `no_consumers_yet`, `approved_destination_unchanged`, `fails_closed_to_safe_default`, `observable_behaviour_preserved`, `no_runtime_effect`
- mid: `company_wide_internal`, `customer_facing`, `third_party_facing`, `all_tenants_shared`, `subset_reach`, `regulatory_obligation`, `runtime_wide_change`, `release_gate_weakened`, `merge_or_deploy_blocking`, `capability_degraded`, `flow_blocked`, `customer_communication_content`, `performance_regression`, `amount_or_rate_capped`
- high: `money_movement_changed`, `financial_record_changed`, `pricing_or_fees_changed`, `fiscal_data_changed`, `tax_authority_reporting`, `fiscal_document_issued`, `personal_data_exposure_changed`, `credentials_or_secrets_handling`, `confidential_info_to_third_party`, `authorization_changed`, `authentication_changed`, `public_contract_changed`, `production_availability`, `deploy_or_rollback_path`

### reversibility

*If this change is wrong, what does it take, beyond reverting it, to get back to a correct state?* Weighs on the result only when `blast_radius` is not `low`.

- `low` `revert_or_isolation`: revert, redeploy, down migration, or flag off is enough, and no state needs repair.
- `mid` `bounded_recovery`: a known, bounded extra step: coordinated down migration, recompute or backfill from a source of truth, cleanup script, deleting logged content, draining scheduled work.
- `high` `lasting_effect`: no clear path back: lost information, wrong data in the source of truth, or effects with customers, third parties, or destroyed infrastructure.

Rules that matter for advice:

- Judge only what the change introduces. Only changing when an existing process runs over the same records adds no new lasting effect; widening the records it reaches does.
- Wrong data recomputable from an untouched source of truth is bounded; wrong data written into the source of truth is not.
- Internal ephemeral messages need no repair; messages to customers or third parties cannot be withdrawn.
- The PR body's Rollback section is direct evidence: declaring rollback unsafe raises the level, and a documented recovery needs the mechanism in the diff to corroborate it.
- A flag lowers the level only if it exists, its read is visible, and every new effect is inactive while off.

Support reasons: `feature_flagged_off` (same conditions as above, for every new effect), `revert_safe` (revert or redeploy restores the relevant state and no new effect survives it), `recomputable_from_source` (any wrong data can be recomputed from a source of truth the change does not touch), `rollback_section_safe` (the Rollback section describes a suitable recovery and the diff corroborates it is bounded).

Signals:

- low: `revert_restores`, `no_persistent_state`, `flag_gated_off`, `reversible_schema_migration`, `regenerable_state`, `ephemeral_internal_effect`, `idempotent_rerun`, `rollback_documented`, `dependency_change`, `no_runtime_effect`
- mid: `writes_derived_data`, `new_persisted_format`, `logged_or_tracked_content`, `queued_or_scheduled_work`, `state_machine_transition`, `backup_declared`, `external_reversal_available`, `rollback_unclear`, `coupled_revert`, `config_outside_deploy`
- high: `writes_source_data`, `data_deletion`, `lossy_transform`, `irreversible_migration`, `destructive_schema_change`, `external_message_sent`, `third_party_state_change`, `money_or_value_moved`, `client_held_artifact`, `infra_destroy_replace`, `rollback_declared_unsafe`

### detectability

*If this change breaks, would we find out, and how fast?* High means low detectability.

- `low` `prompt_detection`: noisy failure, or a prompt channel: CI on the changed case, types or contracts, failed boot/deploy/migration, explicit alert, error tracker, canary, or the author or an internal team using it frequently.
- `mid` `partial_detection`: observed late or partially (periodic or batch process, customer reports, unmonitored logs, dashboard reviewed later), or changed logic, fix, refactor, or non-deterministic behaviour without a test or eval.
- `high` `difficult_detection`: silent failure (wrong value with valid shape, swallowed error, fallback, missing effect, subset-only change) and no channel would surface it.

Rules that matter for advice:

- Tests count only if they exercise the changed case. A test edited only to match the new output is not coverage. Missing captured tests is uncertainty, not proof of absence.
- Prompts, models, and heuristics need evals or tests that exercise them.
- Author claims of manual testing do not lower the level unless the PR shows the verification of the changed case.

Support reasons: `covered_by_tests`, `typed_contract_enforced` (types, schema, DB constraint, or compiled contract reject the failure mode), `noisy_failure`, `runtime_observability` (alert, error tracker, healthcheck, or canary covers the changed failure mode), `internal_users_close`, `fix_with_repro_and_test`, `refactor_verified`, `evals_cover_behaviour`.

Signals:

- low: `fails_on_boot`, `fails_on_deploy`, `fails_in_build`, `raises_on_invalid_state`, `validates_output`, `breaks_visibly`, `hard_dependency_failure`, `hot_path`, `runs_on_deploy_or_boot`, `runs_on_author_action`, `runs_once_supervised`, `tests_exercise_changed_case`, `fix_with_reproducing_test`, `types_enforce_contract`, `db_constraint_enforces`, `evals_cover_behaviour`, `ui_covered_by_snapshot_or_e2e`, `contract_test_external`, `refactor_pinned`, `explicit_alert`, `error_tracker_notifies`, `healthcheck_covers`, `canary_or_progressive_rollout`, `outcome_metric_alerted`, `author_uses_result`, `internal_frequent_use`, `manual_verification_shown`, `no_runtime_effect`, `dead_code_removal`, `observability_added`
- mid: `runs_periodically`, `runs_on_rare_event`, `rarely_used_feature`, `behind_disabled_flag`, `subset_only`, `tests_updated_to_match_only`, `changed_logic_untested`, `fix_unverified`, `refactor_unpinned`, `nondeterministic_without_eval`, `behaviour_config_unvalidated`, `ui_untested`, `no_test_infra`, `dashboard_reviewed_later`, `logs_unmonitored`, `downstream_reconciliation`, `internal_occasional_use`, `customer_visible`, `ops_or_support_reviews`, `dependency_upgrade`, `runtime_tuning`
- high: `wrong_value_valid_shape`, `silent_fallback`, `swallowed_errors`, `missing_effect_unnoticed`, `silent_filter_change`, `duplicate_or_repeated_effect`, `stale_or_cached_data`, `access_grant_silent`, `quality_degrades_without_error`, `concurrency_or_ordering`, `external_effect_unverified`, `observability_reduced`, `customer_cannot_verify`

### change_scope

*How many places must be considered to review the change?* Extent, not depth.

- `low` `localized`: one module, component, or flow with few consumers, even if the diff is medium-sized.
- `mid` `related_modules`: several related units, or several areas for one purpose; several call sites, internal contracts, or global configuration; or more hand-written volume than one sitting.
- `high` `broad_scope`: alters a surface many independent consumers outside the diff depend on, or bundles independent changes that could be reviewed and reverted in separate PRs.

No line threshold. Generated files, lockfiles, schemas, recorded fixtures, tests, and docs do not count. A mechanical change in many places is narrow. Only consumers whose behaviour can change count.

Support reasons: `single_module`, `mechanical_change` (reviewable by sampling), `generated_noise_excluded`.

Signals:

- low: `single_unit`, `small_effective_diff`, `mechanical_bulk`, `tests_and_docs_dominant`, `generated_noise_dominant`, `few_consumers`
- mid: `multi_unit_same_area`, `large_effective_diff`, `new_component`, `multi_area`, `cross_repo_coupling`, `many_call_sites`, `signature_or_contract_change`, `cross_engine_interaction`, `global_configuration`
- high: `bundled_unrelated_changes`, `shared_surface_fan_out`

### review_burden

*How much context and reasoning does a reviewer need to tell whether the change is wrong?* Depth, not extent or consequence.

- `low` `self_contained`: known pattern, mechanical, or reasoning available in the diff, description, or tests.
- `mid` `developer_context`: needs module or domain knowledge: unexplained business rules, dense logic, many branches, non-evident side effects, non-deterministic behaviour, external contracts.
- `high` `maintainer_comprehension`: changes architecture, sets a pattern others will copy, intrinsically hard or security logic, or a plan the diff does not show.

The PR counts as context: a mechanism explained in the description and confirmed by the diff, or behaviour made inspectable by tests. Continuing a feature from earlier PRs is judged by its increment. Size and sensitive subject matter do not raise it. Designing or redesigning concurrency, idempotency, caching, numeric precision, or cryptography is `high` even when explained and tested; applying an existing mechanism is `mid`.

Support reasons: `routine_known_pattern` (the evidence shows the existing pattern), `mechanism_explained_in_pr`, `self_contained_diff`, `verifiable_from_tests`, `mechanical_change`.

Signals:

- low: `follows_established_pattern`, `continues_prior_feature`, `mechanical_change`, `mechanism_explained_in_pr`, `behaviour_pinned_by_tests`, `self_evident_diff`
- mid: `module_knowledge_needed`, `implicit_business_rule`, `domain_knowledge_needed`, `dense_logic`, `branching_complexity`, `nonobvious_side_effects`, `nondeterministic_behaviour`, `implicit_contract_reliance`, `uses_existing_concurrency_pattern`
- high: `architecture_change`, `sets_pattern`, `plan_review_heavy`, `security_reasoning`, `concurrency_design_changed`, `idempotency_or_retry_design_changed`, `cache_or_distributed_state_design_changed`, `numeric_precision_logic`, `cryptography_or_signing`

### path_track_record

*Has the zone the change touches had bugs that reached production recently?* Only `low` or `mid`.

- `low` `ordinary_history`: no history, new files, or ordinary fixes and reverts (cosmetic, part of an ongoing feature, global bumps, share near the repository's).
- `mid` `adverse_history`: reverts of changes to these paths or repeated production fixes above the repository's share.

Judged only from the git history of the touched paths, never from the diff, PR text, or author. Each commit is a squashed PR. Support reason: `stable_path`. Signals (mid): `zone_reverted`, `repeated_production_fixes`.

The PR cannot change this axis; at most it avoids touching a troubled path it does not need.

## Splitting and anti-patterns

From the engine author's guidance to the team (Fintoc engineering Slack, 2026-10-31), not encoded in the engine:

- Order a split by dependency: refactor with behaviour pinned by tests; then types, structure, schemas; then tested logic behind an off flag; then activation. Each PR stands alone in production with no effect and merges before the next starts. The activation PR carries full context: what it enables, links to the previous PRs, tests of the enabled flow.
- An unexpected bug or improvement in a sensitive area gets its own issue and PR.
- Migrations in two steps: add first with code working on both schemas; drop or rename later.
- Do not split into PRs that make no sense alone: each needs more context and no one sees the whole behaviour.
- Do not over-engineer risk: no UX sacrificed for the score, no giant PRs left as-is because they will be `high` anyway, no tiny PRs that lose the context of the change.
