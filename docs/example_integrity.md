# Example Integrity

Paper Scaffold examples are synthetic. They are meant to test workflow shape and documentation, not to make scientific claims.

## What Is Checked

Run:

```bash
python scripts/dev/check_example_integrity.py
```

The checker scans `examples/` and `templates/` for common manuscript artifact and text files:

- PDF, PNG, JPG, and JPEG files;
- CSV tables;
- TeX, BibTeX, YAML, and Markdown files.

It verifies:

- PDF files begin with `%PDF`;
- PNG and JPEG files have the expected magic bytes;
- CSV and text files are UTF-8 text;
- CSV files contain a delimiter or newline;
- example files are small;
- example text files do not contain local/private path patterns.

## Why Fake `.pdf` Text Placeholders Are Avoided

A file named `.pdf` should be a valid PDF, even if it is tiny and synthetic. Text placeholders with a `.pdf` suffix make examples misleading and can hide packaging or validation mistakes.

If a placeholder is intentionally not a real artifact, name it with a `.placeholder` suffix and document it in the scenario README.

## Regenerating Example Artifacts

Run:

```bash
python scripts/dev/generate_example_artifacts.py
```

The generator writes deterministic tiny synthetic PDFs and PNGs used by the dogfood and public examples. It uses only the Python standard library and does not include real research data.

## Adding A New Example Safely

- Keep files small and synthetic.
- Use valid file formats for publication-artifact extensions.
- Avoid private paths, credentials, project-specific data, and real reviewer text.
- Add a `README.md` with the goal, commands, expected result, and manual review notes.
- Add `expected_commands.md` and `expected_outputs.md` for dogfood scenarios.
- Run `check_example_integrity.py`, `check_docs_examples.py`, and `run_dogfood.py` before release.
