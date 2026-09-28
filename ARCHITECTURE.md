# Universal Analytical Agent — Architecture

## Milestone 0 status

This repository is an initialized Git repository rather than an existing
application. Its only tracked project file is an empty `.gitkeep`; there is no
source code, Python project metadata, dependency manifest, environment file,
container configuration, test suite, UI, database integration, LLM integration,
or user documentation to preserve.

Consequently, it is **best treated as a clean foundation for a new modular
architecture**, not as a source of reusable application components. The Git
history and repository identity should be retained, but there is no runtime
architecture to migrate or refactor.

## Current architecture

| Area | Current state |
| --- | --- |
| Application/runtime | Not present. |
| Python configuration | Not committed; the inspection environment provides Python 3.14.4, but that is not a project requirement. |
| Dependencies | No dependency or lock file. |
| LLM, databases, and tools | No integrations. |
| UI | No UI or frontend assets. |
| Tests | No test configuration or tests. |
| Configuration/secrets | No configuration or `.env` handling. |
| Containerization | No Docker or compose files. |
| Documentation | No project documentation before this document. |

## Target architecture

Build a small Python backend with explicit domain interfaces. Keep the backend
independent of a separately deployed UI. Select concrete providers and
libraries during later milestones only after the owner approves the open
questions in `PLAN.md`.

```text
Separate UI
    │ authenticated requests / streamed run events
    ▼
API / application service
    │ creates and observes a run
    ▼
Agent runtime ───────────────► run/event store
    │ plans and requests tool calls
    ├────────► LLM provider abstraction ──► hosted provider or Ollama
    └────────► tool registry ──► validated tool adapters ──► data sources
                                      │
                                      └──► deterministic validation/evaluation
```

### Major components and boundaries

1. **API/application service** accepts authenticated requests, validates input,
   applies authorization and policy, starts runs, and exposes run status. It
   must not embed provider-specific prompting or direct database queries.
2. **Agent runtime** owns the run state machine: context assembly, model calls,
   proposed tool calls, approvals, result handling, termination, and event
   emission. It orchestrates; it does not implement business/data tools.
3. **LLM abstraction** defines provider-neutral request, response, tool-call,
   structured-output, and usage types. Adapters implement that contract for
   selected hosted providers and Ollama. The first implementation is a small
   HTTP-based Ollama adapter; provider SDK types must not cross into runtime or
   tools.
4. **Tool system** is a registry of named tools with versioned input/output
   schemas, permissions, timeout/resource limits, and deterministic handlers. A
   separate executor validates inputs, applies an explicit policy, invokes the
   selected handler, emits run events, and normalizes results. The runtime only
   requests an invocation; tools cannot call the model or mutate agent state.
5. **Data layer** encapsulates connection configuration, query validation,
   parameter binding, execution, result normalization, and audit records.
   SQL should be read-only by default, use allowlisted connections/schemas, and
   require an explicit owner-approved policy and confirmation flow for any
   write capability.
6. **Validation/evaluation layer** validates structured model outputs and tool
   inputs/outputs, performs deterministic calculations and query checks, and
   supports replayable offline evaluation fixtures. LLM prose is never the
   authority for numerical results or policy decisions.
7. **UI layer** is a separate client that renders run timelines, evidence,
   results, warnings, and approval controls. It must never hold database or LLM
   credentials and must not execute tools directly.
8. **Observability and persistence** records immutable/sufficiently detailed
   run events: input references, selected provider/model, prompts or protected
   prompt references, tool requests/results, validations, approvals, errors,
   timings, and usage. Sensitive values need redaction before persistence.

## Agent runtime design

The implemented runtime is a small, explicit, testable state machine rather
than a general-purpose agent framework. Its inspectable per-run state contains
the run ID, original request, current messages, tool invocations/results, step
count, final response, status, and structured errors. It emits events for run
start, LLM request, action receipt, tool lifecycle, final response, failure, and
step-limit exhaustion.

A model response is untrusted text. The runtime alone parses it as strict JSON
into exactly one provider-neutral action: a final response or a named tool call
with object arguments. It then either completes or passes the invocation only
to the Tool Executor, which retains input validation and policy authority. The
runtime does not call handlers, grant approval, or create tools directly.

Each LLM/action iteration counts toward a configured positive maximum; exceeding
it produces a structured failure rather than an unbounded loop. No long-term
memory, automatic summarization, background execution, or multi-agent behavior
is present. Future runtime states may include `awaiting_approval`,
`waiting_for_tool`, `validating`, `completed`, `failed`, and `cancelled` as those
reviewed capabilities are introduced.

The runtime may ask a model to interpret a question, select from allowed tools,
or explain deterministic outputs. It must route computations, SQL validation,
and policy enforcement through deterministic components.

## Security boundaries

* Keep browser/UI, API, runtime, provider adapters, and data-source adapters in
  separate trust boundaries with least-privilege credentials.
* Load secrets from the deployment environment or a secret manager, validate
  configuration at startup, and never log raw secrets or unredacted sensitive
  data.
* Authenticate users and authorize workspaces, data sources, and each tool.
* Use per-source read-only database identities by default; prohibit arbitrary
  connection strings and unbounded query execution.
* Treat model output as untrusted input: schema-validate it, constrain tool
  choices, defend prompts and results against injection, and require approval
  for policy-defined sensitive actions.
* Apply request limits, tool timeouts, result-size limits, audit logging, and
  retention/redaction policies.

## Reuse decision

There are no existing application components to preserve or reuse. Preserve the
repository and its initial history; introduce the target components
incrementally after architectural decisions are approved rather than adding a
large framework up front.
