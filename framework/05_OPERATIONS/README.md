# OPERATIONS

**사람이 보는 통제 화면이다.** 에이전트가 상태를 저장하는 곳이 아니라, 사람이 판단하기 위해 여는 곳이다.

```text
05_OPERATIONS/
├── dashboard/   오늘 무엇을 볼지
├── reviews/     승격·검토 판단
└── reports/     기록과 리포트
```

## dashboard/

| 문서 | 용도 |
|---|---|
| `00_dashboard.md` | 전체 허브. 오늘 프로젝트 중심인지 지식 중심인지 고른다 |
| `10_projects.md` | 활성 프로젝트 상태 |
| `20_knowledge.md` | Inbox / Fleeting 처리 대기 |

Dataview 쿼리로 자동 집계된다. 여기에 상태를 직접 쓰지 않는다.

## reviews/

| 문서 | 용도 |
|---|---|
| `promotion-board.md` | Permanent 승격 후보 |
| `promotion-rules.md` | 승격 판단 기준 |

승격 최종 결정은 사람이 한다. 에이전트는 후보만 제안한다.

## reports/worklog/

Daily / Weekly / Monthly / Yearly 작업 기록.

**현재 2026-04-21 이후 중단 상태다.** 실제 기록은 Daily 2건뿐이고 나머지는 빈 구조다.
되살릴지, `dashboard/`로 흡수할지, 폐기할지는 **아직 결정하지 않았다.** 결정 전까지 새 구조를 덧붙이지 않는다.

## 규칙

- 여기는 Projection Layer다. 정본이 아니다.
- 사람이 보지 않는 화면은 만들지 않는다. 대시보드를 늘리기 전에 기존 것을 실제로 여는지 확인한다.
