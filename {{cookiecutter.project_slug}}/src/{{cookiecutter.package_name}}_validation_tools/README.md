# {{cookiecutter.project_name}} - Validation Tools

**Status**: OPTIONAL

Validation and analysis tools for comparing runs, computing metrics, and visualizing results.

## Delete This Package If

Your Ring 0 MVP doesn't need:
- Workflow output comparison
- Quality metrics (precision, recall, etc.)
- Visualizations and analysis

See `SCAFFOLD_GUIDE.md` for guidance.

## Installation

```bash
pip install {{cookiecutter.package_name}}-validation-tools
```

## Structure

- **comparisons/** - Compare workflow outputs across runs
- **metrics/** - Quality metrics (precision, recall, F1, etc.)
- **visualizations/** - Plots, heatmaps, ROC curves

## Usage

This package imports schemas and models from the core package:

```python
from {{cookiecutter.package_name}}.schemas import load_schema
from {{cookiecutter.package_name}}_validation_tools.metrics import calculate_f1
from {{cookiecutter.package_name}}_validation_tools.visualizations import plot_heatmap
```

## Development

This package is part of a UV workspace. See repository root for development instructions.
