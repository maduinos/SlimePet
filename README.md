> 만든 사람: maduinos<br>
> 문서 만든 날짜: 2026-03-01<br>
> https://maduinos.blogspot.com/

# SlimePet v0.0.5 - 데스크톱 슬라임 펫

> 작성자: maduinos
> Rev. v0.0.5

## 목차
1. [소개](#1-소개)
2. [버전 이력](#2-버전-이력)
3. [릴리스 노트](#3-릴리스-노트)
4. [빠른 시작](#4-빠른-시작)
5. [실행 파일 빌드 PyInstaller](#5-실행-파일-빌드-pyinstaller)
6. [버전 규칙](#6-버전-규칙)
7. [라이선스](#7-라이선스)

## 1. 소개
`SlimePet`는 데스크톱 위를 돌아다니는 간단한 슬라임 펫 앱입니다.

- PyQt6 기반 프레임리스(always-on-top) 위젯
- 시간이 지나면 배고파지고 상태(색/표정)가 변함
- 최대 크기 도달 후 1분마다 슬라임이 계속 추가 생성됨
- 클릭하면 먹이를 준 것으로 처리되어 배고픔이 리셋됨
- 드래그로 위치를 수동 이동 가능

## 2. 버전 이력
| Rev. | 날짜 | 작성자 | 설명 |
| - | - | - | - |
| v0.0.5 | 2026-05-30 | Codex | 음수 화면 경계를 안전하게 처리하도록 `clamp_position()` 보강 |
| v0.0.4 | 2026-05-30 | Codex | core helper 분리와 requirements 문서 추가 |
| v0.0.3 | 2026-03-01 | maduinos | GPL-3.0 license 추가 및 문서/버전 갱신 |
| v0.0.2 | 2026-03-01 | maduinos | AGENTS.md 추가 및 버전 기록 동기화 |
| v0.0.1 | 2026-03-01 | maduinos | SlimePet 최초 공개 버전 |

## 3. 릴리스 노트
### v0.0.5
- `clamp_position()`이 음수 최대 경계를 0으로 처리하도록 보강

### v0.0.4
- `slimepet_core.py`에 앱 메타데이터와 좌표 보정 유틸리티를 분리
- `requirements.txt` 추가

### v0.0.3
- 오픈소스 배포를 위한 `LICENSE`(GNU GPLv3) 파일 추가
- `README.md`에 라이선스 안내 섹션 추가
- 버전 상수 `APP_VERSION`를 `v0.0.3`으로 갱신

### v0.0.2
- `AGENTS.md` 작업 규칙 문서 추가
- 버전 상수 `APP_VERSION`를 `v0.0.2`로 갱신
- `PROGRESS.md`/`README.md` 버전 기록 동기화

### v0.0.1
- `SlimePet.py` 기본 동작 구현
- 클릭 급식 / 드래그 이동 / 화면 랜덤 이동
- 배고픔 상태에 따른 표정/색상 변화
- 코드 버전 상수(`APP_VERSION`) 유지
- PyInstaller 빌드 스크립트와 아이콘 생성 스크립트 추가

## 4. 빠른 시작
### 요구 사항
- Python 3.10+
- `PyQt6`
- `PyInstaller` (실행파일 빌드용)

### 의존성 설치
```bash
cd SlimePet
python3 -m pip install -r requirements.txt
```

### 소스에서 실행
```bash
cd SlimePet
python3 SlimePet.py
```

### 조작
- `마우스 좌클릭`: 슬라임에게 먹이 주기 (배고픔/성장 리셋)
- `좌클릭 드래그`: 슬라임 위치 이동
- `슬라임 클릭 후 q`: 앱 종료

## 5. 실행 파일 빌드 PyInstaller
아이콘은 저장소에 포함된 `assets/SlimePet.ico`를 사용합니다.

### 빌드 자동 OS 분기
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

## 6. 버전 규칙
- 시작 버전은 `v0.0.1`
- 기능 수정/추가 후 Git에 push할 때마다 버전을 1단계 올림
- 버전 상승 시 아래 3개를 함께 업데이트
  - `README.md`의 버전 이력/릴리스 노트
  - `PROGRESS.md` 로그

## 7. 라이선스
- 이 프로젝트는 `GNU General Public License v3.0 (GPL-3.0)`로 배포됩니다.
- 자세한 내용은 저장소의 `LICENSE` 파일을 참고하세요.

## 8. 프로젝트 관리
- 변경 이력: `CHANGELOG.md`
- 릴리스 절차: `RELEASE.md`
- 지원 범위: `SUPPORT.md`
- 기여 가이드: `CONTRIBUTING.md`
- 보안/비공개 데이터 신고: `SECURITY.md`
