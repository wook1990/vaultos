---
type: governance
policy: project
status: active
updated: 2026-09-19
---

# Project Policy

프로젝트를 어떻게 만들고 운영하는지에 대한 공통 계약이다.

## 1. 3-Zone 모델

```
Zone A (Tracker of Record)   workspace repo의 tracker/*.yaml — git에 있고 유일한 실행 정본
Zone B (Control Plane)       02_WORKSPACES/<scope>/projects/<slug>/ — 의도·요구사항·결정·상태
Zone C (Knowledge)           03_KNOWLEDGE/ — 프로젝트를 넘어 재사용하는 지식
```

- **Zone B는 Zone A를 복제하지 않는다.** 가리킨다.
- 코드가 없는 프로젝트는 Zone A가 없고 Zone B가 곧 전부다.
- 모든 에이전트(Codex / Claude / Gemini / 그 외)는 같은 스키마를 읽고 쓴다. 실행 환경만 다르고 데이터 모델은 갈라지지 않는다.

### 무엇을 어디에 두는가

가장 자주 틀리는 지점이다. 기준은 하나다 — **"무엇을 했는가"는 repo, "왜 그렇게 하기로 했는가"는 VaultOS.**

| 산출물 | 위치 | 이유 |
|---|---|---|
| 코드, 테스트 | **repo** | 실행 정본 |
| `tracker/tasks.yaml` | **repo** | task가 branch·commit·PR과 연결돼야 한다 |
| `tracker/issues.yaml` | **repo** | 코드 수정과 같은 커밋에 들어간다 |
| `tracker/decisions.yaml` | **repo** | 구현 수준의 판단 기록 |
| `tracker/releases.yaml` `progress.md` | **repo** | 릴리스는 커밋 묶음이다 |
| `project.yaml` | VaultOS | 에이전트 진입점 |
| `governance/constitution.md` | VaultOS | 프로젝트 불변 원칙 |
| `requirements/requirements.yaml` | VaultOS | 무엇을 만들기로 했는가 |
| `changes/CR-xxx.md` | VaultOS | 왜 요구사항을 바꿨는가 |
| `architecture/adr/ADR-xxx.md` | VaultOS | 왜 이 구조를 골랐는가 |
| `status/current-state.yaml` | VaultOS | 지금 어디쯤인가 — **한 화면 요약** |
| `evidence/` | VaultOS | 검증 결과의 인덱스 (실제 테스트는 repo) |

`current-state.yaml`은 tracker의 복제가 아니다. task 목록을 옮겨 적지 않고 `phase / 막힌 것 / 다음 할 것` 수준만 남긴다.

**"폰에서 task를 보고 싶다"는 이유로 tracker를 VaultOS에 복제하지 않는다.** GitHub 웹에서 `tracker/tasks.yaml`을 열면 어느 기기에서든 같은 상태를 본다. 이전 시스템이 이 복제를 자동화해서 프로젝트당 미러 15개와 Drive 충돌을 만들었다. → [[01_GOVERNANCE/sync-policy|Sync Policy]]

### 코드가 없는 프로젝트

회사 문서 업무, 리서치처럼 repo가 없는 프로젝트는 Zone A가 없다. 이때는 tracker도 VaultOS 안(`status/`)에 둔다. 복제가 아니라 **애초에 한 곳뿐**이므로 문제가 없다.

## 2. Governance Profile

프로젝트마다 통제 강도가 다르다. `project.yaml`에 명시한다.

| Profile | 대상 | 구조 |
|---|---|---|
| `personal-light` | 개인 실험 | **`project.yaml` 하나** |
| `personal-full` | 개인 프로덕션 | + `requirements/`, `changes/`, `evidence/` |
| `company-standard` | 회사 내부 업무 | + `architecture/adr/`, `status/risks.yaml`, `status/decision-log.md` |
| `company-strict` | 회사 핵심/민감 업무 | + `logs/events.jsonl`, Data Classification, Release Approval |

프로젝트가 커지면 프로필을 승격한다. **처음부터 무거운 프로필로 시작하지 않는다.**

## 3. personal-light 구조 (기본값)

```text
02_WORKSPACES/personal/projects/<slug>/
└── project.yaml    ← 이게 전부다
```

`project.yaml` 하나가 mission, 현재 phase, 다음 할 일, 막힌 것, repo 주소를 모두 담는다.

**개인 실험에 문서 3개를 요구하지 않는다.** 시작 마찰이 높으면 시스템을 안 쓰게 되고,
안 쓰는 시스템은 구조가 아무리 좋아도 무의미하다. 이 볼트는 그 실패를 이미 한 번 겪었다.

`constitution.md`와 `requirements.yaml`은 프로젝트가 실제로 그것을 필요로 할 때 추가한다 —
다른 사람이 쓰기 시작하거나, 되돌리기 어려운 결정이 쌓이기 시작할 때 `personal-full`로 올린다.

실행 정본(code, tests, `tracker/*.yaml`)은 repo에 둔다.
→ [[00_SYSTEM/templates/project/README|Project Template]]

### repo 주소

```yaml
repo:
  url: https://github.com/<you>/my-app   # 정본. 어느 기기에서든 같다
  local:                                     # 기기별 편의 정보. 정본 아님
    wsl: /home/<you>/workspace/my-app
    mac: /Users/<you>/workspace/my-app
```

**로컬 절대경로를 정본으로 쓰지 않는다.** repo는 옮기는 것이 아니라 각 기기가 clone하는 것이다.
→ [[01_GOVERNANCE/sync-policy|Sync Policy]]

## 4. company-standard 구조

```text
02_WORKSPACES/company/projects/<slug>/
├── project.yaml
├── governance/{constitution,charter,scope}.md
├── requirements/{requirements,traceability}.yaml
├── architecture/{context,containers}.md + adr/
├── changes/CR-xxx.md
├── features/F-xxx/{spec,plan,tasks,checklist}
├── evidence/{tests,evaluations,reviews}/
├── status/{current-state,risks}.yaml + convergence.md + decision-log.md
└── logs/events.jsonl
```

## 5. Project Constitution

프로젝트의 불변 원칙이다. **AI는 이 문서를 임의로 수정할 수 없다.**

```markdown
# PROJECT CONSTITUTION
## Mission        이 프로젝트가 존재하는 이유
## Core Principles  P-001, P-002...
## Non Goals      NG-001, NG-002...
## Technical Constraints  TC-001, TC-002...
## Governance     Requirement 변경은 CR, Architecture 변경은 ADR
```

## 6. 문서의 세 단계

| Level | 역할 | 변경 빈도 |
|---|---|---|
| Constitution | 프로젝트 불변 원칙 | 매우 낮음 |
| Baseline | 현재 승인 상태 | 중간 |
| Working Docs | Feature / Task / 구현 | 높음 |

## 7. Current State는 최소로 유지한다

`current-state.yaml`에 프로젝트의 모든 내용을 넣지 않는다. 현재 운영에 필요한 것만 남긴다.

```yaml
phase: implementation
current_feature: [F-018]
blocked: [TASK-122]
pending_approval: [CR-014]
open_risks: [RISK-007]
next: [TASK-138]
```

과거 기록은 `decision-log.md`, `changes/`, `adr/`에 남긴다. **Current Truth ≠ History.**

## 8. 금지

- Zone A의 내용을 Zone B에 별도 미러 파일로 복제하는 것
- `current-state.yaml` 외에 추가 트래킹 표면(승인 게이트, 역량 계획, 요구사항 추적 매트릭스, 테스트 매트릭스)을 **선제적으로** 만드는 것 — 실제로 필요해지면 그때 하나씩 추가한다
- 프로젝트 output을 permanent note처럼 바로 취급하는 것
- 생성 주체(AI/사람)로 output 폴더를 나누는 것
- Personal 프로젝트와 Company 프로젝트의 컨텍스트를 섞는 것

## 9. 재발 경보

이 볼트는 과거 프로젝트당 파일이 53~115개까지 불어난 이력이 있다(Tracking Mirror 15개, 거버넌스 문서 10개 이상). 2026-09-19에 9~28개로 되돌렸다.

**프로젝트 폴더의 파일 수가 늘기 시작하면 원인을 먼저 확인한다.**
배경: [Zone Simplification](https://github.com/wook1990/vaultos/blob/main/docs/CASE-STUDY.md)
