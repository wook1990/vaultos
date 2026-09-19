# Projects

프로젝트 운영 화면이다.

## 오늘 순서

1. 프로젝트의 `project.yaml`을 연다 — **진입점이다. 전체 문서를 읽지 않는다**
2. `next_actions`와 `blocked`를 본다
3. 코드가 있으면 `repo.url`의 저장소에서 작업한다
4. 세션을 마칠 때 `project.yaml`(또는 `status/current-state.yaml`)을 한 번 갱신한다

세션 경계에서만 쓴다. 연속 자동 반영은 하지 않는다. → [[01_GOVERNANCE/sync-policy|Sync Policy]]

## 새 프로젝트 시작

`00_SYSTEM/templates/project/project.yaml` 하나를 복사한다.

```
02_WORKSPACES/<personal|company>/projects/<slug>/project.yaml
```

프로필은 `personal-light`로 시작한다. 필요해지면 올린다. → [[01_GOVERNANCE/project-policy|Project Policy]]

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
