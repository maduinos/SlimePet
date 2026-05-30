# Release Process

## Before Release

1. Run `python3 -m unittest discover -s tests -v`.
2. Run `python3 -m py_compile SlimePet.py slimepet_core.py tests/test_slimepet_core.py`.
3. Update `APP_VERSION` in `slimepet_core.py`.
4. Update `README.md`, `PROGRESS.md`, and `CHANGELOG.md`.
5. Run `./build_pyinstaller.sh` on the target OS when publishing binaries.
6. Confirm build artifacts are not committed unless intentionally attached to a GitHub release.

## Tag Format

Use the app version:

```bash
git tag v0.0.4
git push origin v0.0.4
```

