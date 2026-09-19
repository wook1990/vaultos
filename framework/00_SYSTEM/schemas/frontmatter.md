# VO Frontmatter Standard

모든 새 문서에 아래 공통 필드를 우선 적용한다.

## Common Fields

- `type`
- `project_key` 또는 해당 문서의 식별자
- `voSystem`
- `voLayer`
- `voKind`
- `voStage`
- `voSource`
- `voDomain`
- `voBridge`

## Defaults

- `voSystem: vaultos`
- `voLayer: inbox | fleeting | permanent | reference | project | system | governance | agent | operations | personal | archive`
- `voKind`: 문서 역할
- `voStage`: `capture | refine | distill | operate | sync | review | archive`
- `voSource`: `workspace | workspace_sync | manual | imported`
- `voDomain`: `project | knowledge | system | personal`
- `voBridge`: `none | promoted_from_project | referenced_by_project`

## voLayer와 폴더 대응

| voLayer | 폴더 |
|---|---|
| `system` | `00_SYSTEM/` |
| `governance` | `01_GOVERNANCE/` |
| `project` | `02_WORKSPACES/<scope>/projects/` |
| `inbox` | `03_KNOWLEDGE/00_inbox/` |
| `fleeting` | `03_KNOWLEDGE/10_fleeting/` |
| `permanent` | `03_KNOWLEDGE/20_permanent/` |
| `reference` | `03_KNOWLEDGE/references/` |
| `agent` | `04_AGENTS/` |
| `operations` | `05_OPERATIONS/` |
| `personal` | `98_PERSONAL/` |
| `archive` | `99_ARCHIVE/` |

2026-09-19 구조 이행 전의 `area`(구 `500_Areas`), `resource`(구 `600_Resources`), `qt`(구 `800_QT`) 값은 각각 `operations`, `reference`, `personal`로 대체되었다. 기존 문서의 구 값은 그대로 두고, 그 문서를 다시 열 때 갱신한다.

## Project Examples

- project home: `voLayer: project`, `voKind: project_home`
- workspace mirror: `voLayer: project`, `voKind: workspace_mirror`, `voStage: sync`
- permanent note: `voLayer: permanent`, `voKind: principle` 또는 `concept`

## Domain Rules

- ProjectOS 문서: `voDomain: project`
- KnowledgeOS 문서: `voDomain: knowledge`
- 시스템 문서: `voDomain: system`
- 개인 기록 문서: `voDomain: personal`

## Bridge Rules

- 기본값은 `voBridge: none`
- 프로젝트 산출물에서 영구 지식으로 승격된 노트는 `voBridge: promoted_from_project`
- 프로젝트 문서가 외부 지식 노트를 참조만 할 때는 `voBridge: referenced_by_project`

## 원칙

- 외부 시스템 접두사는 쓰지 않는다
- VaultOS 표준 메타데이터는 `vo*` 네임스페이스로 통일한다
