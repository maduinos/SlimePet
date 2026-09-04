> 만든 사람: maduinos<br>
> 문서 만든 날짜: 2026-05-30<br>
> https://maduinos.blogspot.com/

# Release Process

## Before Release

1. Run `python3 -m py_compile SlimePet.py slimepet_core.py`.
2. Update `APP_VERSION` in `slimepet_core.py`.
3. Update `README.md`, `PROGRESS.md`, and `CHANGELOG.md`.
4. Run `./build_pyinstaller.sh` on the target OS when publishing binaries.
5. Confirm build artifacts are not committed unless intentionally attached to a GitHub release.

## Tag Format

Use the app version:

```bash
git tag v0.0.4
git push origin v0.0.4
```
