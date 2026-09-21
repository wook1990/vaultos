# Dashboard

오늘 무엇을 볼지 여기서 고른다. Dataview 플러그인이 있으면 아래 표가 자동으로 채워진다.

## 오늘 할 일

1. 프로젝트 중심인가, 지식 정리 중심인가 고른다
2. 해당 대시보드로 간다

- [[05_OPERATIONS/dashboard/10_projects|Projects]]
- [[05_OPERATIONS/dashboard/20_knowledge|Knowledge]]
- [[05_OPERATIONS/dashboard/30_products|Products]] — 배포된 제품·운영 중인 자동화
- [[05_OPERATIONS/dashboard/40_devices|Devices]] — 지금 뭐가 어디서 돌고 있는가
- [[05_OPERATIONS/reviews/promotion-board|Promotion Board]] — 승격 판단 대기열

## 활성 프로젝트

`project.yaml`은 Dataview가 읽지 못해서 여기 자동 표는 없다. 전체 목록은 [[05_OPERATIONS/dashboard/10_projects|Projects Dashboard]]의 손으로 유지하는 한판 표를 본다.

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
