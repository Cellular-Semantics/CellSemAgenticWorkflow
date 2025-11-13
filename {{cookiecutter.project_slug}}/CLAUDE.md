# Development Rules

## Test-Driven Development (MANDATORY)
1. Write unit and integration tests FIRST
2. Tests must fail initially (red)
3. Commit tests before implementation
4. Write minimal code to pass tests (green)
5. Refactor while keep**ing tests green, commit

## TDD Workflow Commands (using uv)
```bash
# Install dependencies and sync environment
uv sync --dev            # Install all dependencies including dev tools

# Run tests
uv run pytest                    # All tests
uv run pytest -m unit           # Unit tests only
uv run pytest -m integration    # Integration tests only
uv run pytest --cov             # With coverage

# Code quality (run before committing!)
uv run ruff format src/ tests/        # Format code
uv run ruff check --fix src/ tests/   # Lint and auto-fix
uv run mypy src/                      # Type checking

# Documentation (run before committing!)
python scripts/check-docs.py         # Build docs and check for errors
cd docs && uv run sphinx-build . _build/html -W  # Alternative direct command

# Pre-commit hooks (recommended)
uv run pre-commit install       # Install git hooks
uv run pre-commit run --all-files   # Run on all files

# Add new dependencies
uv add requests              # Add runtime dependency
uv add --dev pytest         # Add development dependency

# Environment management
uv sync                      # Sync dependencies (production only)
uv sync --dev               # Sync with development dependencies
```

## Code Quality Strategy
- **Pre-commit hooks**: Auto-run ruff to lint AND format /mypy to type check before each commit
- **Local checks**: Always run `ruff format` and `ruff check --fix` before pushing
- **GitHub Actions**: Runs same checks on PRs - should never fail if run locally
- **IDE integration**: Configure your editor to run formatters on save

## Environment Configuration
- **ALWAYS use dotenv**: Use `from dotenv import load_dotenv; load_dotenv()` for environment variables, never use `os.getenv()` directly
- **Never hardcode secrets**: All API keys, emails, and sensitive data must come from .env files
- **Environment precedence**: Constructor params > environment variables > sensible defaults

## FORBIDDEN Patterns
- Mock data generation for integration tests
- Simulated API responses
- Dummy database connections
- Placeholder implementations
- Integration tests that pass without real integration
- Skipping failing tests with pytest.mark.skip

## Required Test Structure
- Unit tests: tests/unit/ (fast, isolated, no external deps)
- Integration tests: tests/integration/ (environment-dependent behavior)
- Fixtures with real connection setup/teardown
- Coverage minimum: 80%
- All tests must use pytest markers (@pytest.mark.unit or @pytest.mark.integration)

## Integration Testing Strategy
**Local Development (Real APIs Only):**
- Integration tests REQUIRE real API keys (e.g. OPENAI_API_KEY, ANTHROPIC_API_KEY)
- Tests FAIL HARD if no API keys are present
- Forces developers to test against real APIs before pushing
- Pre-commit hooks enforce integration test passage
- Command: `uv run pytest -m integration`

**CI/GitHub Actions (Unit Tests Only):**
- NO integration tests run in CI to avoid mock complexity
- Only unit tests run (fast, no external dependencies)
- Command: `uv run pytest -m unit`

**Rationale:**
- Local: Mandatory real API testing ensures integration quality
- CI: Simple, fast, reliable unit test validation
- Avoids complex mock maintenance and false confidence
- Forces developers to have working API access

## Documentation Requirements
- Google-style docstrings for all public functions/classes
- **RST syntax in docstrings**: Use `.. code-block:: python` instead of markdown ```python
- Auto-generated API docs via Sphinx + AutoAPI
- Manual docs in docs/ using MyST markdown
- Build docs: `python scripts/check-docs.py` (recommended) or `sphinx-build docs docs/_build`
- **Always run docs check before committing** to catch RST syntax errors

## MVP Definition
For each feature:
1. Clear, testable goal
2. Integration test demonstrating real API connection
3. Error handling for actual failure modes (network, malformed data, rate limits)
4. No feature complete until real integration test passes

## Planning

Each proposed plan of work should include an MVP and a critique section detailing potential issues/risks with the approach.
