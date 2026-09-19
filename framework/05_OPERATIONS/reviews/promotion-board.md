# Promotion Board

승격 여부를 판단할 후보만 모아 보는 곳이다. **판단은 사람이 한다.**

## 먼저 볼 기준

- 지금 `20_permanent`로 올릴 수 있는가
- 아직 더 다듬어야 하는가
- 특정 프로젝트 안에만 남겨야 하는가

## 정제 중인 노트

```dataview
TABLE file.mtime AS "수정"
FROM "03_KNOWLEDGE/10_fleeting"
SORT file.mtime DESC
LIMIT 20
```

## 최근 승격된 것

```dataview
TABLE file.mtime AS "수정"
FROM "03_KNOWLEDGE/20_permanent"
SORT file.mtime DESC
LIMIT 10
```

## 프로젝트에서 넘어올 후보

```dataview
TABLE file.folder AS "프로젝트", file.mtime AS "수정"
FROM "02_WORKSPACES"
WHERE contains(file.path, "/evidence/") OR contains(file.path, "/architecture/")
SORT file.mtime DESC
LIMIT 10
```

## 규칙

- project artifact는 **사람이 검토한 뒤에만** permanent 후보가 된다
- 승격된 지식이 어떤 프로젝트에서 재사용되면 `applies_to_projects`에 기록한다
- 에이전트는 **제안만 한다.** 최종 승격은 사람이 확정한다

→ [[01_GOVERNANCE/knowledge-policy|Knowledge Policy]] / [[01_GOVERNANCE/data-policy|Data Policy]]
