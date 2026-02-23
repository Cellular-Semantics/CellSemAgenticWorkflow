# CellSem Agentic Workflow Template

> Standard cookiecutter template for the Cellular Semantics team. Generates reproducible, production-ready agentic workflow repositories.

[![Template Tests](https://github.com/Cellular-Semantics/CellSemAgenticWorkflow/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/Cellular-Semantics/CellSemAgenticWorkflow/actions/workflows/tests.yml)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![cookiecutter](https://img.shields.io/badge/built%20with-cookiecutter-blue.svg)](https://cookiecutter.readthedocs.io/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

## Why use this template?

Building LLM-powered workflows well is harder than it looks. Prompts drift silently,
model outputs change between releases, validation is bolted on late, and exploratory
notebooks gradually become production code with no tests. This template encodes the
Cellular Semantics team's accumulated approach to avoiding those failure modes.

**You get:**

- A project that works the same way whether you run it programmatically or hand it to a
  Claude agent — prompts and schemas are the shared source of truth for both.
- Validation built in from day one, not retrofitted: every run writes a provenance record
  before touching any API.
- A ring-based development discipline that stops scope from expanding before an MVP ships.
- Automated quality checks that scale with the project: loose for exploratory Week 0,
  tighter once the MVP is proven.

---

## Design philosophy

### Declarative prompts and schemas

Prompts live in versioned `.prompt.yaml` files co-located with the code that uses them —
never hardcoded in Python. Schemas live in `schemas/` as JSON Schema files that serve as
the single contract between agents, services, and tests. Pydantic models are generated
from those JSON schemas, not written by hand, so the schema stays canonical.

This makes it trivial to review a prompt change (`git diff **/*.prompt.yaml`), reproduce
any past run by checking out an old commit, and share the same prompts between the Python
runtime and the Claude agent without duplication.

### Dual-mode operation

Every generated project supports two modes that read the same prompts and schemas:

| Mode | How to invoke | When to use |
| --- | --- | --- |
| **Programmatic** | `python` / `uv run` | Automated pipelines, batch runs, CI |
| **Agentic** | `claude --context AGENT.md` or `/run-workflow` | Interactive runs, exploration, manual QA |

`AGENT.md` uses Claude Code `@` imports to pull the `.prompt.yaml` and `.schema.json`
files directly from `src/` at session start. The agent follows the same workflow steps
as the Python code — no separate prompt maintenance.

### Provenance first

Every run — including `--dry-run` — writes `provenance.json` as the first file in its
output directory, before any LLM call. It records the git version, package version,
sha256 hash of each prompt and schema file, active model settings, and a hash of the
serialised input. This means every output directory is self-contained evidence of
exactly what ran and what it used.

`--dry-run` prints the full provenance report (prompts, schemas, settings, hashes) and
exits without making any API calls, making it safe to inspect a workflow before running it.

### Ring-based development

Projects move through rings. You cannot start Ring N+1 until Ring N has shipped and been
validated with users.

```text
Exploratory (Week 0)  →  Ring 0 (MVP)  →  Ring 1  →  Ring 2  →  …
```

The `strict_quality_checks` cookiecutter variable encodes which ring you are starting in:

| Setting | Ring | Coverage floor | mypy on commit |
| --- | --- | --- | --- |
| `n` | Ring 0 (MVP) | 60% | No |
| `y` | Ring 1+ | 80% | Yes |

This prevents quality gates from blocking an MVP while ensuring they are in place before
the codebase matures.

---

## What gets generated

```text
<your-project-slug>/
├── pyproject.toml                  # UV workspace; ruff, mypy, pytest, coverage config
├── CLAUDE.md                       # Dev-mode instructions (auto-loaded by Claude Code)
├── AGENT.md                        # Run-mode instructions (loaded explicitly)
├── SCAFFOLD_GUIDE.md               # What to keep/delete for your Ring 0 MVP
├── experiments/                    # No-rules scratch space (excluded from all checks)
├── src/
│   ├── <package_name>/             # Core package (always keep)
│   │   └── <package_name>/
│   │       ├── agents/             # Agent classes + co-located *.prompt.yaml files
│   │       ├── graphs/             # pydantic-ai graph orchestration (optional)
│   │       ├── schemas/            # JSON schemas — source of truth for all data models
│   │       ├── services/           # LLM + API integrations + *.prompt.yaml files
│   │       ├── utils/              # Shared utilities (includes provenance.py)
│   │       └── validation/         # Cross-cutting validation helpers (optional)
│   └── <package_name>_validation_tools/  # Validation package (optional)
│       └── ...                     # comparisons/, metrics/, visualizations/
├── tests/
│   ├── unit/                       # Fast, no network, @pytest.mark.unit
│   └── integration/                # Real APIs, fail hard if keys missing, @pytest.mark.integration
├── docs/                           # Sphinx + MyST; auto-built and checked pre-commit
├── scripts/check-docs.py           # Build docs with warnings-as-errors
├── .githooks/pre-commit            # Lint → unit tests → integration tests (if keys present)
├── .github/workflows/test.yml      # CI: lint + unit tests only (no API keys needed)
└── .claude/commands/run-workflow.md  # /run-workflow skill: switches Claude to agent mode
```

---

## Libraries

### [`cellsem_llm_client`](https://github.com/Cellular-Semantics/cellsem_llm_client)

The standard LLM client used across all CellSem workflow projects. It wraps
[LiteLLM](https://github.com/BerriAI/litellm) (provider-agnostic model calls) with
[pydantic-ai](https://ai.pydantic.dev/) for typed, validated agent outputs.
`pydantic-ai` graphs define multi-step workflows with typed dependency injection and
safe node routing. The client loads `.env` via `python-dotenv` automatically so API
keys are available to agents and services without extra wiring.

### [`deep-research-client`](https://github.com/monarch-initiative/deep-research-client)

Client for deep research workflows — literature search, Perplexity API integration, and
multi-source synthesis. Include if your Ring 0 involves research-heavy steps; remove from
`pyproject.toml` otherwise.

---

## Quality checks

| Check | When it runs | Tool |
| --- | --- | --- |
| Lint + format | commit, CI | `ruff check --fix` + `ruff format --check` |
| Type checking | commit (Ring 1+) | `mypy src/` |
| Unit tests | commit, CI | `pytest -m unit` |
| Integration tests | commit (if API keys present) | `pytest -m integration` |
| Docs build | commit | `python scripts/check-docs.py` |
| Coverage floor | CI | 60% (Ring 0) or 80% (Ring 1+) |

Integration tests use real APIs and fail hard if keys are absent. There are no mocks.
CI runs only unit tests to avoid requiring secrets in GitHub Actions.

---

## Generate a new project

```bash
# Install prerequisites (once)
pipx install cookiecutter
# uv: see https://github.com/astral-sh/uv

cookiecutter gh:Cellular-Semantics/CellSemAgenticWorkflow

# Answer prompts: project_name, project_slug, package_name, python_version,
# github_org, git_remote, strict_quality_checks (n = Ring 0, y = Ring 1+)

cd <your-project-slug>
uv sync --dev
git config core.hooksPath .githooks
uv run pytest -m unit
```

Read the generated `SCAFFOLD_GUIDE.md` before writing any code. It has a decision tree
for every optional component so you can delete what your Ring 0 does not need.

---

## Developing this template

1. Write (or update) tests in `tests/unit/test_template_structure.py` **first**.
2. Confirm red: `uv run pytest -m unit`.
3. Add the template files, confirm green.
4. Commit tests and implementation in separate commits.

When adding new files to the template, add their paths to `expected_paths` in the
structure test — the guardrail will catch regressions on every future change.

## Release process

1. Confirm all unit tests pass: `uv run pytest -m unit`.
2. Tag the release: `git tag v0.x.y && git push --tags`.
3. Consumers pin a version:

   ```bash
   cookiecutter gh:Cellular-Semantics/CellSemAgenticWorkflow --checkout v0.x.y
   ```

## Support

Open an issue or PR. Contributions must follow the repo rules: TDD, real integration
testing (no mocks), dotenv for secrets, tests updated before implementation.
