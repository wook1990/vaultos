---
type: knowledge_root
updated: 2026-09-19
---

# 03_KNOWLEDGE

프로젝트를 넘어 **재사용하는 지식**을 담는 영역이다.
입력, 초안, 영구 지식, 참조 자료를 장기적으로 일관되게 축적하는 것이 목적이다.

규칙은 [[01_GOVERNANCE/knowledge-policy|Knowledge Policy]], 프로젝트와의 경계는 [[01_GOVERNANCE/data-policy|Data Policy]]를 본다.

## 구조

```text
03_KNOWLEDGE/
├── 00_inbox/        triage 대기열 — 오늘/이번 주에 볼 것만
├── 10_fleeting/     정제 중인 노트 — 카테고리별 하위폴더
├── 20_permanent/    사람이 검토한 장기 재사용 지식
│   ├── ai-agents/
│   └── methods/
└── references/      raw backlog와 반복 조회용 참조 자료
```

## 파이프라인

```
references(raw) → 00_inbox(triage) → 10_fleeting(refine) → 20_permanent(distill)
```

| 층 | 역할 | 핵심 원칙 |
|---|---|---|
| `references` | 아직 분석하지 않은 원문·자료 적재소 | raw가 많을수록 여기가 기본이다 |
| `00_inbox` | 오늘/이번 주 triage 대기열 | **무한 저장소가 아니다** |
| `10_fleeting` | 요약·비교·초안·전문 큐레이션 | LLM 초안은 여기서 멈추는 것이 기본 |
| `20_permanent` | 장기 재사용 지식 | 사람이 직접 검토한 것만 |

raw가 많을수록 `00_inbox`를 키우지 말고 `references`와 `10_fleeting`으로 분산한다.

## 10_fleeting 카테고리

자료 유입량이 많아지면서 카테고리 폴더가 기본 탐색 축이 됐다.

```text
10_AI_코딩에이전트_하네스엔지니어링/   (소분류 5개)
20_AX_기업AI전환_비즈니스사례/
30_옵시디언_PKM_세컨드브레인/
40_로컬LLM_오픈소스모델_ML기법/
50_학습법_인지과학_생산성/
60_마인드셋_자기계발_커리어/
70_CS기초_인프라_시스템사고/
80_재테크_창업/
90_언어학습/
99_미분류_라이프스타일/
```

소분류 폴더는 항목이 많아 탐색이 어려워질 때만 만든다. 애매하면 `99_미분류_라이프스타일`에 두고 나중에 재분류한다.
이 카테고리 구조는 `20_permanent` 승격 시에도 그대로 이어받는다.

## 20_permanent

| 폴더 | 내용 |
|---|---|
| `ai-agents/` | 에이전트 운영 가이드 (Codex subagent, gstack 실무 가이드, OMX 마스터 운영 등) |
| `methods/` | PKM·방법론 문서, AI Agent Builder OS 커리큘럼 |

## references

반복 조회용 참조 자료와 아직 분석하지 않은 raw backlog가 함께 있다.

- `agent-team-academy/` — ProjectOS/KnowledgeOS 에이전트팀 강의 최종 제공본 (md 119 + pptx 23). 2026-09-19에 정본으로 확정했고, 이전 세대 3개 트리(`00_Curriculum_Path`, `26_V2`, `28_제작_정리본`)는 `99_ARCHIVE/academy-generations/`로 내렸다

## 무엇이 여기 들어오지 않는가

| 대상 | 위치 |
|---|---|
| 프로젝트 상태·요구사항·결정 | `02_WORKSPACES/` |
| 업무와 무관한 개인 기록 (QT, 음악 등) | `98_PERSONAL/` — **KnowledgeOS가 아니다** |
| 이전 세대 문서 | `99_ARCHIVE/` |

**ProjectOS는 지금 일을 끝내기 위한 문서, KnowledgeOS는 앞으로도 계속 쓸 지식이다.**

## 바로 열기

- [[05_OPERATIONS/dashboard/20_knowledge|Knowledge Dashboard]]
- [[05_OPERATIONS/reviews/promotion-board|Promotion Board]] — 승격 판단 대기열
- [[01_GOVERNANCE/knowledge-policy|Knowledge Policy]] — 수집·정제·승격 규칙, AI Curation/Caution System
- [[04_AGENTS/curation/01_AI_Curation_Caution_Agent|AI Curation/Caution Agent]]

## QuickAdd 연결

`KnowledgeOS Inbox Capture` / `Refine Note` / `AI Curation/Caution Note` / `Query Note` / `Distill Note`
→ [[00_SYSTEM/conventions|Conventions]]
