---
type: governance
policy: approval
status: active
updated: 2026-09-19
---

# Approval Policy

**AI Executes, Human Governs.**
AI는 실행하고, 사람은 방향·우선순위·범위·주요 변경을 통제한다. 이 문서는 그 경계를 정한다.

## 1. Human Approval이 필요한 변경

아래 중 하나라도 해당하면 **에이전트는 실행하지 않고 멈춘다.**

| # | 변경 |
|---|---|
| 1 | Project Mission 변경 |
| 2 | Scope 변경 |
| 3 | Requirement 삭제 |
| 4 | 핵심 Requirement 수정 |
| 5 | Architecture 변경 |
| 6 | Data Model 변경 |
| 7 | External Interface 변경 |
| 8 | Security 정책 변경 |
| 9 | 개인정보 처리 방식 변경 |
| 10 | 비용 구조 변경 |
| 11 | 일정에 큰 영향을 미치는 변경 |
| 12 | 회사 Confidential / Restricted 데이터의 외부 전송 |
| 13 | Release 승인 |

## 2. 게이트에 걸렸을 때 에이전트가 하는 일

순서를 지킨다. **"일단 해보고 나중에 물어본다"는 금지다.**

1. **멈춘다.** 구현·수정·삭제를 시작하지 않는다.
2. **Impact Analysis를 출력한다.**
   ```
   Affected Requirements / Components / APIs / Data / Tests
   Risks
   Why this needs approval  (위 표의 몇 번인지)
   ```
3. **선택지를 제시하고 묻는다.** 승인 없이 진행할 수 있는 축소 범위가 있다면 같이 제안한다.
4. 승인을 받으면 근거를 남긴다 — `changes/CR-xxx.md` 또는 `status/decision-log.md`.
5. 승인을 못 받으면 상태를 `NEEDS_APPROVAL`로 남긴다. → [[01_GOVERNANCE/definition-of-done|Definition of Done]]

## 3. 최소 Human Review 화면

사람이 모든 코드를 검토하는 것은 불가능하다. 검토 대상을 다음으로 제한한다.

- Mission / Scope / Requirement / Architecture
- High Risk Change / Major CR / Release
- Convergence Report

저수준 구현은 AI Review와 Test에 맡긴다.

에이전트가 사람에게 올리는 보고는 **이 7개 질문에 답할 수 있으면 충분하다.**

```
1. WHAT CHANGED?          무엇이 바뀌었는가
2. WHY?                   왜 바꿨는가
3. WHAT IS AFFECTED?      무엇에 영향을 주는가
4. IS APPROVAL REQUIRED?  승인이 필요한가
5. WHAT WAS IMPLEMENTED?  무엇이 구현되었는가
6. WHAT WAS VERIFIED?     무엇이 검증되었는가
7. WHAT REMAINS OPEN?     무엇이 남아있는가
```

7번을 비워두지 않는다. 남은 것이 없으면 "없음"이라고 쓴다.

## 4. Governance Profile별 적용

| Profile | 승인 게이트 |
|---|---|
| `personal-light` | **형식 승인 생략 가능.** 단 위 표 1·2·5번(Mission / Scope / Architecture)은 사람에게 알린다 |
| `personal-full` | Requirement·Architecture 변경은 승인 필요 |
| `company-standard` | **전체 적용.** 생략 불가 |
| `company-strict` | 전체 적용 + Reviewer 지정 + Release Approval 별도 |

개인 실험에서 형식 승인을 강제하면 아무도 쓰지 않는다. 회사 업무에서 생략하면 통제가 사라진다.
**프로필로 분기하는 것이 이 정책의 핵심이다.**

## 5. 승인 없이 진행해도 되는 것

명시적으로 허용한다. 이것까지 물으면 시스템이 마비된다.

- 오타 수정, 포맷팅, 주석
- 기존 Requirement 범위 안의 구현
- 테스트 추가
- 로컬 리팩토링 (외부 인터페이스 불변)
- 문서 갱신 (Constitution 제외)
