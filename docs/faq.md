# FAQ

## Do I Need Overleaf?

No. Paper Scaffold creates and validates manuscript repositories. Overleaf is optional.

## Do I Need LaTeX Installed?

No. You can scaffold, copy artifacts, and validate repo structure without LaTeX. You need LaTeX only if you want to compile locally.

## Do I Need Pandoc?

Only for automated Word `.docx` conversion. Without Pandoc, use the manual Word-to-LaTeX workflow.

## Can I Use Word?

Yes. Use Word for drafting, then convert or manually move text into the manuscript repo. Conversion always needs manual review.

## Can I Use Google Docs?

Yes. Export to `.docx` or Markdown, then use the Word/Markdown workflow.

## Can I Use Zotero?

Yes. Export BibTeX from Zotero and use it as `references.bib`.

## Should My Research Code And Manuscript Be In The Same Repo?

Usually no. Keep computation in the research repo and manuscript source in a clean manuscript repo.

## What If My Figures Are Huge?

Keep source data and high-volume outputs in the research repo or archive. Commit only publication-ready figures. Consider Git LFS if your project requires large assets.

## What If My Professor Edits In Word?

Keep Word as a drafting format if needed. Convert or manually port accepted text into the manuscript repo before GitHub/Overleaf sync.

## What If Collaborators Edit In Overleaf?

Treat GitHub as the source of truth. Push local changes before syncing Overleaf; pull local changes after Overleaf pushes.

## Can This Create A GitHub Repo?

No. It prints guidance. Use the GitHub website or GitHub CLI yourself.

## Can This Upload To Overleaf?

No. Create or sync Overleaf projects through Overleaf.

## What Does Artifact Manifest Mean?

An artifact manifest is a YAML file that records where copied manuscript figures and tables came from. It preserves provenance without copying raw outputs.
