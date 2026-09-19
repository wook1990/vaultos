---
type: governance
policy: grill-gate
status: active
updated: 2026-09-19
---

# Grill Gate — 만들기 전에 캐묻는다

## 1. 두 가지 원칙

1. **"이 프로젝트 만들어줘"로 바로 시작하지 않는다.** 먼저 소스 자료를 모으고, 그것을 근거로 캐묻는다.
2. **소스 자료가 있으면 맨 아이디어에서 시작하지 않는다.** 기존 문서에서 먼저 뽑아내고, 빈 곳만 사람에게 묻는다.

```sh
vaultos grill <slug>                  # grill-me — 아이디어만 있을 때
vaultos grill <slug> --docs <경로>    # grill-with-docs — 기획서·RFP·노트가 있을 때
```

## 2. Success criteria는 요구사항의 일부다

나중에 QA가 붙이는 것이 아니다. **무엇이 측정되면 성공인지 모르는 채로 구현을 시작하지 않는다.**

필수 항목 7개가 채워져야 게이트가 열린다.

| 항목 | 묻는 것 |
|---|---|
| `outcome` | 끝나면 무엇이 달라져 있어야 하는가 |
| `problem` | 지금 무엇이 문제이고 누가 불편한가 |
| `non_goals` | **이번에 하지 않기로 명시할 것** |
| `features` | 핵심 기능 1~3개 |
| `success` | 무엇이 측정되면 성공인가 (판정 가능한 문장) |
| `verification` | 그것을 어떻게 검증하는가 |
| `stop` | **언제 멈추는가** (더 다듬고 싶어도 그만둘 조건) |

선택 항목: `users` `surfaces` `constraints` `vocabulary` `approval`

## 3. 게이트가 막는 것

`project.yaml`에 `grill: pending | complete`가 기록된다.

- `pending`이면 `vaultos status`가 **[Grill pending — 구현 시작 전]**으로 표시한다
- **pending 상태에서 구현을 시작하지 않는다**
- 자동화가 팀 실행을 막는 것이 아니라, **상태가 보이게 해서 사람이 멈추게 한다**

## 4. 산출물 6개

게이트를 통과하면 생성된다. **빈 템플릿이 아니라 답변에서 채워진 문서다.**

| 산출물 | 내용 |
|---|---|
| `intake/sources.md` | 소스 목록, 추출된 사실 후보, 가정, 모순, 열린 질문 |
| `intake/grill.md` | 질문과 답, 게이트 상태, 멈추는 조건 |
| `governance/constitution.md` | mission / non-goals / 제약 / 용어 |
| `requirements/requirements.yaml` | REQ + **success criteria + verification** |
| `status/timeline.md` | phase 표 + mermaid gantt |
| `<repo>/tracker/tasks.yaml` | task slice + 담당 에이전트 |

> 이전 설계는 산출물이 26개(project-os 13 + tracker 13)였다. 대부분 빈 채로 방치됐다.
> **빈 템플릿을 많이 만드는 것보다, 답변에서 채워진 문서를 적게 만드는 것이 낫다.**

## 5. 추정을 사실처럼 쓰지 않는다

`grill-with-docs`가 문서에서 뽑은 것은 **전부 후보**다. `intake/sources.md`에 출처와 함께 남기고,
사람이 확인하기 전에는 요구사항으로 승격하지 않는다. 불확실한 것은 `status: inferred`로 표기한다.

## 6. Task 라우팅

기능 하나가 `spec → build → verify` 3개 slice로 쪼개지고, 제목에 따라 담당이 정해진다.

| 제목에 있으면 | 담당 |
|---|---|
| 요구사항 / spec / PRD | `pm` |
| 설계 / 구조 / 스키마 | `architect` |
| 조사 / 리서치 / 검토 | `research` |
| 테스트 / 검증 / QA | `qa` |
| 배포 / 릴리스 / 운영 | `ops` |
| 그 외 | `developer` |

각 담당의 권한과 금지는 [[04_AGENTS/README|Agents]]에 있다.

## 7. Loop Control

**success criteria가 충족되면 멈춘다.** optional polish로 계속하지 않는다.
더 할 것이 보이면 follow-up task로 기록한다. 막히면 루프를 돌지 말고 사람에게 묻는다.

멈추는 조건은 `intake/grill.md`와 `status/timeline.md` 양쪽에 남는다.
