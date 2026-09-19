#!/usr/bin/env python3
"""VaultOS 초기화.

이 저장소를 clone한 뒤 실행하면, 지정한 위치에 VaultOS 환경을 만든다.

    python3 init.py                    # 대화형
    python3 init.py --path <경로> --storage gdrive --company

저장소 백엔드에 따라 동기화 정책이 달라지므로 시작할 때 묻는다.
표준 라이브러리만 사용한다.
"""

import argparse
import os
import shutil
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMEWORK = os.path.join(HERE, "framework")

ROOTS = [
    ("00_SYSTEM", "VaultOS 자체 정의, 규약, 스키마, 템플릿, 마이그레이션 기록"),
    ("01_GOVERNANCE", "공통 통제 정책 — 프로젝트별로 복사하지 않고 참조한다"),
    ("02_WORKSPACES", "실제 작업 — personal / company 물리 분리"),
    ("03_KNOWLEDGE", "재사용 지식 — 프로젝트 상태와 분리"),
    ("04_AGENTS", "에이전트 역할 계약"),
    ("05_OPERATIONS", "사람이 보는 통제 화면"),
    ("98_PERSONAL", "업무와 무관한 개인 기록"),
    ("99_ARCHIVE", "삭제하지 않고 내리는 곳"),
]

SUBDIRS = [
    "02_WORKSPACES/personal/projects",
    "03_KNOWLEDGE/00_inbox",
    "03_KNOWLEDGE/10_fleeting",
    "03_KNOWLEDGE/20_permanent",
    "03_KNOWLEDGE/references",
    "04_AGENTS/curation",
    "05_OPERATIONS/dashboard",
    "05_OPERATIONS/reviews",
    "05_OPERATIONS/reports",
    "99_ARCHIVE/_backups",
]

# 저장소 백엔드별 동기화 성질. sync-policy.md에 주입된다.
STORAGE = {
    "gdrive": {
        "label": "Google Drive",
        "merge": False,
        "conflict": "`파일명 (conflict YYYY-MM-DD-HH-MM-SS).ext` 사본을 조용히 만든다. 알림이 없다.",
        "history": "파일 단위 버전 기록 30일 (웹에서 복원)",
        "note": "여러 기기가 같은 파일을 동시에 쓰면 충돌 사본이 생긴다. 규칙 1~2를 반드시 지킨다.",
    },
    "dropbox": {
        "label": "Dropbox",
        "merge": False,
        "conflict": "`파일명 (사용자 conflicted copy 날짜).ext` 사본을 만든다.",
        "history": "파일 단위 버전 기록 30일 (플랜에 따라 더 김)",
        "note": "Drive와 성질이 같다. 병합이 없으므로 단일 쓰기를 지킨다.",
    },
    "onedrive": {
        "label": "OneDrive",
        "merge": False,
        "conflict": "`파일명-기기이름.ext` 사본을 만들거나 충돌 해결을 요구한다.",
        "history": "파일 단위 버전 기록 (플랜에 따라 다름)",
        "note": "병합이 없다. 단일 쓰기를 지킨다.",
    },
    "icloud": {
        "label": "iCloud Drive",
        "merge": False,
        "conflict": "충돌 사본을 만들고, 앱에 따라 사용자에게 선택을 요구한다.",
        "history": "제한적",
        "note": "동기화 지연이 길 수 있다. 기기 전환 시 완료를 반드시 확인한다.",
    },
    "obsidian-sync": {
        "label": "Obsidian Sync (구독)",
        "merge": True,
        "conflict": "자체 충돌 처리와 버전 기록을 제공한다.",
        "history": "볼트 단위 버전 기록 (플랜에 따라 1~12개월)",
        "note": "동기화 계층이 충돌을 다뤄주므로 규칙이 가장 느슨해도 된다. 단 코드는 여전히 git에 둔다.",
    },
    "git": {
        "label": "Git 저장소 자체를 볼트로",
        "merge": True,
        "conflict": "git이 병합한다. 충돌 시 명시적으로 해결해야 한다.",
        "history": "전체 이력",
        "note": "병합은 되지만 첨부파일이 커지면 저장소가 무거워진다. 모바일 접근이 불편하다.",
    },
    "local": {
        "label": "로컬 전용 (동기화 없음)",
        "merge": True,
        "conflict": "해당 없음",
        "history": "없음 — 백업이 유일한 복구 수단",
        "note": "기기 간 공유가 필요해지면 그때 백엔드를 고른다.",
    },
}


def ask(prompt, default=None, choices=None):
    while True:
        hint = f" [{default}]" if default else ""
        raw = input(f"{prompt}{hint}: ").strip()
        val = raw or default
        if not val:
            print("  값이 필요합니다.")
            continue
        if choices and val not in choices:
            print(f"  다음 중 하나여야 합니다: {', '.join(choices)}")
            continue
        return val


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def inject_storage_section(vault, storage_key):
    """sync-policy.md 앞에 이 볼트의 백엔드 성질을 박아넣는다."""
    meta = STORAGE[storage_key]
    path = os.path.join(vault, "01_GOVERNANCE", "sync-policy.md")
    with open(path, encoding="utf-8") as fh:
        s = fh.read()
    block = f"""
## 0. 이 볼트의 저장소 백엔드

> `init` 시점에 기록된 값이다. 백엔드를 바꾸면 이 절을 다시 작성한다.

| 항목 | 값 |
|---|---|
| 백엔드 | **{meta['label']}** (`{storage_key}`) |
| 병합 지원 | {'있음' if meta['merge'] else '**없음 — 마지막 저장자 우선**'} |
| 충돌 시 동작 | {meta['conflict']} |
| 버전 기록 | {meta['history']} |

{meta['note']}

"""
    anchor = "## 1. 정본은 하나가 아니라 둘이다"
    s = s.replace(anchor, block.lstrip() + anchor, 1)
    write(path, s)


def write_obsidian_config(vault, company):
    """Obsidian이 바로 열 수 있는 최소 설정. 플러그인 없이도 동작한다."""
    import json
    d = os.path.join(vault, ".obsidian")
    os.makedirs(d, exist_ok=True)
    conf = {
        "app.json": {
            "attachmentFolderPath": "03_KNOWLEDGE/references/_attachments",
            "alwaysUpdateLinks": True,       # 볼트 안에서 파일을 옮기면 링크를 자동 갱신
            "newLinkFormat": "absolute",     # 경로 링크를 기본으로 — 구조 이동에 강하다
            "useMarkdownLinks": False,
            "promptDelete": False,
        },
        "appearance.json": {"accentColor": "", "theme": "obsidian"},
        "core-plugins.json": {
            "file-explorer": True, "global-search": True, "switcher": True,
            "graph": True, "backlink": True, "outgoing-link": True,
            "tag-pane": True, "page-preview": True, "templates": True,
            "note-composer": True, "command-palette": True, "outline": True,
            "word-count": True, "file-recovery": True, "bookmarks": True,
        },
        "templates.json": {"folder": "00_SYSTEM/templates"},
        "hotkeys.json": {},
    }
    for name, data in conf.items():
        with open(os.path.join(d, name), "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
    os.makedirs(os.path.join(vault, "03_KNOWLEDGE/references/_attachments"), exist_ok=True)


def main():
    ap = argparse.ArgumentParser(description="VaultOS 환경을 생성한다")
    ap.add_argument("--path", help="볼트를 만들 경로")
    ap.add_argument("--storage", choices=sorted(STORAGE), help="저장소 백엔드")
    ap.add_argument("--company", action="store_true", help="company 워크스페이스도 생성")
    ap.add_argument("--force", action="store_true", help="비어있지 않은 경로에도 설치")
    args = ap.parse_args()

    interactive = not (args.path and args.storage)
    if interactive:
        print("VaultOS 초기화\n")
        print("볼트를 어디에 만들지 정합니다. 클라우드 동기화 폴더 안을 권장합니다.")
        print("예) ~/Library/CloudStorage/GoogleDrive-.../My Drive/vault")
        print("    /mnt/g/My Drive/vault   |   ~/Dropbox/vault\n")

    vault = os.path.abspath(os.path.expanduser(
        args.path or ask("볼트 경로")))

    if interactive:
        print("\n저장소 백엔드를 고릅니다. 동기화 정책이 여기에 따라 달라집니다.\n")
        for k, v in STORAGE.items():
            mark = "병합 O" if v["merge"] else "병합 X"
            print(f"  {k:<15} {v['label']}  ({mark})")
        print()
    storage = args.storage or ask("백엔드", default="gdrive", choices=sorted(STORAGE))

    company = args.company
    if interactive and not company:
        company = ask("company 워크스페이스도 만들까요? (y/n)", default="n").lower().startswith("y")

    if os.path.isdir(vault) and os.listdir(vault) and not args.force:
        existing = os.path.join(vault, "00_SYSTEM", "VAULTOS.md")
        if os.path.exists(existing):
            print(f"\n이미 VaultOS가 설치된 경로입니다: {vault}")
            print("덮어쓰려면 --force 를 붙입니다.")
            return 1
        print(f"\n경로가 비어있지 않습니다: {vault}")
        if not ask("계속할까요? (y/n)", default="n").lower().startswith("y"):
            return 1

    # 1) 루트 골격
    for name, _ in ROOTS:
        os.makedirs(os.path.join(vault, name), exist_ok=True)
    for sub in SUBDIRS:
        os.makedirs(os.path.join(vault, sub), exist_ok=True)
    if company:
        os.makedirs(os.path.join(vault, "02_WORKSPACES/company/projects"), exist_ok=True)

    # 2) 프레임워크 문서 배치
    for rel in ("00_SYSTEM", "01_GOVERNANCE", "04_AGENTS", "05_OPERATIONS"):
        src = os.path.join(FRAMEWORK, rel)
        dst = os.path.join(vault, rel)
        for dirpath, _, filenames in os.walk(src):
            for fn in filenames:
                s = os.path.join(dirpath, fn)
                d = os.path.join(dst, os.path.relpath(s, src))
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)

    # 3) 백엔드 성질 주입
    inject_storage_section(vault, storage)

    # 3.5) Obsidian 볼트로 즉시 열 수 있게
    write_obsidian_config(vault, company)

    # 4) 볼트 설정 기록
    write(os.path.join(vault, "00_SYSTEM", "vault-config.yaml"), f"""# 이 볼트의 설치 설정. init이 기록한다.

vaultos_version: {open(os.path.join(HERE, 'VERSION')).read().strip()}
initialized: {date.today().isoformat()}

storage:
  backend: {storage}          # {STORAGE[storage]['label']}
  merge_support: {str(STORAGE[storage]['merge']).lower()}
  # 백엔드를 바꾸면 01_GOVERNANCE/sync-policy.md §0을 다시 쓴다

workspaces:
  personal: true
  company: {str(company).lower()}
""")

    # 5) 에이전트 진입 포인터
    pointer = """# {title}

**먼저 `00_SYSTEM/VAULTOS.md`를 읽는다.** 이 볼트의 최상위 운영 문서다.

- 공통 에이전트 계약: `01_GOVERNANCE/agent-policy.md`
- 프로젝트 작업: `01_GOVERNANCE/project-policy.md`
- 지식 작업: `01_GOVERNANCE/knowledge-policy.md`
- 승인이 필요한 변경: `01_GOVERNANCE/approval-policy.md`
- 동기화 규칙: `01_GOVERNANCE/sync-policy.md`

작업 전 확인: 이 작업은 `personal`인가 `company`인가. 두 워크스페이스의 컨텍스트를 섞지 않는다.
"""
    for fn, title in (("CLAUDE.md", "Claude Instructions"),
                      ("AGENTS.md", "Codex Agent Instructions"),
                      ("GEMINI.md", "Gemini Instructions")):
        write(os.path.join(vault, fn), pointer.format(title=title))

    # 6) 영역 README
    write(os.path.join(vault, "02_WORKSPACES/personal/README.md"),
          "# Personal Workspace\n\n개인 프로젝트 영역이다. 현재 비어 있다.\n\n"
          "새 프로젝트는 `00_SYSTEM/templates/project/project.yaml` 하나를 복사해서 시작한다.\n"
          "→ `01_GOVERNANCE/project-policy.md`\n")
    if company:
        write(os.path.join(vault, "02_WORKSPACES/company/README.md"),
              "# Company Workspace\n\n회사 업무 영역이다. `company-standard` 이상 프로필로 시작한다.\n\n"
              "개인 자료를 이 영역의 컨텍스트에 넣지 않는다. → `01_GOVERNANCE/data-policy.md`\n")
    write(os.path.join(vault, "03_KNOWLEDGE/README.md"),
          "# Knowledge\n\n```\n00_inbox/    새 입력\n10_fleeting/  정리 중\n"
          "20_permanent/ 장기 재사용 지식\nreferences/   참조 자료\n```\n\n"
          "규칙: `01_GOVERNANCE/knowledge-policy.md`\n")
    write(os.path.join(vault, "99_ARCHIVE/README.md"),
          "# Archive\n\n삭제하지 않고 내리는 곳이다. **여기 있는 내용을 현재 기준으로 인용하지 않는다.**\n")
    write(os.path.join(vault, "00_SYSTEM/migrations/README.md"),
          "# Migrations\n\n구조를 바꿀 때마다 무엇을 왜 바꿨는지 여기에 남긴다.\n"
          "파일명: `YYYY-MM-DD_<주제>.md`\n\n**끝난 것은 끝났다고 적는다.** "
          "조건부 항목을 미완 과제처럼 남겨두지 않는다.\n")

    print(f"\nVaultOS를 만들었습니다: {vault}")
    print(f"  백엔드: {STORAGE[storage]['label']}")
    print(f"  워크스페이스: personal{' + company' if company else ''}")
    print("\n다음:")
    print(f"  1. Obsidian에서 이 폴더를 볼트로 엽니다 (.obsidian 설정 생성됨)")
    print(f"  2. 00_SYSTEM/VAULTOS.md 를 읽습니다")
    print(f"  3. 구조 검사: python3 {os.path.join(HERE, 'tools/vaultos_health.py')} \"{vault}\"")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n중단했습니다.")
        sys.exit(130)
