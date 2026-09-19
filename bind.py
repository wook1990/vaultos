#!/usr/bin/env python3
"""워크스페이스에 VaultOS 계약 표면을 고정한다.

프로젝트 워크스페이스는 코드만 있는 곳이 아니다.
**VaultOS 계약에 종속되는 기능이 고정으로 설치된 곳**이다.

설치되는 것:

    .vaultos/contract.yaml   이 저장소가 따르는 계약 버전·프로필·게이트 상태
    .vaultos/link            볼트 주소와 프로젝트 경로
    tracker/*.yaml           계약이 정한 5개 스키마 (임의 확장 금지)
    AGENTS.md CLAUDE.md GEMINI.md   볼트 계약을 가리키는 진입점 (복사하지 않는다)
    .githooks/pre-commit     Grill 미완료·계약 위반 시 경고 (선택)

고정의 뜻: 이 파일들이 없거나 어긋나면 `vaultos validate`가 실패한다.
"""

import os
import stat

CONTRACT_VERSION = "1.0"

TRACKER_FILES = {
    "tasks.yaml": """# 계약 스키마. 이 5개 외에 tracker 파일을 임의로 늘리지 않는다.
# task는 반드시 requirement_ids에 연결된다 (No Requirement, No Code).
tasks: []
""",
    "issues.yaml": """# issue는 영향 범위와 연결 task를 반드시 가진다.
issues: []
""",
    "decisions.yaml": """# decision은 context와 consequence가 없으면 incomplete다.
decisions: []
""",
    "releases.yaml": """# release는 known_risks가 빈 채로 끝나지 않는다.
releases: []
""",
    "progress.md": """# Progress

## (날짜)

- 이번 주 목표:
- 진행 중:
- 막힌 것:
- 결정 필요:
- 다음 액션:
""",
}

AGENT_ENTRY = """# {title}

이 저장소는 VaultOS의 **Zone A(실행 정본)**다. 코드·테스트·`tracker/*.yaml`이 여기 있다.

## 먼저 읽을 것

의도 계층(왜 이렇게 만들기로 했는가)은 이 저장소가 아니라 **볼트**에 있다.
경로는 `.vaultos/link`에 있다. **계약 본문을 이 저장소로 복사하지 않는다.**

```
<vault>/{project_path}/
├── project.yaml                 진입점. 이것부터 읽는다
├── intake/grill.md              Grill Gate — 무엇을 왜 만들기로 했는가
├── governance/constitution.md   불변 원칙 / Non-Goals
├── requirements/requirements.yaml
└── architecture/adr/
```

공통 규칙: `<vault>/00_SYSTEM/VAULTOS.md`, `<vault>/01_GOVERNANCE/`

## 이 저장소에서 하는 일

| 대상 | 규칙 |
|---|---|
| `src/` `tests/` | 구현. **REQ에 연결된 task 없이 기능을 추가하지 않는다** |
| `tracker/tasks.yaml` | task 생성·상태 전이. **Evidence 없이 done으로 바꾸지 않는다** |
| `tracker/issues.yaml` | 영향 범위와 연결 task를 반드시 남긴다 |
| `tracker/decisions.yaml` | context와 consequence가 없으면 incomplete |

tracker는 **단일 쓰기**다. 쓰기 전 `git pull`, 쓰기 후 즉시 커밋. 커밋 메시지에 task id를 넣는다.

## 계약이 막는 것

```sh
vaultos validate      # 계약 준수 검사. 실패하면 구현을 시작하지 않는다
vaultos grill         # Grill Gate. pending이면 구현 시작 전이다
vaultos sync          # 세션 종료 시 1회. 볼트에 상태 요약만 보낸다
```

- Grill Gate가 `pending`이면 **구현을 시작하지 않는다**
- Requirement 변경은 볼트에서 CR을 거친다
- 구조 변경은 볼트에서 ADR을 남긴다
- 의도 문서(product-brief, roadmap 등)를 이 저장소에 만들지 않는다
"""

PRE_COMMIT = """#!/bin/sh
# VaultOS 계약 검사. 설치: git config core.hooksPath .githooks
# 차단하지 않고 경고만 한다. 강제하려면 exit 1 로 바꾼다.

if command -v vaultos >/dev/null 2>&1; then
  vaultos validate --quiet || {
    echo ""
    echo "  VaultOS 계약 검사에 걸렸습니다. 'vaultos validate' 로 확인하세요."
    echo "  계속하려면 --no-verify 를 쓰되, 왜 우회하는지 기록에 남기세요."
    echo ""
  }
fi
exit 0
"""


def bind(repo, vault, scope, slug, profile="personal-light", force=False):
    made, skipped = [], []

    d = os.path.join(repo, ".vaultos")
    if os.path.isfile(d):          # 구버전 단일 파일 → 디렉터리로 승격
        os.remove(d)
    os.makedirs(d, exist_ok=True)

    project_path = f"02_WORKSPACES/{scope}/projects/{slug}"

    with open(os.path.join(d, "link"), "w", encoding="utf-8") as fh:
        fh.write(f"""# 이 저장소가 속한 VaultOS 프로젝트.
vault: {vault}
workspace: {scope}
project: {slug}
project_path: {project_path}
""")
    made.append(".vaultos/link")

    cpath = os.path.join(d, "contract.yaml")
    if force or not os.path.exists(cpath):
        with open(cpath, "w", encoding="utf-8") as fh:
            fh.write(f"""# 이 저장소가 따르는 VaultOS 계약.
# 내용을 복사하지 않는다. 무엇을 따르는지만 선언한다.

contract_version: {CONTRACT_VERSION}
governance_profile: {profile}

# 계약이 요구하는 것 — vaultos validate 가 검사한다
requires:
  tracker: [tasks.yaml, issues.yaml, decisions.yaml, releases.yaml, progress.md]
  entrypoints: [AGENTS.md, CLAUDE.md, GEMINI.md]
  vault_documents:
    - project.yaml
    - intake/grill.md
    - governance/constitution.md
    - requirements/requirements.yaml

# 계약이 금지하는 것
forbids:
  - tracker 스키마를 임의로 늘리는 것
  - 의도 문서(product-brief, roadmap, architecture)를 이 저장소에 두는 것
  - 볼트 계약 본문을 이 저장소로 복사하는 것
  - Requirement 없이 기능을 추가하는 것
  - Evidence 없이 task를 done 처리하는 것

# Grill Gate — 볼트의 project.yaml 이 정본이다. 여기는 캐시다.
grill: unknown
""")
        made.append(".vaultos/contract.yaml")
    else:
        skipped.append(".vaultos/contract.yaml")

    tdir = os.path.join(repo, "tracker")
    os.makedirs(tdir, exist_ok=True)
    for name, body in TRACKER_FILES.items():
        p = os.path.join(tdir, name)
        if os.path.exists(p) and not force:
            skipped.append(f"tracker/{name}")
            continue
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(body)
        made.append(f"tracker/{name}")

    for fn, title in (("AGENTS.md", "Codex Agent Instructions"),
                      ("CLAUDE.md", "Claude Instructions"),
                      ("GEMINI.md", "Gemini Instructions")):
        p = os.path.join(repo, fn)
        if os.path.exists(p) and not force:
            skipped.append(fn)
            continue
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(AGENT_ENTRY.format(title=title, project_path=project_path))
        made.append(fn)

    hdir = os.path.join(repo, ".githooks")
    os.makedirs(hdir, exist_ok=True)
    hp = os.path.join(hdir, "pre-commit")
    if force or not os.path.exists(hp):
        with open(hp, "w", encoding="utf-8") as fh:
            fh.write(PRE_COMMIT)
        os.chmod(hp, os.stat(hp).st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        made.append(".githooks/pre-commit")
    else:
        skipped.append(".githooks/pre-commit")

    return made, skipped


def read_link(repo):
    p = os.path.join(repo, ".vaultos", "link")
    if not os.path.isfile(p):
        p = os.path.join(repo, ".vaultos")      # 구버전 단일 파일
        if not os.path.isfile(p):
            return None
    data = {}
    with open(p, encoding="utf-8") as fh:
        for line in fh:
            if ":" in line and not line.strip().startswith("#"):
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip()
    return data or None
