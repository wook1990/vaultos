---
type: weekly_worklog
week: {{date:gggg-[W]ww}}
---

# {{date:gggg-[W]ww}} Weekly Worklog

## Quick Links

- [[05_OPERATIONS/dashboard/00_dashboard|Dashboard]]
- [[05_OPERATIONS/dashboard/10_projects|Project Dashboard]]
- [[05_OPERATIONS/dashboard/20_knowledge|Knowledge Dashboard]]
- [[05_OPERATIONS/reviews/promotion-board|Promotion Board]]

## Daily Logs This Week

```dataview
TABLE file.link AS "Daily Log"
FROM "05_OPERATIONS/reports/worklog/10_Daily"
WHERE week = this.week
SORT file.name ASC
```

## 이번 주 한 일 요약
- 
- 

## 프로젝트 작업 요약
### 프로젝트명
- 이번 주 진전:
- 완료한 task:
- 남은 task:
- 핵심 문서/산출물:

## 연구 / 학습 요약
- 연구:
- 학습:
- 다음 주에 이어갈 주제:

## 지식 정리 요약
- 처리한 Inbox:
- 생성한 Fleeting:
- 승격한 Permanent:
- 연결된 프로젝트:

## 이번 주 주요 산출물
- 
- 

## 이번 주 주요 결정 / blocker
- decision:
- blocker:

## 다음 주 우선순위
- 
- 
