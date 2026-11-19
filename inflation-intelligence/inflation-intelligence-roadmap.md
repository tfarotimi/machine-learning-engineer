# Inflation Intelligence Platform — Project Roadmap

## Project objectives

Build a platform that combines your existing inflation forecasts with current economic evidence to produce traceable, evaluated inflation briefings.

Use this project to demonstrate three capabilities: research agents, evaluation, and dependable deployment.

## Starting position and sequence

- **Forecasting pipeline:** Already built. Preserve it and verify its interface and validation.
- **Research agent:** Underway. Continue from its current state.
- **Evaluation:** Begin now, alongside agent development.
- **Critic and verification:** Add after establishing a measurable research baseline.
- **Infrastructure:** Use minimal storage early; consolidate after the workflow works.
- **Deployment:** Follow a stable integrated local workflow.
- **Hardening:** Improve reliability using observed failures.

**Sequence:** Scope → early evaluation → research agent → verification and critic → integration and infrastructure → deployment → hardening → portfolio evidence.

## How to use this roadmap

1. Import this Markdown file into Notion.
2. Add three to five tasks from your current phase to the “This week” section.
3. Check off tasks only after verifying their acceptance criteria.
4. Add evidence links or short notes below completed tasks.
5. Check the phase exit criteria before advancing.
6. Keep new ideas in the deferred backlog instead of expanding the current release.

You can use the checklist directly. A task database is optional.

## This week

- [ ] Save one current forecast output.
- [ ] Save one current research-agent output.
- [ ] Choose the first geography, inflation measure, and intended user.
- [ ] Draft one example briefing.
- [ ] Create the initial evaluation cases.

## Optional Notion task database

| Property | Purpose |
| --- | --- |
| Task | One concrete action |
| Task ID | Stable reference, such as EVAL-03 |
| Phase | Owning phase |
| Status | Backlog / Ready / In progress / Blocked / Review / Done |
| Priority | P0: release blocker / P1: core / P2: later |
| Dependency | Task or milestone required first |
| Deliverable | What the task produces |
| Acceptance criterion | Observable completion condition |
| Evidence | Link to code, result, report, or decision |
| Effort | Small: one session / Medium: several sessions / Large: split it |
| Target date | Optional planning date |
| Blocker / next action | Exact obstacle and next step |

### Working rules

- [ ] Keep no more than two implementation tasks in progress.
- [ ] Split tasks that cannot finish in a few focused sessions.
- [ ] Define acceptance criteria before starting.
- [ ] End each session by recording the next concrete action.
- [ ] Review deliverables and exit criteria weekly.

**Phase progress:** Completed required tasks divided by total required tasks. Exclude optional backlog items.

**Release readiness:** All mandatory exit criteria pass. Task completion percentage alone is insufficient.

### Reusable task template

- **Task ID and title:**
- **Outcome:**
- **Dependency:**
- **Steps:**
- **Acceptance criterion:**
- **Evidence:**
- **Decision or tradeoff:**
- **Next action if blocked:**

## Phase 0 — Define the first release and audit existing work

**Purpose:** Make the next release small enough to finish and specific enough to evaluate.

**Dependency:** None.

### Product scope

- [ ] SCOPE-01 — Choose one primary user, such as an economist or macroeconomic analyst.
- [ ] SCOPE-02 — Choose one geography.
- [ ] SCOPE-03 — Choose one main inflation measure and forecast horizon.
- [ ] SCOPE-04 — Define one recurring question the platform must answer.
- [ ] SCOPE-05 — Select the output: saved briefing, simple dashboard, or both.
- [ ] SCOPE-06 — Define the required contents of a useful answer.
- [ ] SCOPE-07 — Record first-release exclusions.

Suggested question: “As of this date, what is the inflation outlook, what evidence explains recent developments, and what risks could change it?”

Suggested exclusions: additional countries, automated trading, a general-purpose chatbot, autonomous retraining, and elaborate multi-agent coordination.

### Audit and output design

- [ ] AUDIT-01 — Run the existing forecast pipeline and save a representative output.
- [ ] AUDIT-02 — Document inputs, outputs, execution steps, and dependencies.
- [ ] AUDIT-03 — Locate existing backtests and performance reports.
- [ ] AUDIT-04 — Record known forecasting limitations.
- [ ] AUDIT-05 — Run the current research agent and save its result.
- [ ] AUDIT-06 — List working, incomplete, and failing capabilities.
- [ ] AUDIT-07 — Inventory reusable acquisition code, sources, and storage.
- [ ] AUDIT-08 — Draw the source-to-briefing workflow.
- [ ] OUTPUT-01 — Draft a sample briefing by hand.
- [ ] OUTPUT-02 — Include forecasts, recent developments, evidence, risks, and limitations.
- [ ] OUTPUT-03 — Distinguish observed data, forecasts, and interpretation.
- [ ] OUTPUT-04 — Include an as-of date and information cutoff.
- [ ] OUTPUT-05 — Define when to report insufficient evidence.

**Deliverables:** One-page scope, system inventory, sample briefing, workflow diagram.

### Exit criteria

- [ ] Explain the release in two sentences.
- [ ] Run the existing forecast pipeline successfully.
- [ ] Save one sample question and expected briefing.
- [ ] Identify the next implementation task.

## Phase 1 — Establish early evaluation

**Purpose:** Measure whether changes improve the system.

**Dependency:** Phase 0 scope and sample output.

Start with saved cases and a small runner; a full evaluation service can wait.

### Evaluation cases

- [ ] EVAL-01 — Save 10 representative research questions.
- [ ] EVAL-02 — Include retrieval and multi-source synthesis.
- [ ] EVAL-03 — Include missing evidence, conflicting sources, stale data, and source failures.
- [ ] EVAL-04 — Assign case IDs and information cutoffs.
- [ ] EVAL-05 — Record expected facts, acceptable sources, and unacceptable claims.
- [ ] EVAL-06 — Use a rubric where multiple interpretations are reasonable.
- [ ] EVAL-07 — Save fixed source excerpts or snapshots for repeatability.
- [ ] EVAL-08 — Separate development cases from held-out cases.
- [ ] EVAL-09 — Keep forecast evaluation separate from briefing evaluation.

### Scoring and baseline

- [ ] EVAL-10 — Define factual-correctness scoring.
- [ ] EVAL-11 — Define citation-support scoring.
- [ ] EVAL-12 — Define numerical-correctness scoring: values, units, periods, and transformations.
- [ ] EVAL-13 — Define temporal-correctness scoring against the cutoff.
- [ ] EVAL-14 — Define completeness and uncertainty-quality scoring.
- [ ] EVAL-15 — Define expected failure handling.
- [ ] EVAL-16 — Record runtime and estimated cost.
- [ ] EVAL-17 — Distinguish critical failures from minor defects.
- [ ] EVAL-18 — Run and manually score the current agent on development cases.
- [ ] EVAL-19 — Save outputs, tool activity, configuration, and scores.
- [ ] EVAL-20 — Group failures into a small taxonomy.
- [ ] EVAL-21 — Create one action that reruns the suite.
- [ ] EVAL-22 — Set provisional release thresholds before further tuning.

Use Pass / Partial / Fail with a short reason initially.

Suggested release gates: no fabricated citations; no critical numerical or cutoff errors; unsupported material claims removed, qualified, or blocked; visible limitations for missing evidence; runtime and cost within chosen limits.

Passing a small evaluation set establishes performance on those cases, not universal reliability.

**Deliverables:** Versioned cases, rubric, baseline report, repeatable runner.

### Exit criteria

- [ ] Compare two agent versions on the same evidence.
- [ ] Identify the most important failure categories.
- [ ] Run evaluation before accepting major agent changes.

## Phase 2 — Finish the research agent

**Purpose:** Produce useful research with inspectable evidence.

**Dependencies:** Output contract and evaluation baseline.

### Workflow and limits

- [ ] AGENT-01 — Define inputs: question, geography, cutoff, period, and optional forecast context.
- [ ] AGENT-02 — Define outputs: findings, evidence, citations, uncertainty, and unresolved questions.
- [ ] AGENT-03 — Specify tools and when each is used.
- [ ] AGENT-04 — Limit searches, documents, retries, runtime, and cost.
- [ ] AGENT-05 — Define success, insufficient-evidence, and failure stop conditions.
- [ ] AGENT-06 — Choose the simplest workflow supporting the scope.
- [ ] AGENT-07 — Justify additional agents or planning loops before adding them.

### Sources and grounding

- [ ] SOURCE-01 — Build a source registry prioritizing primary material.
- [ ] SOURCE-02 — Define when secondary commentary is acceptable.
- [ ] SOURCE-03 — Capture publisher, title, URL, publication date, and retrieval time.
- [ ] SOURCE-04 — Capture reporting period separately from publication date.
- [ ] SOURCE-05 — Save the excerpt or table supporting each material claim.
- [ ] SOURCE-06 — Detect duplicate sources and repeated reporting of one original source.
- [ ] SOURCE-07 — Handle inaccessible pages, parsing failures, and empty results.
- [ ] SOURCE-08 — Enforce the information cutoff.
- [ ] SOURCE-09 — Record source-use constraints relevant to storage and display.
- [ ] AGENT-08 — Extract evidence before drafting narrative.
- [ ] AGENT-09 — Attach evidence IDs to factual claims.
- [ ] AGENT-10 — Distinguish sourced facts from interpretation.
- [ ] AGENT-11 — Preserve credible source disagreements.
- [ ] AGENT-12 — Report unavailable values instead of inventing them.
- [ ] AGENT-13 — Treat instructions in retrieved material as untrusted source content.
- [ ] AGENT-14 — Save an execution trace sufficient to explain the answer.

### Iteration

- [ ] AGENT-15 — Run evaluation and fix the highest-impact recurring failure.
- [ ] AGENT-16 — Rerun affected cases and the regression suite.
- [ ] AGENT-17 — Compare quality, runtime, and cost with baseline.
- [ ] AGENT-18 — Save three representative successful outputs.
- [ ] AGENT-19 — Document remaining weaknesses.

**Deliverables:** Working agent, source registry, traceable outputs, evaluation comparison.

### Exit criteria

- [ ] Answer scoped questions within limits.
- [ ] Link material factual claims to inspectable evidence.
- [ ] Show missing and conflicting evidence clearly.
- [ ] Demonstrate measured improvement against baseline.

## Phase 3 — Add verification and a critic

**Purpose:** Catch errors and control what reaches the briefing.

**Dependency:** Structured research claims linked to evidence.

### Explicit verification

- [ ] VERIFY-01 — Give each material claim an ID, type, importance, and evidence references.
- [ ] VERIFY-02 — Define statuses: Supported / Partially supported / Unsupported / Contradicted / Unverifiable.
- [ ] VERIFY-03 — Specify how each status affects publication.
- [ ] VERIFY-04 — Check that cited evidence exists in the saved collection.
- [ ] VERIFY-05 — Check dates against the information cutoff.
- [ ] VERIFY-06 — Check units, geography, period, and inflation measure.
- [ ] VERIFY-07 — Distinguish monthly, yearly, and annualized changes.
- [ ] VERIFY-08 — Check arithmetic independently.
- [ ] VERIFY-09 — Distinguish percentage changes from percentage-point changes.
- [ ] VERIFY-10 — Match forecast numbers exactly to pipeline output.
- [ ] VERIFY-11 — Check observed-versus-forecast labels.

### Critic and revision

- [ ] CRITIC-01 — Give the critic claims, source evidence, and draft.
- [ ] CRITIC-02 — Assess support for each material claim.
- [ ] CRITIC-03 — Check overstated certainty and unsupported causal explanations.
- [ ] CRITIC-04 — Check omitted contradictory evidence.
- [ ] CRITIC-05 — Require structured findings with reasons and evidence references.
- [ ] CRITIC-06 — Allow keep, revise, remove, retrieve more, or request review.
- [ ] CRITIC-07 — Limit revision cycles and recheck revised claims.
- [ ] CRITIC-08 — Block publication for unresolved critical issues.

### Evaluate the critic

- [ ] CRITIC-09 — Create known-error examples and correct examples.
- [ ] CRITIC-10 — Measure missed errors and incorrect flags.
- [ ] CRITIC-11 — Compare agent-only and agent-plus-critic results.
- [ ] CRITIC-12 — Check whether revisions introduce errors.
- [ ] CRITIC-13 — Measure added runtime and cost.
- [ ] CRITIC-14 — Preserve human review for ambiguous cases.

**Deliverables:** Verification checks, claim ledger, critic workflow, comparison report.

### Exit criteria

- [ ] Known critical errors trigger the intended response.
- [ ] Correct claims are not routinely damaged by revision.
- [ ] Unresolved critical issues prevent successful publication.
- [ ] Measured benefits justify added time and cost.

## Phase 4 — Integrate forecasts and consolidate infrastructure

**Purpose:** Create one reproducible platform.

**Dependencies:** Working research and verification; minimal evidence storage.

### Forecast interface

- [ ] FORECAST-01 — Define the existing pipeline's output schema.
- [ ] FORECAST-02 — Include measure, geography, frequency, horizon, units, and generation date.
- [ ] FORECAST-03 — Include model version and input-data cutoff.
- [ ] FORECAST-04 — Include uncertainty intervals only where the pipeline provides them.
- [ ] FORECAST-05 — Preserve existing validation and baseline comparisons.
- [ ] FORECAST-06 — Check historical validation for future-information leakage.
- [ ] FORECAST-07 — Document limitations from unavailable historical data vintages.

### Data and workflow

- [ ] DATA-01 — Define source, observation, forecast, claim, evaluation, and run records.
- [ ] DATA-02 — Separate raw sources, processed data, and generated outputs.
- [ ] DATA-03 — Store observation period, publication date, retrieval time, and vintage where available.
- [ ] DATA-04 — Validate required fields, types, ranges, and duplicates.
- [ ] DATA-05 — Define freshness requirements and stale-input behavior.
- [ ] DATA-06 — Choose storage suitable for current scale.
- [ ] DATA-07 — Implement deduplication and safe reruns.
- [ ] DATA-08 — Define backup, retention, and schema-change procedures.
- [ ] FLOW-01 — Assign unique run IDs.
- [ ] FLOW-02 — Connect acquisition → forecast → research → verification → briefing.
- [ ] FLOW-03 — Save intermediate outputs and version information.
- [ ] FLOW-04 — Define Pending / Running / Succeeded / Failed / Blocked stage states.
- [ ] FLOW-05 — Prevent partial outputs from appearing completed.
- [ ] FLOW-06 — Retry safely without duplicate publications.
- [ ] FLOW-07 — Preserve evidence and original outputs even if exact LLM replay is unavailable.
- [ ] FLOW-08 — Add an end-to-end smoke test.
- [ ] FLOW-09 — Exercise one failure in each major stage.

**Deliverables:** Integrated workflow, schemas, storage, run history, failure rules.

### Exit criteria

- [ ] One action produces a complete briefing from valid inputs.
- [ ] Trace each briefing to its forecast and evidence.
- [ ] Failed stages create understandable failed or blocked runs.
- [ ] Inspect historical runs without relying on current source contents.

## Phase 5 — Build the usable release and deploy

**Purpose:** Make the system accessible outside your development session.

**Dependency:** Stable local integration and passing release evaluation.

### User experience

- [ ] UI-01 — Choose the smallest useful interface.
- [ ] UI-02 — Display forecasts, charts, and forecast horizon.
- [ ] UI-03 — Show information cutoff and generation date.
- [ ] UI-04 — Make citations and evidence accessible.
- [ ] UI-05 — Show limitations and important verification findings.
- [ ] UI-06 — Distinguish completed, running, failed, and stale results.
- [ ] UI-07 — Provide access to previous briefings.
- [ ] UI-08 — Test the full journey with someone unfamiliar with the project.

### Deployment and validation

- [ ] DEPLOY-01 — Choose hosting using runtime, storage, scheduling, and budget requirements.
- [ ] DEPLOY-02 — Separate development and deployed settings.
- [ ] DEPLOY-03 — Keep credentials outside code and generated reports.
- [ ] DEPLOY-04 — Restrict access appropriately.
- [ ] DEPLOY-05 — Document clean installation and startup.
- [ ] DEPLOY-06 — Add a health check.
- [ ] DEPLOY-07 — Add scheduling if required and prevent overlapping runs.
- [ ] DEPLOY-08 — Specify the schedule timezone.
- [ ] DEPLOY-09 — Verify persistent storage survives restarts.
- [ ] DEPLOY-10 — Add logs and actionable failure alerts.
- [ ] DEPLOY-11 — Add run limits and spending visibility.
- [ ] DEPLOY-12 — Document stopping and rollback procedures.
- [ ] DEPLOY-13 — Run deployed smoke and full-briefing tests.
- [ ] DEPLOY-14 — Test restart and external-request failure.
- [ ] DEPLOY-15 — Check that credentials do not appear in the interface or logs.
- [ ] DEPLOY-16 — Run release evaluation against the deployed configuration.

**Deliverables:** Accessible application, deployment configuration, operating guide, release results.

### Exit criteria

- [ ] A user can access and understand results.
- [ ] The platform runs without your development session.
- [ ] Persistence, failure reporting, and rollback have been exercised.
- [ ] The deployed configuration passes release gates.

## Phase 6 — Harden using observed failures

**Purpose:** Improve dependable operation under realistic conditions.

**Dependency:** Working deployed release.

### Failure testing

- [ ] HARDEN-01 — Test source downtime, rate limits, and timeouts.
- [ ] HARDEN-02 — Test changed page formats and missing tables.
- [ ] HARDEN-03 — Test stale, duplicated, revised, and malformed data.
- [ ] HARDEN-04 — Test invalid model responses and invalid forecast output.
- [ ] HARDEN-05 — Test simultaneous and interrupted runs.
- [ ] HARDEN-06 — Test source content attempting to redirect the agent.
- [ ] HARDEN-07 — Verify retry limits and recovery.
- [ ] HARDEN-08 — Exercise backup restoration.
- [ ] HARDEN-09 — Verify critical failures cannot silently produce normal-looking briefings.

### Operational improvement

- [ ] OPS-01 — Track run success, duration, cost, and freshness.
- [ ] OPS-02 — Track verification failures and human corrections.
- [ ] OPS-03 — Choose an observation window and reliability targets before assessing results.
- [ ] OPS-04 — Operate through that window and record material incidents.
- [ ] OPS-05 — Add suitable incidents to evaluation cases.
- [ ] OPS-06 — Fix recurring high-impact problems first.
- [ ] OPS-07 — Rerun relevant evaluations after fixes.
- [ ] OPS-08 — Document limitations and recovery steps.

**Deliverables:** Failure-test results, operational report, regression cases, recovery guide.

### Exit criteria

- [ ] Meet declared reliability and cost targets over the observation window.
- [ ] Make material failures visible and diagnosable.
- [ ] Exercise recovery procedures successfully.
- [ ] Document known limitations accurately.

## Phase 7 — Package portfolio evidence

**Purpose:** Demonstrate the work through reproducible results and clear explanations.

**Dependency:** Working release. Capture evidence throughout earlier phases.

- [ ] PORT-01 — Publish the workflow diagram and explain tool choices.
- [ ] PORT-02 — Show a complete research trace from question to cited finding.
- [ ] PORT-03 — Explain one failure and the resulting improvement.
- [ ] PORT-04 — Justify workflow complexity.
- [ ] PORT-05 — Describe evaluation cases, rubric, and limitations.
- [ ] PORT-06 — Present baseline-versus-improved results.
- [ ] PORT-07 — Present agent-only versus agent-plus-critic results.
- [ ] PORT-08 — Report quality alongside cost and runtime.
- [ ] PORT-09 — Explain leakage and data-revision handling.
- [ ] PORT-10 — Report held-out results without repeated tuning against them.
- [ ] PORT-11 — Show deployment architecture and operating workflow.
- [ ] PORT-12 — Demonstrate a successful run and a handled failure.
- [ ] PORT-13 — Include monitoring and recovery evidence.
- [ ] PORT-14 — Record a short demonstration.
- [ ] PORT-15 — Write the problem, decisions, results, and limitations case study.
- [ ] PORT-16 — Verify another person can follow setup and reproduction instructions.

**Deliverables:** Case study, demonstration, diagrams, evaluation report, usable documentation.

### Exit criteria

- [ ] Another person can understand what you built and why.
- [ ] Quality and reliability claims link to evidence.
- [ ] Agents, evaluation, and deployment are demonstrated within one system.

## Milestone dashboard

| Milestone | Completion gate | Initial status |
| --- | --- | --- |
| M0 — Scope | Scope, inventory, sample briefing | To confirm |
| M1 — Evaluation | Repeatable cases, rubric, baseline | To build |
| M2 — Agent | Traceable research passes agreed criteria | In progress |
| M3 — Verification | Critical failures trigger controlled responses | To build |
| M4 — Integration | Complete traceable local workflow | To build |
| M5 — Deployment | Accessible system passes release checks | To build |
| M6 — Hardening | Reliability targets met over observation window | To build |
| M7 — Portfolio | Demo and evidence-backed case study | To build |

The existing forecasting pipeline is a component within M4. Rebuilding it is not required before M1–M3.

## Learning ownership

Use AI coding assistance throughout. Own the specification, inspection, and verification of important behavior.

| Area | Understand and verify personally | AI implementation assistance |
| --- | --- | --- |
| Agent | Tools, evidence flow, limits, stopping | Connectors, extraction, orchestration |
| Evaluation | Cases, scoring, severity, interpretation | Runner, reports, storage |
| Critic | Claim support, false flags, publication rules | Extraction, checks, revision |
| Forecast integration | Units, cutoffs, horizons, limitations | Adapters, validation |
| Infrastructure | Provenance, freshness, revisions, recovery | Storage, ingestion, migrations |
| Deployment | Credentials, persistence, monitoring, rollback | Packaging, configuration, automation |

For each major component:

- [ ] Explain its purpose.
- [ ] Identify inputs and outputs.
- [ ] Predict failure behavior.
- [ ] Inspect a successful run.
- [ ] Exercise a meaningful failure.
- [ ] Confirm recovery.

## Weekly review template

**Week of:**

**Current milestone:**

**Deliverable to finish:**

- [ ] Review completed tasks and evidence.
- [ ] Run relevant evaluations.
- [ ] Review important failures.
- [ ] Compare quality, cost, and runtime where relevant.
- [ ] Resolve or defer open decisions.
- [ ] Remove unnecessary scope.
- [ ] Select the next three Ready tasks.

**What now works:**

**What remains unreliable:**

**Decision and reason:**

**Blocker:**

**Next concrete action:**

## First five work sessions

### Session 1 — Establish the starting point

- [ ] Save current forecast and research outputs.
- [ ] Complete the inventory.
- [ ] Choose geography, measure, user, and output.
- [ ] Draft the sample briefing.

**Finish with:** A clear target and accurate inventory.

### Session 2 — Build the evaluation seed

- [ ] Write 10 cases with expected facts, evidence, and cutoffs.
- [ ] Define scoring and critical failures.
- [ ] Reserve held-out cases.

**Finish with:** A usable initial evaluation set.

### Session 3 — Measure the current agent

- [ ] Run and manually score development cases.
- [ ] Identify the three most important failure patterns.
- [ ] Choose one improvement.

**Finish with:** A baseline report and justified implementation task.

### Session 4 — Improve evidence traceability

- [ ] Implement the chosen improvement.
- [ ] Ensure findings retain evidence references and dates.
- [ ] Rerun evaluation and inspect regressions.

**Finish with:** A measured change in performance.

### Session 5 — Close the next agent gap

- [ ] Fix the next highest-impact failure.
- [ ] Verify stop conditions and resource limits.
- [ ] Save an end-to-end trace.
- [ ] Choose the first explicit verification check.

**Finish with:** A stronger baseline and concrete verification task.

## Deferred backlog

- [ ] Add future ideas here only after recording why they can wait.

Advance according to exit criteria. Anchor each session to an observable output.
