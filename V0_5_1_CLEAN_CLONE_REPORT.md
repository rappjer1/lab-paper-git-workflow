# v0.5.1 Clean Clone Report

## Scope

v0.5.1 is a public-readiness hotfix based on a clean-clone test of the v0.5 release.

## Clean Clone Results

- Clean clone passed.
- Editable install succeeded.
- Pytest passed with `36 passed` in the original clean-clone check.
- Hotfix test suite passed with `39 passed`.
- Installed CLI worked when called directly as `R:/Code/Envs/nh_quantum/Scripts/paper-scaffold.exe`.
- Git Bash did not find `paper-scaffold` until the environment `Scripts` directory was added to `PATH`.
- Windows pytest initially hit a temp-directory `PermissionError`; repo-local `TMP`, `TEMP`, and `--basetemp` fixed it.

## Fixes Applied

- Added Windows/Git Bash installed CLI notes to `docs/troubleshooting.md` and `CONTRIBUTING.md`.
- Added Windows pytest temp-directory workaround to `docs/troubleshooting.md` and `CONTRIBUTING.md`.
- Updated `paper-scaffold demo` so the demo manuscript references `figures/example_metric_plot.pdf`.
- Updated `paper-scaffold demo` so the demo manuscript cites `example_reference`.
- Kept the PNG example output in `examples/minimal_python_artifacts/outputs`, but stopped copying it into the demo manuscript as an unreferenced figure.

## Demo Warning Status

The v0.5 clean-clone demo warnings were:

- `W005` for unreferenced PDF/PNG figures.
- `W015` for uncited `example_reference`.

v0.5.1 addresses those warnings by referencing the included PDF figure and citation from demo `main.tex`.

## Validation Commands

```text
R:\Code\Envs\nh_quantum\python.exe scripts\paper-scaffold.py demo --output scratch\demo_manuscript --overwrite
R:\Code\Envs\nh_quantum\python.exe scripts\paper-scaffold.py validate --manuscript-repo scratch\demo_manuscript --write-report scratch\demo_manuscript\validation_report.md --write-json scratch\demo_manuscript\validation_report.json
R:\Code\Envs\nh_quantum\python.exe scripts\paper-scaffold.py overleaf-check --manuscript-repo scratch\demo_manuscript
R:\Code\Envs\nh_quantum\python.exe -m pytest tests
```

## Hotfix Validation Results

- `demo`: passed with `0 errors, 0 warnings`.
- `validate --write-report --write-json`: passed with `0 errors, 0 warnings`.
- `overleaf-check`: passed with `0 errors, 0 warnings`.
- Exact `python -m pytest tests`: reproduced the Windows temp-directory `PermissionError`.
- Documented repo-local temp workaround: passed with `39 passed`.
