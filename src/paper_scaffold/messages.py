"""Structured diagnostic messages for Paper Scaffold."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DiagnosticMessage:
    code: str
    severity: str
    title: str
    explanation: str
    suggested_fix: str
    example_command: str = ""
    docs_path: str = ""


@dataclass(frozen=True)
class DiagnosticFinding:
    code: str
    detail: str = ""
    path: str = ""
    line: int | None = None

    @property
    def message(self) -> DiagnosticMessage:
        return get_message(self.code)


MESSAGES: dict[str, DiagnosticMessage] = {
    "E001": DiagnosticMessage(
        "E001",
        "ERROR",
        "main.tex missing",
        "The manuscript repository does not contain the configured main TeX file.",
        "Create main.tex or set project.main_tex in metadata/manuscript_config.yaml.",
        "paper-scaffold init --manuscript-repo ./paper",
        "docs/validation.md",
    ),
    "E002": DiagnosticMessage(
        "E002",
        "ERROR",
        "references.bib missing",
        "The manuscript repository does not contain references.bib.",
        "Add references.bib or update the manuscript to use the correct bibliography file.",
        "",
        "docs/validation.md",
    ),
    "E003": DiagnosticMessage(
        "E003",
        "ERROR",
        "Missing figure path",
        "A LaTeX includegraphics command points to a file that does not exist in the manuscript repository.",
        "Copy the figure into the manuscript repo or fix the relative path.",
        "paper-scaffold check-figures --manuscript-repo ./paper",
        "docs/troubleshooting.md",
    ),
    "E004": DiagnosticMessage(
        "E004",
        "ERROR",
        "Manifest artifact missing",
        "An artifact manifest entry points to a manuscript file that is missing.",
        "Copy the artifact into the manuscript repo or update metadata/artifact_manifest.yaml.",
        "paper-scaffold copy-artifacts --manuscript-repo ./paper",
        "docs/artifact_manifest.md",
    ),
    "E005": DiagnosticMessage(
        "E005",
        "ERROR",
        "Forbidden raw output found",
        "The manuscript repository contains a raw/model/cache output pattern that should stay in the research repo.",
        "Remove the file from the manuscript repo and keep it in the research/code repo or data archive.",
        "paper-scaffold validate --manuscript-repo ./paper",
        "docs/validation.md",
    ),
    "E006": DiagnosticMessage(
        "E006",
        "ERROR",
        "Banned implementation label found",
        "A term banned by the terminology map appears in manuscript text.",
        "Replace it with the publication-facing label or adjust the terminology map.",
        "paper-scaffold terminology-check --manuscript-repo ./paper",
        "docs/terminology_cleanup.md",
    ),
    "E007": DiagnosticMessage(
        "E007",
        "ERROR",
        "Git remote origin missing",
        "The repository does not have a Git remote named origin.",
        "Add the GitHub manuscript repository as origin before GitHub/Overleaf sync.",
        "git remote add origin https://github.com/<owner>/<paper-repo>.git",
        "docs/github_overleaf_sync.md",
    ),
    "E008": DiagnosticMessage(
        "E008",
        "ERROR",
        "Absolute local path found",
        "A manuscript source file contains an absolute local path that will not work for collaborators or Overleaf.",
        "Replace it with a relative path inside the manuscript repository.",
        "",
        "docs/troubleshooting.md",
    ),
    "E009": DiagnosticMessage(
        "E009",
        "ERROR",
        "Supplement configured but missing",
        "The config says a supplement exists, but the supplement TeX file is missing.",
        "Create supplement/supplement.tex or set has_supplement to false.",
        "",
        "docs/validation.md",
    ),
    "E010": DiagnosticMessage(
        "E010",
        "ERROR",
        "Duplicate LaTeX label",
        "The same LaTeX label is defined more than once.",
        "Rename duplicate labels so every label key is unique.",
        "paper-scaffold check-labels --manuscript-repo ./paper",
        "docs/error_codes.md",
    ),
    "E011": DiagnosticMessage(
        "E011",
        "ERROR",
        "Missing LaTeX label target",
        "A reference points to a label that is not defined.",
        "Add the missing label or fix the reference key.",
        "paper-scaffold check-labels --manuscript-repo ./paper",
        "docs/error_codes.md",
    ),
    "E012": DiagnosticMessage(
        "E012",
        "ERROR",
        "Citation key missing from bibliography",
        "A citation key used in TeX is not present in references.bib.",
        "Add the BibTeX entry or correct the citation key.",
        "paper-scaffold check-citations --manuscript-repo ./paper",
        "docs/error_codes.md",
    ),
    "E013": DiagnosticMessage(
        "E013",
        "ERROR",
        "File larger than configured maximum",
        "A file exceeds the configured size threshold for manuscript repositories.",
        "Remove large raw outputs or explicitly review whether the file belongs in the manuscript repo.",
        "",
        "docs/validation.md",
    ),
    "E014": DiagnosticMessage(
        "E014",
        "ERROR",
        "Forbidden directory found",
        "The manuscript repository contains a directory pattern reserved for raw/model/cache outputs.",
        "Move that directory back to the research repo or archive.",
        "",
        "docs/validation.md",
    ),
    "E015": DiagnosticMessage(
        "E015",
        "ERROR",
        "Artifact source missing",
        "copy-artifacts cannot find a source path listed in the artifact manifest.",
        "Regenerate the source artifact, correct source_repo/source_path, or remove the stale entry.",
        "paper-scaffold copy-artifacts --manuscript-repo ./paper",
        "docs/artifact_manifest.md",
    ),
    "W001": DiagnosticMessage("W001", "WARNING", "Pandoc missing", "Pandoc is not installed or not on PATH.", "Install Pandoc only if you need Word/Markdown conversion.", "paper-scaffold import-word --input draft.docx --output converted.tex", "docs/word_to_overleaf.md"),
    "W002": DiagnosticMessage("W002", "WARNING", "LaTeX compiler missing", "latexmk or pdflatex is not installed or not on PATH.", "Install LaTeX only if you want local compilation; Overleaf can compile remotely.", "", "docs/faq.md"),
    "W003": DiagnosticMessage("W003", "WARNING", "GitHub CLI missing", "gh is not installed or not on PATH.", "Use the GitHub website or install GitHub CLI if desired.", "", "docs/github_overleaf_sync.md"),
    "W004": DiagnosticMessage("W004", "WARNING", "Working tree has uncommitted changes", "Git reports modified, staged, or untracked files.", "Review git status and commit intentionally before syncing.", "git status --short", "docs/github_overleaf_sync.md"),
    "W005": DiagnosticMessage("W005", "WARNING", "Figure present but not referenced", "A figure file exists but does not appear in includegraphics references.", "Remove stale figures or reference them from the manuscript.", "paper-scaffold check-figures --manuscript-repo ./paper", "docs/error_codes.md"),
    "W006": DiagnosticMessage("W006", "WARNING", "Raster figure concern", "A PNG/JPG figure may need review for resolution or vector alternatives.", "Prefer PDF for vector plots and high-resolution PNG/JPG for raster images.", "", "docs/python_outputs_to_overleaf.md"),
    "W007": DiagnosticMessage("W007", "WARNING", "Table may be too wide", "A table-like file may need manual review for manuscript layout.", "Review generated tables in the compiled manuscript.", "", "docs/error_codes.md"),
    "W008": DiagnosticMessage("W008", "WARNING", "Word conversion needs cleanup", "Converted Word/Markdown content contains patterns that often require manual cleanup.", "Review equations, citations, tables, figures, captions, and tracked changes.", "paper-scaffold audit-word-conversion --input converted.tex", "docs/word_to_overleaf.md"),
    "W009": DiagnosticMessage("W009", "WARNING", "Overleaf sync may fail with Git LFS or submodules", "Git LFS pointers or submodules can complicate Overleaf sync.", "Avoid submodules/LFS in simple manuscript repos or confirm Overleaf supports your setup.", "", "docs/github_overleaf_sync.md"),
    "W010": DiagnosticMessage("W010", "WARNING", "No artifact manifest found", "metadata/artifact_manifest.yaml is missing.", "Create a manifest to track copied figure/table provenance.", "", "docs/artifact_manifest.md"),
    "W011": DiagnosticMessage("W011", "WARNING", "No terminology map found", "metadata/terminology_map.yaml is missing.", "Create one if implementation labels need cleanup.", "", "docs/terminology_cleanup.md"),
    "W012": DiagnosticMessage("W012", "WARNING", "No supplement found", "No supplement file was detected.", "Ignore this if the manuscript has no supplement.", "", "docs/validation.md"),
    "W013": DiagnosticMessage("W013", "WARNING", "No LICENSE found", "The repository does not contain a LICENSE file.", "Add a license before public release if this is a public repository.", "", "docs/faq.md"),
    "W014": DiagnosticMessage("W014", "WARNING", "No README found", "The repository does not contain a README file.", "Add a README that explains the manuscript repository.", "", "docs/faq.md"),
    "W015": DiagnosticMessage("W015", "WARNING", "Uncited bibliography entry", "A BibTeX entry is not cited by the TeX source.", "Remove stale references or cite them intentionally.", "paper-scaffold check-citations --manuscript-repo ./paper", "docs/error_codes.md"),
    "W016": DiagnosticMessage("W016", "WARNING", "Figure or table may be missing a label", "A figure/table environment may not contain a label.", "Add labels if you need cross-references.", "paper-scaffold check-labels --manuscript-repo ./paper", "docs/error_codes.md"),
    "W017": DiagnosticMessage("W017", "WARNING", "Possible private or secret text", "A privacy scan found a local path, credential-like token, email, or private marker.", "Remove or redact private values before publishing.", "paper-scaffold privacy-check --path .", "docs/error_codes.md"),
    "I001": DiagnosticMessage("I001", "INFO", "Running inside Paper Scaffold tool repo", "This is the Paper Scaffold tool repository, not a manuscript repository. Missing main.tex is expected here.", "Run manuscript checks inside a manuscript repo.", "", "docs/getting_started.md"),
    "I002": DiagnosticMessage("I002", "INFO", "Optional tool missing but workflow can continue", "An optional tool is missing, but the current workflow can continue.", "Install the tool only if you need that feature.", "", "docs/faq.md"),
    "I003": DiagnosticMessage("I003", "INFO", "Manuscript repo shape detected", "Expected manuscript files/folders were found.", "Continue with validation before sync.", "paper-scaffold validate --manuscript-repo ./paper", "docs/validation.md"),
    "I004": DiagnosticMessage("I004", "INFO", "Git remote origin configured", "A Git remote named origin is configured.", "Confirm it points to the intended manuscript repository.", "git remote -v", "docs/github_overleaf_sync.md"),
    "I005": DiagnosticMessage("I005", "INFO", "Artifact manifest valid", "The artifact manifest parsed successfully.", "Keep it updated when figures/tables change.", "", "docs/artifact_manifest.md"),
    "I006": DiagnosticMessage("I006", "INFO", "No forbidden files found", "No raw/model/cache output patterns were detected.", "Continue reviewing staged files before sync.", "git status --short", "docs/validation.md"),
}


def get_message(code: str) -> DiagnosticMessage:
    normalized = code.upper()
    if normalized not in MESSAGES:
        raise KeyError(normalized)
    return MESSAGES[normalized]


def all_messages() -> list[DiagnosticMessage]:
    return [MESSAGES[code] for code in sorted(MESSAGES)]


def format_message(message: DiagnosticMessage) -> str:
    lines = [
        f"{message.code} [{message.severity}] {message.title}",
        "",
        message.explanation,
        "",
        f"Suggested fix: {message.suggested_fix}",
    ]
    if message.example_command:
        lines.extend(["", f"Example: {message.example_command}"])
    if message.docs_path:
        lines.extend(["", f"Docs: {message.docs_path}"])
    return "\n".join(lines)


def format_finding(finding: DiagnosticFinding) -> str:
    message = finding.message
    location = ""
    if finding.path:
        location = finding.path
        if finding.line is not None:
            location += f":{finding.line}"
    suffix = f" ({location})" if location else ""
    detail = f": {finding.detail}" if finding.detail else ""
    return f"{message.code} [{message.severity}] {message.title}{suffix}{detail}"


def severity_counts(findings: list[DiagnosticFinding]) -> dict[str, int]:
    counts = {"ERROR": 0, "WARNING": 0, "INFO": 0}
    for finding in findings:
        counts[finding.message.severity] = counts.get(finding.message.severity, 0) + 1
    return counts
