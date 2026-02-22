from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_ROOT = REPO_ROOT / "{{cookiecutter.project_slug}}"


def _relative(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


@pytest.mark.unit
def test_cookiecutter_json_defines_core_variables() -> None:
    config_path = REPO_ROOT / "cookiecutter.json"
    assert config_path.exists(), "cookiecutter.json is missing at the repo root"

    config = json.loads(config_path.read_text())
    required_keys = {
        "project_name",
        "project_slug",
        "package_name",
        "python_version",
        "github_org",
        "git_remote",
        "strict_quality_checks",
    }
    missing = required_keys.difference(config)
    assert not missing, f"cookiecutter.json missing keys: {sorted(missing)}"

    # Validate strict_quality_checks is a list with 'y' and 'n' options
    assert isinstance(config["strict_quality_checks"], list), \
        "strict_quality_checks must be a list of options"
    assert "y" in config["strict_quality_checks"], \
        "strict_quality_checks must include 'y' option"
    assert "n" in config["strict_quality_checks"], \
        "strict_quality_checks must include 'n' option"


@pytest.mark.unit
def test_template_contains_minimal_agentic_structure() -> None:
    assert TEMPLATE_ROOT.exists(), _relative(TEMPLATE_ROOT) + " directory is missing"

    expected_paths = [
        TEMPLATE_ROOT / "pyproject.toml",
        TEMPLATE_ROOT / "README.md",
        TEMPLATE_ROOT / "CLAUDE.md",
        TEMPLATE_ROOT / "LICENSE",
        TEMPLATE_ROOT / ".gitignore",
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "{{cookiecutter.package_name}}" / "__init__.py",
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "{{cookiecutter.package_name}}" / "graphs" / "__init__.py",
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "{{cookiecutter.package_name}}" / "agents" / "__init__.py",
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "{{cookiecutter.package_name}}" / "schemas" / "__init__.py",
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "{{cookiecutter.package_name}}" / "services" / "__init__.py",
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "{{cookiecutter.package_name}}" / "utils" / "__init__.py",
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "{{cookiecutter.package_name}}" / "validation" / "__init__.py",
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "{{cookiecutter.package_name}}" / "graphs" / "definitions.py",
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "{{cookiecutter.package_name}}" / "graphs" / "graph_agent.py",
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "{{cookiecutter.package_name}}" / "schemas" / "workflow_output.schema.json",
        TEMPLATE_ROOT / "tests" / "unit" / "test_unit_placeholder.py",
        TEMPLATE_ROOT / "tests" / "integration" / "test_integration_env.py",
        TEMPLATE_ROOT / "docs" / "conf.py",
        TEMPLATE_ROOT / "scripts" / "check-docs.py",
        TEMPLATE_ROOT / ".githooks" / "pre-commit",
        TEMPLATE_ROOT / ".github" / "workflows" / "test.yml",
        TEMPLATE_ROOT / "experiments" / "README.md",
        TEMPLATE_ROOT / "AGENT.md",
        TEMPLATE_ROOT / ".claude" / "commands" / "run-workflow.md",
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "{{cookiecutter.package_name}}" / "schemas" / "run_provenance.schema.json",
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "{{cookiecutter.package_name}}" / "utils" / "provenance.py",
    ]

    missing = [p for p in expected_paths if not p.exists()]
    human_readable = [_relative(path) for path in missing]
    assert not missing, f"Missing template files/directories: {human_readable}"

    expected_directories = [
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "{{cookiecutter.package_name}}" / "agents",
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "{{cookiecutter.package_name}}" / "graphs",
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "{{cookiecutter.package_name}}" / "schemas",
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "{{cookiecutter.package_name}}" / "services",
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "{{cookiecutter.package_name}}" / "utils",
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "{{cookiecutter.package_name}}" / "validation",
        TEMPLATE_ROOT / "experiments",
        TEMPLATE_ROOT / ".claude",
        TEMPLATE_ROOT / ".claude" / "commands",
    ]
    dir_missing = [d for d in expected_directories if not d.is_dir()]
    human_dirs = [_relative(path) for path in dir_missing]
    assert not dir_missing, f"Missing src subdirectories: {human_dirs}"

    readme_text = (TEMPLATE_ROOT / "README.md").read_text()
    expected_fragments = [
        "[![Tests]",
        "[![coverage]",
        "[![Python {{cookiecutter.python_version}}+]",
        "## 🚀 Quick Start",
        "## 🏗️ Architecture",
        "### Development Workflow",
        "{{cookiecutter.github_org}}/{{cookiecutter.project_slug}}",
        "Optional workflow graphs powered by Pydantic",
        "pydantic-ai",
        "JSON Schema",
        "Supporting utilities",
        "src/{{cookiecutter.package_name}}/validation",
        "git config core.hooksPath .githooks",
        "GitHub Actions runs only `uv run pytest -m unit`",
        "pre-commit hook runs unit and integration tests",
        "Generated repo auto-inits git and sets origin to",
    ]
    absent = [fragment for fragment in expected_fragments if fragment not in readme_text]
    assert not absent, f"README missing required sections: {absent}"

    workflow_text = (TEMPLATE_ROOT / ".github" / "workflows" / "test.yml").read_text()
    workflow_fragments = [
        "name: Tests",
        "uv sync --dev",
        "uv run ruff check",
        "uv run ruff format --check",
        "uv run mypy",
        "uv run pytest -m unit",
        'python-version: ["3.10", "3.11", "3.12"]',
        "exit 0 # skip integration tests in CI",
    ]
    workflow_missing = [
        fragment for fragment in workflow_fragments if fragment not in workflow_text
    ]
    assert not workflow_missing, f"Workflow missing required commands: {workflow_missing}"



@pytest.mark.unit
def test_json_schema_definitions_are_valid() -> None:
    schema_path = (
        TEMPLATE_ROOT
        / "src"
        / "{{cookiecutter.package_name}}"
        / "{{cookiecutter.package_name}}"
        / "schemas"
        / "workflow_output.schema.json"
    )
    assert schema_path.exists(), _relative(schema_path) + " missing"

    schema = json.loads(schema_path.read_text())
    for key in ("$schema", "title", "type", "properties"):
        assert key in schema, f"{_relative(schema_path)} missing '{key}'"
    assert schema["type"] == "object", "workflow output schema must describe an object"
    assert "summary" in schema["properties"], "workflow output schema must define 'summary'"


@pytest.mark.unit
def test_pyproject_declares_required_dependencies() -> None:
    # Workspace root declares uv management
    workspace_pyproject = (TEMPLATE_ROOT / "pyproject.toml").read_text()
    assert (
        "[tool.uv]" in workspace_pyproject and "managed = true" in workspace_pyproject
    ), "workspace pyproject.toml must declare uv management via [tool.uv]"

    # Runtime dependencies live in the core package's own pyproject.toml
    core_pyproject = (
        TEMPLATE_ROOT / "src" / "{{cookiecutter.package_name}}" / "pyproject.toml"
    ).read_text()
    required_dependency_snippets = [
        "cellsem-llm-client @ git+https://github.com/Cellular-Semantics/cellsem_llm_client.git@main",
        "deep-research-client @ git+https://github.com/monarch-initiative/deep-research-client.git@main",
        "pydantic-ai>=",
    ]
    missing = [s for s in required_dependency_snippets if s not in core_pyproject]
    assert not missing, f"core package pyproject.toml missing required dependencies: {missing}"


@pytest.mark.unit
def test_pyproject_enforces_coverage_and_excludes_experiments() -> None:
    pyproject_text = (TEMPLATE_ROOT / "pyproject.toml").read_text()
    assert "omit" in pyproject_text, \
        "pyproject.toml must have omit under [tool.coverage.run]"
    assert "experiments" in pyproject_text, \
        "pyproject.toml must reference experiments/ in exclusions"
    assert "fail_under" in pyproject_text, \
        "pyproject.toml must declare fail_under in [tool.coverage.report]"


@pytest.mark.unit
def test_agent_md_exists_and_has_at_imports() -> None:
    agent_md = TEMPLATE_ROOT / "AGENT.md"
    assert agent_md.exists(), "AGENT.md missing from template root"
    content = agent_md.read_text()
    assert "@src/" in content, \
        "AGENT.md must use @ imports to reference canonical prompts/schemas in src/"
    assert "CLAUDE.md" in content, \
        "AGENT.md must reference CLAUDE.md so users know how to switch to dev mode"


@pytest.mark.unit
def test_run_workflow_skill_references_agent_md() -> None:
    skill = TEMPLATE_ROOT / ".claude" / "commands" / "run-workflow.md"
    assert skill.exists(), ".claude/commands/run-workflow.md skill missing"
    content = skill.read_text()
    assert "AGENT.md" in content, \
        "run-workflow skill must reference AGENT.md"


@pytest.mark.unit
def test_post_gen_hook_initializes_git_with_remote() -> None:
    hook_path = REPO_ROOT / "hooks" / "post_gen_project.sh"
    assert hook_path.exists(), "Cookiecutter post_gen_project hook missing"
    contents = hook_path.read_text()
    assert "git init" in contents, "Hook must initialize git repo"
    assert "{{cookiecutter.git_remote}}" in contents, "Hook must configure git remote via template variable"


@pytest.mark.unit
def test_provenance_schema_exists_and_is_valid() -> None:
    schema_path = (
        TEMPLATE_ROOT
        / "src"
        / "{{cookiecutter.package_name}}"
        / "{{cookiecutter.package_name}}"
        / "schemas"
        / "run_provenance.schema.json"
    )
    assert schema_path.exists(), "run_provenance.schema.json missing"
    schema = json.loads(schema_path.read_text())
    for key in ("$schema", "title", "type", "properties"):
        assert key in schema, f"run_provenance.schema.json missing '{key}'"
    required_fields = {"run_id", "timestamp", "mode", "dry_run"}
    assert required_fields <= set(schema.get("required", [])), \
        f"run_provenance.schema.json must require: {required_fields}"


@pytest.mark.unit
def test_provenance_util_has_required_functions() -> None:
    util_path = (
        TEMPLATE_ROOT
        / "src"
        / "{{cookiecutter.package_name}}"
        / "{{cookiecutter.package_name}}"
        / "utils"
        / "provenance.py"
    )
    assert util_path.exists(), "utils/provenance.py missing"
    content = util_path.read_text()
    assert "capture_provenance" in content, \
        "provenance.py must define capture_provenance()"
    assert "format_dry_run_report" in content, \
        "provenance.py must define format_dry_run_report()"
