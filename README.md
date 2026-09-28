# Universal Analytical Agent

A human-controlled foundation for a future analytical agent. The project is
currently at **Milestone 4: Minimal Agent Runtime**. It provides typed contracts,
configuration validation, provider-neutral LLM interfaces, an offline fake
provider, a small Ollama adapter, safe deterministic tool execution, and a
bounded single-agent runtime.

It deliberately does **not** implement planning/reasoning loops beyond the
bounded action cycle, SQL, RAG, web search, Python execution, a backend API, or
a UI. Those capabilities require architectural review and later milestones.

## Requirements

* Python 3.11 or later.
* `pip` (or another PEP 517-compatible installer).

## Setup

Create and activate an isolated environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the package and developer tools:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Configuration

The foundation reads process environment variables; it does not load `.env`
files itself. Copy `.env.example` for local reference and have your shell or
deployment environment provide the values.

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `UAA_ENVIRONMENT` | No | `development` | One of `development`, `test`, or `production`. |
| `UAA_LOG_LEVEL` | No | `INFO` | Standard level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`. |
| `UAA_DEPLOYMENT_ID` | In production only | None | Non-secret deployment identifier for future run events. |
| `UAA_OLLAMA_BASE_URL` | For Ollama only | None | HTTP(S) endpoint of the selected Ollama deployment. |
| `UAA_OLLAMA_MODEL` | For Ollama only | None | Approved Ollama model identifier. |
| `UAA_OLLAMA_TIMEOUT_SECONDS` | For Ollama only | None | Positive timeout for one non-streaming request. |
| `UAA_AGENT_MAX_STEPS` | No | `4` | Positive maximum LLM/action steps in a runtime run. |

There are intentionally no default Ollama URL or model values. Constructing an
`OllamaProvider` requires all three Ollama settings. Do not commit API keys,
tokens, passwords, connection strings, or a local `.env` file. No secret-valued
setting exists until an approved concrete integration needs one.

## LLM provider layer

Application code depends on the `LLMProvider` protocol and provider-neutral
`LLMRequest`, `LLMMessage`, `GenerationOptions`, and `LLMCompletion` contracts.
The Ollama adapter translates those values to the non-streaming `/api/chat` HTTP
endpoint using the Python standard library; no Ollama SDK or AI framework is a
runtime dependency.

Use `FakeLLMProvider` for offline unit tests and future runtime fixtures. It
returns a configured deterministic response, records requests, or raises a
configured project `ProviderError`. Tests can inject an `OllamaHTTPTransport`
into `OllamaProvider`, so normal tests never require an Ollama server or network
access.

No optional live-Ollama integration test is included in this milestone.

## Tool execution layer

A **Tool Registry** stores explicitly registered tool definitions and their
handlers. A **Tool Executor** receives a caller-selected `ToolInvocation`, looks
up its definition, validates the declared input-schema subset, checks an explicit
**Execution Policy**, invokes a deterministic synchronous or asynchronous
handler, and returns a correlated `ToolResult`.

The executor never selects tools, calls an LLM, grants approval, or runs shell
commands, arbitrary Python, subprocesses, or filesystem traversal. Those
responsibilities do not exist in this milestone. `AdditionTool` is the only small
infrastructure example; it adds two validated integers without external effects.

The default policy permits registered tools unless a definition declares that
human approval is required. Policy decisions, validation failures, execution
starts/completions/failures, and denials emit structured run events. The future
agent/planner may request an invocation, but it must remain separate from this
registry, policy, and executor boundary.

## Minimal agent runtime

`AgentRuntime` runs a single bounded interaction: user request → provider-neutral
LLM → strict JSON action → either final response or `ToolExecutor` invocation →
tool result → LLM → final response. Model output is untrusted and only two action
shapes are accepted: `{"action":"final","content":"..."}` and
`{"action":"tool_call","tool_name":"...","arguments":{...}}`.

For example, a deterministic fake provider can first request
`addition(left=2, right=3)` and then return a final response after the executor
supplies its result. Each run keeps inspectable messages, invocations, results,
step count, final response, status, and structured errors. Runs stop safely when
a final action is produced, a tool/provider/action failure occurs, or
`UAA_AGENT_MAX_STEPS` is reached. The runtime does not call tool handlers
directly, grant approval, evaluate generated code, or select/implement tools.

## Quality checks

Run the offline test suite:

```bash
python -m pytest
```

Run style and type checks:

```bash
python -m ruff check .
python -m ruff format --check .
python -m mypy
```

## Architecture and plan

`ARCHITECTURE.md` is the architectural source of truth, and `PLAN.md` records
the approved milestone sequence and open owner decisions. This milestone keeps
the implementation intentionally small so later runtime, data, API, and UI
components can remain independently testable.
