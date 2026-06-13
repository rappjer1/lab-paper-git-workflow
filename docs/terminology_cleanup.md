# Terminology Cleanup

Scientific labels belong in the paper. Implementation labels belong in provenance.

Manuscripts should not expose raw cache names, model run IDs, class names, or short labels that only make sense inside code.

Use:

```text
metadata/terminology_map.yaml
```

to map implementation labels to publication-facing labels.

## Example

```yaml
terms:
  baseline_run_slug:
    publication_label: baseline model
    allowed_contexts:
      - supplement provenance table
      - artifact manifest
    banned_in:
      - abstract
      - introduction
      - main results
  experiment_model_slug:
    publication_label: probabilistic model
    banned_in:
      - abstract
      - main results
  package_name_used_in_code:
    publication_label: modeling workflow
    note: Use package names only for software provenance.
```

## How To Use It

1. Add implementation terms under `terms`.
2. Set `publication_label`.
3. Add `banned_in` for terms that should not appear in main manuscript text.
4. Add `allowed_contexts` when a code label is acceptable in supplement provenance or metadata.
5. Run the terminology check.

```bash
paper-scaffold terminology-check --manuscript-repo ./paper
```

## Validation Rule

`paper-scaffold validate` searches `.tex`, `.bib`, and `.md` files for terms with `banned_in` entries. When it finds one, it reports the file, line number, banned term, and suggested replacement.

The tool does not infer scientific terminology automatically. The map must be curated by the project team.

## Practical Rule

If a reader needs to understand code history to understand the label, it probably does not belong in the main text.

Use implementation labels in:

- Artifact manifests.
- Supplement provenance tables.
- Reproducibility notes.
- Code comments inside the research repo.

Use publication labels in:

- Title.
- Abstract.
- Introduction.
- Main methods.
- Main results.
- Discussion.
