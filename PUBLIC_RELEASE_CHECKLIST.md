# Public Release Checklist

Use this before changing repository visibility or announcing a public release.

## Required

- [ ] Docs complete.
- [ ] README explains value in under one minute.
- [ ] Examples run.
- [ ] Demo command works.
- [ ] `paper-scaffold explain E003` works.
- [ ] `paper-scaffold validate --write-report` works.
- [ ] Focused diagnostics pass or produce only reviewed warnings.
- [ ] Tests pass locally.
- [ ] GitHub Actions passes after push.
- [ ] No private paths.
- [ ] No unpublished manuscript content.
- [ ] No project-specific manuscript details.
- [ ] No raw data.
- [ ] No secrets.
- [ ] No large files.
- [ ] License present.
- [ ] Contributing docs present.
- [ ] Code of conduct present.
- [ ] Security policy present.
- [ ] Citation file present.
- [ ] Public-readiness audit reviewed.

## Version Tag Instructions

After merge to `main` and after CI passes:

```bash
git tag v0.4.0
git push origin v0.4.0
```

## Manual Review Before Public Visibility

Before changing visibility to public, inspect:

```bash
git status --short
git diff --stat
git ls-files
```

Then search for private material:

```bash
rg -n -i "R:/Code|R:\\Code|secret|token|password|private data|unpublished"
```

Confirm that example artifacts are small and synthetic.

Run diagnostics:

```bash
paper-scaffold explain --list
paper-scaffold privacy-check --path .
paper-scaffold github-check --repo .
```
