#!/usr/bin/env python3
"""VaultOS 구조 검사기.

REQ-LINT-001 루트 구조 / REQ-LINT-002 깨진 링크 / REQ-LINT-003 프로젝트 허브.
ADR-001에 따라 표준 라이브러리만 사용하고 전체를 1패스로 스캔한다.

사용법:
    python3 src/vaultos_health.py <vault_path>
    VAULT_PATH=<vault_path> python3 src/vaultos_health.py

종료 코드: 0 = error 없음, 1 = error 있음
"""

import os
import re
import sys
from collections import defaultdict

REQUIRED_ROOTS = [
    "00_SYSTEM", "01_GOVERNANCE", "02_WORKSPACES", "03_KNOWLEDGE",
    "04_AGENTS", "05_OPERATIONS", "98_PERSONAL", "99_ARCHIVE",
]
REQUIRED_SYSTEM_DOCS = ["00_SYSTEM/VAULTOS.md", "00_SYSTEM/architecture.md"]
REQUIRED_GOVERNANCE_DOCS = [
    "01_GOVERNANCE/README.md", "01_GOVERNANCE/aipm-trace.md",
    "01_GOVERNANCE/project-policy.md", "01_GOVERNANCE/agent-policy.md",
    "01_GOVERNANCE/data-policy.md", "01_GOVERNANCE/sync-policy.md",
]
ALLOWED_ROOT_FILES = {"CLAUDE.md", "AGENTS.md", "GEMINI.md"}
VALID_PROFILES = {"personal-light", "personal-full", "company-standard", "company-strict"}
# 출처: 01_GOVERNANCE/project-policy.md §2. 이 표를 바꾸려면 정책 문서를 먼저 고친다.
PROFILE_REQUIRED_FILES = {
    "personal-light": ["project.yaml"],
    "personal-full": ["project.yaml", "governance/constitution.md",
                      "status/current-state.yaml", "requirements/requirements.yaml"],
    "company-standard": ["project.yaml", "governance/constitution.md",
                         "requirements/requirements.yaml", "status/current-state.yaml"],
    "company-strict": ["project.yaml", "governance/constitution.md",
                       "requirements/requirements.yaml", "status/current-state.yaml"],
}
SKIP_DIRS = {".obsidian", ".git", "node_modules"}
LINK_RE = re.compile(r"\[\[([^\]\|#\^]+)")
FENCE_RE = re.compile(r"```.*?```|~~~.*?~~~", re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


def strip_code(text):
    """코드 펜스와 인라인 코드를 제거한다.

    Obsidian은 백틱 안의 [[...]]를 링크로 해석하지 않는다(ISSUE-002).
    링크를 예시로 인용하는 문서가 오탐되는 것을 막는다.
    """
    text = FENCE_RE.sub("", text)
    return INLINE_CODE_RE.sub("", text)


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, check, message):
        self.items.append((level, check, message))

    def count(self, level):
        return sum(1 for lv, _, _ in self.items if lv == level)

    def render(self):
        order = {"error": 0, "warn": 1, "note": 2}
        icon = {"error": "ERROR", "warn": "WARN ", "note": "note "}
        lines = []
        for lv, check, msg in sorted(self.items, key=lambda x: (order[x[0]], x[1])):
            lines.append(f"  [{icon[lv]}] {check}: {msg}")
        return "\n".join(lines)


def scan_vault(root):
    """1패스 스캔. ADR-001: Drive 마운트에서 프로세스 spawn을 피한다."""
    notes = {}          # 확장자 제외 상대경로 -> 실제 경로 (.md 전용)
    by_basename = defaultdict(list)
    all_files = set()   # 확장자 포함 상대경로 전체 (.md 아닌 파일도 링크 대상이 될 수 있다)
    root_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            if os.path.dirname(rel) == "":
                root_files.append(rel)
            all_files.add(rel)
            if fn.endswith(".md"):
                notes[rel[:-3]] = rel
                by_basename[fn[:-3]].append(rel)
    return notes, by_basename, root_files, all_files


def check_root_structure(root, root_files, report):
    """REQ-LINT-001"""
    for name in REQUIRED_ROOTS:
        if not os.path.isdir(os.path.join(root, name)):
            report.add("error", "root-structure", f"표준 루트 없음: {name}/")
    for doc in REQUIRED_SYSTEM_DOCS + REQUIRED_GOVERNANCE_DOCS:
        if not os.path.isfile(os.path.join(root, doc)):
            report.add("error", "required-doc", f"필수 문서 없음: {doc}")
    for fn in sorted(root_files):
        if fn not in ALLOWED_ROOT_FILES and not fn.startswith("."):
            report.add("warn", "root-loose-file", f"루트에 정리되지 않은 파일: {fn}")


def check_links(root, notes, by_basename, all_files, report, include_archive=False):
    """REQ-LINT-002

    .md가 아닌 파일(project.yaml 등)로의 위키링크도 대상이 될 수 있다 —
    Obsidian은 어떤 파일이든 링크할 수 있다. all_files로 확장자 포함
    정확히 존재하는지 먼저 확인하고, 없을 때만 .md 전용 인덱스(notes)로
    폴백한다.
    """
    broken_paths = 0
    unwritten = defaultdict(list)
    for rel_dir, actual in sorted(notes.items()):
        if not include_archive and actual.startswith("99_ARCHIVE/"):
            continue
        try:
            with open(os.path.join(root, actual), encoding="utf-8") as fh:
                text = fh.read()
        except (OSError, UnicodeDecodeError) as exc:
            report.add("warn", "unreadable", f"{actual}: {exc}")
            continue
        base_dir = os.path.dirname(actual)
        for match in LINK_RE.finditer(strip_code(text)):
            target = match.group(1).strip().rstrip("\\")   # 표 안의 \| 이스케이프
            if not target or target.startswith("http") or "{{" in target:
                continue                                    # 템플릿 치환자 제외
            if target in all_files:
                continue                                     # 확장자 포함 정확히 존재 (.md 아닌 파일 포함)
            if target.startswith("./") or target.startswith("../"):
                resolved = os.path.normpath(os.path.join(base_dir, target)).replace(os.sep, "/")
                if resolved in notes or resolved in all_files:
                    continue
            if target in notes or os.path.basename(target) in by_basename:
                continue
            if "/" in target:
                report.add("error", "broken-link", f"{actual} -> [[{target}]]")
                broken_paths += 1
            else:
                unwritten[target].append(actual)
    for target, sources in sorted(unwritten.items(), key=lambda x: -len(x[1])):
        report.add("note", "unwritten-note",
                   f"[[{target}]] — 아직 만들지 않은 노트 ({len(sources)}곳에서 참조)")
    return broken_paths, len(unwritten)


def read_profile(path):
    """project.yaml에서 governance_profile만 뽑는다. YAML 파서 없이(TC-002)."""
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                if line.startswith("governance_profile:"):
                    return line.split(":", 1)[1].split("#")[0].strip()
    except OSError:
        pass
    return None


def check_projects(root, report):
    """REQ-LINT-003"""
    counts = []
    for scope in ("personal", "company"):
        base = os.path.join(root, "02_WORKSPACES", scope, "projects")
        if not os.path.isdir(base):
            continue
        for slug in sorted(os.listdir(base)):
            proj = os.path.join(base, slug)
            if not os.path.isdir(proj):
                continue
            label = f"{scope}/{slug}"
            n = sum(len(f) for _, _, f in os.walk(proj))
            counts.append((label, n))
            manifest = os.path.join(proj, "project.yaml")
            if not os.path.isfile(manifest):
                report.add("error", "project-hub", f"{label}: project.yaml 없음")
                continue
            profile = read_profile(manifest)
            if profile not in VALID_PROFILES:
                report.add("error", "project-hub",
                           f"{label}: governance_profile 값이 유효하지 않음 ({profile})")
                continue
            for required in PROFILE_REQUIRED_FILES[profile]:
                if not os.path.isfile(os.path.join(proj, required)):
                    report.add("error", "project-hub",
                               f"{label} ({profile}): 필수 파일 없음 — {required}")
            if scope == "company" and profile.startswith("personal"):
                report.add("error", "workspace-boundary",
                           f"{label}: company 프로젝트가 personal 프로필을 쓰고 있음")
    return counts


def main(argv):
    root = argv[1] if len(argv) > 1 else os.environ.get("VAULT_PATH")
    if not root:
        print("사용법: vaultos_health.py <vault_path>  (또는 VAULT_PATH 환경변수)")
        return 2
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        print(f"경로를 찾을 수 없음: {root}")
        return 2

    report = Report()
    notes, by_basename, root_files, all_files = scan_vault(root)
    check_root_structure(root, root_files, report)
    broken, unwritten = check_links(root, notes, by_basename, all_files, report)
    counts = check_projects(root, report)

    print(f"VaultOS Health Check — {root}")
    print(f"  md {len(notes)}개 스캔 / 프로젝트 {len(counts)}개\n")
    if counts:
        print("프로젝트 파일 수")
        for label, n in counts:
            print(f"  {n:4d}  {label}")
        print()
    body = report.render()
    print(body if body else "  문제 없음")
    print(f"\nerror {report.count('error')} / warn {report.count('warn')} "
          f"/ note {report.count('note')}")
    return 1 if report.count("error") else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
