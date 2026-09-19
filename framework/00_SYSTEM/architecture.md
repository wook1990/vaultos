---
type: system
architecture_version: 2
updated: 2026-09-19
---

# VaultOS Architecture

폴더 구조와 각 영역의 책임을 정의한다. 진입 문서는 [[00_SYSTEM/VAULTOS|VAULTOS]]다.

## 루트

```text
00_SYSTEM/        VaultOS 커널 — 자체 정의, 규약, 스키마, 템플릿, 마이그레이션 기록
01_GOVERNANCE/    공통 통제 정책 — 프로젝트별로 복사하지 않고 참조한다
02_WORKSPACES/    실제 작업 — personal/ 과 company/ 물리 분리
03_KNOWLEDGE/     재사용 지식 — 프로젝트 상태와 분리
04_AGENTS/        에이전트 역할 계약
05_OPERATIONS/    사람이 보는 통제 화면
98_PERSONAL/      업무와 무관한 개인 기록
99_ARCHIVE/       삭제하지 않고 내리는 곳
```

루트의 `CLAUDE.md` / `AGENTS.md` / `GEMINI.md`는 도구가 읽는 진입 포인터다. 내용을 따로 유지하지 않고 `00_SYSTEM/VAULTOS.md`와 `01_GOVERNANCE/`를 가리킨다.

## 각 영역의 책임

### 00_SYSTEM

```text
VAULTOS.md          최상위 운영 문서 (모든 에이전트가 먼저 읽는다)
architecture.md     이 문서
conventions.md      문서 생성 규약, QuickAdd, 수집 자동화
lifecycle.md        프로젝트 생애주기와 phase
context-loading.md  Progressive Context Loading 규칙
naming-rules.md     이름과 ID 체계
schemas/            frontmatter, requirement, change-request, adr
templates/          문서 템플릿 + project/ 프로젝트 시작 템플릿
migrations/         구조 변경 이력
```

### 01_GOVERNANCE

프로젝트가 몇 개든 정책은 여기 한 벌만 존재한다. 프로젝트 폴더로 복사하지 않는다.

```text
README.md              정책 인덱스
aipm-trace.md          운영 방법론과 8대 원칙
project-policy.md      프로젝트 구조와 Governance Profile
agent-policy.md        에이전트 권한과 금지
approval-policy.md     사람 승인이 필요한 변경
definition-of-done.md  Evidence 기반 완료 정의
data-policy.md         Project/Knowledge 경계 + Personal/Company 경계 + 분류 + Secret
knowledge-policy.md    수집·정제·승격 규칙과 AI Curation/Caution System
vaultos-health.md      유지보수와 구조 drift 점검
```

### 02_WORKSPACES

```text
personal/projects/<slug>/    개인 프로젝트
company/projects/<slug>/     회사 업무 (현재 비어 있음)
```

개인과 회사는 **물리적으로 분리한다.** 경계 규칙은 [[01_GOVERNANCE/data-policy|Data Policy]].

### 03_KNOWLEDGE

```text
00_inbox/       새 입력 (판단 전)
10_fleeting/    분석·정리 중인 노트 (토픽별 분류)
20_permanent/   장기 재사용 지식
  ai-agents/
  methods/
references/     외부·대용량 참조 자료
```

성숙도(inbox → fleeting → permanent)가 1차 축이고, 토픽이 2차 축이다.

### 04_AGENTS

```text
README.md        역할 인덱스
orchestrator/    요청 분류, 영향 분석, 흐름 제어
developer/       구현
auditor/         추적성과 drift 검사
curation/        AI Curation/Caution 에이전트와 프롬프트
```

### 05_OPERATIONS

```text
dashboard/       00_dashboard, 10_projects, 20_knowledge
reviews/         승격 보드, 리뷰 규칙
reports/worklog/ 일간·주간·월간 기록
```

### 98_PERSONAL / 99_ARCHIVE

`98_PERSONAL`은 업무 체계와 분리된 개인 기록이다. 에이전트는 명시적 요청 없이 컨텍스트에 포함하지 않는다.
`99_ARCHIVE`는 삭제 대신 내리는 곳이다. **여기 있는 내용을 현재 기준으로 인용하지 않는다.**

## 이름 규칙 요약

- 루트는 `2-digit` 번호 + 영문 역할 이름 (`00_SYSTEM`, `01_GOVERNANCE`)
- 프로젝트 슬러그는 영문 소문자 + 하이픈 (`my-new-app`)
- 하위 폴더는 로컬 번호 또는 의미 이름
- 링크 안정성을 구조 미학보다 우선한다

상세: [[00_SYSTEM/naming-rules|Naming Rules]]

## 금지

- 같은 책임을 가진 문서를 두 곳에 두는 것 — 이 볼트는 VaultOS 정의 문서가 4곳에 존재했던 이력이 있다
- 정책을 프로젝트 폴더로 복사하는 것
- `99_ARCHIVE` 내용을 현재 기준처럼 참조하는 것
- Personal과 Company 자료를 같은 컨텍스트에 넣는 것

## 이전 구조

2026-09-19 이전에는 PARA 기반 `000_VaultOS` ~ `900_Templates` 구조였다.
매핑표와 이행 기록: [Target Architecture And Migration](https://github.com/wook1990/vaultos/blob/main/docs/CASE-STUDY.md)
