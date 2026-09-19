---
type: governance
policy: data
status: active
updated: 2026-09-19
---

# Data Policy

무엇을 어디에 두는가, 그리고 **무엇을 섞으면 안 되는가**를 정한다.

## 1. Project Work vs Knowledge Work

용어는 [[01_GOVERNANCE/project-policy|Project Policy]]의 3-Zone 모델을 따른다.

```
Project Work  = Zone A (workspace repo tracker) + Zone B (02_WORKSPACES/<scope>/projects/)
Knowledge Work = Zone C (03_KNOWLEDGE/)
```

### Zone A + B에 두는 것

- 현재 프로젝트를 진행하기 위한 문서
- tracker, status, decision, issue, risk
- phase artifact와 final deliverable
- workspace 연결 문서

### Zone C에 두는 것

- 새 입력과 수집물 → `03_KNOWLEDGE/00_inbox`
- 초안, 요약, 비교, 임시 정리 → `03_KNOWLEDGE/10_fleeting`
- 장기 재사용 지식 → `03_KNOWLEDGE/20_permanent`
- 참조 자료 → `03_KNOWLEDGE/references`

### 실전 판단

- 지금 하는 일이 현재 프로젝트를 끝내기 위한 것인가 → **Project**
- 지금 남기는 내용이 앞으로도 다시 쓸 지식인가 → **Knowledge**
- 아직 판단 전인가 → `00_inbox` 또는 `10_fleeting`

### 지식으로 승격하는 기준

- 프로젝트를 넘어 반복 재사용 가능한 개념
- 승인된 원칙, 체크리스트, 판단 기준
- 다른 프로젝트에도 그대로 참고할 가치가 있는 내용

## 2. Project ↔ Knowledge 연결

- project artifact는 **사람이 검토한 뒤에만** permanent 후보가 된다.
- knowledge note는 project에 **참조 링크로만** 연결한다.
- Permanent Note가 어떤 프로젝트에서 재사용되면 그 Note의 frontmatter에 프로젝트를 추가한다.

```yaml
applies_to_projects: [my-new-app, data-pipeline]
```

- 프로젝트 문서는 재사용 가능한 개념을 새로 쓰지 않고 그 Permanent Note를 위키링크로 참조한다.
- **이 이상의 Bridge 인프라(전용 계약 문서, 전용 폴더)는 만들지 않는다.** [[05_OPERATIONS/reviews/promotion-board|Promotion Board]]로 충분하다.

## 3. Personal / Company 경계

**가장 중요한 경계다. 물리적으로 분리한다.**

```text
02_WORKSPACES/
├── personal/projects/     개인 프로젝트
└── company/projects/      회사 업무
```

### 금지

- 회사 자료를 개인 프로젝트의 RAG 또는 Context에 **자동으로 포함하지 않는다.**
- 개인 자료를 회사 업무 Agent에게 **자동으로 제공하지 않는다.**
- 두 워크스페이스의 문서를 하나의 Context Window에 함께 넣지 않는다. 필요하면 사람이 명시적으로 지시한다.
- 회사 Confidential / Restricted 데이터를 외부로 전송하지 않는다. 전송은 승인 항목이다. → [[01_GOVERNANCE/approval-policy|Approval Policy]]

### 에이전트가 작업 시작 시 확인할 것

1. 이 작업은 `personal`인가 `company`인가
2. 참조하려는 문서가 같은 워크스페이스에 있는가
3. 아니라면 사람에게 명시적으로 묻는다

`98_PERSONAL/`(업무와 무관한 개인 기록)은 어느 워크스페이스에도 자동으로 제공하지 않는다.

## 4. Data Classification

회사 영역은 최소 다음 분류를 가진다.

| 등급 | 의미 |
|---|---|
| `PUBLIC` | 외부 공개 가능 |
| `INTERNAL` | 사내 사용 |
| `CONFIDENTIAL` | 제한된 팀 |
| `RESTRICTED` | 매우 민감한 자료 |

문서 frontmatter에 남긴다.

```yaml
classification: INTERNAL
workspace: company
project: generator-health
```

- 분류가 없는 company 문서는 기본 `INTERNAL`로 취급한다.
- `CONFIDENTIAL` 이상은 외부 도구·외부 모델에 전달하기 전에 승인을 받는다.
- `personal` 워크스페이스는 분류를 요구하지 않는다. 필요하면 붙일 수 있다.

## 5. Secret 관리

다음은 **VaultOS 문서에 직접 저장하지 않는다.**

```
API Key / Password / Private Token / Secret Key / Credential
```

대신 Secret Manager 또는 환경변수를 쓰고, 문서에는 **참조만** 남긴다.

```
OPENAI_API_KEY  → ENV
DB_PASSWORD     → Secret Manager
```

경로 참조(`.codex/vault-sync.env` 같은 파일 위치)는 허용한다. 값 자체를 적는 것이 금지다.

> 2026-09-19 전수 스캔 결과, 이 볼트에는 실제 API 키·토큰·자격증명 문자열이 **발견되지 않았다.** 환경변수 참조 경로만 기록돼 있어 현재는 허용 범위다. 기록: [Inventory](https://github.com/<you>/vaultos/blob/main/docs/CASE-STUDY.md)

## 6. 금지 요약

- 프로젝트 output을 permanent note처럼 바로 취급하는 것
- 생성 주체(AI/사람)로 output 폴더를 나누는 것
- Personal과 Company 컨텍스트를 암묵적으로 섞는 것
- Secret 값을 문서에 직접 쓰는 것
