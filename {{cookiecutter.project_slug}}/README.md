# {{cookiecutter.project_name}}

[![Tests](https://github.com/{{cookiecutter.github_org}}/{{cookiecutter.project_slug}}/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/{{cookiecutter.github_org}}/{{cookiecutter.project_slug}}/actions/workflows/test.yml)
[![coverage](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/{{cookiecutter.github_org}}/{{cookiecutter.project_slug}}/main/.github/badges/coverage.json)](https://github.com/{{cookiecutter.github_org}}/{{cookiecutter.project_slug}}/actions/workflows/test.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Python {{cookiecutter.python_version}}+](https://img.shields.io/badge/python-{{cookiecutter.python_version}}+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

{{cookiecutter.description}}

---

## What this project does

This repo implements an agentic workflow using the [CellSem Agentic Workflow Template](https://github.com/Cellular-Semantics/CellSemAgenticWorkflow). The approach is built around three principles:

**Declarative prompts and schemas.** Every prompt lives in a versioned `.prompt.yaml` file co-located with the code that uses it. Every data contract lives in a JSON Schema file in `schemas/`. Pydantic models are generated from those schemas — the schema is always the source of truth. This makes prompt changes reviewable (`git diff **/*.prompt.yaml`) and every past run reproducible.

**Dual-mode operation.** The same prompts and schemas power two modes:

- **Programmatic** — call the Python package directly from scripts or pipelines
- **Agentic** — load `AGENT.md` and let Claude execute the workflow interactively

There is no separate prompt set for each mode. `AGENT.md` reads the same `.prompt.yaml` and `.schema.json` files from `src/` via `@` imports.

**Provenance first.** Every run writes `provenance.json` as the first file in its output directory, before any LLM call. This records the git version, package version, sha256 hash of each prompt and schema, model settings, and a hash of the input. `--dry-run` prints the full provenance report and exits without calling any API.

---

## 🚀 Quick Start

**First time setup:**

```bash
git clone https://github.com/{{cookiecutter.github_org}}/{{cookiecutter.project_slug}}.git
cd {{cookiecutter.project_slug}}
uv sync --dev
git config core.hooksPath .githooks
```

Generated repo auto-inits git and sets origin to whatever you entered for `git_remote`
(default: `git@github.com:{{cookiecutter.github_org}}/{{cookiecutter.project_slug}}.git`).
Update the remote if you plan to push elsewhere.

**API keys** — create `.env` in the project root (never commit it):

```bash
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

`cellsem_llm_client` calls `load_dotenv()` on import, so the keys are available to all
agents, services, and tests automatically.

**Run the workflow (programmatic):**

```python
from {{cookiecutter.package_name}} import bootstrap

bootstrap()  # loads .env and performs startup checks
```

**Run the workflow (agentic):**

```bash
claude --context AGENT.md
# or within a Claude Code session:
# /run-workflow
```

In agentic mode, Claude reads the canonical prompts and schemas from `src/` via the
`@` imports in `AGENT.md` and executes the workflow steps interactively.

**Week 0 task:** before writing any domain logic, read `SCAFFOLD_GUIDE.md`. It has a
decision tree for every optional component so you can delete what your Ring 0 MVP does
not need.

---

## 🏗️ Architecture

```text
{{cookiecutter.project_slug}}/
├── pyproject.toml                           # UV workspace config
├── CLAUDE.md                                # Dev-mode instructions (auto-loaded)
├── AGENT.md                                 # Run-mode agent instructions
├── experiments/                             # Exploratory scripts (no TDD required)
├── src/
│   ├── {{cookiecutter.package_name}}/       # CORE PACKAGE (always keep)
│   │   ├── pyproject.toml
│   │   └── {{cookiecutter.package_name}}/
│   │       ├── agents/                      # Agent orchestration + *.prompt.yaml
│   │       ├── graphs/                      # Optional workflow graphs powered by Pydantic
│   │       ├── schemas/                     # JSON Schema source of truth
│   │       ├── services/                    # LLM + API integrations + *.prompt.yaml
│   │       ├── utils/                       # Supporting utilities (incl. provenance.py)
│   │       └── validation/                  # Cross-cutting validations (OPTIONAL)
│   └── {{cookiecutter.package_name}}_validation_tools/  # VALIDATION PACKAGE (OPTIONAL)
│       ├── pyproject.toml
│       └── {{cookiecutter.package_name}}_validation_tools/
│           ├── comparisons/                 # Compare workflow runs
│           ├── metrics/                     # Quality metrics
│           └── visualizations/             # Analysis plots
├── tests/
│   ├── unit/                                # Fast, isolated — @pytest.mark.unit
│   └── integration/                         # Real APIs, no mocks — @pytest.mark.integration
├── docs/                                    # Sphinx + MyST documentation
├── scripts/check-docs.py                    # Build docs with warnings-as-errors
├── .githooks/pre-commit                     # Lint → unit tests → integration tests
├── .github/workflows/test.yml               # CI: lint + unit tests only
└── .claude/commands/run-workflow.md         # /run-workflow skill
```

### Core package (always keep)

- `agents/`: Agent classes coordinating workflows (prompts co-located as `*.prompt.yaml`)
- `graphs/`: Optional workflow graphs powered by Pydantic + pydantic-ai
- `schemas/`: JSON Schema contracts — source of truth for all data models
- `services/`: LLM and API integrations (cellsem_llm_client, deep-research-client)
- `utils/`: Supporting utilities including provenance capture
- `validation/`: Cross-cutting validations (OPTIONAL — delete if `src/{{cookiecutter.package_name}}/validation` logic not needed)

### Validation package (optional)

Delete `src/{{cookiecutter.package_name}}_validation_tools/` if your Ring 0 does not need it.
It depends on the core package (imports schemas and models from it — no duplication).

- `comparisons/`: Tools for comparing workflow runs
- `metrics/`: Quality metrics (precision, recall, F1, etc.)
- `visualizations/`: Analysis plots (heatmaps, ROC curves, etc.)

---

## 📦 Packages

Two independently publishable packages managed as a UV workspace. A single `uv sync` installs both.

```bash
pip install {{cookiecutter.package_name}}                  # core workflow package
pip install {{cookiecutter.package_name}}-validation-tools # optional analysis tools
```

---

## 🔬 Output and provenance

Every run writes to a structured output directory:

```text
outputs/
└── {run_name}/
    └── {YYYY-MM-DD_HH-MM-SS}/
        ├── provenance.json       ← written first, before any LLM calls
        ├── step_1_output.json
        └── summary.json
```

`provenance.json` conforms to `schemas/run_provenance.schema.json` and records the git
commit, package version, sha256 hash of every prompt and JSON Schema used, model
settings, and a hash of the serialised input. Dry-run mode prints this report and exits
without executing any LLM calls.

---

## 🧪 Testing

- **Unit tests** (`tests/unit`, `@pytest.mark.unit`): no network, deterministic, fast
- **Integration tests** (`tests/integration`, `@pytest.mark.integration`): real APIs, fail hard if env vars missing — no mocks
- **Coverage**: 60% floor enforced (Ring 0 default); run `python scripts/graduate-ring.py --to 1` when Ring 0 ships to raise to 80% and add mypy
- **CI**: ruff lint, ruff format check, unit tests with coverage. Integration tests are skipped in CI — run them locally before pushing
- **Hooks**: pre-commit hook runs unit and integration tests before every commit (skips integration if API keys missing)

---

## 🛠️ Development

> This project was generated from the [CellSem Agentic Workflow Template](https://github.com/Cellular-Semantics/CellSemAgenticWorkflow).
> The template is a work in progress — some features have been tested in semi-vibe-coded
> library development but YMMV. Check the template repo for known issues and updates.

Read `CLAUDE.md` for the full development philosophy (TDD-first, ring-based scope
discipline, prompt and schema conventions). The short version:

1. Write a failing test first.
2. Implement the minimum code to make it pass.
3. Run the quality suite before committing.

### Development Workflow

```bash
# Run tests
uv run pytest                    # all tests
uv run pytest -m unit            # unit only
uv run pytest -m integration     # integration only (requires API keys)

# Code quality (Ring 0)
uv run ruff check --fix src/ tests/
uv run ruff format src/ tests/
# mypy is added when you graduate to Ring 1:
# python scripts/graduate-ring.py --to 1

# Docs
python scripts/check-docs.py
```

---

## 📋 Requirements

- **Python**: {{cookiecutter.python_version}}+
- **Dependencies**: managed via `uv sync --dev`
- **API keys**: OpenAI + Anthropic keys required for integration tests (hard fail if missing)

---

## 📄 License

{{cookiecutter.license}} License — see `LICENSE` for details.
