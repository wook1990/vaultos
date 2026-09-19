---
type: system_root
vaultos_version: 2.0.0
architecture_version: 2
governance_version: 1
updated: 2026-09-19
---

# VAULTOS

**모든 에이전트가 가장 먼저 읽는 문서다.**

## 1. VaultOS란 무엇인가

VaultOS는 문서를 저장하는 시스템이 아니다.
프로젝트의 의도를 보존하고, AI의 실행을 통제하며, 변경사항을 추적하고, 요구사항과 실제 구현의 일치 여부를 검증하는 **AI 프로젝트 운영체제(Control Plane)**다.

중심 연결 구조는 다음 하나다.

```
Intent → Goal → Requirement → Specification → Decision → Task → Implementation → Test → Evidence
```

모든 AI 작업은 이 체인 안에서 발생해야 한다.

## 2. VaultOS와 Repository의 역할 분담

```
VaultOS  = Control Plane   왜 그렇게 만들기로 했는가 (Intent / Requirement / CR / ADR / Approval / Evidence)
Repo     = Execution SSOT  실제로 무엇이 만들어졌는가 (Code / Test / tasks.yaml / 산출물)
```

**VaultOS는 코드의 정본이 아니라, 코드가 왜 그렇게 되었는지의 정본이다.**
코드가 있는 프로젝트는 실행 상태를 workspace repo에 두고, VaultOS는 그것을 가리킨다. 코드가 없는 프로젝트(문서·리서치·회사 업무)는 VaultOS 안이 곧 전부다.

## 3. 폴더 구조

```text
00_SYSTEM/        VaultOS 자체 정의, 규약, 스키마, 템플릿, 마이그레이션 기록
01_GOVERNANCE/    공통 통제 정책 — 프로젝트별로 복사하지 않고 참조한다
02_WORKSPACES/    personal/ 과 company/ 물리 분리
03_KNOWLEDGE/     재사용 지식 (프로젝트 상태와 분리)
04_AGENTS/        에이전트 역할 계약
05_OPERATIONS/    사람이 보는 통제 화면 (대시보드 / 리뷰 / 리포트)
98_PERSONAL/      업무와 무관한 개인 기록
99_ARCHIVE/       삭제하지 않고 내리는 곳
```

루트의 `CLAUDE.md` / `AGENTS.md` / `GEMINI.md`는 도구가 읽는 진입 포인터이며, 내용은 이 문서와 `01_GOVERNANCE/`를 가리킨다.

## 4. 8가지 핵심 원칙

| # | 원칙 | 뜻 |
|---|---|---|
| 1 | No Requirement, No Code | 모든 기능 변경은 Requirement / Bug / CR / ADR / Refactoring Task 중 하나와 연결된다 |
| 2 | No Architecture Change, No ADR | 구조적 변경은 반드시 결정 기록을 남긴다 |
| 3 | No Requirement Change, No CR | 승인된 요구사항을 바꾸려면 Change Request가 필요하다 |
| 4 | No Evidence, No Done | 구현만 끝난 상태는 Done이 아니다 |
| 5 | AI Executes, Human Governs | AI는 실행하고, 사람은 방향·우선순위·범위·주요 변경을 통제한다 |
| 6 | Repository = Single Source of Truth | 문서는 Drive, 코드는 git. → [[01_GOVERNANCE/sync-policy\|Sync Policy]] |
| 7 | Every Change Must Be Traceable | 모든 의미 있는 변경은 원인과 결과를 추적할 수 있어야 한다 |
| 8 | Current Truth ≠ History | 현재 상태와 과거 의사결정은 분리해서 보관한다 |

상세: [[01_GOVERNANCE/aipm-trace|AIPM-Trace]]

## 5. 에이전트 작업 규칙

### 시작할 때

1. 이 문서를 읽는다.
2. 작업 대상 워크스페이스를 확인한다 — `personal`인가 `company`인가.
3. 프로젝트 작업이면 그 프로젝트의 `project.yaml`을 읽는다. **전체 문서를 한 번에 읽지 않는다.**
4. 필요한 컨텍스트만 단계적으로 가져온다 → [[00_SYSTEM/context-loading|Context Loading]]

### 작업할 때

- 사용자의 요청을 먼저 분류한다 (Goal / Requirement / Feature / Bug / Change / Research / Refactoring / Operation). **분류 없이 바로 구현하지 않는다.**
- 승인이 필요한 변경인지 확인한다 → [[01_GOVERNANCE/approval-policy|Approval Policy]]
- 새 트래킹 표면이나 새 폴더를 임의로 만들지 않는다.

### 절대 하면 안 되는 것

1. Requirement를 암묵적으로 변경한다
2. Constitution을 임의 수정한다
3. Architecture 변경을 ADR 없이 수행한다
4. Scope를 조용히 확대한다
5. Requirement 없는 기능을 추가한다
6. Evidence 없이 Task를 Done 처리한다
7. 변경 이유를 삭제한다
8. 과거 결정과 현재 상태를 섞는다
9. **Personal과 Company 컨텍스트를 섞는다**
10. 실패한 작업을 성공으로 표시한다

전문: [[01_GOVERNANCE/agent-policy|Agent Policy]]

## 6. Governance Profile

프로젝트마다 통제 강도가 다르다. `project.yaml`의 `governance_profile`로 정한다.

| Profile | 대상 | 필수 |
|---|---|---|
| `personal-light` | 개인 실험 | Mission, Current State, Task |
| `personal-full` | 개인 프로덕션 | + Requirement, CR, Evidence |
| `company-standard` | 회사 내부 업무 | + ADR, Approval, Traceability, Risk |
| `company-strict` | 회사 핵심/민감 업무 | + Data Classification, Reviewer, Release Approval, Audit Log |

**개인 실험을 무겁게 만들지 않고, 회사 업무를 가볍게 만들지 않는다.**

## 7. 지금 어디서 시작하는가

- 오늘 운영 판단: [[05_OPERATIONS/dashboard/00_dashboard|Dashboard]]
- 프로젝트 작업: [[05_OPERATIONS/dashboard/10_projects|Project Dashboard]]
- 지식 정리: [[05_OPERATIONS/dashboard/20_knowledge|Knowledge Dashboard]]
- 규칙 확인: [[01_GOVERNANCE/README|Governance]]
- 새 문서 만들기: [[00_SYSTEM/conventions|Conventions]]

## 8. 이 구조의 이력

- 2026-09-19: 3-Zone 단순화 → [기록](https://github.com/wook1990/vaultos/blob/main/docs/CASE-STUDY.md)
- 2026-09-19: 전수 조사 → [기록](https://github.com/wook1990/vaultos/blob/main/docs/CASE-STUDY.md)
- 2026-09-19: AIPM-Trace 구조로 이행 → [기록](https://github.com/wook1990/vaultos/blob/main/docs/CASE-STUDY.md)

이전 세대 문서는 `99_ARCHIVE/legacy-vault/`에 동결 보관한다. **평소에는 열지 않는다.**
