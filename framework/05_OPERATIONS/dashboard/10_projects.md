# Projects

프로젝트 운영 화면이다. 아래 표가 **전체 프로젝트를 한판에 보는 곳**이고, 그 아래는 개별 프로젝트를 다룰 때의 순서다.

## 전체 프로젝트 한판

> Dataview는 `.yaml`을 직접 읽지 못해서 이 표는 **손으로 유지한다.** 각 프로젝트의 `project.yaml`을 갱신할 때 이 표도 같이 고친다. 프로젝트가 많아져서 손으로 유지하기 번거로워지면(대략 10개 이상) 그때 `project.yaml`을 읽어 이 표를 생성하는 작은 스크립트를 만든다 — 처음부터 만들지 않는다.

| Project | Workspace | Phase | Blocked | Next Actions | Risks | Repo |
|---|---|---|---|---|---|---|
| _(새 프로젝트를 만들면 여기 한 줄 추가)_ | | | | | | |

## 오늘 순서 (개별 프로젝트를 다룰 때)

1. 프로젝트의 `project.yaml`을 연다 — **진입점이다. 전체 문서를 읽지 않는다**
2. `next_actions`와 `blocked`를 본다
3. 코드가 있으면 `repo.url`의 저장소에서 작업한다
4. 세션을 마칠 때 `project.yaml`(또는 `status/current-state.yaml`)과 **위 한판 표**를 같이 갱신한다

세션 경계에서만 쓴다. 연속 자동 반영은 하지 않는다. → [[01_GOVERNANCE/sync-policy|Sync Policy]]

## 새 프로젝트 시작

`00_SYSTEM/templates/project/project.yaml` 하나를 복사한다.

```
02_WORKSPACES/<personal|company>/projects/<slug>/project.yaml
```

프로필은 `personal-light`로 시작한다. 필요해지면 올린다. → [[01_GOVERNANCE/project-policy|Project Policy]]

**새 프로젝트를 만들면 위 한판 표에 한 줄 추가하는 걸 잊지 않는다.**

## 최근 프로젝트 문서

```dataview
TABLE file.folder AS "프로젝트", file.mtime AS "수정"
FROM "02_WORKSPACES"
SORT file.mtime DESC
LIMIT 15
```

## 참고

- [[01_GOVERNANCE/project-policy|Project Policy]] — 구조와 프로필
- [[01_GOVERNANCE/definition-of-done|Definition of Done]] — 무엇이 완료인가
- [[01_GOVERNANCE/approval-policy|Approval Policy]] — 사람 승인이 필요한 변경
- [[04_AGENTS/pm/README|PM Agent]] — tracker를 다루는 계약
