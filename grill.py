#!/usr/bin/env python3
"""Grill Gate — 프로젝트를 만들기 전에 캐묻는다.

두 가지 원칙 위에 서 있다.

1. **"이 프로젝트 만들어줘"로 바로 시작하지 않는다.**
   먼저 소스 자료를 모으고, 그것을 근거로 캐묻는다.
2. **소스 자료가 있으면 맨 아이디어에서 시작하지 않는다.**
   기존 문서가 있으면 거기서 먼저 뽑아내고, 빈 곳만 사람에게 묻는다.

    grill-me         대화형. 아이디어만 있을 때
    grill-with-docs  문서 기반. 기획서·RFP·노트가 이미 있을 때

**Success criteria는 요구사항 정의의 일부다. 나중의 QA 추가물이 아니다.**

산출물 (구 설계의 26개가 아니라 6개):

    intake/sources.md          소스 목록, 사실/가정/모순/열린 질문
    intake/grill.md            질문과 답, 게이트 상태
    governance/constitution.md mission / non-goals / 제약
    requirements/requirements.yaml  REQ + success criteria + verification
    status/timeline.md         phase와 mermaid gantt
    <repo>/tracker/tasks.yaml  task slice + 담당 에이전트 라우팅
"""

import os
import re
from datetime import date, timedelta

# 캐물을 것. 구 Grill Routing Contract §5의 항목을 그대로 쓴다.
QUESTIONS = [
    ("outcome", "이 프로젝트가 끝나면 무엇이 달라져 있어야 합니까?", True),
    ("problem", "지금 무엇이 문제입니까? 누가 불편합니까?", True),
    ("users", "누가 씁니까?", False),
    ("non_goals", "이번에 **하지 않기로** 명시할 것은? (쉼표로 구분)", True),
    ("features", "핵심 기능 1~3개는? (쉼표로 구분)", True),
    ("success", "무엇이 측정되면 성공입니까? (판정 가능한 문장으로)", True),
    ("verification", "그것을 어떻게 검증합니까? (테스트/수동확인/지표)", True),
    ("surfaces", "영향받는 영역은? (예: 백엔드 API, 모바일 화면, 데이터 스키마)", False),
    ("constraints", "바꿀 수 없는 제약은? (기술/일정/비용/규제)", False),
    ("vocabulary", "이 프로젝트에서만 특별한 뜻을 갖는 용어가 있습니까?", False),
    ("approval", "사람 승인이 반드시 필요한 지점은?", False),
    ("stop", "언제 멈춥니까? (더 다듬고 싶어도 그만둘 조건)", True),
]

# 기본 phase. timeline/gantt의 뼈대가 된다.
PHASES = [
    ("intake", "소스 수집과 Grill", 2),
    ("spec", "요구사항 확정", 3),
    ("build", "구현", 10),
    ("verify", "검증", 3),
    ("release", "릴리스 판단", 1),
]

# task를 어느 에이전트에게 보낼지. 04_AGENTS의 계약과 대응한다.
ROUTING = [
    (r"(요구사항|requirement|스펙|spec|PRD)", "pm"),
    (r"(설계|구조|architecture|스키마|schema)", "architect"),
    (r"(조사|리서치|research|비교|검토)", "research"),
    (r"(테스트|검증|test|QA|qa)", "qa"),
    (r"(배포|릴리스|release|운영|ops)", "ops"),
]
DEFAULT_OWNER = "developer"


def route(title):
    for pat, owner in ROUTING:
        if re.search(pat, title, re.I):
            return owner
    return DEFAULT_OWNER


def slug_of(text, n=4):
    words = re.findall(r"[A-Za-z0-9가-힣]+", text.lower())
    return "-".join(words[:n]) or "task"


# ------------------------------------------------------------------ 소스 수집

def scan_docs(doc_dir):
    """grill-with-docs — 기존 문서에서 사실 후보를 뽑는다.

    추정을 사실처럼 쓰지 않는다. 전부 inferred로 표시하고 사람이 확인하게 한다.
    """
    facts, files = [], []
    exts = (".md", ".txt", ".yaml", ".yml", ".json")
    for dirpath, dirnames, filenames in os.walk(doc_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith((".", "node_modules"))]
        for fn in sorted(filenames):
            if not fn.lower().endswith(exts):
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, doc_dir)
            try:
                text = open(p, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            files.append((rel, len(text)))
            # 제목 줄과 목적/목표를 말하는 문장을 후보로 본다
            for line in text.splitlines():
                t = line.strip()
                if not t or len(t) > 200:
                    continue
                if re.match(r"^#{1,3}\s+\S", t):
                    facts.append((rel, "heading", t.lstrip("# ").strip()))
                elif re.search(r"(목적|목표|문제|해결|사용자|요구사항|제약|성공|범위)\s*[:：]", t):
                    facts.append((rel, "statement", t))
    return files, facts


def write_sources(pdir, mode, doc_dir=None, files=None, facts=None, note=None):
    os.makedirs(os.path.join(pdir, "intake"), exist_ok=True)
    lines = [
        "# Intake Sources",
        "",
        "> 이 프로젝트가 무엇을 근거로 시작됐는지 남긴다.",
        "> **소스 없이 시작한 프로젝트는 나중에 왜 그렇게 만들었는지 답할 수 없다.**",
        "",
        f"- 수집 방식: `{mode}`",
        f"- 수집일: {date.today().isoformat()}",
    ]
    if doc_dir:
        lines.append(f"- 소스 위치: `{doc_dir}`")
    lines += ["", "## 소스 목록", ""]
    if files:
        lines += ["| 파일 | 크기 |", "|---|---|"]
        lines += [f"| `{rel}` | {n:,}자 |" for rel, n in files[:40]]
        if len(files) > 40:
            lines.append(f"| … 외 {len(files)-40}개 | |")
    else:
        lines.append("_(문서 소스 없음 — 대화로 수집)_")

    lines += ["", "## 추출된 사실 후보", ""]
    if facts:
        lines.append("> **전부 `inferred`다.** 사람이 확인하기 전에는 사실로 취급하지 않는다.")
        lines.append("")
        lines += ["| 출처 | 유형 | 내용 |", "|---|---|---|"]
        for rel, kind, t in facts[:60]:
            safe = t.replace("|", "\\|")[:120]
            lines.append(f"| `{rel}` | {kind} | {safe} |")
        if len(facts) > 60:
            lines.append(f"| … | | 외 {len(facts)-60}건 |")
    else:
        lines.append("_(없음)_")

    lines += [
        "", "## 가정", "",
        "- (확인되지 않았지만 참이라고 보고 진행하는 것을 적는다)",
        "", "## 모순", "",
        "- (소스끼리 어긋나는 지점을 적는다. 비워두지 말고 '없음'이라고 쓴다)",
        "", "## 열린 질문", "",
    ]
    lines.append(note or "- (소스만으로는 답할 수 없어 사람에게 물어야 하는 것)")
    open(os.path.join(pdir, "intake", "sources.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")


# ------------------------------------------------------------------ 캐묻기

def run_grill(answers, interactive=True, prefill=None):
    prefill = prefill or {}
    out = {}
    if interactive:
        print("\nGrill — 프로젝트를 캐묻습니다. 비워두면 건너뜁니다.")
        print("필수 항목(*)을 비우면 게이트가 pending으로 남습니다.\n")
    for key, q, required in QUESTIONS:
        if key in answers:
            out[key] = answers[key]
            continue
        hint = prefill.get(key)
        if not interactive:
            out[key] = hint or ""
            continue
        mark = " *" if required else ""
        if hint:
            print(f"  (문서에서 추출: {hint[:80]})")
        try:
            v = input(f"{q}{mark}\n> ").strip()
        except EOFError:
            v = ""
        out[key] = v or hint or ""
        print()
    return out


def gate_status(ans):
    missing = [k for k, _, req in QUESTIONS if req and not ans.get(k)]
    return ("complete" if not missing else "pending"), missing


def write_grill(pdir, ans, status, missing, mode):
    lines = [
        "# Grill Gate", "",
        f"- 상태: **{status}**",
        f"- 방식: `{mode}`",
        f"- 일자: {date.today().isoformat()}",
        "",
    ]
    if status != "complete":
        lines += [
            "> **게이트가 열리지 않았다.** 아래 필수 항목이 비어 있다.",
            "> 이 상태에서 구현을 시작하지 않는다.", "",
            *[f"- `{k}`" for k in missing], "",
        ]
    lines += ["## 질문과 답", ""]
    for key, q, required in QUESTIONS:
        v = ans.get(key) or "_(미응답)_"
        lines += [f"### {q}{' *' if required else ''}", "", v, ""]
    lines += [
        "## 멈추는 조건", "",
        ans.get("stop") or "_(미정)_", "",
        "> success criteria가 충족되면 멈춘다. **optional polish로 계속하지 않는다.**",
        "> 더 할 것이 보이면 follow-up task로 기록한다.", "",
    ]
    open(os.path.join(pdir, "intake", "grill.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")


# ------------------------------------------------------------------ 산출물

def write_constitution(pdir, name, ans):
    os.makedirs(os.path.join(pdir, "governance"), exist_ok=True)
    ngs = [x.strip() for x in re.split(r"[,\n]", ans.get("non_goals", "")) if x.strip()]
    tcs = [x.strip() for x in re.split(r"[,\n]", ans.get("constraints", "")) if x.strip()]
    lines = [
        "# PROJECT CONSTITUTION", "",
        "> 이 문서는 프로젝트의 **불변 원칙**이다. **AI는 임의로 수정할 수 없다.**",
        "> Grill Gate 결과에서 생성됐다. 바꾸려면 사람이 직접 한다.", "",
        "## Mission", "",
        ans.get("outcome") or "_(미정)_", "",
    ]
    if ans.get("problem"):
        lines += ["해결하려는 문제:", "", ans["problem"], ""]
    lines += ["## Core Principles", "",
              "- **P-001**: success criteria가 충족되면 멈춘다. optional polish로 계속하지 않는다.",
              "- **P-002**: 요구사항에 연결되지 않은 구현을 하지 않는다.", ""]
    lines += ["## Non Goals", ""]
    lines += [f"- **NG-{i:03d}**: {v}" for i, v in enumerate(ngs, 1)] or ["- _(미정)_"]
    lines += ["", "## Technical Constraints", ""]
    lines += [f"- **TC-{i:03d}**: {v}" for i, v in enumerate(tcs, 1)] or ["- _(없음)_"]
    if ans.get("vocabulary"):
        lines += ["", "## Vocabulary", "", ans["vocabulary"]]
    lines += ["", "## Governance", "",
              "- Requirement 변경은 Change Request(CR)를 사용한다.",
              "- Architecture 변경은 Architecture Decision Record(ADR)를 사용한다.",
              "- Evidence 없이 Done 처리하지 않는다.", ""]
    if ans.get("approval"):
        lines += ["사람 승인이 필요한 지점:", "", ans["approval"], ""]
    open(os.path.join(pdir, "governance", "constitution.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")


def write_requirements(pdir, slug, ans):
    """기능 하나당 REQ 하나. success criteria와 verification을 반드시 붙인다."""
    os.makedirs(os.path.join(pdir, "requirements"), exist_ok=True)
    feats = [x.strip() for x in re.split(r"[,\n]", ans.get("features", "")) if x.strip()]
    dom = re.sub(r"[^A-Z0-9]", "", slug.upper())[:6] or "CORE"
    success = ans.get("success", "")
    verify = ans.get("verification", "")
    out = ["# Grill Gate에서 생성됐다. success criteria는 요구사항의 일부다.", "", "requirements:"]
    for i, f in enumerate(feats, 1):
        out += [
            f"  - id: REQ-{dom}-{i:03d}",
            f"    statement: {f}",
            f"    rationale: {ans.get('problem', '(Grill에서 미기재)')}",
            "    source: intake/grill.md",
            "    priority: MUST",
            "    acceptance:",
            f"      - {success or '(판정 가능한 문장으로 채운다)'}",
            "    verification:",
            f"      - {verify or '(어떻게 검증할지 채운다)'}",
            "    status: draft",
            "",
        ]
    if not feats:
        out += ["  # Grill에서 핵심 기능이 수집되지 않았다. 게이트가 열리지 않은 상태다.", ""]
    open(os.path.join(pdir, "requirements", "requirements.yaml"), "w", encoding="utf-8").write("\n".join(out))
    return [f"REQ-{dom}-{i:03d}" for i in range(1, len(feats) + 1)]


def write_timeline(pdir, name, ans, start=None):
    """phase와 mermaid gantt. Obsidian이 mermaid를 그대로 렌더한다."""
    os.makedirs(os.path.join(pdir, "status"), exist_ok=True)
    d = start or date.today()
    rows, gantt = [], []
    for key, label, days in PHASES:
        end = d + timedelta(days=days)
        rows.append(f"| {key} | {label} | {d.isoformat()} | {end.isoformat()} | {days}일 |")
        gantt.append(f"    {label} :{key}, {d.isoformat()}, {days}d")
        d = end
    lines = [
        "# Timeline", "",
        "> Grill Gate에서 생성된 **초안**이다. 실제 일정은 task가 쌓이면서 조정한다.",
        "> 날짜가 확정되지 않았으면 기간만 의미가 있다.", "",
        "| phase | 내용 | 시작 | 종료 | 기간 |", "|---|---|---|---|---|",
        *rows, "",
        "```mermaid", "gantt",
        f"    title {name}",
        "    dateFormat YYYY-MM-DD",
        "    axisFormat %m/%d",
        "    section Phases",
        *gantt,
        "```", "",
        "## 멈추는 조건", "",
        ans.get("stop") or "_(Grill에서 미정)_", "",
    ]
    open(os.path.join(pdir, "status", "timeline.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")


def write_tasks(repo_path, ans, req_ids, dom):
    """요구사항을 task slice로 쪼개고 담당 에이전트를 라우팅한다."""
    if not repo_path or not os.path.isdir(repo_path):
        return None
    tdir = os.path.join(repo_path, "tracker")
    os.makedirs(tdir, exist_ok=True)
    tpath = os.path.join(tdir, "tasks.yaml")
    # 실제 task가 들어 있을 때만 보존한다.
    # 게이트가 pending일 때 만든 자리표시자는 덮어쓴다.
    if os.path.exists(tpath):
        if re.search(r"^\s*-\s*id:", open(tpath, encoding="utf-8").read(), re.M):
            return tpath

    feats = [x.strip() for x in re.split(r"[,\n]", ans.get("features", "")) if x.strip()]
    verify = ans.get("verification", "")
    out = ["# Grill Gate에서 생성된 task slice.",
           "# 정본은 이 파일이다. 볼트에는 요약만 간다.", "", "tasks:"]
    n = 0
    for i, f in enumerate(feats):
        req = req_ids[i] if i < len(req_ids) else ""
        for kind, suffix in (("spec", "요구사항 확정"), ("build", "구현"), ("verify", "검증")):
            n += 1
            title = f"{f} — {suffix}"
            out += [
                f"  - id: T-{dom}-{n:03d}",
                f"    title: {title}",
                "    status: planned",
                f"    phase: {kind}",
                f"    owner: {route(title)}",
                f"    requirement_ids: [{req}]" if req else "    requirement_ids: []",
                f"    branch: feat/{slug_of(f)}",
                "    definition_of_done:",
                f"      - {verify or '(검증 방법을 채운다)'}" if kind == "verify" else "      - (완료 조건을 채운다)",
                "    evidence: []",
                "",
            ]
    if not feats:
        out += ["  # Grill이 완료되지 않아 task를 만들지 않았다.", ""]
    open(tpath, "w", encoding="utf-8").write("\n".join(out))
    return tpath
