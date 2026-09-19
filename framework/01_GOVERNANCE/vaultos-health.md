---
type: governance
policy: vaultos-health
status: active
updated: 2026-09-19
---

# VaultOS Health

VaultOS를 장기적으로 읽을 수 있고 신뢰할 수 있는 상태로 유지하기 위한 계약이다.
**볼트 자체도 정기적으로 검사한다.**

## 1. 유지보수 원칙

- lint는 구조 drift를 잡는다. **사람은 의미와 품질을 판단한다.**
- Project와 Knowledge를 섞지 않는다.
- Personal과 Company를 섞지 않는다.
- Zone B가 Zone A를 다시 복제하기 시작하면 즉시 되돌린다.
- 문서가 많아질수록 **삭제와 archive 기준이 더 중요해진다.**

## 2. Health 검사 항목

| 항목 | 무엇을 찾는가 |
|---|---|
| Broken Links | 대상이 사라진 위키링크 |
| Duplicate Knowledge | 내용이 같은 문서가 여러 곳에 존재 |
| Stale Context | 오래 갱신되지 않은 채 참조되는 문서 |
| Orphan Requirements | 구현·Task로 이어지지 않은 요구사항 |
| Orphan Tasks | Requirement에 연결되지 않은 작업 |
| Unlinked ADR | 어떤 변경과도 연결되지 않은 결정 기록 |
| Open CR | 오래 열려 있는 Change Request |
| Unverified Features | 구현됐지만 Evidence가 없는 기능 |
| Archive Candidates | 더 이상 운영되지 않는 영역 |

## 3. 구조 lint 항목

- root bucket 존재 (`00_SYSTEM` ~ `99_ARCHIVE`)
- `00_SYSTEM/VAULTOS.md` 존재
- canonical governance 문서 존재
- project hub 필수 문서 존재
- root loose file 경고
- root naming sanity

원칙:

- lint는 **구조**만 검증한다. 의미 판단을 대신하지 않는다.
- Knowledge 영역은 구조와 입구 문서까지만 강하게 검사한다.
- lint는 볼트를 **수정하지 않는다.** 읽기 전용이다.

### 실행

```sh
python3 <repo>/src/vaultos_health.py "<vault_path>"
```

구현: [[02_WORKSPACES/personal/projects/vaultos-health-check/governance/constitution|vaultos-health-check]] — repo 경로는 그 프로젝트의 `project.yaml`에 있다 (ADR-001에 따라 Python 표준 라이브러리 1패스)
종료 코드 `0` = error 없음, `1` = error 있음. 출력 등급은 `error` / `warn` / `note` 세 단계다.

`note`의 대부분은 **아직 만들지 않은 노트를 가리키는 링크**다. Zettelkasten에서는 정상이므로 오류로 보지 않는다.

## 4. 유지보수 리듬

### Daily

- Inbox를 비운다
- AI draft 검토 대기를 줄인다
- 활성 프로젝트의 상태 문서를 확인한다

### Weekly

- lint 실행
- broken link 확인
- active / inactive 프로젝트 상태 점검
- permanent 승격 후보를 하나 이상 판단
- **프로젝트 폴더의 파일 수가 최소 표준을 넘고 있는지 확인**

### 구조 변경 전

1. 이 변경이 Zone A/B/C 경계를 넘는가
2. Personal/Company 경계를 넘는가
3. 새 규칙이 기존 project hub와 충돌하는가
4. naming 규칙과 가이드 문서를 같이 갱신했는가
5. **아래 §5 재발 경보를 확인했는가**

## 5. 재발 경보 — 구조를 늘리기 전에 이 이력을 확인한다

이 볼트의 실패 모드는 **"구조 부족"이 아니라 "운영되지 않는 구조의 과잉 생성"이다.**
2026-09-19 전수 조사에서 측정된 실제 수치다.

| 측정값 | 의미 |
|---|---|
| **중복 md 61개** (837 → 고유 776) | 전량 Academy 폴더. 같은 강의가 4개 트리에 병존했다 |
| **고아 문서 283 / 850 (34%)** | 어떤 문서에서도 링크되지 않는다. 템플릿은 17개 중 15개가 고아였다 |
| **4월 489개 → 6월 4개** | 4월에 전체의 58%를 만들고 2개월 만에 활동이 멈췄다 |
| 프로젝트당 53~115 파일 | Tracking Mirror 15개 + 거버넌스 문서 10개 이상. 9~28개로 되돌렸다 |

4~5월에 만든 `500_Areas`(11개 빈 README), `800_QT`(3건 후 정지), 템플릿 대부분은 **만들어졌지만 운영되지 않았다.** 실제로 살아남은 것은 `00_inbox → 10_fleeting` 파이프라인과 프로젝트뿐이다.

### 따라서

- 새 폴더·새 정책·새 트래킹 표면을 추가하기 전에 **"이미 만들었다가 방치한 것과 무엇이 다른가"**에 먼저 답한다.
- 자동화(Traceability 검사, Drift 탐지, Event Log, Dashboard)는 **실제로 필요해진 시점에** 만든다.
- 한 바퀴 돌려보고 아쉬웠던 것만 추가한다.

전체 기록: [Inventory](https://github.com/<you>/vaultos/blob/main/docs/CASE-STUDY.md) / [Target Architecture](https://github.com/<you>/vaultos/blob/main/docs/CASE-STUDY.md)

## 6. 사람이 반드시 판단해야 하는 것

- 어떤 fleeting note를 permanent로 승격할지
- 어떤 프로젝트 문서를 knowledge로 승격할지
- 어떤 프로젝트를 archive로 보낼지
- **새 트래킹 표면이 정말 필요한지**
