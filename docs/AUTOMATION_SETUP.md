# Daily research automation setup

## Current status

This workflow is intended to run at 18:00 India Standard Time (12:30 UTC) for a ten-day date window. GitHub scheduled workflows run from the repository's default branch, so this file must be reviewed and merged into `main` before the schedule can start. The job checks out and updates `research/novelty`; it does not merge pull requests.

The workflow uses the official OpenAI Codex GitHub Action and requires an OpenAI API key. A successful commit/push requires GitHub Actions to be allowed to write contents and pull requests. Review these permissions before enabling it.

## Configure the repository

1. Add `.github/workflows/daily-research.yml` and this guide on `research/novelty`, then review the pull request.
2. Merge the workflow setup into the default branch (`main`) only after owner approval. Until then no schedule is active.
3. In **Settings → Secrets and variables → Actions → Secrets**, create repository secret `OPENAI_API_KEY` containing an API key dedicated to this workflow. Never commit the key.
4. In **Settings → Secrets and variables → Actions → Variables**, create repository variable `RESEARCH_START_DATE` in `YYYY-MM-DD` format. It controls a ten-calendar-day UTC date window; set it before the first intended scheduled run. The first day must match the UTC date of that run (the 18:00 IST run occurs at 12:30 UTC on the same calendar date).
5. Under **Settings → Actions → General → Workflow permissions**, permit read and write access if the workflow is expected to push the research branch or create/update pull requests. Organization policy may prohibit this setting.
6. Verify Actions is enabled. Review any action-allowlist policy so it permits `actions/checkout`, `actions/setup-python`, and `openai/codex-action`.
7. After merging the workflow file and adding the secret and variable, open **Actions → Daily research continuation → Run workflow** for a one-time check. Confirm the summary reports the expected day and inspect logs before relying on the scheduled run.

## Schedule and ten-day guard

GitHub cron uses UTC. `30 12 * * *` corresponds to 18:00 IST. The workflow permits runs only when the current UTC calendar date is between `RESEARCH_START_DATE` and nine days after it, inclusive. This is a ten-day window, not a guarantee of ten successful executions: GitHub can delay or drop scheduled events, and a failed run is not automatically replayed. Check the Actions page daily. If a scheduled execution is missed, document and recover it manually rather than silently claiming ten completed runs.

The `workflow_dispatch` button is subject to the same date guard. It cannot be used outside the ten-day window. The concurrency group prevents overlapping runs.

## Permissions and security

The workflow grants repository contents and pull-request write access to its job so it can push `research/novelty` and create/update the research pull request. It does not grant merge permission, and the workflow prompt prohibits merging. Keep `main` protected with required human review and status checks. Use a dedicated API key, rotate it if exposed, and keep only the necessary repository scope and spending limit on the OpenAI account.

The Codex Action runs with its workspace permission profile. It can change checked-out files; review every generated diff and workflow log. Scheduled workflows execute trusted code from the default branch, so changes to the workflow itself require normal review.

The research job is pinned to `ubuntu-24.04`. The Codex Action's `drop-sudo` setup currently fails to restrict `/run/dbus/system_bus_socket` on Ubuntu 26.04; see [openai/codex-action issue #188](https://github.com/openai/codex-action/issues/188). Revisit this pin after upstream confirms compatibility.

## Billing and run records

GitHub-hosted runner usage is governed by the repository's plan and current GitHub Actions limits. OpenAI API usage is billed separately and depends on model, context, and output. Set an API budget/usage alert before the first run. The Actions run page retains the logs and summary; failed runs are visible there and through GitHub notifications configured for the repository. No separate external notification service is configured.

## Failure recovery

- **No scheduled run:** verify the workflow is merged to `main`, Actions is enabled, the start date is correct, and the date window remains open.
- **Missing API key:** add or replace `OPENAI_API_KEY` in repository Actions secrets, then rerun a failed run if appropriate.
- **Permission denied on push:** review repository/org Actions workflow permissions and branch rules for `research/novelty`; do not weaken protections on `main`.
- **Failed benchmark or Codex step:** inspect the job log, record the failure, and create a fix only after determining the cause. Do not report the day as successful when required checks failed.
- **Missed scheduled day:** GitHub may delay or drop scheduled runs under load. Record the missed run and decide whether to extend/reset the date window; never count a missed day as an execution.

## Pull request lifecycle

The workflow is in `main` so GitHub can schedule it. The daily job works on `research/novelty` and does not merge. Create or update the research pull request separately; owner review and approval are required before merging research changes into `main`.
