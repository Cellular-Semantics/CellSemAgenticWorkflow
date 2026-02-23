# Roadmap

This document tracks the planned and possible future development of the CellSem Agentic Workflow Template.

---

## Current functionality

The template generates a complete, opinionated project scaffold for agentic workflow development. Key capabilities in the generated project:

**Core architecture**
- UV workspace with two independently publishable packages: core workflow + optional validation tools
- Schema-first design: JSON schemas in `schemas/` are the single source of truth; Pydantic models generated from them programmatically
- Declarative prompts: `*.prompt.yaml` files co-located with the agents and services that use them; never hardcoded in Python
- pydantic-ai graph orchestration for multi-step workflows with typed dependencies

**Dual-mode operation**
- Programmatic mode: Python package runnable from scripts, pipelines, and CI
- Agentic mode: `AGENT.md` with Claude Code `@` imports pulls the same canonical prompts and schemas from `src/`; no duplication
- `/run-workflow` Claude Code skill switches an active session from dev mode to run mode

**Run provenance**
- `provenance.json` written as the first file in every output directory, before any LLM call
- Records: git version, package version, sha256 hash of every prompt and schema, model settings, input hash
- `--dry-run` prints the full provenance report and exits without making API calls
- Schema at `schemas/run_provenance.schema.json`; implementation at `utils/provenance.py`

**Ring-based quality enforcement**
- All projects start at Ring 0: ruff lint + format, 60% coverage, no mypy
- `scripts/graduate-ring.py --to 1` patches hook, CI, and pyproject.toml to Ring 1 (80% coverage + mypy) in one step
- `CLAUDE.md` instructs the agent to remind the developer to run the graduation script when Ring 0 scope is complete
- Pre-commit hook and CI are consistent at both rings; integration tests are local-only (real APIs, no mocks)

**Exploratory space**
- `experiments/` directory excluded from ruff, mypy, and coverage; not subject to TDD
- Clear graduation convention: proven patterns move to `src/` with tests

**Libraries bundled**
- [`cellsem_llm_client`](https://github.com/Cellular-Semantics/cellsem_llm_client): LiteLLM + pydantic-ai wrapper; handles dotenv, provider routing, typed outputs
- [`deep-research-client`](https://github.com/monarch-initiative/deep-research-client): Perplexity API / deep research workflows (optional; remove if not needed for Ring 0)

**Template quality guardrails**
- `tests/unit/test_template_structure.py`: 14 structural tests that fail if template files go missing or required fragments are removed

---

## Priority 1: Propagate agentic environment settings across platforms

**Goal:** Support propagating the agentic environment configuration from Claude Code to other agentic environments — specifically Codex and Copilot/VSCode — so a single repo definition drives consistent agent behaviour across platforms.

**Context:** Scripts and skills for this already exist in other repos. The consolidation path is still being determined — it may require a shared library that this template imports, or a standalone propagation tool. Details TBD once the existing work is reviewed.

**Open questions:**

- Where does the consolidation live — a new `cellsem-platform-tools` library, or an extension to an existing one?
- What is the minimum shared surface? (e.g. skills/commands, AGENT.md conventions, MCP server declarations, settings files)
- How are platform-specific settings (key names, model aliases) handled at propagation time?

---

## Possible future development

### Refactor monolithic CLAUDE.md to skills

`CLAUDE.md` currently carries a large amount of instruction: development philosophy, ring rules, scaffold guidance, prompt conventions, ring graduation reminder, and project-specific configuration. As projects grow, this becomes unwieldy.

**Potential approach:** Break domain-independent instructions into reusable Claude Code skills (`.claude/commands/*.md`) that can be invoked on demand — e.g. `/ring-status`, `/scaffold-review`, `/prompt-conventions` — leaving `CLAUDE.md` as a lightweight project-specific config file that imports them.

**Consideration:** Skills require explicit invocation; `CLAUDE.md` is always loaded. Some instructions (ring rules, TDD discipline) benefit from always being in context. The split needs to distinguish "always-on constraints" from "reference documentation".

### Orchestrator + distinct subagents

The current agentic mode uses a single Claude session with all context loaded via AGENT.md. For more complex workflows this may be insufficient.

**Potential approach:** An orchestrator agent that:
- Delegates research tasks to a research subagent (deep-research-client, literature synthesis)
- Delegates implementation tasks to a coding subagent (with CLAUDE.md context)
- Delegates review/validation tasks to a review subagent (with schema and provenance context)

**Consideration:** Subagent orchestration adds coordination overhead and cost. Justified only once single-session complexity becomes a clear bottleneck — likely Ring 2+ for most projects.
