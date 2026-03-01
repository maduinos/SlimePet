# SlimePet v0.0.1 - Desktop Slime Pet
> Written by maduinos
> Rev. v0.0.1

## Contents
1. [Introduction](#1-introduction)
2. [Revision History](#2-revision-history)
3. [Release Notes](#3-release-notes)
4. [Quick Start Guide](#4-quick-start-guide)
5. [Build Executable (PyInstaller)](#5-build-executable-pyinstaller)
6. [Version Rule](#6-version-rule)

## 1. Introduction
`SlimePet`는 데스크톱 위를 돌아다니는 간단한 슬라임 펫 앱입니다.

- PyQt6 기반 프레임리스(always-on-top) 위젯
- 시간이 지나면 배고파지고 상태(색/표정)가 변함
- 최대 크기 도달 후 1분마다 슬라임이 계속 추가 생성됨
- 클릭하면 먹이를 준 것으로 처리되어 배고픔이 리셋됨
- 드래그로 위치를 수동 이동 가능

## 2. Revision History
| Rev. | Date | Author | Description |
| - | - | - | - |
| v0.0.1 | 2026-03-01 | maduinos | Initial public version of SlimePet |

## 3. Release Notes
### v0.0.1
- `SlimePet.py` 기본 동작 구현
- 클릭 급식 / 드래그 이동 / 화면 랜덤 이동
- 배고픔 상태에 따른 표정/색상 변화
- 코드 버전 상수(`APP_VERSION`) 유지
- PyInstaller 빌드 스크립트와 아이콘 생성 스크립트 추가

## 4. Quick Start Guide
### Requirements
- Python 3.10+
- `PyQt6`
- `PyInstaller` (실행파일 빌드용)

### Run from source
```bash
cd SlimePet
python3 SlimePet.py
```

### Controls
- `마우스 좌클릭`: 슬라임에게 먹이 주기 (배고픔/성장 리셋)
- `좌클릭 드래그`: 슬라임 위치 이동
- `슬라임 클릭 후 q`: 앱 종료

## 5. Build Executable (PyInstaller)
아이콘은 저장소에 포함된 `assets/SlimePet.ico`를 사용합니다.

### Build (Auto OS Split)
```bash
cd SlimePet
./build_pyinstaller.sh
```

결과물(자동 분기):
- Linux/macOS: `dist/linux/SlimePet`
- Windows: `dist/windows/SlimePet.exe`

참고:
- Windows 실행파일은 Windows 환경에서 `build_pyinstaller.sh`를 실행해야 빌드됩니다.
- 빌드 완료 후 임시 빌드파일(`build/*`, `*.spec`)은 자동 삭제됩니다.

## 6. Version Rule
- 시작 버전은 `v0.0.1`
- 기능 수정/추가 후 Git에 push할 때마다 버전을 1단계 올림
- 버전 상승 시 아래 3개를 함께 업데이트
  - `README.md`의 Revision/Release Notes
  - `PROGRESS.md` 로그
