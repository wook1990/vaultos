---
type: governance
policy: agent
status: active
updated: 2026-09-19
---

# Agent Policy

Codex, Claude, Gemini를 포함한 **모든 에이전트가 공통으로 따르는 계약**이다.
루트의 `CLAUDE.md` / `AGENTS.md` / `GEMINI.md`는 이 문서를 가리키는 포인터일 뿐, 내용을 따로 유지하지 않는다.

## 1. Multi-Model 원칙

**역할 중심으로 운영하고, 특정 모델 이름에 구조를 종속시키지 않는다. 모델은 교체 가능해야 한다.**

```
Research Model              → 외부 조사, 근거 수집
Analysis / Architecture     → Requirement, Architecture, Planning
Coding Model                → Implementation, Test, Refactoring
Independent Reviewer        → Traceability, Verification, Drift Detection
Human                       → Approval, Direction, Priority
```

같은 역할을 어떤 모델이 맡든 **읽고 쓰는 스키마는 동일하다.** 실행 환경(harness)만 다르다.

### 현재 에이전트별 강점 (역할 배분 기준, 우열 아님)

| 에이전트 | 강점 |
|---|---|
| Claude | 깊은 소스 정독, 논증 구조 재구성, caution 검토, 과잉주장·숨은 전제·근거 경계 탐지, 문장 다듬기 |
| Gemini | 긴 문맥 소스 정독, 다중 소스 비교, source map 작성, 최신성·일관성 확인, 단일 소스 과일반화 탐지 |
| Codex | 실행(코드/워크스페이스), tracker 갱신, 구현·구조 작업 |

이 표는 참고값이다. 모델이 바뀌면 이 표만 갱신하고 나머지 구조는 그대로 둔다.

## 2. AI가 절대 하면 안 되는 것

```
 1. Requirement를 암묵적으로 변경한다
 2. Constitution을 임의 수정한다
 3. Architecture 변경을 ADR 없이 수행한다
 4. Scope를 조용히 확대한다
 5. Requirement 없는 기능을 추가한다
 6. Evidence 없이 Task를 Done 처리한다
 7. 기존 문서를 무조건 최신 내용으로 덮어쓴다
 8. 변경 이유를 삭제한다
 9. Historical Decision과 Current State를 혼합한다
10. Personal / Company Context를 암묵적으로 혼합한다
11. 민감한 회사 정보를 외부 Context에 자동 포함한다
12. 실패한 작업을 성공으로 표시한다
```

7번이 특히 자주 깨진다. **문서를 갱신할 때 왜 그렇게 되어 있었는지를 먼저 확인한다.**

## 3. 공통 기본 행동

- 소스를 읽고 나서 주장한다.
- 요청을 먼저 분류한다 (Goal / Requirement / Feature / Bug / Change / Research / Refactoring / Operation). **분류 없이 바로 구현하지 않는다.**
- 승인이 필요한 변경인지 확인한다. → [[01_GOVERNANCE/approval-policy|Approval Policy]]
- 새 트래킹 표면이나 새 폴더를 임의로 만들지 않는다.
- 불확실하면 추정하지 않고 `status: inferred` / `confidence: low`로 표시한다.
- 작업 결과가 실패·부분 성공이면 그대로 기록한다. → [[01_GOVERNANCE/definition-of-done|Definition of Done]]

## 4. KnowledgeOS 작업 계약

Inbox/References 소스를 분석하거나, 큐레이션 노트를 만들거나, dynamic persona를 실행할 때:

- Primary contract: `04_AGENTS/curation/01_AI_Curation_Caution_Agent.md`
- Routing rules: [[01_GOVERNANCE/knowledge-policy|Knowledge Policy]]
- Prompt: `04_AGENTS/curation/01_Dynamic_Persona_Curation_Prompt.md`
- Template: `00_SYSTEM/templates/14_AI_Curation_Caution_Note.md`

행동 규칙:

- Curation/Caution Fleeting Note는 `03_KNOWLEDGE/10_fleeting`에 만든다.
- dynamic persona는 role contract로 쓰고, 어투 모사로 쓰지 않는다.
- curation과 caution을 분리한다.
- Permanent Note 승격은 **제안만** 하고, 사용자가 승인하기 전에는 만들거나 승격하지 않는다.
- 명시적 지시 없이 프로젝트 문서를 KnowledgeOS로 옮기지 않는다.

## 5. 세션 경계 Sync 규칙

프로젝트 상태를 vault에 반영할 때 **세션 경계에서만** 움직인다.

| 명령 | 시점 | 하는 일 |
|---|---|---|
| `resume` | 세션 시작 시 1회 | workspace tracker(Zone A)를 읽고 정렬한다 |
| `sync` | 세션 종료 시 1회 | vault 쪽 상태 문서를 갱신한다 |
| `bootstrap` | drift 발생 시에만 | project surface를 재정렬한다 |

### 폐지: 연속 자동 반영(`watch`)

**Google Drive 동기화 환경에서 여러 기기·여러 에이전트가 동시에 작은 파일을 자주 건드리는 것이 충돌의 구조적 원인이었다.** 실제 충돌 파일이 발견되어 폐지했다.

- 세션 시작·종료 외에는 vault 파일을 자동으로 건드리지 않는다.
- 하위 명령(`sync:vault`, `sync:workspace-agents`)은 상태 문서 갱신 하나로 통합되어 더 이상 필요하지 않다.
- vault 쪽 상태 문서는 정본이 아니므로, 유실되거나 충돌해도 Zone A에서 다시 생성하면 된다.

배경: [Zone Simplification](https://github.com/<you>/vaultos/blob/main/docs/CASE-STUDY.md)

## 6. 프로젝트 작업 시

프로젝트 구조와 Governance Profile은 [[01_GOVERNANCE/project-policy|Project Policy]]를 따른다.
프로젝트별 진입 문서는 각 프로젝트의 `60_Links/11_LLM_Brief.md`다.
