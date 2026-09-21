---
type: system
updated: 2026-09-19
---

# Naming Rules

## 폴더와 파일

- 루트는 `2-digit` 번호 + 영문 역할 이름 (`00_SYSTEM`, `01_GOVERNANCE`, `07_PRODUCTS`, `08_DEVICES`, `99_ARCHIVE`)
- 하위 폴더는 로컬 번호 또는 의미 이름
- 프로젝트 슬러그는 **영문 소문자 + 하이픈** (`my-new-app`, `data-pipeline`)
- 수집·기록 파일은 날짜 기반 이름을 우선한다 (`20260919_openai-agents_inbox.md`)
- 링크 안정성을 구조 미학보다 우선한다

### 금지

- 누적형 긴 번호 체계
- 이동할 때마다 이름 전체를 바꿔야 하는 구조
- 역할보다 생성 주체를 우선하는 폴더명 (`10_AI_Output` 같은 것)
- 공백이 들어간 프로젝트 폴더명 — 스크립트와 경로 참조가 깨진다

## ID 체계

추적성의 기반이다. 모든 ID는 고유하고 재사용하지 않는다.

| 대상 | 형식 | 예시 |
|---|---|---|
| Requirement | `REQ-<DOMAIN>-<NNN>` | `REQ-AUTH-001` |
| Feature | `F-<DOMAIN>-<NNN>` | `F-AUTH-002` |
| Task | `TASK-<DOMAIN>-<NNN>` | `TASK-AUTH-014` |
| Change Request | `CR-<DOMAIN>-<NNN>` | `CR-AUTH-003` |
| Architecture Decision | `ADR-<NNN>` | `ADR-007` |
| Risk | `RISK-<NNN>` | `RISK-004` |
| Test | `TEST-<DOMAIN>-<NNN>` | `TEST-AUTH-011` |
| Issue | `ISSUE-<NNN>` 또는 프로젝트 접두 | `BTC-ISS-001` |

규칙:

- `<DOMAIN>`은 프로젝트 안에서 일관되게 쓴다 (`AUTH`, `DATA`, `DASHBOARD`)
- ADR과 RISK는 도메인 없이 프로젝트 단위 일련번호를 쓴다
- 기존 프로젝트가 이미 자체 접두사를 쓰고 있으면(예: `BTC-PM-058`) **그대로 유지한다.** 소급 변경하지 않는다
- 삭제된 ID의 번호를 다시 쓰지 않는다

## 문서 형식

| 내용 | 형식 |
|---|---|
| 기계가 읽는 상태 | YAML / JSON (`project.yaml`, `current-state.yaml`, `requirements.yaml`) |
| 사람이 읽는 설명 | Markdown (`constitution.md`, `spec.md`, `ADR.md`, `CR.md`) |

## 날짜

- 파일명: `YYYYMMDD` (`20260919_...`)
- frontmatter와 본문: `YYYY-MM-DD` (`2026-09-19`)
- 상대 표현("지난주", "내일")을 기록에 남기지 않는다. 절대 날짜로 쓴다
