"""Consolidated release-readiness checks for manuscript repositories."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .checks import (
    check_citations,
    check_figures,
    check_github_repo,
    check_labels,
    check_manuscript,
    check_overleaf,
    check_privacy,
    check_stale_artifacts,
    check_unused_artifacts,
    format_findings,
)
from .messages import DiagnosticFinding, severity_counts


@dataclass(frozen=True)
class ReleaseCheckSection:
    name: str
    findings: list[DiagnosticFinding]


@dataclass(frozen=True)
class ReleaseCheckResult:
    root: Path
    sections: list[ReleaseCheckSection]

    @property
    def findings(self) -> list[DiagnosticFinding]:
        return [finding for section in self.sections for finding in section.findings]

    @property
    def unique_findings(self) -> list[DiagnosticFinding]:
        seen: set[tuple[str, str, int | None, str]] = set()
        unique: list[DiagnosticFinding] = []
        for finding in self.findings:
            key = (finding.code, finding.path, finding.line, finding.detail)
            if key in seen:
                continue
            seen.add(key)
            unique.append(finding)
        return unique

    @property
    def ok(self) -> bool:
        return severity_counts(self.unique_findings).get("ERROR", 0) == 0


def run_release_check(root: str | Path) -> ReleaseCheckResult:
    repo = Path(root)
    sections = [
        ReleaseCheckSection("validate", check_manuscript(repo)),
        ReleaseCheckSection("overleaf-check", check_overleaf(repo)),
        ReleaseCheckSection("privacy-check", check_privacy(repo)),
        ReleaseCheckSection("check-figures", check_figures(repo)),
        ReleaseCheckSection("check-citations", check_citations(repo)),
        ReleaseCheckSection("check-labels", check_labels(repo)),
        ReleaseCheckSection("stale-artifacts", check_stale_artifacts(repo)),
        ReleaseCheckSection("unused-artifacts", check_unused_artifacts(repo)),
    ]
    if (repo / ".git").exists():
        sections.insert(2, ReleaseCheckSection("github-check", check_github_repo(repo)))
    return ReleaseCheckResult(root=repo, sections=sections)


def format_release_check(result: ReleaseCheckResult) -> str:
    counts = severity_counts(result.unique_findings)
    lines = [
        "# Paper Scaffold Release Check",
        "",
        f"- Manuscript repo: {result.root.as_posix()}",
        f"- Summary: {counts.get('ERROR', 0)} errors, {counts.get('WARNING', 0)} warnings, {counts.get('INFO', 0)} info",
        "",
    ]
    for section in result.sections:
        section_counts = severity_counts(section.findings)
        lines.extend(
            [
                f"## {section.name}",
                "",
                f"- Summary: {section_counts.get('ERROR', 0)} errors, {section_counts.get('WARNING', 0)} warnings, {section_counts.get('INFO', 0)} info",
            ]
        )
        if section.findings:
            lines.extend(["", "```text", format_findings(section.findings), "```", ""])
        else:
            lines.extend(["", "No findings.", ""])
    lines.extend(["## Next Actions", ""])
    if counts.get("ERROR", 0):
        lines.append("- Fix errors before submission, public release, or GitHub/Overleaf sync.")
    else:
        lines.append("- No errors found. Review any warnings and commit intentionally.")
    if counts.get("WARNING", 0):
        lines.append("- Warnings may be acceptable, but they should be explicitly reviewed.")
    return "\n".join(lines).rstrip() + "\n"
