---
type: system
doc: lifecycle
updated: 2026-09-19
---

# Lifecycle

프로젝트가 어떤 단계를 거치며, 각 단계에서 무엇을 만들고 무엇을 갱신하는지 정한다.

## 1. Project Lifecycle

```
IDEA → DISCOVERY → PLANNING → APPROVED → IMPLEMENTATION → VERIFICATION → RELEASE → MAINTENANCE → ARCHIVE
```

| 단계 | 끝나는 조건 |
|---|---|
| IDEA | 문제와 아이디어가 문장으로 고정됨 |
| DISCOVERY | 조사 질문과 초기 근거가 생김 |
| PLANNING | MVP 범위와 요구사항이 고정됨 |
| APPROVED | 사람이 범위·방향을 승인함 |
| IMPLEMENTATION | 코드와 tracker가 실제로 움직임 |
| VERIFICATION | Requirement 대비 Evidence가 확보됨 |
| RELEASE | 내보낼지·막을지 결정이 기록됨 |
| MAINTENANCE | 운영 중. 이슈와 리스크만 관리 |
| ARCHIVE | 더 이상 진행하지 않음. `99_ARCHIVE`로 이동 |

## 2. Canonical Project State

`project.yaml`의 `status.phase`에 아래 중 하나를 쓴다.

```
idea → profiled → scaffolded → planned → building → validating → release_ready → operating
```

이 상태는 `status/current-state.yaml`과 프로젝트 문서에서 **같은 값으로 보여야 한다.**

## 3. 세션 실행 규칙

1. 세션 시작 시 `resume`으로 Zone A(workspace tracker) 상태를 먼저 읽는다
2. 프로젝트의 `60_Links/11_LLM_Brief.md`에서 workspace 경로와 현재 phase를 확인한다
3. 현재 phase의 lead agent를 정한다
4. **현재 phase에 필요한 문서만** 만들거나 갱신한다. 새 트래킹 표면을 만들지 않는다
5. Zone A(`tracker/*.yaml`)를 갱신한다
6. 세션 종료 시 `sync`로 `11_Status.md`(또는 `status/current-state.yaml`)만 갱신한다
7. 승인이 필요한 단계면 사람 검토 후보로 올린다 → [[01_GOVERNANCE/approval-policy|Approval Policy]]

### 연속 자동 반영(`watch`)은 쓰지 않는다

여러 기기가 동시에 Google Drive 파일을 건드리는 것이 **동기화 충돌의 구조적 원인**이었다.
동기화는 세션 경계에서만 한다 — 시작할 때 한 번, 끝낼 때 한 번.

## 4. Phase별 산출물

| Phase | 목적 | 핵심 문서 |
|---|---|---|
| Idea Intake | 문제와 아이디어를 명확히 한다 | initiative brief |
| Research | 조사 질문과 초기 근거를 만든다 | research plan, experiment log |
| Market Validation | 시장 기회와 wedge를 검증한다 | product brief, market validation |
| Product Spec | MVP 범위와 요구사항을 고정한다 | PRD, roadmap |
| Design / Architecture | 화면·상태·구조를 정의한다 | architecture, wireframe notes, screen spec, ADR |
| Implementation | 코드와 tracker를 실제로 움직인다 | code, tasks, issues, progress |
| Review / QA | release 판단 수준인지 확인한다 | QA summary, release checklist |
| Security / Risk | release에 영향을 주는 보안·리스크를 평가한다 | security review |
| Release Decision | 내보낼지·막을지·조건이 더 필요한지 결정한다 | release decision |

Research 결과는 바로 permanent가 아니라 **검토 후보**다.

## 5. Release Gate

release 전 확인한다.

- Critical Requirements Verified
- No High Risk Open Issue
- No Unauthorized Drift
- Required CR / ADR Approved
- Tests Passed, Evidence Collected
- Rollback Plan Exists

## 6. Archive Policy

다음은 삭제하지 않고 `99_ARCHIVE`로 내린다.

Old Specification / Rejected CR / Superseded ADR / Deprecated Architecture / Closed Risk / Previous Baseline

## 상세 안내

재설계 배경: [Zone Simplification](https://github.com/<you>/vaultos/blob/main/docs/CASE-STUDY.md)
