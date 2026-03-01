# SlimePet Progress Log

## 2026-03-01
- 버전 업데이트: `v0.0.1 -> v0.0.2`
- `AGENTS.md` 작업 규칙 문서 추가
- `SlimePet.py` 버전 상수 `APP_VERSION = "v0.0.2"` 반영
- `README.md` Revision/Release Notes `v0.0.2` 반영
- 프로젝트 버전 시작: `v0.0.1`
- `SlimePet.py`에 버전 상수(`APP_VERSION`) 추가
- 앱 시작 시 콘솔에 버전 표시 추가
- 앱 화면 우하단에 버전(`v0.0.1`) 표시 추가
- PyInstaller 아이콘 적용을 위한 `assets/` 폴더 구성 시작
- 아이콘 생성 스크립트(`generate_icon.py`) 및 빌드 스크립트(`build_pyinstaller.sh`) 추가
- `generate_icon.py` 실행으로 `assets/SlimePet.ico` / `assets/SlimePet_icon.png` 생성
- `build_pyinstaller.sh`로 PyInstaller 빌드 성공 (`dist/SlimePet`)
- Linux 빌드에서는 `.ico`가 무시된다는 PyInstaller 경고 확인(Windows/macOS에서는 아이콘 사용됨)
- 슬라임 클릭으로 포커스 획득 후 `q` 키로 종료 기능 추가
- README 조작법에 `슬라임 클릭 후 q: 앱 종료` 항목 반영
- 앱 외형과 더 비슷한 물방울형 파란 슬라임 스타일로 아이콘(`generate_icon.py`) 재작성
- 아이콘 재생성 완료: `assets/SlimePet_icon.png`, `assets/SlimePet.ico`
- 최대 크기 도달 후 1분 무클릭 시 성장 해제 대신 슬라임 1개를 추가 생성(총 2개)하도록 로직 변경
- 슬라임에 보이는 버전 표시 요청에 맞춰 버전 출력(창 제목/콘솔 표시) 제거

## 로그 작성 규칙
- 기능 수정/추가 후 push할 때마다 버전 증가
- 같은 시점에 이 파일에 변경 요약 1~5줄 기록
- 분열 로직을 1회 생성에서 반복 생성으로 변경: 최대 크기 유지 + 무클릭 상태에서 1분마다 슬라임 계속 추가 생성
- 빌드 스크립트를 OS별 분리(`build_linux.sh`, `build_windows.sh`)로 개편
- 빌드 완료 후 임시 빌드파일(`build/`, `*.spec`) 자동 삭제하도록 변경
- Linux 빌드 결과 경로를 `dist/linux/SlimePet`로 분리
- 빌드 스크립트를 단일 파일(`build_pyinstaller.sh`)로 통합
- OS 자동 분기(Linux/macOS -> `dist/linux`, Windows -> `dist/windows`) 로직을 단일 스크립트에 반영
- 별도 스크립트(`build_linux.sh`, `build_windows.sh`) 삭제
- 정리 작업: `__pycache__/`, `generate_icon.py`, `requirements.txt` 제거
- 빌드 스크립트에서 아이콘 생성 스크립트 의존성 제거(`assets/SlimePet.ico` 직접 사용)
- 프로젝트명 표기 통일: `slime_pet` -> `SlimePet` (폴더/파일/스크립트/문서/빌드 산출물명 포함)
