---
type: schema
schema: change-request
status: active
updated: 2026-09-19
---

# Change Request (CR) Schema

## 규칙

**No Requirement Change, No CR — 승인된 Requirement를 변경하려면 Change Request가 필요하다.**

AI는 Requirement를 암묵적으로 바꿀 수 없다. 구현 중에 요구사항이 현실과 맞지 않는 것을 발견하면, 요구사항을 고치는 것이 아니라 **CR을 제안하고 멈춘다.**

## ID 체계

```
CR-<NNN>            프로젝트 전역 연번
CR-<DOMAIN>-<NNN>   도메인이 많은 프로젝트에서
```

저장 위치: `changes/CR-023.md`

## 구조

```yaml
id: CR-023

request:
  로그인 방식을 Email → Google OAuth로 변경

reason:
  가입 friction 감소

affected_requirements:
  - REQ-AUTH-001

affected_architecture:
  - AUTH-SERVICE

affected_features:
  - F-LOGIN

risks:
  - 기존 사용자 migration
  - OAuth 장애 대응

decision:
  approved

approved_by:
  HUMAN
```

## 필드 규칙

| 필드 | 규칙 |
|---|---|
| `request` | 무엇을 바꾸자는 것인가. 한 문장 |
| `reason` | 왜 바꾸는가. 이게 없으면 나중에 되돌릴지 판단할 수 없다 |
| `affected_requirements` | 영향받는 REQ ID. **비어 있으면 CR이 아니라 그냥 Task다** |
| `affected_architecture` | 구조 변경이 포함되면 [[00_SYSTEM/schemas/adr\|ADR]]도 같이 필요하다 |
| `affected_features` | 영향받는 Feature |
| `risks` | 이 변경으로 생기는 위험. 빈 상태로 승인하지 않는다 |
| `decision` | `proposed` / `approved` / `rejected` / `deferred` |
| `approved_by` | 승인 주체. **AI는 여기에 올 수 없다** |

## 흐름

```
발견 (구현 중 / 리뷰 중 / 요청)
 ↓
CR 작성 — proposed
 ↓
Impact Analysis
 ↓
Approval Gate  →  rejected / deferred 이면 여기서 끝
 ↓
approved
 ↓
Requirement 갱신 (ID는 유지, 내용 변경)
 ↓
Baseline 반영
```

## 금지

- AI가 `decision: approved`를 스스로 쓰는 것
- `reason` 없이 변경하는 것
- `risks`를 비워둔 채 승인하는 것
- CR 없이 `approved` 상태 Requirement를 수정하는 것
- 거부된 CR을 삭제하는 것 → `99_ARCHIVE`가 아니라 `changes/`에 `rejected`로 남긴다. **거부 이력도 기록이다**

## Governance Profile별 적용

| Profile | CR |
|---|---|
| `personal-light` | 불필요 |
| `personal-full` | 필요 |
| `company-standard` 이상 | 필수 + Approval 기록 |

승인 대상 판단은 [[01_GOVERNANCE/approval-policy|Approval Policy]]를 따른다.
