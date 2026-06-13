"""Create and update clean manuscript repository scaffolds."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import shutil

from .config import DEFAULT_CONFIG, write_yaml


@dataclass(frozen=True)
class InitOptions:
    research_repo: str
    manuscript_repo: str
    title: str
    slug: str
    has_supplement: bool = True
    use_template: bool = True
    github_repo: str = ""
    overleaf_url: str = ""
    branch_name: str = "main"
    figure_dir: str = "figures"
    table_dir: str = "tables"
    references_file: str = ""


def package_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_template_dir() -> Path:
    return package_root() / "templates" / "manuscript_repo"


def project_config_from_options(options: InitOptions) -> dict[str, Any]:
    return {
        "project": {
            "title": options.title,
            "slug": options.slug,
            "research_repo": options.research_repo,
            "manuscript_repo": options.manuscript_repo,
            "github_repo": options.github_repo,
            "overleaf_url": options.overleaf_url,
            "main_tex": "main.tex",
            "supplement_tex": "supplement/supplement.tex",
            "has_supplement": options.has_supplement,
            "preferred_branch": options.branch_name,
            "figure_dir": options.figure_dir,
            "table_dir": options.table_dir,
        },
        "validation": DEFAULT_CONFIG["validation"].copy(),
    }


def planned_init_actions(options: InitOptions) -> list[str]:
    root = Path(options.manuscript_repo)
    actions = [
        f"create manuscript repo folder: {root}",
        "create sections/, figures/, tables/, metadata/",
        "create supplement folders" if options.has_supplement else "skip supplement folders",
        "copy template LaTeX files" if options.use_template else "leave existing LaTeX files in place",
        "write metadata/manuscript_config.yaml",
        "write metadata/artifact_manifest.yaml",
        "write metadata/terminology_map.yaml",
        "write manuscript README.md",
    ]
    if options.references_file:
        actions.append(f"copy references file: {options.references_file}")
    return actions


def _copy_template_tree(destination: Path, include_supplement: bool, overwrite: bool = False) -> None:
    template = default_template_dir()
    for source in template.rglob("*"):
        rel = source.relative_to(template)
        if not include_supplement and rel.parts and rel.parts[0] == "supplement":
            continue
        target = destination / rel
        if source.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        if target.exists() and not overwrite:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def _write_project_readme(root: Path, options: InitOptions) -> None:
    title = options.title or options.slug or "Manuscript"
    content = f"""# {title}

This repository is the clean manuscript source for `{options.slug or 'this project'}`.

The research/code repository remains the source of computations:

```text
{options.research_repo or '<research-repo>'}
```

Do not commit raw data, model outputs, caches, large evaluation folders, or ZIP snapshots here. Copy only publication figures, publication tables, manuscript source, references, and supplement source.

## Update workflow

1. Regenerate results in the research repo.
2. Copy selected figures/tables into this repo with `paper-scaffold copy-artifacts` or by hand.
3. Update `metadata/artifact_manifest.yaml` with provenance.
4. Run `paper-scaffold validate`.
5. Commit and push to GitHub.
6. Sync Overleaf from GitHub.

## Useful commands

```bash
paper-scaffold validate
paper-scaffold terminology-check
paper-scaffold git-check
```
"""
    (root / "README.md").write_text(content, encoding="utf-8")


def init_manuscript(options: InitOptions, dry_run: bool = False, overwrite: bool = False) -> list[str]:
    actions = planned_init_actions(options)
    if dry_run:
        return actions

    root = Path(options.manuscript_repo)
    root.mkdir(parents=True, exist_ok=True)
    for relative in [
        "sections",
        "figures",
        "tables",
        "metadata",
        "supplement/sections",
        "supplement/tables",
        "supplement/figures",
    ]:
        if relative.startswith("supplement") and not options.has_supplement:
            continue
        (root / relative).mkdir(parents=True, exist_ok=True)

    if options.use_template:
        _copy_template_tree(root, include_supplement=options.has_supplement, overwrite=overwrite)

    config = project_config_from_options(options)
    write_yaml(root / "metadata" / "manuscript_config.yaml", config)
    write_yaml(root / "metadata" / "artifact_manifest.yaml", {"artifacts": []})
    write_yaml(root / "metadata" / "terminology_map.yaml", {"terms": {}})
    _write_project_readme(root, options)

    if options.references_file:
        source = Path(options.references_file)
        if source.exists() and source.is_file():
            shutil.copy2(source, root / "references.bib")

    return actions
