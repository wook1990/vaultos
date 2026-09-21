# Changelog

VaultOS 프레임워크(이 repo)의 버전 기록이다. SemVer를 따른다.

- **MAJOR**: 구조/필수 계약이 바뀐다 (기존 방식으로 만든 볼트가 깨질 수 있다)
- **MINOR**: 새로운 선택적 규칙·필드·템플릿이 추가된다 (기존 볼트는 그대로 동작한다)
- **PATCH**: 문구·설명 보강, 오탈자, 문서 내 인덱스 정정

버전과 실제 배포 상태가 어긋난 적이 있었다 — `VAULTOS.md`는 이미 `vaultos_version: 2.0.0`을 선언하고 있었는데 이 파일의 `VERSION`은 `1.0.0`에 머물러 있었다. 2026-09-21 정합화에서 이 어긋남을 바로잡았다. 앞으로는 framework 파일을 바꾸는 커밋에는 반드시 이 파일과 `VERSION`을 같이 갱신한다.

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
