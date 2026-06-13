# Terminology Cleanup

Scientific labels belong in the paper. Code labels belong in provenance.

Manuscripts should not expose raw cache names, model run IDs, implementation class names, or short labels that only make sense inside the codebase.

Use:

```text
metadata/terminology_map.yaml
```

to convert implementation labels into publication labels.

## Example

```yaml
terms:
  standard_cudalstm_ensemble:
    publication_label: deterministic LSTM ensemble
    allowed_contexts:
      - supplement provenance table
      - code manifest
    banned_in:
      - abstract
      - introduction
      - main results
  classicallstm_ensemble:
    publication_label: quantile LSTM ensemble
  NeuralHydrology:
    publication_label: LSTM rainfall-runoff workflow
    note: Use NeuralHydrology only for software provenance, not as the scientific model label.
```

## How To Use It

1. Add internal terms under `terms`.
2. Set `publication_label`.
3. Add `banned_in` for terms that should not appear in main manuscript text.
4. Add `allowed_contexts` when a code label is acceptable in supplement provenance or metadata.
5. Run the terminology check.

```bash
paper-scaffold terminology-check --manuscript-repo <manuscript-repo>
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
