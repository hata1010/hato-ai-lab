# Hato AI Lab — Continuity Operations

## Scheduler

The continuity workflow is `.github/workflows/test_continuity_write.yml`.

- Scheduled execution: `0 4 * * *`
- Schedule timezone: **UTC**, as required by GitHub Actions cron.
- Manual execution: `workflow_dispatch` and is the **immediate test path**; no 24-hour wait is required to validate the workflow.

The workflow order is:

1. GitHub App token
2. Checkout
3. Integrity check
4. Recovery check
5. Audit trail record
6. Daily continuity commit and push

## Continuity controls

- `tools/integrity_check.py` validates required continuity paths.
- `tools/recovery.py` locates the latest checkpoint and reports a non-destructive recovery action.
- `tools/audit_trail.py` appends UTC JSONL audit events under `memory/audit/continuity.jsonl`.
- `tools/daily_commit.py` commits only continuity-managed paths.

## Testing rule

A change to the scheduler must first be tested with **manual dispatch**. The scheduled UTC execution is confirmation of persistence, not the first opportunity to discover whether the workflow works.

## Timezone policy

The scheduler stores and executes its schedule in UTC. Human-facing local times must be calculated separately and documented rather than embedded ambiguously in cron expressions.
