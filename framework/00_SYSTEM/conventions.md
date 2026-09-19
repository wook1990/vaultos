---
type: system
updated: 2026-09-19
---

# Conventions

문서를 어떻게 만들고 이름 붙이는지에 대한 규약이다. 이름과 ID 규칙은 [[00_SYSTEM/naming-rules|Naming Rules]]를 본다.

## 1. 파일 분류 — 이걸 어디에 둘 것인가

새 파일을 만들 때 **세 질문을 순서대로** 던진다.

```
1. 지금 하는 일을 끝내기 위한 것인가?      → 02_WORKSPACES/<scope>/projects/<slug>/
2. 앞으로도 다시 쓸 지식인가?              → 03_KNOWLEDGE/
3. 볼트 자체를 어떻게 운영할지에 대한 것인가? → 00_SYSTEM/ 또는 01_GOVERNANCE/
```

어디에도 해당하지 않으면 `03_KNOWLEDGE/00_inbox`에 두고 나중에 판단한다.
**판단 전에 새 폴더를 만들지 않는다.**

| 성격 | 위치 |
|---|---|
| 아직 분류 못 한 입력 | `03_KNOWLEDGE/00_inbox/` |
| 분석·정리 중인 노트 | `03_KNOWLEDGE/10_fleeting/` |
| 장기 재사용 지식 | `03_KNOWLEDGE/20_permanent/` |
| 원문·대용량 참조 자료 | `03_KNOWLEDGE/references/` |
| 프로젝트 의도·결정·상태 | `02_WORKSPACES/.../projects/<slug>/` |
| 코드·테스트·tracker | **볼트 아님.** git 저장소 |
| 볼트 운영 규칙 | `01_GOVERNANCE/` |
| 볼트 구조·스키마·템플릿 | `00_SYSTEM/` |
| 에이전트 역할 계약 | `04_AGENTS/` |
| 사람이 보는 화면 | `05_OPERATIONS/` |
| 업무와 무관한 개인 기록 | `98_PERSONAL/` |
| 더 이상 쓰지 않지만 지우지 않을 것 | `99_ARCHIVE/` |

## 2. 파일명

```
지식 노트     YYYYMMDD_<slug>_<kind>.md      20260919_agent-harness_fleeting.md
프로젝트 슬러그 영문 소문자 + 하이픈            my-new-app
정책·시스템 문서 영문 소문자 + 하이픈            sync-policy.md
마이그레이션   YYYY-MM-DD_<주제>.md           2026-09-19_zone-split.md
```

- 공백을 쓰지 않는다. 스크립트와 경로 참조가 깨진다
- `<slug>`는 영문 소문자와 하이픈으로 통일한다
- 파일을 옮겨도 이름을 바꾸지 않는다 — 위키링크는 파일명으로 해석되므로 폴더 이동이 링크를 깨지 않는다

## 3. 문서 형식

| 내용 | 형식 |
|---|---|
| 기계가 읽는 상태 | YAML (`project.yaml`, `requirements.yaml`) |
| 사람이 읽는 설명 | Markdown (`constitution.md`, `ADR-xxx.md`) |

frontmatter 규약: [[00_SYSTEM/schemas/frontmatter|Frontmatter]]

## 4. 링크

- 같은 볼트 안은 위키링크 `[[대상|표시]]`를 쓴다
- **표 안에서는 `\|`로 이스케이프한다** — 안 하면 표가 깨진다
- 예시로 링크를 인용할 때는 백틱으로 감싼다. 검사기가 실제 링크로 오해한다
- `99_ARCHIVE`의 문서를 현재 기준으로 인용하지 않는다

## 5. 캡처 자동화 (선택)

입력 마찰이 시스템 사용을 결정한다. 캡처는 자동화할 가치가 있다.

```
메신저/웹 → 자동화 → 03_KNOWLEDGE/00_inbox/ → 볼트
```

자동화가 지켜야 할 두 조건:

- **새 파일만 만든다.** 기존 노트를 수정하거나 삭제하지 않는다
- 같은 입력이 재전송돼도 같은 파일을 다시 만들지 않는다 (고유 id 기반 중복 방지)

이 두 가지를 지키면 자동화가 로컬 편집과 충돌하지 않는다. → [[01_GOVERNANCE/sync-policy|Sync Policy]]

Obsidian을 쓴다면 QuickAdd / Templater로 노트 생성 단축키를 만들 수 있다. 필수는 아니다.
**플러그인이 없어도 이 구조는 그대로 동작한다.**
