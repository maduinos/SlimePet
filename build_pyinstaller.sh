#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

OS_NAME="$(uname -s)"
OUT_DIR=""
APP_NAME="SlimePet"

case "${OS:-$OS_NAME}" in
  Windows_NT|MINGW*|MSYS*|CYGWIN*)
    OUT_DIR="dist/windows"
    APP_NAME="SlimePet.exe"
    PYI_NAME="SlimePet_win"
    TMP_BUILD_DIR="build/windows"
    ;;
  Linux|Darwin)
    OUT_DIR="dist/linux"
    APP_NAME="SlimePet"
    PYI_NAME="SlimePet"
    TMP_BUILD_DIR="build/linux"
    ;;
  *)
    echo "Unsupported OS: ${OS:-$OS_NAME}"
    exit 1
    ;;
esac

mkdir -p "$OUT_DIR"

pyinstaller \
  --noconfirm \
  --clean \
  --onefile \
  --windowed \
  --name "$PYI_NAME" \
  --icon assets/SlimePet.ico \
  --distpath "$OUT_DIR" \
  --workpath "$TMP_BUILD_DIR" \
  --specpath . \
  SlimePet.py

if [ -f "$OUT_DIR/SlimePet_win.exe" ]; then
  mv -f "$OUT_DIR/SlimePet_win.exe" "$OUT_DIR/SlimePet.exe"
fi

rm -rf build
rm -f ./*.spec
rm -f dist/SlimePet dist/SlimePet.exe dist/SlimePet_win.exe

echo "Build complete: $OUT_DIR/$APP_NAME"
