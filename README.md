> Opinionated cookiecutter template for Cellular Semantics agentic-workflow repositories.

# CellSem Agentic Workflow Template

This repo hosts the source template that generates new agentic workflow projects.  
It codifies the CLAUDE.md rules (TDD-first, strict linting, dotenv usage) and
bundles runtime dependencies like `cellsem_llm_client`, `deep-research-client`, and
`pydantic-ai` so every generated project is ready for LLM orchestration out of the box.

## What's Included

- `cookiecutter.json` prompts for project metadata (`project_name`, `project_slug`, etc.).
- Template directory `{{cookiecutter.project_slug}}/` with:
  - Pyproject configured for uv, Ruff, MyPy, pytest (unit default) and coverage.
  - Source layout: `agents/`, `graphs/` (Pydantic + pydantic-ai), `schemas/` (JSON schemas),
    `services/`, and `utils/`.
  - Docs scaffold, scripts, git hooks, GitHub Actions workflow, and CLAUDE-style README.
- Guardrail tests (`tests/unit/test_template_structure.py`) that ensure the template stays complete.

## Prerequisites

- Python 3.11+ (matching the template default).
- [`cookiecutter`](https://cookiecutter.readthedocs.io/) installed (`pipx install cookiecutter` recommended).
- [`uv`](https://github.com/astral-sh/uv) for dependency management in generated repos.

## Generate a New Project

```bash
cookiecutter gh:Cellular-Semantics/CellSemAgenticWorkflow

# answer prompts for project name, slug, description, etc.
# then jump into the new directory
cd <your-project-slug>

# install dependencies via uv
uv sync --dev

# configure git hooks and run tests
git config core.hooksPath .githooks
uv run pytest -m unit
```

The generated README explains how to add API keys to `.env`, run integration tests locally,
and leverage the provided git hooks + CI workflow.

## Developing the Template

1. Follow `CLAUDE.md` (write/modify tests first).
2. Run the test suite: `pytest -m unit`.
3. Commit changes that keep `tests/unit/test_template_structure.py` green.

When you add new files to the template, also update the structure test so regressions are caught automatically.

## Release Process

1. Update the template content and tests.
2. Optionally tag a release (e.g., `git tag v0.x.y && git push --tags`).
3. Consumers can reference a specific tag via `cookiecutter gh:Cellular-Semantics/CellSemAgenticWorkflow --checkout v0.x.y`.

## Support

If you notice missing pieces or want additional scaffolding (extra workflows, hook scripts, docs),
open an issue or PR. Keep contributions aligned with the repo rules (TDD, real integration testing, dotenv).
