"""Use-case recipe registry for Paper Scaffold."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Recipe:
    id: str
    title: str
    summary: str
    what_for: str
    when_to_use: str
    folder_assumptions: list[str]
    commands: list[str]
    failure_modes: list[str]
    what_not_to_do: list[str]
    next_docs: list[str]


RECIPES: dict[str, Recipe] = {
    "word-to-overleaf": Recipe(
        id="word-to-overleaf",
        title="Word Draft To Overleaf",
        summary="Convert or manually migrate a Word manuscript into a clean LaTeX/GitHub/Overleaf repo.",
        what_for="Teams that draft in Word but want a clean Overleaf project without dragging along research outputs.",
        when_to_use="Use this when the manuscript text starts as .docx and still needs manual review after conversion.",
        folder_assumptions=[
            "A clean manuscript repository will live separately from the research repository.",
            "The Word draft remains an input artifact, not the canonical long-term manuscript source.",
            "Figures and tables are copied deliberately through the artifact manifest.",
        ],
        commands=[
            "paper-scaffold doctor",
            "paper-scaffold init --manuscript-repo ./paper",
            "paper-scaffold import-word --input draft.docx --output ./paper/converted.tex",
            "paper-scaffold audit-word-conversion --input ./paper/converted.tex",
            "paper-scaffold validate --manuscript-repo ./paper",
        ],
        failure_modes=[
            "Pandoc is missing or produces imperfect tables, equations, or citations.",
            "Converted figure placeholders point to local paths.",
            "Tracked changes or comments leak into converted text.",
        ],
        what_not_to_do=[
            "Do not treat conversion output as final without manual review.",
            "Do not upload the entire research repository to Overleaf.",
            "Do not keep editing both Word and LaTeX as competing canonical sources.",
        ],
        next_docs=["docs/word_to_overleaf.md", "docs/use_cases/word-to-overleaf.md"],
    ),
    "python-artifact-handoff": Recipe(
        id="python-artifact-handoff",
        title="Python Artifact Handoff",
        summary="Move selected figures and tables from analysis outputs into a manuscript repo with provenance.",
        what_for="Projects where Python scripts produce many outputs and only a small subset belongs in the paper.",
        when_to_use="Use this before copying figures or tables from an analysis output folder into the manuscript.",
        folder_assumptions=[
            "Research outputs remain in the research/code repository.",
            "The manuscript repo receives only publication-ready figures and tables.",
            "Each copied artifact has a manifest entry with source and generation context.",
        ],
        commands=[
            "paper-scaffold discover-artifacts --source ./outputs/final --manifest ./paper/metadata/artifact_manifest.yaml",
            "paper-scaffold discover-artifacts --source ./outputs/final --manifest ./paper/metadata/artifact_manifest.yaml --write --copy --manuscript-repo ./paper",
            "paper-scaffold stale-artifacts --manuscript-repo ./paper",
            "paper-scaffold validate --manuscript-repo ./paper",
        ],
        failure_modes=[
            "Raw outputs and caches are mixed with manuscript-ready figures.",
            "Figure filenames do not match LaTeX includegraphics paths.",
            "Copied artifacts become stale after a rerun.",
        ],
        what_not_to_do=[
            "Do not copy full output directories.",
            "Do not commit checkpoints, caches, or compressed result archives.",
            "Do not rely on filenames alone as provenance.",
        ],
        next_docs=["docs/python_outputs_to_overleaf.md", "docs/artifact_manifest.md", "docs/use_cases/python-artifact-handoff.md"],
    ),
    "existing-latex-cleanup": Recipe(
        id="existing-latex-cleanup",
        title="Existing LaTeX Cleanup",
        summary="Audit and normalize an existing LaTeX project before GitHub/Overleaf sync.",
        what_for="Manuscripts that already compile locally but have build artifacts, stale figures, or local paths mixed in.",
        when_to_use="Use this before pushing an inherited or long-lived LaTeX folder to GitHub.",
        folder_assumptions=[
            "The existing LaTeX folder is already manuscript-focused.",
            "Raw outputs and research code should be moved out before sync.",
            "Build artifacts are regenerated, not versioned.",
        ],
        commands=[
            "paper-scaffold audit-project --path ./old_latex_project --write-report project_audit.md",
            "paper-scaffold overleaf-check --manuscript-repo ./paper",
            "paper-scaffold unused-artifacts --manuscript-repo ./paper",
            "paper-scaffold release-check --manuscript-repo ./paper --write-report ./paper/release_check.md",
        ],
        failure_modes=[
            "LaTeX build artifacts are staged for commit.",
            "Figures are present but no longer referenced.",
            "Local absolute paths work on one machine but fail on Overleaf.",
        ],
        what_not_to_do=[
            "Do not commit .aux, .log, .bbl, .blg, or synctex files.",
            "Do not preserve repeated final/final2 exports as history.",
            "Do not rename large sets of files without checking TeX references.",
        ],
        next_docs=["docs/existing_latex_project.md", "docs/github_overleaf_sync.md", "docs/use_cases/existing-latex-cleanup.md"],
    ),
    "overleaf-zip-rehab": Recipe(
        id="overleaf-zip-rehab",
        title="Overleaf ZIP Rehab",
        summary="Turn a downloaded Overleaf ZIP into a clean GitHub-backed manuscript repo.",
        what_for="Teams that have been passing Overleaf ZIP exports around instead of using Git.",
        when_to_use="Use this when a ZIP export contains manuscript sources plus generated build artifacts.",
        folder_assumptions=[
            "The ZIP has been unpacked into a scratch folder.",
            "The clean manuscript repo is created separately.",
            "Only source files and intended figures/tables are copied forward.",
        ],
        commands=[
            "paper-scaffold audit-project --path ./overleaf_export --write-report overleaf_export_audit.md",
            "paper-scaffold init --manuscript-repo ./paper",
            "paper-scaffold validate --manuscript-repo ./paper",
            "paper-scaffold overleaf-instructions --manuscript-repo ./paper",
        ],
        failure_modes=[
            "Build artifacts obscure which files are real source.",
            "The ZIP contains duplicate final versions.",
            "Bibliography files or figures are missing after manual cleanup.",
        ],
        what_not_to_do=[
            "Do not commit the ZIP file itself to the manuscript repo.",
            "Do not connect Overleaf to a scratch extraction folder full of build artifacts.",
            "Do not use repeated ZIP filenames as version control.",
        ],
        next_docs=["docs/github_overleaf_sync.md", "docs/use_cases/overleaf-zip-rehab.md"],
    ),
    "paper-archaeology": Recipe(
        id="paper-archaeology",
        title="Paper Archaeology",
        summary="Inventory a messy project folder and identify manuscript sources, outputs, caches, and Overleaf exports.",
        what_for="Starting points where it is unclear which files belong in a manuscript repo.",
        when_to_use="Use this before creating a clean repo from an old project or inherited folder.",
        folder_assumptions=[
            "The project folder may contain code, notes, generated outputs, manuscript drafts, and exports.",
            "The audit is read-only and does not move or delete files.",
            "A human decides which candidates should be copied into a clean manuscript repo.",
        ],
        commands=[
            "paper-scaffold audit-project --path ./messy_project --write-report project_audit.md",
            "paper-scaffold init --manuscript-repo ./paper",
            "paper-scaffold discover-artifacts --source ./messy_project/outputs --manifest ./paper/metadata/artifact_manifest.yaml",
            "paper-scaffold validate --manuscript-repo ./paper",
        ],
        failure_modes=[
            "Multiple final-looking files make the latest source ambiguous.",
            "Raw/generated outputs sit next to publication figures.",
            "Overleaf exports include build artifacts that should not be copied forward.",
        ],
        what_not_to_do=[
            "Do not bulk-copy the whole messy project into a manuscript repo.",
            "Do not delete files during the audit pass.",
            "Do not assume final_FINAL is authoritative without checking content and dates.",
        ],
        next_docs=["docs/use_cases/paper-archaeology.md", "examples/messy_project_archaeology/README.md"],
    ),
    "reviewer-response-binder": Recipe(
        id="reviewer-response-binder",
        title="Reviewer Response Binder",
        summary="Track revision artifacts and response evidence without mixing them into the main manuscript source.",
        what_for="Revision rounds where new analyses, figures, or tables support reviewer responses.",
        when_to_use="Use this when response artifacts need a lightweight manifest and checklist.",
        folder_assumptions=[
            "The manuscript repo is already separate from the research repo.",
            "Response artifacts are small, publication-facing evidence files.",
            "A checklist records which reviewer point each artifact supports.",
        ],
        commands=[
            "paper-scaffold reviewer-binder --manuscript-repo ./paper --round 1 --output ./reviewer_response_round_1",
            "paper-scaffold validate --manuscript-repo ./paper",
            "paper-scaffold stale-artifacts --manuscript-repo ./paper",
            "paper-scaffold compare-lock --manuscript-repo ./paper --lock metadata/artifact_lock.json --write-report ./paper/lock_comparison.md",
            "paper-scaffold release-check --manuscript-repo ./paper --write-report ./paper/release_check.md",
        ],
        failure_modes=[
            "Reviewer-only scratch outputs become permanent manuscript files.",
            "Response figures drift from the final submitted version.",
            "The response checklist and manuscript artifact manifest disagree.",
        ],
        what_not_to_do=[
            "Do not commit large rerun folders just to document a response.",
            "Do not put confidential review text in a public repository.",
            "Do not leave response-only artifacts referenced nowhere.",
        ],
        next_docs=["docs/reviewer_response_binder.md", "docs/use_cases/reviewer-response-binder.md", "examples/reviewer_response_round/README.md"],
    ),
    "undergraduate-artifact-harvest": Recipe(
        id="undergraduate-artifact-harvest",
        title="Undergraduate Artifact Harvest",
        summary="Give junior contributors a safe, reviewable workflow for proposing paper figures and tables.",
        what_for="Mentored projects where contributors should not copy whole output trees into a manuscript repo.",
        when_to_use="Use this when a contributor has generated candidate figures/tables that need review.",
        folder_assumptions=[
            "Contributors work in a research or scratch folder.",
            "The manuscript maintainer reviews suggested artifact candidates before copying.",
            "Large raw outputs stay out of the manuscript repo.",
        ],
        commands=[
            "paper-scaffold discover-artifacts --source ./student_outputs --manifest ./paper/metadata/artifact_manifest.yaml",
            "paper-scaffold audit-project --path ./student_outputs --write-report student_outputs_audit.md",
            "paper-scaffold validate --manuscript-repo ./paper",
        ],
        failure_modes=[
            "Student output folders contain raw data, notebooks, and publication figures together.",
            "Filenames are descriptive to the student but not manuscript-ready.",
            "Generated tables need layout review before inclusion.",
        ],
        what_not_to_do=[
            "Do not give write access to the canonical manuscript branch as the first review step.",
            "Do not ask contributors to guess which raw files are safe to publish.",
            "Do not commit entire experiment folders.",
        ],
        next_docs=["docs/use_cases/undergraduate-artifact-harvest.md", "docs/artifact_manifest.md"],
    ),
    "pre-submission-flight-check": Recipe(
        id="pre-submission-flight-check",
        title="Pre-Submission Flight Check",
        summary="Run focused checks before syncing, sharing, or submitting a manuscript repository.",
        what_for="Final review before GitHub/Overleaf sync, collaborator handoff, or journal submission.",
        when_to_use="Use this after manuscript files are in place and before a release-like commit.",
        folder_assumptions=[
            "The manuscript repo is already created.",
            "Figures, tables, bibliography, and supplement are in their expected locations.",
            "Warnings are reviewed explicitly rather than ignored.",
        ],
        commands=[
            "paper-scaffold release-check --manuscript-repo ./paper --write-report ./paper/release_check.md",
            "paper-scaffold validate --manuscript-repo ./paper --write-json ./paper/validation_report.json",
            "paper-scaffold overleaf-check --manuscript-repo ./paper",
            "paper-scaffold freeze-artifacts --manuscript-repo ./paper --write-lock ./paper/metadata/artifact_lock.json",
            "paper-scaffold compare-lock --manuscript-repo ./paper --lock metadata/artifact_lock.json --write-report ./paper/lock_comparison.md",
            "paper-scaffold package-submission --manuscript-repo ./paper --output ./submission_package",
        ],
        failure_modes=[
            "A last-minute figure path change breaks Overleaf.",
            "A raw output archive slips into the repo.",
            "Bibliography, labels, or stale artifacts drift during revision.",
        ],
        what_not_to_do=[
            "Do not submit with unresolved errors.",
            "Do not assume a clean local compile means the repository is clean.",
            "Do not skip privacy checks for public repositories.",
        ],
        next_docs=[
            "docs/validation.md",
            "docs/error_codes.md",
            "docs/artifact_locks.md",
            "docs/submission_packaging.md",
            "docs/use_cases/pre-submission-flight-check.md",
        ],
    ),
    "multi-paper-project-split": Recipe(
        id="multi-paper-project-split",
        title="Multi-Paper Project Split",
        summary="Separate multiple manuscript repos from one shared research project while preserving artifact provenance.",
        what_for="Large projects that produce outputs for more than one manuscript.",
        when_to_use="Use this when Paper A and Paper B share code or data but need separate manuscript histories.",
        folder_assumptions=[
            "One research repo may feed multiple manuscript repos.",
            "Each manuscript repo has its own artifact manifest and terminology map.",
            "Shared outputs are copied selectively into the relevant manuscript repo.",
        ],
        commands=[
            "paper-scaffold init --manuscript-repo ./paper_a",
            "paper-scaffold init --manuscript-repo ./paper_b",
            "paper-scaffold discover-artifacts --source ./outputs/paper_a --manifest ./paper_a/metadata/artifact_manifest.yaml",
            "paper-scaffold discover-artifacts --source ./outputs/paper_b --manifest ./paper_b/metadata/artifact_manifest.yaml",
        ],
        failure_modes=[
            "Manuscript-specific figures are copied into the wrong repo.",
            "Shared terminology maps drift between papers.",
            "One repo accumulates artifacts for both papers.",
        ],
        what_not_to_do=[
            "Do not make one manuscript repo contain every paper's artifacts.",
            "Do not fork the research repo as the manuscript repo.",
            "Do not reuse artifact IDs ambiguously across papers.",
        ],
        next_docs=["docs/use_cases/multi-paper-project-split.md", "examples/multi_paper_split/README.md"],
    ),
}


def list_recipes() -> str:
    lines = ["Available recipes:"]
    for recipe in RECIPES.values():
        lines.append(f"- {recipe.id}: {recipe.summary}")
    lines.append("")
    lines.append("Use `paper-scaffold recipes show <recipe-id>` for the full workflow.")
    return "\n".join(lines)


def format_recipe(recipe: Recipe) -> str:
    lines = [
        f"{recipe.id}: {recipe.title}",
        "",
        "What for:",
        f"- {recipe.what_for}",
        "",
        "When to use:",
        f"- {recipe.when_to_use}",
        "",
        "Folder assumptions:",
        *[f"- {item}" for item in recipe.folder_assumptions],
        "",
        "Recommended commands:",
        *[f"- `{command}`" for command in recipe.commands],
        "",
        "Common failure modes:",
        *[f"- {item}" for item in recipe.failure_modes],
        "",
        "What not to do:",
        *[f"- {item}" for item in recipe.what_not_to_do],
        "",
        "Next docs:",
        *[f"- {item}" for item in recipe.next_docs],
    ]
    return "\n".join(lines)


def get_recipe(recipe_id: str) -> Recipe:
    normalized = recipe_id.strip().lower()
    if normalized not in RECIPES:
        raise KeyError(normalized)
    return RECIPES[normalized]
