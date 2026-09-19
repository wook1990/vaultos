---
type: system
doc: context-loading
updated: 2026-09-19
---

# Context Loading

에이전트가 **프로젝트 전체를 한 번에 읽지 않게** 하는 규칙이다.

## 1. 왜 필요한가

전체 문서를 통째로 넣으면 다음이 발생한다.

- Token이 낭비된다
- 오래된 정보가 현재 정보와 함께 노출된다
- 관련 없는 컨텍스트가 판단을 흐린다
- 에이전트 집중도가 떨어지고 잘못된 추론이 늘어난다

## 2. Progressive Context Loading

필요한 것만 순서대로 가져온다.

```
project.yaml
     ↓
Current State
     ↓
Active Feature
     ↓
Related Requirements
     ↓
Relevant ADR / CR
     ↓
Required Code
```

**`project.yaml`을 먼저 읽고, 거기서 필요하다고 지목된 것만 다음 단계로 내려간다.**
지목되지 않은 문서는 열지 않는다.

## 3. context.md는 영구 저장소가 아니다

### 금지

`context.md`나 `project.md`에 정보를 **계속 덧붙이는 방식**은 쓰지 않는다.
시간이 지나면 비대해지고, 과거 의사결정과 현재 상태가 섞인다.

### 대신

```
Project State + Active Feature + Relevant Requirement + Relevant ADR + Open CR
        ↓
  Context Builder
        ↓
  context.generated.md
        ↓
      Agent
```

`context.generated.md`는 **이번 작업용 임시 컨텍스트**다. 작업이 끝나면 폐기할 수 있다.
영구 보관이 필요한 내용은 Requirement / ADR / CR / decision-log에 남긴다.

## 4. Context Budget

컨텍스트가 넘칠 때 무엇부터 지킬지에 대한 우선순위다.

| 우선순위 | 내용 |
|---|---|
| **P0** | System Rules (`00_SYSTEM/VAULTOS.md`, `01_GOVERNANCE/`) |
| **P1** | Project Constitution |
| **P2** | Current Project State |
| **P3** | Active Requirement / Feature |
| **P4** | Relevant Decision (ADR / CR) |
| **P5** | Relevant Knowledge (`03_KNOWLEDGE/`) |
| **P6** | Code |

**전체 문서를 무조건 넣지 않는다.** 낮은 우선순위부터 덜어낸다.

## 5. Index 분리

VaultOS 전체를 **하나의 RAG index로 만들지 않는다.**

| Index | 대상 |
|---|---|
| Knowledge Index | `03_KNOWLEDGE/` |
| Project Index | `02_WORKSPACES/` |
| Decision Index | ADR / CR / decision-log |
| Code Index | workspace repo |

에이전트는 목적에 따라 **필요한 index만** 검색한다.
검색·RAG는 주로 Knowledge Layer에 적용한다. 프로젝트 상태는 검색이 아니라 `project.yaml`을 통해 정확히 짚어서 읽는다.

## 6. Workspace 경계

`personal`과 `company` 컨텍스트를 **절대 자동으로 섞지 않는다.**

- 회사 자료를 개인 프로젝트의 RAG나 컨텍스트에 자동 포함하지 않는다
- 개인 자료를 회사 업무 에이전트에게 자동 제공하지 않는다

상세: [[01_GOVERNANCE/data-policy|Data Policy]]
