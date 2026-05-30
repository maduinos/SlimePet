# Contributing

This repository is a personal desktop toy app.

## Scope

Good contributions include:

- Documentation improvements.
- Small behavior fixes.
- Tests for non-GUI helper logic.
- Packaging and build script maintenance.

Out of scope:

- Large rewrites unrelated to the current PyQt6 app.
- Generated build artifacts.

## Checklist

- Run `python3 -m unittest discover -s tests -v`.
- Run `python3 -m py_compile SlimePet.py slimepet_core.py tests/test_slimepet_core.py`.
- Update `README.md` and `PROGRESS.md` when behavior or version changes.

