# Changelog

VaultOS 프레임워크(이 repo)의 버전 기록이다. SemVer를 따른다.

- **MAJOR**: 구조/필수 계약이 바뀐다 (기존 방식으로 만든 볼트가 깨질 수 있다)
- **MINOR**: 새로운 선택적 규칙·필드·템플릿이 추가된다 (기존 볼트는 그대로 동작한다)
- **PATCH**: 문구·설명 보강, 오탈자, 문서 내 인덱스 정정

버전과 실제 배포 상태가 어긋난 적이 있었다 — `VAULTOS.md`는 이미 `vaultos_version: 2.0.0`을 선언하고 있었는데 이 파일의 `VERSION`은 `1.0.0`에 머물러 있었다. 2026-09-21 정합화에서 이 어긋남을 바로잡았다. 앞으로는 framework 파일을 바꾸는 커밋에는 반드시 이 파일과 `VERSION`을 같이 갱신한다.

## [2.2.0] - 2026-09-21

`07_PRODUCTS/` 신설 — 배포된 제품과 운영 중인 자동화를 위한 새 계층. 사용자가 붙여넣은 원본 spec(`VaultOS × AIPM-Trace Final Architecture Specification v1.0`)에는 없던 개념으로, Project Lifecycle의 `RELEASE → MAINTENANCE` 단계 이후를 위한 자리가 없다는 실사용 필요에서 신설했다.

### Added
- `07_PRODUCTS/README.md`, `personal/README.md`, `company/README.md`
- `00_SYSTEM/templates/product/product.yaml` — 운영 상태 요약 전용 템플릿(개발 상태 복제 금지)
- `05_OPERATIONS/dashboard/30_products.md`
- `VAULTOS.md`/`architecture.md`/`naming-rules.md`/`project-policy.md`/`00_dashboard.md`에 `07_PRODUCTS` 반영, `06_AUTOMATIONS`(VaultOS 자체 검사용, 07과 다른 계층)는 여전히 보류 중임을 명시

### Fixed
- (이전 커밋에서 반영, 이번에 버전 기록만 정리) `01_GOVERNANCE/vaultos-health.md`의 "구현" 포인터가 `vaultos-health-check` 흡수 전 경로를 가리키던 것을 vault·framework 양쪽에서 정정

## [2.2.3] - 2026-09-21

실제 vault에 "완전히 개발됐는지" 확인해달라는 요청을 받고 `vaultos_health.py`를 돌려보다가 두 개의 진짜 버그를 발견했다.

### Fixed
- `tools/tests/test_vaultos_health.py`가 `sys.path`에 존재하지 않는 `tools/src/`를 넣고 있어 **테스트 스위트 자체가 한 번도 실행된 적이 없었다** (`ModuleNotFoundError`). `tools/`로 정정
- `vaultos_health.py`의 링크 검사가 `.md` 파일만 알고 있어서, `project.yaml`처럼 실제로 존재하는 비-`.md` 파일로의 위키링크를 전부 broken-link로 오탐했다. `scan_vault`가 모든 파일(`all_files`)도 함께 인덱싱하도록 고치고, 링크 검사에서 먼저 확인하도록 했다

### Verified
- 수정 후 `tools/tests/test_vaultos_health.py` 23개 테스트 전부 통과
- 실제 vault(`/mnt/g/내 드라이브/LvUp_Storage/Storage`) 대상 실행: error 0 / warn 0 / note 1

## [2.2.2] - 2026-09-21

### Fixed
- `05_OPERATIONS/dashboard/00_dashboard.md`의 "활성 프로젝트" dataviewjs 블록이 죽은 코드였다 — Dataview는 `.yaml`을 인덱싱하지 않아 `project.yaml`을 절대 찾지 못하는데도 마치 동작하는 것처럼 남아 있었다. 제거하고 `10_projects.md`로 안내만 남겼다

### Added
- `05_OPERATIONS/dashboard/10_projects.md`에 손으로 유지하는 "전체 프로젝트 한판" 표 추가 — 프로젝트가 늘어도 한 페이지에서 phase/blocked/next_actions/risks를 본다. 자동화(스크립트로 생성)는 프로젝트가 많아져서 손 관리가 아쉬워질 때 추가하기로 미뤘다

## [2.2.1] - 2026-09-21

### Fixed
- `update-policy.md`의 "인스턴스 전용 링크" 예시가 특정 vault의 `00_SYSTEM/migrations/` 경로를 구체적으로 인용하고 있어 일반화 — vault마다 실제로 뭘 인스턴스 기록으로 두는지는 다를 수 있다
- `07_PRODUCTS/README.md`가 애초에 framework에는 존재한 적 없는 `00_SYSTEM/migrations/2026-09-19_target-architecture.md`(특정 vault의 이행 기록)를 인용하고 있던 것을 정정 (v2.2.0 백포트 시 vault 버전을 그대로 복사하면서 생긴 실수)

## [2.1.0] - 2026-09-21

vault(`wook1990`의 실제 운영 볼트)에서 먼저 검증된 큐레이션 규칙 개선을 framework로 백포트했다.

### Added
- `00_SYSTEM/templates/`에 11개 템플릿 추가 (`11_Inbox_Capture` 등 project/* 제외 전부) — 이전에는 `project/*` 템플릿만 framework에 있었다
- `03_KNOWLEDGE/README.md`, `05_OPERATIONS/README.md`, `05_OPERATIONS/reviews/promotion-rules.md` 추가
- `01_GOVERNANCE/knowledge-policy.md`, `04_AGENTS/curation/01_AI_Curation_Caution_Agent.md`, `04_AGENTS/curation/01_Dynamic_Persona_Curation_Prompt.md`에 **"지식과 프로젝트의 연결 방향"** 규칙 추가 — 연결은 프로젝트 쪽에서 지식을 찾아 읽을 때 시작되는 것이지, 큐레이션 시점에 먼저 프로젝트를 찾아 붙이는 것이 아니다. `linked_project` 명시 / `connect_to_project` intent / source가 프로젝트를 직접 언급 — 이 세 조건이 아니면 Project Hooks는 비워둔다
- `04_AGENTS/curation/01_AI_Curation_Caution_Agent.md`에 Inbox 파일명 확인 규칙 추가 — `source_link_path` 등에 확인하지 않은 파일명을 추측해서 쓰지 않는다 (broken link의 실측 원인이었다)

### Fixed
- `00_SYSTEM/templates/01_README.md`의 템플릿 목록이 이미 폐지된 항목(`22_프로젝트_칸반`, `31_임시메모_템플릿`, `32_연구메모_템플릿`)을 가리키고 실제 존재하는 항목(`25_VO_Phase_Artifact`, `26_VO_Query_Note`, `43_Monthly_Worklog`, `44_Yearly_Worklog`)은 누락하고 있던 것을 실제 폴더 상태에 맞게 정정

### Not backported (의도적으로 제외)
- `00_SYSTEM/templates/45_QT_Note.md`, `46_QT_Clipboard_Capture.md` — 개인 신앙 기록 템플릿, 프레임워크 범용 배포 대상이 아니다
- `05_OPERATIONS/reports/worklog/*` — 이 vault 안에서도 "되살릴지 결정 안 함" 상태인 기능. 확정되지 않은 걸 배포판에 넣지 않는다
- `00_SYSTEM/migrations/*`, `00_SYSTEM/vault-config.yaml` — 특정 vault의 설치 이력·설정값. 애초에 framework 템플릿이 아니라 인스턴스 데이터다
- `04_AGENTS/curation/02_강의_기획자_에이전트.md` — 특정 프로젝트 전용 에이전트, 범용 아님

## [2.0.0] - 2026-09-19

3-Zone 단순화 + AIPM-Trace 이행. `VERSION` 파일이 이때 갱신되지 않아 2.1.0과 함께 소급 기록한다. 상세 내역은 `docs/CASE-STUDY.md`.

## [1.0.0] - 2026-09-19 (오전 이전)

VaultOS v1.0.0 — 지식 저장소 + 프로젝트 관리 프레임워크 초판.
