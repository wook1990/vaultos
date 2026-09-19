---
type: agent_index
status: active
updated: 2026-09-19
---

# Agents

에이전트 역할 계약을 모아두는 곳이다. 각 계약은 **무엇을 책임지고, 무엇을 하면 안 되며, 언제 사람에게 넘기는지**를 정한다.

## 역할 구성

| Agent | 역할 | 계약 |
|---|---|---|
| Orchestrator | 전체 흐름 제어. 분류 → 영향분석 → 승인 판단 → 위임 | [[04_AGENTS/orchestrator/README\|계약]] |
| Research | 외부 조사 / 근거 수집 | 미정의 (필요해질 때 작성) |
| Product | Goal / Requirement 정의 | 미정의 |
| Architect | Architecture / ADR | 미정의 |
| PM | Scope / Task / Risk / CR — **tracker 쓰기 전담** | [[04_AGENTS/pm/README\|계약]] |
| Developer | 구현 / 단위 테스트 / 리팩터링 | [[04_AGENTS/developer/README\|계약]] |
| QA | Test / Acceptance 검증 | 미정의 |
| Auditor | Traceability / Drift 검사 | [[04_AGENTS/auditor/README\|계약]] |
| Curation | KnowledgeOS 소스 분석 / 전문 큐레이션 | [[04_AGENTS/curation/01_AI_Curation_Caution_Agent\|계약]] |
| **Human** | 방향 / Scope / 우선순위 / 승인 | — |

**미정의 역할은 지금 만들지 않는다.** 실제로 그 역할이 필요해진 시점에 계약을 작성한다. 이 볼트는 쓰지 않는 구조를 미리 만들어 방치한 이력이 있다([인벤토리](https://github.com/<you>/vaultos/blob/main/docs/CASE-STUDY.md) 참고).

## Multi-Model 원칙

**역할 중심으로 운영하고, 특정 모델 이름에 구조를 종속시키지 않는다. 모델은 교체 가능해야 한다.**

| 역할 축 | 담당 작업 |
|---|---|
| Research Model | 조사 |
| Analysis / Architecture Model | Requirement, Architecture, Planning |
| Coding Model | Implementation, Test, Refactoring |
| Independent Reviewer | Traceability, Verification, Drift Detection |
| Human | Approval, Direction, Priority |

같은 모델이 여러 역할을 맡아도 되지만, **검증 역할과 구현 역할은 가능하면 분리한다.** 자기가 짠 것을 자기가 검증하면 Drift를 놓친다.

## 계약이 정의해야 하는 것

모든 agent 계약은 다음을 명시한다.

- Identity — 누구인가
- Responsibility — 무엇을 책임지는가
- Allowed Actions — 무엇을 할 수 있는가
- Forbidden Actions — 무엇을 하면 안 되는가
- Required Inputs — 시작 전 무엇을 읽어야 하는가
- Required Outputs — 무엇을 남겨야 하는가
- Escalation Conditions — 언제 멈추고 사람에게 넘기는가

## 기존 계약

`04_AGENTS/curation/`에 이미 운영 중인 계약이 있다.

- [[04_AGENTS/curation/01_AI_Curation_Caution_Agent|AI Curation/Caution Agent]] — KnowledgeOS 소스 분석 공용 계약
- [[04_AGENTS/curation/01_Dynamic_Persona_Curation_Prompt|Dynamic Persona Curation Prompt]] — 복사해서 쓰는 실행 프롬프트

## 공통 상위 규칙

모든 에이전트는 [[00_SYSTEM/VAULTOS|VAULTOS]]와 [[01_GOVERNANCE/agent-policy|Agent Policy]]를 먼저 따른다. 개별 계약은 그 위에 얹는 것이지, 그것을 덮어쓰지 않는다.
