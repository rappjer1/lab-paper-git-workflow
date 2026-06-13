New lab workflow repo: <GITHUB_REPO_URL>

Use this when you have research outputs in Python and a manuscript draft in Word/Markdown/LaTeX, and you need a clean manuscript GitHub repo that Overleaf can import.

What it does today:
- Gives a clear workflow for Word/docx -> LaTeX/Overleaf.
- Helps move Python-generated figures/tables into a manuscript repo without copying raw outputs.
- Tracks figure/table provenance in `metadata/artifact_manifest.yaml`.
- Checks your setup with `paper-scaffold doctor`.
- Validates manuscript repos before GitHub/Overleaf sync.

What it does not do:
- It does not write the science for you.
- It does not replace version control.
- It does not require LaTeX, Pandoc, or GitHub CLI.
- It does not create GitHub or Overleaf projects automatically.
- It does not upload anything to Overleaf.

5-minute start:

```bash
python scripts/paper-scaffold.py doctor
python scripts/paper-scaffold.py init
python scripts/paper-scaffold.py discover-artifacts --source <final-output-folder> --manifest metadata/artifact_manifest.yaml
python scripts/paper-scaffold.py validate --manuscript-repo <manuscript-repo>
```

Start with:
- `README.md`
- `QUICKSTART.md`
- `docs/word_to_overleaf.md`
- `docs/python_outputs_to_overleaf.md`
- `docs/overleaf_from_github.md`

Important: do not commit raw data, model outputs, `.npz`, `.pt`, `.pkl`, `.nc`, `full_eval`, `prediction_cache`, or external API caches to manuscript repos.

Report issues by opening a GitHub issue or posting in Slack with the command you ran, your OS/shell, and the error text.
