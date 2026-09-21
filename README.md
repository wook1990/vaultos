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

# 워크스페이스에서
vaultos new my-app --path .              # 볼트 등록 + 계약 표면 고정
vaultos grill                            # Grill Gate — docs/ 를 읽고 빈 곳만 묻는다
vaultos validate                         # 계약 준수 검사
vaultos sync                             # 세션 종료 시 1회, 볼트에 요약만

# 볼트에서
vaultos status                           # 지금 무엇이 어디까지 됐는지
vaultos check                            # 볼트 구조 검사
```

**프로젝트 워크스페이스는 코드만 있는 곳이 아니다.** `vaultos bind`가 계약 종속 기능을 고정한다.

```
<repo>/.vaultos/link + contract.yaml   볼트 주소와 따르는 계약
<repo>/tracker/                        계약이 정한 5개 스키마 (임의 확장 금지)
<repo>/AGENTS.md CLAUDE.md GEMINI.md   볼트를 가리키는 진입점 (복사하지 않는다)
<repo>/.githooks/pre-commit            계약 위반 시 경고
```

`vaultos validate`가 잡는 것: Grill 미완료 / Requirement 없는 task / Evidence 없는 done /
의도 문서가 저장소에 있음 / tracker 임의 확장.

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
00_SYSTEM/        볼트 자체 정의, 규약, 스키마, 템플릿
01_GOVERNANCE/    공통 통제 정책 — 프로젝트별로 복사하지 않고 참조한다
02_WORKSPACES/    personal/ 과 company/ 물리 분리
03_KNOWLEDGE/     00_inbox → 10_fleeting → 20_permanent + references
04_AGENTS/        에이전트 역할 계약
05_OPERATIONS/    사람이 보는 대시보드·리뷰
06_AUTOMATIONS/   (아직 안 만든다 — 볼트 자체를 검사하는 내부 도구용. 필요해질 때)
07_PRODUCTS/      배포된 제품·운영 중인 자동화의 상태 (개발 상태가 아니라 운영 상태)
08_DEVICES/       지금 뭐가 어디서 돌고 있는가 — 기기 레지스트리
98_PERSONAL/      업무와 무관한 개인 기록
99_ARCHIVE/       삭제하지 않고 내리는 곳 (또는 완전히 지운다 — 프로젝트 규모가 작으면 이력을 안 남기는 것도 선택지다)
```

`02_WORKSPACES`가 "지금 만들고 있는 것"이라면 `07_PRODUCTS`는 "지금 실제로 떠 있는 것"이다 — 개발 진행 상태(task/CR/ADR)는 여전히 `02_WORKSPACES` 프로젝트에 남고, 여기는 `live`/`degraded`/`paused`/`retired` 같은 운영 상태 요약만 가진다. `RELEASE`에 도달한 프로젝트를 등록한다.

`08_DEVICES`는 그것들이 물리적으로 어느 기기 위에서 도는지를 기록한다 — 구독 계정으로 도는 CLI 코딩 에이전트(Claude Code, Codex CLI 등)는 항상 특정 기기에 로그인 세션으로 묶여 실행되기 때문이다. `04_AGENTS/assistant/`(채널로 들어온 질문에 vault를 읽고 답하는 역할)와 `05_OPERATIONS/channels/`(Slack/Telegram 등, Query-Response부터 시작)가 이 위에서 동작한다.

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

## 볼트 구조를 검사한다

```sh
python3 tools/vaultos_health.py <볼트경로>
# 또는: VAULT_PATH=<볼트경로> python3 tools/vaultos_health.py
```

읽기 전용, 외부 의존성 없음, 1패스 스캔. 표준 루트 존재 / 필수 문서 존재 / 깨진 위키링크 / 프로젝트 허브 최소 구조를 검사한다. 종료 코드 `0`=문제없음, `1`=error 있음. 자체 테스트: `python3 tools/tests/test_vaultos_health.py`.

## 볼트를 최신 버전으로 맞춘다

이 repo(framework)와 실제로 만든 볼트는 시간이 지나면 벌어진다 — 볼트 쪽에서 규칙을 고치거나, 이 repo에 새 기능이 추가되거나. `VERSION`과 [CHANGELOG.md](CHANGELOG.md)가 이 repo의 버전 정본이고, 어떤 차이가 "당연히 달라야 하는 것"(개인 값, 인스턴스 전용 기록)이고 어떤 차이가 "반영해야 하는 개선"인지의 기준은 [framework/01_GOVERNANCE/update-policy.md](framework/01_GOVERNANCE/update-policy.md)에 있다. 지금은 `vaultos update` 커맨드가 없다 — 파일을 직접 diff해서 손으로 맞춘다(문서에 절차 있음). 자동화는 이 방식을 몇 번 더 해보고 패턴이 안정되면 만든다.

## 구성

```
init.py                  환경 생성
VERSION                  이 repo의 SemVer 버전
CHANGELOG.md              버전별 변경 기록
framework/               볼트에 배치될 문서 원본
  00_SYSTEM/             규약·스키마·템플릿
  01_GOVERNANCE/         정책 13개 (ecosystem, update-policy 포함)
  03_KNOWLEDGE/          지식 계층 안내
  04_AGENTS/             역할 계약 (orchestrator / developer / auditor / pm / curation / assistant)
  05_OPERATIONS/         대시보드·리뷰 보드
  07_PRODUCTS/           배포 제품·자동화 등록 템플릿
  08_DEVICES/            기기 레지스트리 템플릿
vaultos                  CLI — 볼트 탐색, 프로젝트 연동, 상태 동기화
tools/vaultos_health.py  구조 검사 (읽기 전용, 의존성 없음)
tools/tests/             vaultos_health.py 자체 테스트
docs/CASE-STUDY.md       설계 근거
```

## 요구사항

Python 3.8+ 만 있으면 된다. **외부 의존성이 없다.**
Obsidian은 선택이다 — 플러그인 없이도 구조는 그대로 동작한다.

## 라이선스

MIT
