---
type: governance
policy: aipm-trace
status: active
updated: 2026-09-19
---

# AIPM-Trace

VaultOS의 프로젝트 운영 방법론이다. 다섯 체계를 하나로 결합한다.

```
Project Management + Systems Engineering + Spec-Driven Development + DevOps + AI Governance
```

| 영역 | 관리 대상 |
|---|---|
| Project Management | Scope, Schedule, Risk, Change |
| Systems Engineering | Requirement, Traceability, Verification |
| Spec-Driven Development | Specification, Plan, Task |
| DevOps | Issue, PR, CI, Test, Release |
| AI Governance | Agent, Context, Approval, Evidence, Drift |

## 왜 필요한가

AI로 프로젝트를 하면 초반엔 빠르지만 시간이 지나면 다음이 발생한다.

- 초기 기획과 실제 구현의 차이가 벌어진다
- 문서가 덧붙여지며 어떤 것이 현재 기준인지 불분명해진다
- AI가 작은 요구를 해결하며 예상 밖 영역까지 수정한다
- 기능은 동작하지만 왜 그렇게 설계됐는지 역추적이 안 된다
- Task는 완료됐지만 Requirement가 충족됐는지 확인되지 않는다
- 새 에이전트가 들어올 때마다 전체 문서를 다시 읽어야 한다
- 과거 의사결정과 현재 상태가 섞인다

AIPM-Trace는 이 문제를 구조로 해결한다.

## 항상 답할 수 있어야 하는 7가지 질문

1. 우리가 무엇을 만들기로 했는가?
2. 왜 그것을 만들기로 했는가?
3. 무엇이 변경되었는가?
4. 왜 변경되었는가?
5. 누가 또는 어떤 Agent가 변경했는가?
6. 현재 구현이 요구사항과 일치하는가?
7. 그것을 증명할 Evidence가 존재하는가?

## 세 개의 Loop

### ① Intent Loop — 무엇을 왜 만드는가

```
WHY → Goal → Requirement → Scope / Constraint
```

관리 대상: Mission, Goal, Scope, Non-Goal, Requirement, Constraint, Success Metric, Assumption

### ② Delivery Loop — 어떻게 만드는가

```
Spec → Plan → Task → Agent → Code → Test → PR
```

### ③ Control Loop — 의도와 결과가 일치하는가

```
Requirement ↕ Code ↔ Test ↔ Evidence
```

다음을 지속적으로 비교한다.

```
Initial Intent vs Requirement vs Specification vs Architecture vs Actual Implementation vs Test
```

불일치가 발생하면 **Drift**로 기록한다. 조용히 덮지 않는다.

## 8가지 핵심 원칙

1. **No Requirement, No Code** — 모든 기능 변경은 Requirement / Bug / CR / ADR / Refactoring Task 중 하나와 연결된다
2. **No Architecture Change, No ADR** — 구조적 변경은 반드시 Architecture Decision Record를 가진다
3. **No Requirement Change, No CR** — 승인된 Requirement를 변경하려면 Change Request가 필요하다
4. **No Evidence, No Done** — 구현 완료는 Done이 아니다. 검증 Evidence가 있어야 한다
5. **AI Executes, Human Governs** — AI는 실행하고, 사람은 방향·우선순위·범위·주요 변경을 통제한다
6. **Repository = Single Source of Truth** — PMS, Notion, 대시보드는 Projection Layer다
7. **Every Change Must Be Traceable** — 모든 의미 있는 변경은 원인과 결과를 추적할 수 있어야 한다
8. **Current Truth ≠ History** — 현재 상태는 간결하게 유지하고, 과거 기록은 삭제하지 않는다

## 표준 작업 흐름

```
INTAKE → CLASSIFY → IMPACT ANALYSIS → APPROVAL GATE → SPECIFICATION
→ PLAN → TASK → IMPLEMENT → VERIFY → CONVERGE → BASELINE UPDATE
```

### Intake — 요청을 분류한다

Goal / Requirement / Feature / Bug / Change / Research / Refactoring / Operation 중 하나로 분류한다.
**AI는 분류 없이 바로 구현하지 않는다.**

### Impact Analysis — 건드리기 전에 확인한다

Constitution, Requirements, Architecture, ADR, Current State, Active Features, Existing Code, Tests, Open Risks를 확인하고 다음을 출력한다.

```
Affected Requirements / Components / APIs / Data / Tests
Risks
Need Human Approval?
```

### Approval Gate

→ [[01_GOVERNANCE/approval-policy|Approval Policy]]

### Verify / Converge

Requirement vs Specification vs Implementation vs Test vs Evidence를 비교한다.
Drift 검사 항목: Requirement Missing / Implementation Missing / Unexpected Code Change / Architecture Drift / Unapproved Change / Test Missing / Evidence Missing

## 측정 지표

```
Traceability Coverage  = Evidence가 연결된 Requirement / 전체 Active Requirement
Change Discipline      = CR이 존재하는 Requirement 변경 / 전체 Requirement 변경
Drift Rate             = Requirement 없는 구현 변경 / 전체 구현 변경
Verification Coverage  = PASS Evidence가 있는 Requirement / 구현 완료 Requirement
```

**이 지표들은 자동화가 필요해진 시점에 만든다.** 지금은 개념만 고정한다.

## 이 볼트에서의 적용 원칙

이 볼트는 과거에 "운영되지 않는 구조를 과잉 생성"하는 실패를 반복했다([인벤토리](https://github.com/<you>/vaultos/blob/main/docs/CASE-STUDY.md) 참고 — 4월에 만든 구조의 상당수가 2개월 내 방치됨).

따라서 AIPM-Trace는 **한 번에 전부 적용하지 않는다.**

1. 구조와 Governance를 먼저 고정한다 (지금 단계)
2. 실제 프로젝트 1개로 Intake → Requirement → Spec → Task → Verify → Evidence를 한 바퀴 돌린다
3. 그 한 바퀴에서 실제로 아쉬웠던 것만 추가한다

Traceability 검사, Drift 탐지, Event Log, Dashboard 자동화는 **필요해진 시점에** 만든다.
