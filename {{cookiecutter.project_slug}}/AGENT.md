# {{cookiecutter.project_name}}: Workflow Run Mode

> **You are running the workflow as an agent, not developing the codebase.**
> For development instructions, see `CLAUDE.md`.
> To return to dev mode: start a new Claude session (AGENT.md will not be loaded).

---

## Your Role

You are the **{{cookiecutter.project_name}}** workflow agent. You:

- Accept input from the user
- Execute workflow steps using the prompts and schemas below
- Validate all outputs against the defined schemas before returning them
- Save intermediate results to `outputs/{run_name}/{timestamp}/`

Do **not** write or modify source code unless the user explicitly asks.
Do **not** run the test suite. Do **not** commit changes.

---

## Prompts

These are the canonical prompts — the same YAML files the programmatic Python
implementation reads at runtime. Treat them as your instructions for each step.

@src/{{cookiecutter.package_name}}/{{cookiecutter.package_name}}/agents/example_agent.prompt.yaml

<!-- Add additional prompts as you build out the workflow:
@src/{{cookiecutter.package_name}}/{{cookiecutter.package_name}}/services/your_service.prompt.yaml
-->

---

## Output Schemas

All outputs must conform to these schemas. Validate before returning to the user.

@src/{{cookiecutter.package_name}}/{{cookiecutter.package_name}}/schemas/workflow_output.schema.json

<!-- Add additional schemas as needed:
@src/{{cookiecutter.package_name}}/{{cookiecutter.package_name}}/schemas/your_schema.schema.json
-->

---

## Workflow Steps

<!-- [CUSTOMIZE THIS SECTION: describe the steps for your specific workflow] -->

1. **Input** — accept user query or data
2. **Process** — apply the prompts above to the input
3. **Validate** — check output conforms to the schema above
4. **Save** — write to `outputs/{run_name}/{timestamp}/step_N.json`

---

## Output Directory Convention

`provenance.json` is **always the first file written**, even in dry-runs.

```text
outputs/
└── {run_name}/
    └── {YYYY-MM-DD_HH-MM-SS}/
        ├── provenance.json       ← written first, before any LLM calls
        ├── step_1_output.json
        └── summary.json
```

---

## Dry-Run Mode

If the user requests a dry run:

1. **Capture provenance first** (before any LLM calls):
   - Run `git describe --tags --always --dirty` and record the output
   - For each prompt loaded via `@`, record its path and compute `sha256(content)`
   - Note active model/preset settings and input data

2. **Print the provenance report** in this format:

   ```text
   === DRY RUN ===

   PROVENANCE
     Git:     v0.3.1-2-gabcdef (or 'unknown' if not in a tagged repo)
     Package: {{cookiecutter.package_name}}==<version>
     Time:    <ISO 8601 UTC timestamp>

   PROMPTS
     <label>  <path>
              sha256:<first 16 chars>...
              --- content ---
              <full resolved prompt content>

   SCHEMAS
     <label>  <path>
              sha256:<first 16 chars>...

   SETTINGS
     preset: <preset name>
     model:  <model name>
     temperature: <value>

   NO CHANGES MADE. Run without --dry-run to execute.
   ```

3. Write `provenance.json` to `outputs/{run_name}/{timestamp}/provenance.json`
   conforming to:

   @src/{{cookiecutter.package_name}}/{{cookiecutter.package_name}}/schemas/run_provenance.schema.json

4. Do **not** make any LLM API calls

---

## Platform Propagation (Future)

This file is the canonical run-mode instruction source. When the
`cellsem-platform-tools` library is available, run:

```bash
uv run python -c "from cellsem_platform_tools import generate; generate('AGENT.md')"
```

This generates `.github/copilot-instructions.md`, `.cursor/rules`, and `AGENTS.md`
from this file without duplicating content.
