---
type: governance
policy: knowledge
status: active
updated: 2026-09-19
---

# Knowledge Policy

지식을 어떻게 수집하고, 정제하고, 승격하는지에 대한 공통 계약이다.
구조와 탐색은 [[03_KNOWLEDGE/README|03_KNOWLEDGE README]], 프로젝트와의 경계는 [[01_GOVERNANCE/data-policy|Data Policy]]를 본다.

---

# Part 1. Capture → Refine → Distill 파이프라인

```
references(raw backlog) → 00_inbox(triage) → 10_fleeting(refine) → 20_permanent(distill)
```

## 0. Raw Source

- 위치: `03_KNOWLEDGE/references`
- 목적: 아직 직접 분석하지 않은 원문·자료·레퍼런스 적재
- 원칙: raw backlog가 많을수록 여기가 기본 적재소다

### Raw Backlog 운영 기준

- 많이 쌓인 원문은 먼저 `03_KNOWLEDGE/references`에 넣는다
- **이번 주에 실제로 볼 것만** `03_KNOWLEDGE/00_inbox`로 끌어온다
- `00_inbox`는 무한 저장소가 아니라 오늘/이번 주 triage 대기열이다
- 분석이 시작된 순간부터 `10_fleeting`으로 옮긴다
- raw가 많을수록 Inbox를 키우지 말고 `references`와 `10_fleeting`으로 분산한다

## 1. Capture

- 위치: `03_KNOWLEDGE/00_inbox`
- 목적: 아직 판단하지 않은 입력을 과도한 정리 없이 빠르게 저장

규칙:

- 새 입력은 먼저 `00_inbox`
- 판단 전에는 permanent로 바로 올리지 않는다
- `source_url`, `source_path`, `source_type` 중 가능한 값을 남긴다
- 제목은 나중에 바꿔도 되지만, 무슨 자료인지 알아볼 정도는 유지한다

금지:

- 수집 단계에서 구조를 과하게 정리하는 것
- 프로젝트 산출물을 inbox처럼 섞는 것
- 링크 없이 맥락을 완전히 잃는 것

## 2. Refine

- 위치: `03_KNOWLEDGE/10_fleeting`
- 목적: 요약, 비교, 초안, 질문 기반 정리
- **LLM 초안은 이 레이어에서 멈추는 것이 기본이다**

고급 모드인 AI Curation/Caution은 Part 2에서 다룬다.

## 3. Distill

- 위치: `03_KNOWLEDGE/20_permanent`
- 목적: 사람이 직접 검토한 장기 재사용 지식만 남긴다

판단 기준:

- 다음 프로젝트에서도 다시 쓸 수 있는가
- 특정 프로젝트 맥락 없이도 읽을 가치가 있는가
- 원칙, 프레임워크, 판단 기준으로 남길 수 있는가

## 4. 프로젝트에서 넘어온 지식

- project artifact에서 승격된 경우 `voBridge: promoted_from_project`
- 가능하면 `origin_project` 또는 `linked_project`를 남긴다
- Permanent Note가 특정 프로젝트에서 재사용되면 `applies_to_projects`에 프로젝트를 추가한다

## 5. 메타데이터 기준

- KnowledgeOS 문서 기본값: `voDomain: knowledge`
- 기본 Bridge 상태: `voBridge: none`
- 프로젝트에서 승격된 permanent: `voBridge: promoted_from_project`

---

# Part 2. AI Curation/Caution System

`동적 페르소나 부여 기반 전문 AI Curation/Caution 지식 저장소`를 운영하기 위한 실행 기준이다.
자료를 단순 요약하지 않고, 자료 성격과 사용자 의도에 따라 전문가 페르소나 보드를 배치해 분석하는 **고급 Refine 모드**다.

목적:

- 자료를 전문 관점으로 읽는다
- 근거, 한계, 리스크를 함께 표시한다
- Fleeting Note를 재사용 가능한 전문 큐레이션 산출물로 만든다
- Permanent Note 후보를 개념 단위로 분리한다
- 프로젝트에 연결 가능한 실행 포인트를 남긴다

## 작동 위치

```text
03_KNOWLEDGE/references / 03_KNOWLEDGE/00_inbox
  → Source Intake
  → Source Profiling
  → Intent Detection
  → Consultant Board Routing
  → Curation/Caution Fleeting Note
  → Permanent Candidates
  → Project Hooks
```

| 단계 | 위치 |
|---|---|
| 분석 전 자료 | `03_KNOWLEDGE/00_inbox` 또는 `03_KNOWLEDGE/references` |
| 전문 큐레이션 결과 | `03_KNOWLEDGE/10_fleeting` |
| 장기 개념 | `03_KNOWLEDGE/20_permanent` |
| 프로젝트 실행 연결 | `02_WORKSPACES/personal/projects` |

## Curation과 Caution의 차이

### Curation — 자료를 내 지식체계 안에 다시 배치한다

핵심 주장 해석 / 배경 맥락 복원 / 내 프로젝트·관심사와 연결 / 재사용 가능한 개념 추출 / Permanent 후보 분리

### Caution — AI가 권위 있는 말투로 과잉 확정하지 못하게 막는다

근거 수준 표시 / 일반화 가능 범위 / 적용 전제 / 과장·마케팅성 주장 / 실행 리스크 / 확인이 필요한 추가 질문

**좋은 산출물은 Curation만 강한 문서가 아니라 Caution까지 살아 있는 문서다.**

## 동적 페르소나 = 말투가 아니라 작업 계약

각 페르소나는 다음 필드를 가진다.

- `mandate` 무엇을 책임지는가
- `domain_scope` 어떤 자료를 잘 다루는가
- `question_stack` 어떤 질문부터 던지는가
- `evidence_standard` 어떤 근거를 충분하다고 보는가
- `decision_lens` 어떤 판단 기준을 쓰는가
- `deliverable_shape` 어떤 산출물을 내야 하는가
- `failure_modes` 어떤 실패를 조심해야 하는가
- `do_not_do` 무엇을 하면 안 되는가

## 기본 컨설턴트 보드

**초기 운영에서 보드를 너무 많이 만들지 않는다.**

| Board | 적합한 자료 | Primary / Challenger / Curator |
|---|---|---|
| **Technical** | AI agent, software engineering, architecture, automation, repository operations, coding workflow | AI Systems Architect / Reliability·Risk Reviewer / Knowledge Systems Curator |
| **Operating** | 업무 프로세스, 조직 운영, 자동화 흐름, agent 운영 모델, 생산성 시스템 | Operating Model Consultant / Execution Risk Advisor / Implementation Translator |
| **Knowledge Distillation** | 개념 정리, 지식관리, PKM, 장기 저장 가치가 있는 글, 여러 노트로 분해할 자료 | Knowledge Curator / Concept Boundary Reviewer / Distillation Editor |
| **Strategy** | 시장 변화, 사업 전략, 제품 방향, 경쟁우위, 투자 판단 | Strategy Partner / Market Skeptic / Executive Memo Editor |
| **Risk** | 보안, 정책, 규제, 신뢰성, 개인정보, 품질 보증 | Risk Assurance Advisor / Abuse·Failure Mode Reviewer / Governance Curator |

## 표준 실행 절차 (10단계)

### 1. Source Intake — 출처를 먼저 고정한다

source title / source url 또는 local path / source type / 작성일·발행일 / 가져온 날짜 / 원문 접근 가능 여부

source가 불명확하면 분석을 시작하더라도 `source_access_status: partial` 또는 `unknown`으로 남긴다.

### 2. Source Profiling — 바로 요약하지 말고 먼저 profile한다

topic domain / document mode / evidence density / novelty level / actionability / decision relevance

### 3. Intent Detection — 사용자가 이 자료로 무엇을 하려는가

`understand` 이해 / `curate` 전문 큐레이션 / `critique` 비판적 검토 / `apply` 적용 방안 도출 / `distill` Permanent 후보 추출 / `connect_to_project` 프로젝트 연결 / `design_system` 시스템 설계 반영

### 4. Board Routing

source profile과 intent를 기준으로 보드를 선택한다. 라우팅 규칙은 Part 2의 "라우팅 규칙" 절을 따른다.

반드시 남길 값: board type / primary consultant / challenger / curator / routing reason / routing confidence

### 5. Primary Analysis

Primary Consultant는 원문의 핵심 주장과 전문적 의미를 해석한다.

결과: 핵심 주장 / 주장 구조 / 중요한 근거 / 내 시스템에 주는 의미 / 적용 가능한 패턴

### 6. Caution Review

Challenger는 다음을 확인한다.

근거가 약한 부분 / 과장 가능성 / 숨은 전제 / 적용하면 위험한 조건 / 추가 검증이 필요한 부분

### 7. Curator Synthesis

Curator는 최종 Fleeting Note를 만든다. 필수 조건:

- 여러 전문가 의견을 단순 병합하지 않는다
- 최종 해석을 내 언어로 다시 쓴다
- Caution을 별도 섹션으로 남긴다
- Permanent 후보를 개념 단위로 분리한다
- 프로젝트 연결 후보를 표시한다
- 다음 결정을 명확히 남긴다

### 8. Watch Verdict

"이 원본을 실제로 시청/열람할 가치가 있는가"를 **별도로** 판단한다.
Curation 품질과 원본 시청 가치는 다른 질문이다 — 근거가 약해도 caution과 함께 잘 정리된 노트를 만들 수 있고, 반대로 노트는 잘 만들어졌어도 원본은 반복적이거나 저밀도라 다시 볼 필요가 없을 수 있다.

판단 기준:

- **정보 고유성**: 이 vault의 기존 Fleeting/Permanent Note와 겹치는가
- **근거 밀도**: `evidence_density`가 낮으면 원본을 직접 봐도 얻는 게 적다
- **시간 대비 가치**: 러닝타임 대비 실행 가능한 정보 밀도
- **상업적 잡음**: 광고·자기홍보 비중이 커서 신호대잡음비가 낮은가

결과는 `watch_verdict` frontmatter 필드에 4단계 중 하나로 남긴다 (템플릿의 "Watch Verdict" 섹션):

| 값 | 뜻 |
|---|---|
| `watch_full` | 시청 추천 — 고유하고 근거 밀도 높음 |
| `watch_key_sections` | 특정 구간만 시청 권장 (타임스탬프 표시) |
| `skim_summary_only` | 이 노트 요약으로 충분, 원본 시청 불필요 |
| `skip` | 스킵 권장 — 반복적이거나 저밀도이거나 광고성 |

### 9. Curator Grade

이 노트의 **지식자산으로서의 가치**를 A~D 등급으로 남긴다.
Watch Verdict가 "원본을 볼 가치가 있는가"라면, Curator Grade는 "이 큐레이션 노트 자체를 지식자산으로 남길 가치가 있는가"다. 둘은 대체로 같은 방향으로 움직이지만 항상 일치하지는 않는다 — 원본은 광고 비중이 커서 `skip`이어도, 거기서 뽑아낸 패턴 하나는 `grade: B`로 남길 수 있다.

| 등급 | 기준 |
|---|---|
| **A (핵심 자산)** | evidence_density medium~high, caution_level low~medium. 재사용 가치가 높고 이 vault의 실제 판단(3S 프레임워크, 하네스 엔지니어링 등 기존 노트)과 연결되거나 새로운 축을 더한다. 대체로 `promotion_candidate: true`와 일치 |
| **B (유용한 참고)** | evidence_density medium. 실행 가능한 패턴은 있으나 적용 범위가 좁거나 caution이 있다. Permanent 후보는 아닐 수 있어도 재참조 가치가 있다 |
| **C (제한적 참고)** | evidence_density low~medium, caution_level high (상업적 편향, 근거 부족, 무출처 인용, 단일 일화 등). 특정 조건에서만 참고 가치가 있다 |
| **D (저가치)** | evidence_density low. 근거 없는 동기부여·광고성·일반론. 지식자산으로 남길 이유가 약하다. 대체로 `promotion_candidate: false`, `watch_verdict: skip`과 일치 |

등급은 **필드값만으로 기계적으로 계산하지 않는다.** Curator가 evidence_density / caution_level / promotion_candidate와의 정합성을 근거로 직접 판단하고 2~3문장으로 설명한다 (템플릿의 "Curation Grade" 섹션).

등급은 노트 제목에도 표시한다: H1을 `# [{grade}] {제목}` 형식으로 쓴다 (예: `# [A] DoRA vs LoRA — 분리형 파인튜닝 원칙`).
**파일명(슬러그)은 바꾸지 않는다** — 기존 위키링크가 파일명 기준이므로 등급 표시는 본문 제목에만 반영한다.

### 10. Knowledge Category 배치

완성된 노트를 `03_KNOWLEDGE/10_fleeting` 아래 카테고리 하위폴더에 배치한다.
Fleeting Notes는 원래 "Permanent 승격 전 완충 구간"으로 설계됐지만, 자료 유입량이 많아지면서 카테고리 폴더가 지식 자산의 기본 탐색 축이 됐다.

```text
03_KNOWLEDGE/10_fleeting/
├── 10_AI_코딩에이전트_하네스엔지니어링/   (소분류 5개: 하네스·루프·그래프 / AI활용·프롬프트 / MCP·스킬 / 멀티에이전트 오케스트레이션 / 에이전트 설계·거버넌스)
├── 20_AX_기업AI전환_비즈니스사례/
├── 30_옵시디언_PKM_세컨드브레인/
├── 40_로컬LLM_오픈소스모델_ML기법/
├── 50_학습법_인지과학_생산성/
├── 60_마인드셋_자기계발_커리어/
├── 70_CS기초_인프라_시스템사고/
├── 80_재테크_창업/
├── 90_언어학습/
└── 99_미분류_라이프스타일/
```

규칙:

- 소분류(3단계) 폴더는 **항목 수가 많아 탐색이 어려워질 때만** 만든다. 현재는 `10_AI_코딩에이전트_하네스엔지니어링`만 소분류가 있다. 항목이 적은 카테고리를 억지로 세분화하지 않는다
- `knowledge_category` frontmatter에 실제 폴더 경로를 기록한다. 나중에 재분류로 이동해도 이 필드로 이력을 추적할 수 있다
- 파일명(슬러그)은 폴더 이동과 무관하게 유지한다 — 위키링크는 파일명 기준이라 폴더 변경이 링크를 깨지 않는다
- 카테고리가 애매하면 `99_미분류_라이프스타일`에 두고 나중에 사람이 재분류한다
- 이 카테고리 구조는 `20_permanent`로 승격할 때도 그대로 이어받는 것을 기본으로 한다

## 라우팅 규칙

라우팅의 목적은 가장 그럴듯한 페르소나를 고르는 것이 아니라, **source와 사용자 의도에 맞는 분석 계약을 고르는 것**이다.

좋은 라우팅이 남기는 것: 왜 이 보드인가 / 누가 primary인가 / 누가 challenger인가 / 어떤 caution을 반드시 확인하는가 / 결과물이 Fleeting·Permanent·Project 중 어디로 이어지는가

### 입력 필드

```yaml
source_type:
topic_domain:
document_mode:
analysis_intent:
evidence_density:
actionability:
decision_relevance:
linked_project:
```

### Source Type Gate

| 자료 유형 | 조건 | Board | 필수 caution |
|---|---|---|---|
| 기술/개발 | code, software engineering, AI agent, architecture, tooling, repository workflow, automation | Technical | 실제 구현 가능성, 환경 의존성, 벤치마크·주장 재현성, 운영 복잡도, 유지보수 비용 |
| 운영/프로세스 | workflow, team operation, productivity system, automation process, knowledge operation, agent operation | Operating | 실제 반복 가능성, 사람 개입이 필요한 지점, 예외 처리, 운영 비용, 과도한 자동화 위험 |
| 지식/개념 | concept, essay, PKM, learning note, theory, conceptual framework, long-term reusable idea | Knowledge Distillation | 개념 경계, 과잉 일반화, 원문 맥락 손실, 기존 노트와 중복, Permanent 승격 기준 충족 여부 |
| 전략/시장 | market, business strategy, product strategy, competitor, investment, positioning, trend | Strategy | 데이터 최신성, 시장 일반화 위험, 이해관계자 편향, 단기 유행과 구조 변화 구분, 실행 가능성 |
| 리스크/정책 | security, privacy, legal, compliance, governance, safety, audit, reliability | Risk | 최신성, jurisdiction·적용 범위, 정책 해석 한계, 의사결정 전 전문가 확인 필요성, downstream risk |

### Intent Override

source type보다 사용자 의도가 강하면 intent가 라우팅을 덮어쓴다.

- `design_system` → `Operating Board` 또는 `Technical Board` 우선 (QuickAdd 개선, OpenClaw workflow 설계, agent harness 설계, KnowledgeOS 구조 변경 등)
- `distill` → `Knowledge Distillation Board` 우선
- `critique` → 기존 board 유지하되 challenger 비중을 높인다
- `connect_to_project` → `linked_project`를 반드시 채우고 Project hook을 필수 산출물로 둔다

### Complexity Rule

| 복잡도 | 조건 | 보드 구성 |
|---|---|---|
| Low | 단일 주제, 짧은 자료, 실행 리스크 낮음 | Primary + Curator |
| Medium | 여러 주장, 적용 가능성 있음, Permanent 후보 있음 | Primary + Challenger + Curator |
| High | 기술·운영·전략이 섞임, 프로젝트 의사결정에 영향, 근거 검토 필요, 자동화 설계에 반영 예정 | Primary + Secondary Specialist + Challenger + Curator |

### Routing Confidence

- `high` — source type 명확, intent 명확, 적합한 board가 하나로 수렴
- `medium` — source type은 명확하나 intent가 넓음, 두 board 모두 가능하지만 하나가 우세
- `low` — source 불완전, 링크만 있고 원문 접근 어려움, 의도 모호, 여러 board가 비슷하게 가능

**`low`이면 최종 노트에 `Next Decision`을 반드시 남긴다.**

### Output Decision

| 유형 | 조건 |
|---|---|
| Fleeting Only | source 이해와 큐레이션이 목적, 장기 개념이 아직 선명하지 않음 |
| Fleeting + Permanent Candidates | 재사용 가능한 개념이 있음, 다른 프로젝트에도 쓰일 원칙이 있음 |
| Fleeting + Project Hooks | 활성 프로젝트 실행에 연결됨, 작업 지시·설계 변경·backlog 후보가 있음 |
| Fleeting + Permanent + Project | 장기 개념과 즉시 실행 포인트가 모두 있음 |

## 표준 명령문

공용 agent contract는 [[04_AGENTS/curation/01_AI_Curation_Caution_Agent|AI Curation/Caution Agent]], 복사해서 쓰는 실행 prompt는 [[04_AGENTS/curation/01_Dynamic_Persona_Curation_Prompt|Dynamic Persona Curation Prompt]]에 있다.
모델별 진입 파일은 vault root의 [[AGENTS|AGENTS.md]] (Codex) / [[CLAUDE|CLAUDE.md]] (Claude) / [[GEMINI|GEMINI.md]] (Gemini)다.

```text
03_KNOWLEDGE/00_inbox의 [문서명] source를 확인해서 KnowledgeOS AI Curation/Caution 방식으로 분석해줘.
source profiling을 먼저 하고, 적절한 consultant board를 routing한 뒤,
Primary Analysis, Caution Review, Curator Synthesis를 거쳐
03_KNOWLEDGE/10_fleeting에 Curation/Caution Fleeting Note를 만들어줘.
Permanent 후보와 Project hook도 따로 제안해줘.
```

짧게 요청할 때:

```text
이 Inbox 자료를 전문 AI Curation/Caution 노트로 만들어줘.
```

템플릿: `00_SYSTEM/templates/14_AI_Curation_Caution_Note.md`

## 산출물 품질 기준

좋은 Curation/Caution Note는 다음을 만족한다.

- 원문 출처가 명확하다
- 어떤 보드가 왜 배치됐는지 보인다
- 단순 요약보다 전문적 해석이 많다
- 근거와 한계가 분리되어 있다
- KnowledgeOS 또는 프로젝트에 연결된다
- Permanent 후보가 여러 개념으로 분해되어 있다
- 다음 사람이 할 판단이 남아 있다

## 자동화 단계

| 단계 | 내용 |
|---|---|
| Manual | 사용자가 Inbox 자료를 지정하고 Codex/Claude가 한 번 처리 |
| Assisted | QuickAdd로 템플릿을 만들고 LLM이 빈 섹션을 채움 |
| Agentic | OpenClaw가 새 Inbox 자료를 감지해 source profiling과 board routing을 자동 수행 |
| Semi-Autonomous | OpenClaw가 Fleeting Note 초안까지 만들고 사용자는 Permanent 승격만 승인 |

---

# Part 3. Agent 권한과 금지

## agent가 맡는 일

- raw source를 `03_KNOWLEDGE/references` 또는 `00_inbox`로 분류 제안
- inbox triage 후보 제안
- `10_fleeting` 초안과 비교 정리 작성
- source profiling, board routing, caution review, curated fleeting note 작성
- related note 연결 후보 제안
- permanent 승격 **후보** 제안
- reference 자료 요약

## agent routing 기본안

| Agent | 역할 |
|---|---|
| capture | raw source를 `references` 또는 `00_inbox`로 분류 |
| refine | `10_fleeting` 초안과 비교 정리 작성 |
| curation/caution | source profile, board routing, caution review, curated note 작성 |
| distill reviewer | permanent 승격 후보와 핵심 문장 제안 |
| linker | 기존 permanent/reference와 연결 후보 제안 |

모델별 강점: Codex는 vault 파일 읽기·쓰기와 Note 생성, Claude는 긴 원문 독해·caution review·문장 refinement, Gemini는 긴 컨텍스트와 multi-source 비교.

## agent가 하면 안 되는 일

- permanent 승격을 **사람 승인 없이 확정**
- 프로젝트 문서를 KnowledgeOS로 임의 이동
- canonical contract 문서 수정
- source 확인 없이 authoritative conclusion 작성
- consultant brand name만으로 라우팅
- caution 없이 Permanent 승격 제안
- 모든 자료에 모든 보드를 붙이기
- 프로젝트 실행 문서를 Permanent Note처럼 저장

## 운영 원칙

- **agent는 초안과 제안을 만든다. 최종 분류와 승격은 사람이 결정한다**
- 자동화보다 source 신뢰도와 해석 품질이 먼저다
- routing이 애매하면 confidence를 낮게 남긴다
- 전문가 페르소나는 권위 연출이 아니라 분석 품질을 위한 구조다
- **Caution 없는 Curation은 KnowledgeOS의 기본 산출물로 인정하지 않는다**
- ProjectOS와 KnowledgeOS를 절대 섞지 않는다
