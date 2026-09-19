---
type: schema
schema: requirement
status: active
updated: 2026-09-19
---

# Requirement Schema

> Machine State는 YAML, Human Explanation은 Markdown. Requirement는 기계 상태이므로 `requirements/requirements.yaml`에 YAML로 쓴다.

## ID 체계

```
REQ-<DOMAIN>-<NNN>
```

예: `REQ-AUTH-001`, `REQ-DATA-004`, `REQ-DASHBOARD-003`

- `DOMAIN`은 대문자 영문. 프로젝트 안에서 일관되게 쓴다
- `NNN`은 3자리 연번. **재사용하지 않는다** — 삭제된 Requirement의 번호도 비워둔다
- ID는 한 번 부여하면 바뀌지 않는다. 내용이 바뀌면 CR을 거치되 ID는 유지한다

## 구조

```yaml
id: REQ-PROJECT-001

statement:
  사용자는 프로젝트를 생성할 수 있어야 한다.

rationale:
  프로젝트 단위 관리가 필요하기 때문이다.

source:
  PRD-001

priority:
  MUST

acceptance:
  - 프로젝트명 입력 가능
  - 생성자 자동 owner
  - 생성시간 저장
  - 프로젝트 목록 즉시 반영

verification:
  - API integration test
  - UI E2E test

status:
  approved
```

## 필드 규칙

| 필드 | 규칙 |
|---|---|
| `statement` | 무엇이 되어야 하는가. **어떻게 만들지는 쓰지 않는다** |
| `rationale` | 왜 필요한가. 이게 없으면 나중에 이 요구사항을 지울지 말지 판단할 수 없다 |
| `source` | 어디서 나왔는가 (PRD, 회의, 사용자 요청, 규제) |
| `priority` | `MUST` / `SHOULD` / `COULD` |
| `acceptance` | 충족 여부를 **판정 가능한** 문장으로 쓴다. "잘 동작한다" 같은 문장은 쓰지 않는다 |
| `verification` | 어떻게 검증할 것인가. Evidence의 근거가 된다 |
| `status` | `draft` / `approved` / `implemented` / `verified` / `deprecated` |

## Traceability Chain

모든 Requirement는 구현과 검증까지 연결되어야 한다.

```
REQ-PROJECT-001
       ↓
SPEC-PROJECT-001
       ↓
ADR-014
       ↓
TASK-031
       ↓
PR #284
       ↓
TEST-PROJECT-001
       ↓
EVIDENCE
       ↓
PASS
```

`requirements/traceability.yaml`에 이 연결을 기록한다.

```yaml
REQ-PROJECT-001:
  spec: SPEC-PROJECT-001
  adr: [ADR-014]
  tasks: [TASK-031]
  pr: ["#284"]
  tests: [TEST-PROJECT-001]
  evidence: evidence/tests/test_project_create.log
  result: PASS
```

체인이 끊긴 지점이 [[04_AGENTS/auditor/README|Auditor]]가 찾는 Drift다.

## 원칙

- **No Requirement, No Code** — 모든 기능 변경은 Requirement / Bug / CR / ADR / Refactoring Task 중 하나에 묶인다
- **No Evidence, No Done** — `verification`이 실행되고 결과가 남아야 완료다
- **No Requirement Change, No CR** — `approved` 이후의 변경은 [[00_SYSTEM/schemas/change-request|CR]]을 거친다
- 확실하지 않은 역복원 Requirement는 `status: inferred`, `confidence: low`로 표기한다. **추정을 사실처럼 쓰지 않는다**

## Governance Profile별 적용

| Profile | Requirement 관리 |
|---|---|
| `personal-light` | 불필요. Mission과 Current State로 충분 |
| `personal-full` | 필요. 단 `traceability.yaml`은 선택 |
| `company-standard` 이상 | 필수. Traceability 포함 |
