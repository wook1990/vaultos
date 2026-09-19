# VaultOS

**지식 저장소 + 프로젝트 관리 프레임워크.**
Obsidian 볼트 하나에 개인 지식과 프로젝트 통제를 함께 올리되, **AI 에이전트가 같은 규칙 아래에서 일하도록** 만든다.

```
VaultOS = Control Plane   왜 그렇게 만들기로 했는가  (Intent / Requirement / CR / ADR / Evidence)
Repo    = Execution SSOT  실제로 무엇이 만들어졌는가  (Code / Test / tracker)
```

**VaultOS는 코드의 정본이 아니라, 코드가 왜 그렇게 되었는지의 정본이다.**

## 시작하기

```sh
git clone https://github.com/wook1990/vaultos.git
cd vaultos
python3 init.py
```

`init`이 두 가지를 묻는다.

1. **볼트를 어디에 만들 것인가** — 클라우드 동기화 폴더 안을 권장한다
2. **저장소 백엔드가 무엇인가** — `gdrive` / `dropbox` / `onedrive` / `icloud` / `obsidian-sync` / `git` / `local`

백엔드에 따라 **동기화 정책의 강도가 달라진다.** 병합을 지원하지 않는 백엔드(Drive, Dropbox 등)는 단일 쓰기 규칙이 강제되고, `obsidian-sync`처럼 자체 충돌 처리가 있으면 느슨해진다. 선택값은 `00_SYSTEM/vault-config.yaml`과 `01_GOVERNANCE/sync-policy.md §0`에 기록된다.

비대화형:

```sh
python3 init.py --path ~/Dropbox/vault --storage dropbox --company
```

## 프로젝트를 볼트에 연동한다

이 프레임워크의 핵심이다. **저장소가 자기 볼트를 찾고, 볼트가 자기 저장소를 안다.**

```sh
vaultos config --vault <볼트경로>        # 볼트 위치 한 번 기록

vaultos new my-app --path ~/work/my-app  # 볼트 등록 + 저장소 연결을 한 번에
vaultos link my-app                      # 이미 있는 저장소를 나중에 연결
vaultos status                           # 지금 무엇이 어디까지 됐는지
vaultos sync                             # 저장소 tracker → 볼트 상태 요약
vaultos check                            # 구조 검사
```

`vaultos new`는 두 개의 표식을 만든다. **둘 다 내용을 복사하지 않고 주소만 담는다.**

```
저장소/.vaultos              →  볼트 위치와 프로젝트 경로
볼트/…/project.yaml의 repo   →  저장소 URL과 기기별 clone 위치
```

이 배선이 있으면 어느 저장소에서 일하는 에이전트든 **의도 계층(Requirement / ADR / 정책)을 찾아간다.**
없으면 각자 자기 저장소에 계약 사본을 만들기 시작하고, 사본은 곧 갈라진다.

볼트를 찾는 순서: `--vault` → `VAULTOS_HOME` → 저장소의 `.vaultos` → `~/.config/vaultos/config` → 클라우드 경로 탐색.
**경로를 하드코딩하지 않는다.**

→ [framework/01_GOVERNANCE/ecosystem.md](framework/01_GOVERNANCE/ecosystem.md)

## 만들어지는 구조

```
00_SYSTEM/        볼트 자체 정의, 규약, 스키마, 템플릿, 마이그레이션 기록
01_GOVERNANCE/    공통 통제 정책 — 프로젝트별로 복사하지 않고 참조한다
02_WORKSPACES/    personal/ 과 company/ 물리 분리
03_KNOWLEDGE/     00_inbox → 10_fleeting → 20_permanent + references
04_AGENTS/        에이전트 역할 계약
05_OPERATIONS/    사람이 보는 대시보드·리뷰
98_PERSONAL/      업무와 무관한 개인 기록
99_ARCHIVE/       삭제하지 않고 내리는 곳
```

루트의 `CLAUDE.md` / `AGENTS.md` / `GEMINI.md`는 도구가 읽는 진입 포인터다. **계약을 복사하지 않고 `00_SYSTEM/VAULTOS.md`를 가리킨다.**

## 핵심 원칙 8가지

| # | 원칙 |
|---|---|
| 1 | No Requirement, No Code |
| 2 | No Architecture Change, No ADR |
| 3 | No Requirement Change, No CR |
| 4 | No Evidence, No Done |
| 5 | AI Executes, Human Governs |
| 6 | Repository = Single Source of Truth |
| 7 | Every Change Must Be Traceable |
| 8 | Current Truth ≠ History |

## 가볍게 시작한다

프로젝트는 **파일 하나**로 시작한다.

```
02_WORKSPACES/personal/projects/<slug>/project.yaml
```

| Profile | 구조 | 언제 |
|---|---|---|
| `personal-light` | `project.yaml` 하나 | 기본값. 개인 실험 |
| `personal-full` | + constitution / requirements / evidence | 남이 쓰기 시작하거나 되돌리기 어려운 결정이 쌓일 때 |
| `company-standard` | + adr / risks / decision-log | 회사 업무 |
| `company-strict` | + events / classification / release approval | 민감 데이터·외부 영향 |

**개인 실험을 무겁게 만들지 않고, 회사 업무를 가볍게 만들지 않는다.**

## 왜 이렇게 설계했나

이 프레임워크는 이론이 아니라 **두 번 무너진 개인 볼트를 전수 조사한 결과**에서 나왔다.

| 실측된 실패 | 대응 규칙 |
|---|---|
| 내용이 같은 중복 문서 61개, 같은 자료가 4개 트리에 병존 | 정본은 하나. 나머지는 `99_ARCHIVE` |
| 볼트 정의 문서가 4곳에 존재 | `00_SYSTEM/VAULTOS.md` 하나만 최상위 |
| 850개 중 283개(34%)가 고아. 템플릿 17개 중 15개 미사용 | 구조 검사 도구로 자동 탐지 |
| 4월 489개 생성 → 6월 4개로 활동 중단 | **시작은 파일 1개.** 자동화는 필요해진 뒤에 |
| 프로젝트당 파일 53~115개 (tracker 미러 15개) | Zone 분리. 볼트는 repo를 복제하지 않고 가리킨다 |
| 5개월 방치된 동기화 충돌 사본 | 백엔드별 동기화 규칙 + 세션 경계 쓰기 |

전문: [docs/CASE-STUDY.md](docs/CASE-STUDY.md)

> **실패 모드는 "구조 부족"이 아니라 "운영되지 않는 구조의 과잉 생성"이다.**

## 구성

```
init.py                  환경 생성
framework/               볼트에 배치될 문서 원본
  00_SYSTEM/             규약·스키마·템플릿
  01_GOVERNANCE/         정책 11개 (ecosystem 포함)
  04_AGENTS/             역할 계약 (orchestrator / developer / auditor / pm / curation)
  05_OPERATIONS/         대시보드·리뷰 보드
vaultos                  CLI — 볼트 탐색, 프로젝트 연동, 상태 동기화
tools/vaultos_health.py  구조 검사 (읽기 전용, 의존성 없음)
docs/CASE-STUDY.md       설계 근거
```

## 요구사항

Python 3.8+ 만 있으면 된다. **외부 의존성이 없다.**
Obsidian은 선택이다 — 플러그인 없이도 구조는 그대로 동작한다.

## 라이선스

MIT
