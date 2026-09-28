# Universal Analytical Agent — Implementation Plan

## Milestone 0: reconnaissance and architecture baseline — complete

Completed work: inspected the repository, runtime environment, project
configuration candidates, tests, Git state, and tracked files; recorded the
findings in `ARCHITECTURE.md`; and deliberately made no application changes.

## Proposed milestones and dependencies

| Milestone | Scope | Depends on |
| --- | --- | --- |
| 1. Foundation | Approve Python support policy; create a minimal package, typed configuration, lint/test tooling, CI, and local developer instructions. | Owner decisions on Python version, packaging, and deployment target. |
| 2. Core contracts | Define provider-neutral LLM types, tool schemas/registry, run state/events, policy/approval interfaces, and deterministic validation contracts with unit tests. | 1 |
| 3. Data access MVP | Implement a selected read-only SQL adapter, connection allowlists, query policy/limits, result normalization, and auditing. | 2; owner decision on first database and authorization model. |
| 4. Runtime MVP | Implement the explicit orchestration state machine, one LLM adapter, approval gates, observability, and a small set of safe analytical tools. | 2 and 3 |
| 5. Backend API | Expose authenticated run creation, approval, cancellation, status, and event-stream endpoints; add persistence as required. | 4; owner decision on identity/persistence. |
| 6. Separate UI | Build a standalone UI for submitting analyses, inspecting evidence/timelines, and approving actions. | 5; owner decision on UI stack. |
| 7. Evaluation and hardening | Add replay fixtures, provider/tool contract tests, security testing, load/limit tests, redaction checks, and operational documentation. | 3–6 |
| 8. Additional providers/tools | Add Ollama and further providers/tools through the contracts, based on measured needs. | 7 |

## Proposed implementation order

1. Resolve the open questions below and explicitly approve Milestone 1 scope.
2. Establish minimal project conventions and automated quality checks.
3. Write contracts and tests before selecting SDKs or implementing integrations.
4. Deliver a read-only, audited data path before agentic orchestration.
5. Add a narrow, observable runtime with approval gates.
6. Add API, then a separately deployed UI.
7. Expand only after evaluation demonstrates correctness, safety, and operator
   visibility.

This ordering keeps deterministic data work, policy enforcement, and test
fixtures ahead of autonomous behavior.

## Testing strategy

* **Unit tests:** state transitions, schema validation, SQL policy decisions,
  result normalization, redaction, and configuration validation.
* **Contract tests:** run each LLM adapter and tool adapter against stable
  provider/tool-neutral fixtures; mock external services at the boundary.
* **Integration tests:** use disposable databases with read-only credentials to
  test parameterization, query restrictions, limits, timeouts, and audit data.
* **Runtime/replay tests:** persist sanitized event fixtures and assert the
  runtime produces expected decisions and terminal states without live model
  calls.
* **Security tests:** authorization isolation, tool allowlists, prompt-injection
  resistance scenarios, secret-redaction checks, and attempts to bypass SQL
  read-only policy.
* **End-to-end tests:** exercise API and UI approval flows against controlled
  fixtures. Live provider checks should be opt-in and must not be the sole
  correctness signal.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Model hallucination or unsafe tool selection | Constrain tool calls with schemas and policies; validate all outputs; make deterministic systems authoritative. |
| SQL data exposure or mutation | Read-only credentials by default, connection/schema allowlists, query limits, audits, and approval for exceptions. |
| Prompt injection through data/results | Treat all external content as untrusted, delimit/label it, constrain actions, and require policy checks independent of model output. |
| Provider lock-in | Keep provider SDK code behind a small abstraction and contract-test every adapter; retain an Ollama-compatible path. |
| Premature framework complexity | Start with standard-library-friendly modular Python and introduce dependencies only for demonstrated needs. |
| Insufficient observability | Make run events, transitions, validation outcomes, and approval records first-class from the runtime MVP. |
| Ambiguous human authority | Specify approval policies and UI decision points before enabling material actions. |

## Open architectural questions for owner approval

1. What is the initial analytical use case, user persona, and success metric?
2. Which database(s), data classifications, tenancy model, and identity provider
   are in scope for the first release?
3. Is all SQL strictly read-only in the first release, and which exceptional
   actions require an explicit human approval?
4. Which LLM provider/model is the first target, and are local/Ollama deployment
   requirements mandatory or optional for the MVP?
5. What data may leave the deployment boundary for a hosted model, and what
   retention, redaction, and audit requirements apply?
6. What deployment environment and Python version support policy should be
   adopted? The inspected container's Python 3.14.4 is not yet a project
   decision.
7. What UI stack, authentication experience, and approval/audit workflow does
   the owner prefer?
8. How should run history and data-source credentials be stored, retained, and
   deleted?
9. Which performance, cost, availability, and evaluation thresholds define MVP
   readiness?

## Current validation result

No existing test suite, test configuration, or tests were discovered at
Milestone 0. No application code was added; future milestones should add tests
alongside each component.
