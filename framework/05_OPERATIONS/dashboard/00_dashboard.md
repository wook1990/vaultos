# Dashboard

오늘 무엇을 볼지 여기서 고른다. Dataview 플러그인이 있으면 아래 표가 자동으로 채워진다.

## 오늘 할 일

1. 프로젝트 중심인가, 지식 정리 중심인가 고른다
2. 해당 대시보드로 간다

- [[05_OPERATIONS/dashboard/10_projects|Projects]]
- [[05_OPERATIONS/dashboard/20_knowledge|Knowledge]]
- [[05_OPERATIONS/reviews/promotion-board|Promotion Board]] — 승격 판단 대기열

## 활성 프로젝트

```dataviewjs
const rows = [];
for (const p of dv.pages()) {
  if (!p.file.path.includes("/projects/")) continue;
  if (p.file.name !== "project") continue;
  rows.push([p.file.link, p.status?.phase ?? "-", (p.next_actions ?? []).length]);
}
dv.table(["프로젝트", "phase", "다음 할 일"], rows);
```

> `project.yaml`은 Dataview가 읽지 못한다. 프로젝트 수가 늘면 각 프로젝트에
> `01_Project_Home.md` 같은 인덱스 노트를 두거나, 이 블록을 지우고 폴더를 직접 연다.
> **대시보드가 안 돌아간다고 시스템이 멈추지는 않는다.**

## 최근 지식 활동

```dataview
TABLE file.mtime AS "수정"
FROM "03_KNOWLEDGE/00_inbox" OR "03_KNOWLEDGE/10_fleeting"
SORT file.mtime DESC
LIMIT 10
```

## 주간 점검

- [ ] 구조 검사 실행 (`tools/vaultos_health.py`)
- [ ] 충돌 사본 확인 (`find . -iname "*conflict*"`)
- [ ] Inbox 비우기
- [ ] 승격 후보 하나 판단
- [ ] 프로젝트 폴더 파일 수가 늘고 있지 않은지 확인

기준: [[01_GOVERNANCE/vaultos-health|VaultOS Health]]
