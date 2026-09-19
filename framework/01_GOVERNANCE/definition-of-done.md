---
type: governance
policy: definition-of-done
status: active
updated: 2026-09-19
---

# Definition of Done

## 기존 정의

```
Code Complete  →  Done
```

이 정의의 문제는 "동작하는 것"과 "요구한 것을 충족한 것"을 구분하지 못한다는 점이다.

## VaultOS 정의

```
Requirement Defined
+ Implementation Complete
+ Acceptance Criteria Passed
+ Test Evidence Exists
+ Traceability Complete
+ No Unauthorized Drift
= DONE
```

**No Evidence, No Done.** 구현만 끝난 상태는 Done이 아니다.

| 조건 | 확인 방법 |
|---|---|
| Requirement Defined | 이 작업이 어떤 REQ / Bug / CR / ADR에서 왔는가 |
| Implementation Complete | 코드·문서가 실제로 존재하는가 |
| Acceptance Criteria Passed | Spec의 AC 항목이 전부 통과했는가 |
| Test Evidence Exists | 통과를 증명할 파일이 있는가 (테스트 결과, 스크린샷, 로그) |
| Traceability Complete | REQ → Task → PR → Test → Evidence 연결이 끊기지 않았는가 |
| No Unauthorized Drift | 승인 없이 바뀐 것이 있는가 |

## 실패 상태

작업이 끝나지 않았을 때 **완료로 표시하지 않는다.** 아래 중 하나로 남긴다.

| 상태 | 뜻 | 다음에 필요한 것 |
|---|---|---|
| `FAILED` | 시도했고 실패했다 | 원인 기록, 재시도 또는 방향 전환 |
| `PARTIAL` | 일부만 되었다 | 무엇이 남았는지 명시 |
| `BLOCKED` | 외부 의존으로 막혔다 | 무엇을 기다리는지 명시 |
| `NEEDS_APPROVAL` | 승인 게이트에 걸렸다 | → [[01_GOVERNANCE/approval-policy\|Approval Policy]] |
| `NEEDS_RESEARCH` | 판단할 정보가 부족하다 | 어떤 질문에 답해야 하는지 명시 |

**실패를 성공으로 표시하는 것은 금지 항목이다.** → [[01_GOVERNANCE/agent-policy|Agent Policy]]

## Governance Profile별 적용

| Profile | 필수 조건 |
|---|---|
| `personal-light` | Implementation Complete + 무엇을 확인했는지 한 줄 |
| `personal-full` | + Acceptance Criteria, Test Evidence |
| `company-standard` | 전체 6개 조건 |
| `company-strict` | 전체 + Reviewer 승인 + Evidence 보관 |

## Release Gate

Release는 개별 Task의 Done과 다르다. 아래를 전부 확인한다.

- Critical Requirements Verified
- No High Risk Open Issue
- No Unauthorized Drift
- Required CR / ADR Approved
- Tests Passed
- Evidence Collected
- Rollback Plan Exists
