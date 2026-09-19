---
type: governance
policy: index
status: active
updated: 2026-09-19
---

# Governance

공통 통제 정책이다. **프로젝트별로 복사하지 않고 참조한다.**
모든 프로젝트가 같은 규칙을 바라보기 때문에, 규칙을 바꾸면 여기 한 곳만 고친다.

## 정책 문서

| 문서 | 무엇을 정하는가 |
|---|---|
| [[01_GOVERNANCE/aipm-trace\|aipm-trace]] | 운영 방법론 전체 — 3개 Loop, 8가지 핵심 원칙, 표준 작업 흐름 |
| [[01_GOVERNANCE/project-policy\|project-policy]] | 프로젝트 구조, 3-Zone 모델, Governance Profile |
| [[01_GOVERNANCE/approval-policy\|approval-policy]] | 어떤 변경이 사람 승인을 요구하는가, 게이트에 걸렸을 때 에이전트의 행동 |
| [[01_GOVERNANCE/definition-of-done\|definition-of-done]] | 무엇이 Done인가, 실패 상태를 어떻게 기록하는가 |
| [[01_GOVERNANCE/data-policy\|data-policy]] | Project/Knowledge 경계, Personal/Company 경계, Data Classification, Secret 관리 |
| [[01_GOVERNANCE/agent-policy\|agent-policy]] | 에이전트 공통 계약, 절대 금지 12항, 세션 경계 sync 규칙 |
| [[01_GOVERNANCE/knowledge-policy\|knowledge-policy]] | 지식 수집·정제·승격 규칙, AI Curation/Caution 라우팅 |
| [[01_GOVERNANCE/ecosystem\|ecosystem]] | 볼트와 저장소를 잇는 양방향 표식, 볼트 탐색 순서, 상태 흐름 방향 |
| [[01_GOVERNANCE/sync-policy\|sync-policy]] | 정본 계층(Drive vs git), Drive 충돌 방지 규칙, 백업·롤백 |
| [[01_GOVERNANCE/vaultos-health\|vaultos-health]] | 볼트 자체의 유지보수 리듬, lint 항목, 재발 경보 |

## 규칙이 아니라 구조를 찾는다면

- 폴더 구조·명명·스키마·템플릿: [[00_SYSTEM/VAULTOS|00_SYSTEM]]
- 에이전트 역할별 계약: [[04_AGENTS/README|04_AGENTS]]
- 사람이 보는 화면: [[05_OPERATIONS/dashboard/00_dashboard|05_OPERATIONS]]

## 읽는 순서

처음이면 [[01_GOVERNANCE/aipm-trace|aipm-trace]] 하나만 읽으면 된다.
실제로 프로젝트를 건드릴 때 [[01_GOVERNANCE/project-policy|project-policy]]와 [[01_GOVERNANCE/approval-policy|approval-policy]]를 본다.
나머지는 해당 상황이 왔을 때 연다.
