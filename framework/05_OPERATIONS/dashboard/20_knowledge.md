# Knowledge

지식 파이프라인 화면이다.

```
references(raw) → 00_inbox(triage) → 10_fleeting(정제) → 20_permanent(장기)
```

규칙: [[01_GOVERNANCE/knowledge-policy|Knowledge Policy]]

## Inbox — 오늘 볼 것

```dataview
TABLE file.mtime AS "수집"
FROM "03_KNOWLEDGE/00_inbox"
SORT file.mtime DESC
LIMIT 15
```

**Inbox는 무한 저장소가 아니다.** 쌓이면 `references`로 내리거나 버린다.

## 정제 중

```dataview
TABLE file.folder AS "분류", file.mtime AS "수정"
FROM "03_KNOWLEDGE/10_fleeting"
SORT file.mtime DESC
LIMIT 15
```

## 최근 승격된 지식

```dataview
TABLE file.mtime AS "수정"
FROM "03_KNOWLEDGE/20_permanent"
SORT file.mtime DESC
LIMIT 10
```

## 승격 판단

[[05_OPERATIONS/reviews/promotion-board|Promotion Board]]에서 한다.

판단 기준:
- 다음 프로젝트에서도 다시 쓸 수 있는가
- 특정 프로젝트 맥락 없이도 읽을 가치가 있는가
- 원칙·프레임워크·판단 기준으로 남길 수 있는가
