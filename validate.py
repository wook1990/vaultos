#!/usr/bin/env python3
"""워크스페이스가 VaultOS 계약을 지키고 있는지 검사한다.

이전 설계에서 `start-pm-team.sh`가 Grill 미완료 시 실행을 막았던 역할이다.
**차단이 아니라 상태를 보이게 하는 것**이 목적이다. 사람이 보고 멈춘다.

    vaultos validate           워크스페이스 계약 검사
    vaultos validate --quiet   실패만 출력 (hook용)

종료 코드: 0 = 통과, 1 = 위반
"""

import os
import re

TRACKER_REQUIRED = ["tasks.yaml", "issues.yaml", "decisions.yaml", "releases.yaml", "progress.md"]
ENTRYPOINTS = ["AGENTS.md", "CLAUDE.md", "GEMINI.md"]
FORBIDDEN_DOCS = ["docs/product-brief.md", "docs/roadmap.md", "docs/architecture.md",
                  "docs/initiative-brief.md", "docs/release-checklist.md"]
VAULT_REQUIRED = {
    "personal-light": ["project.yaml"],
    "personal-full": ["project.yaml", "intake/grill.md", "governance/constitution.md",
                      "requirements/requirements.yaml"],
    "company-standard": ["project.yaml", "intake/grill.md", "governance/constitution.md",
                         "requirements/requirements.yaml", "status/current-state.yaml"],
    "company-strict": ["project.yaml", "intake/grill.md", "governance/constitution.md",
                       "requirements/requirements.yaml", "status/current-state.yaml"],
}


def check(repo, vault, link, profile):
    """(violations, warnings, facts) 를 돌려준다."""
    v, w, facts = [], [], {}

    # 1) 계약 표면이 고정돼 있는가
    for name in TRACKER_REQUIRED:
        if not os.path.isfile(os.path.join(repo, "tracker", name)):
            v.append(f"계약 스키마 없음: tracker/{name}")
    for name in ENTRYPOINTS:
        if not os.path.isfile(os.path.join(repo, name)):
            w.append(f"에이전트 진입점 없음: {name}")

    # 2) tracker를 임의로 늘리지 않았는가
    tdir = os.path.join(repo, "tracker")
    if os.path.isdir(tdir):
        extra = [f for f in sorted(os.listdir(tdir))
                 if f not in TRACKER_REQUIRED and not f.startswith(".")
                 and f not in ("experiments.yaml",)]
        for f in extra:
            w.append(f"계약에 없는 tracker 파일: tracker/{f} (연구형은 experiments.yaml만 허용)")

    # 3) 의도 문서를 저장소에 두지 않았는가 (Zone 경계)
    for rel in FORBIDDEN_DOCS:
        if os.path.isfile(os.path.join(repo, rel)):
            v.append(f"의도 문서가 저장소에 있음: {rel} — 볼트가 담당한다")

    # 4) 볼트 쪽 계약 문서가 있는가
    pdir = os.path.join(vault, link["project_path"])
    facts["project_dir"] = pdir
    if not os.path.isdir(pdir):
        v.append(f"볼트에 프로젝트가 없음: {link['project_path']}")
        return v, w, facts
    for rel in VAULT_REQUIRED.get(profile, VAULT_REQUIRED["personal-light"]):
        if not os.path.isfile(os.path.join(pdir, rel)):
            v.append(f"볼트 계약 문서 없음: {rel}  (profile={profile})")

    # 5) Grill Gate
    manifest = os.path.join(pdir, "project.yaml")
    grill = None
    if os.path.isfile(manifest):
        m = re.search(r"^grill:\s*(\S+)", open(manifest, encoding="utf-8").read(), re.M)
        grill = m.group(1) if m else None
    facts["grill"] = grill or "unknown"
    if grill == "pending":
        v.append("Grill Gate가 pending이다 — 구현을 시작하지 않는다")
    elif grill is None:
        w.append("Grill Gate를 통과한 적이 없다 — vaultos grill 을 먼저 실행한다")

    # 6) No Requirement, No Code — task가 REQ에 연결됐는가
    tpath = os.path.join(repo, "tracker", "tasks.yaml")
    if os.path.isfile(tpath):
        text = open(tpath, encoding="utf-8").read()
        ids = re.findall(r"^\s*-\s*id:\s*(\S+)", text, re.M)
        blocks = re.split(r"^\s*-\s*id:\s*", text, flags=re.M)[1:]
        # 빈 배열([])과 미기재를 모두 '연결 안 됨'으로 본다 (No Requirement, No Code)
        def linked(block):
            m = re.search(r"requirement_ids:\s*\[([^\]]*)\]", block)
            if m:
                return bool(m.group(1).strip())
            return bool(re.search(r"requirement_ids:\s*\n(\s+-\s*\S)", block))
        unlinked = [i for i, b in zip(ids, blocks) if not linked(b)]
        facts["tasks"] = len(ids)
        facts["unlinked"] = len(unlinked)
        if unlinked:
            v.append(f"Requirement에 연결되지 않은 task {len(unlinked)}개: {', '.join(unlinked[:5])}"
                     + (" …" if len(unlinked) > 5 else ""))
        # Evidence 없이 done
        done_no_ev = []
        for i, b in zip(ids, blocks):
            if re.search(r"status:\s*(done|completed)", b) and not re.search(r"evidence:\s*\n?\s*-\s*\S", b):
                done_no_ev.append(i)
        if done_no_ev:
            v.append(f"Evidence 없이 done인 task {len(done_no_ev)}개: {', '.join(done_no_ev[:5])}"
                     + (" …" if len(done_no_ev) > 5 else ""))

    # 7) REQ가 task로 이어졌는가 (반대 방향)
    rpath = os.path.join(pdir, "requirements", "requirements.yaml")
    if os.path.isfile(rpath) and os.path.isfile(tpath):
        reqs = re.findall(r"^\s*-\s*id:\s*(REQ-\S+)", open(rpath, encoding="utf-8").read(), re.M)
        ttext = open(tpath, encoding="utf-8").read()
        orphan = [r for r in reqs if r not in ttext]
        facts["requirements"] = len(reqs)
        if orphan:
            w.append(f"task로 이어지지 않은 Requirement {len(orphan)}개: {', '.join(orphan[:5])}"
                     + (" …" if len(orphan) > 5 else ""))
    return v, w, facts
