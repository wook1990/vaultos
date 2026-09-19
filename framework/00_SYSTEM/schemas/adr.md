---
type: schema
schema: adr
status: active
updated: 2026-09-19
---

# Architecture Decision Record (ADR) Schema

## 규칙

**No Architecture Change, No ADR — 구조적 변경은 반드시 결정 기록을 가진다.**

ADR은 "무엇을 골랐는가"보다 **"무엇을 안 골랐고 왜 안 골랐는가"**를 남기기 위한 문서다. 이게 없으면 6개월 뒤에 같은 선택지를 다시 검토하게 된다.

## ID 체계

```
ADR-<NNN>
```

저장 위치: `architecture/adr/ADR-017-<slug>.md`

번호는 **재사용하지 않는다.** 폐기된 결정도 `superseded`로 남기고 번호를 비우지 않는다.

## 구조

```markdown
# ADR-017

## Context

현재 구조의 문제

## Options

A.
B.
C.

## Decision

B

## Reason

B를 선택한 이유

## Consequences

이 결정으로 발생하는 영향
```

## 섹션 규칙

| 섹션 | 규칙 |
|---|---|
| Context | 왜 지금 이 결정이 필요한가. 문제 상황을 쓴다 |
| Options | **최소 2개.** 하나뿐이면 결정이 아니라 통보다 |
| Decision | 고른 것 하나 |
| Reason | 왜 그것인가. 다른 것을 왜 버렸는지도 포함한다 |
| Consequences | 좋은 결과와 나쁜 결과를 **둘 다** 쓴다. 감수하기로 한 비용이 여기 남는다 |

상태는 frontmatter에 둔다: `proposed` / `accepted` / `superseded`

`superseded`가 되면 어떤 ADR이 대체했는지 명시한다.

## Architecture 관리 레벨

구조 문서는 네 층으로 본다. **층마다 관리 주체가 다르다.**

```
System Context   ← Human Managed
      ↓
Container        ← Human Managed
      ↓
Component        ← AI Managed
      ↓
Code             ← AI Managed
```

| 레벨 | 관리 | 이유 |
|---|---|---|
| System Context | Human | 시스템 경계와 외부 연동은 사람의 판단 영역 |
| Container | Human | 배포 단위·기술 스택 선택은 되돌리기 비싸다 |
| Component | AI | 내부 모듈 구성은 구현 과정에서 조정 가능 |
| Code | AI | 구현 세부 |

**AI는 Component와 Code를 조정할 수 있지만, System Context나 Container를 바꾸려면 ADR과 사람 승인이 필요하다.**

## 언제 ADR을 쓰는가

쓴다:
- 기술 스택 선택·교체
- 데이터 모델 변경
- 외부 인터페이스 변경
- 배포 구조 변경
- 되돌리기 비싼 선택

안 쓴다:
- 함수 이름 변경
- 내부 리팩터링 (동작·경계 변화 없음)
- 설정값 조정

애매하면 기준은 하나다. **6개월 뒤에 "왜 이렇게 했지?"라고 물을 만한가.**

## 금지

- ADR 없이 구조 변경을 진행하는 것
- Options를 1개만 쓰는 것
- Consequences에 좋은 점만 쓰는 것
- 기존 ADR을 덮어쓰는 것 → 새 ADR을 쓰고 이전 것을 `superseded`로 표시한다. **변경 이유를 삭제하지 않는다**

## Governance Profile별 적용

| Profile | ADR |
|---|---|
| `personal-light` | 불필요 |
| `personal-full` | 되돌리기 비싼 결정만 |
| `company-standard` 이상 | 필수 |
