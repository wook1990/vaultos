---
type: governance
policy: ecosystem
status: active
updated: 2026-09-19
---

# Ecosystem — 볼트와 저장소는 어떻게 하나로 움직이는가

정책과 구조가 있어도 **연결 장치가 없으면 사람이 매번 손으로 잇게 되고, 결국 복사로 해결하게 된다.**
이 문서는 그 연결 장치를 정의한다.

## 1. 문제

볼트와 작업 저장소는 서로 다른 곳에 있다. 기기마다 경로도 다르다.

```
볼트    클라우드 동기화 폴더 안        기기마다 경로가 다름
저장소  로컬 어딘가 + GitHub          기기마다 clone 위치가 다름
```

연결 장치가 없으면 이런 일이 생긴다.

- 저장소에서 일하는 에이전트가 **의도 계층(Requirement / ADR / 정책)을 찾지 못한다**
- 볼트가 **자기 프로젝트가 어디에 clone돼 있는지 모른다**
- 사람이 경로를 하드코딩하고, 기기가 바뀌면 깨진다
- 결국 **필요한 문서를 저장소로 복사한다** — 정본이 둘이 된다

마지막 항목이 핵심이다. **복제는 연결 장치가 없을 때 나오는 증상이다.**

## 2. 양방향 표식

연결은 두 개의 작은 파일로 이뤄진다. 둘 다 내용을 복사하지 않고 **주소만** 담는다.

### 저장소 쪽 — `.vaultos`

```
vault: /path/to/vault
workspace: personal
project: my-app
project_path: 02_WORKSPACES/personal/projects/my-app
```

저장소에서 일하는 에이전트는 이 파일을 보고 의도 계층을 찾는다.
**계약 본문을 저장소로 복사하지 않는다.**

### 볼트 쪽 — `project.yaml`의 `repo`

```yaml
repo:
  url: https://github.com/<you>/my-app   # 정본. 어느 기기에서든 같다
  branch: main
  local:
    this: /home/<you>/workspace/my-app   # 기기별. 정본 아님
```

`url`이 정본이고 `local`은 편의 정보다. 기기가 바뀌면 `local`만 달라진다.

## 3. 볼트를 찾는 순서

저장소나 에이전트가 볼트 위치를 결정하는 방법은 **하나로 고정한다.**

```
1. 명시적 인자        --vault <경로>
2. 환경변수           VAULTOS_HOME
3. 저장소의 .vaultos  (상위 디렉터리로 거슬러 올라가며 탐색)
4. 사용자 설정        ~/.config/vaultos/config
5. 클라우드 경로 탐색  Library/CloudStorage, Dropbox, OneDrive, /mnt/g ...
```

**경로를 문서나 코드에 하드코딩하지 않는다.** 하드코딩하는 순간 그 기기 전용이 된다.

## 4. 연결 시점

| 상황 | 방법 |
|---|---|
| 새 프로젝트 | `vaultos new <slug> --path <저장소>` — 볼트 등록과 저장소 표식을 한 번에 |
| 기존 저장소를 나중에 연결 | `vaultos link <slug>` |
| 다른 기기에서 처음 clone | `vaultos link <slug>` 한 번 더 — `local`만 그 기기 값으로 갱신 |

## 5. 상태가 흐르는 방향

```
저장소 tracker  ──요약──▶  볼트 project.yaml
   (정본)                    (요약만)
```

`vaultos sync`는 저장소의 `tracker/tasks.yaml`을 읽어 볼트의 `next_actions`와 `blocked`만 갱신한다.

**task 목록을 옮겨 적지 않는다.** 개수와 다음 할 일만 남긴다.
반대 방향(볼트 → 저장소)으로는 상태를 쓰지 않는다.

실행 시점은 **세션 종료 시 1회**다. 연속 자동 반영은 하지 않는다. → [[01_GOVERNANCE/sync-policy|Sync Policy]]

## 6. 이것이 에이전트 협업에 주는 것

여러 에이전트가 여러 저장소에서 동시에 일해도 다음이 성립한다.

| 질문 | 답이 나오는 곳 |
|---|---|
| 내가 지금 어느 프로젝트에 있는가 | 저장소의 `.vaultos` |
| 무엇을 만들기로 했는가 | 볼트의 `requirements/` |
| 왜 이 구조인가 | 볼트의 `architecture/adr/` |
| 무엇을 하면 안 되는가 | 볼트의 `01_GOVERNANCE/` |
| 내 역할의 경계는 | 볼트의 `04_AGENTS/<역할>/` |
| 지금 어디까지 왔는가 | 저장소의 `tracker/` (정본), 볼트의 `project.yaml` (요약) |

**모든 에이전트가 같은 한 곳을 읽는다.** 모델이 무엇이든, 저장소가 어디든 마찬가지다.
이것이 없으면 각 에이전트가 자기 저장소에 계약 사본을 만들기 시작하고, 사본은 곧 갈라진다.

## 7. 금지

- 볼트 경로를 문서·코드·설정에 하드코딩하는 것
- 계약·정책 문서를 저장소로 복사하는 것 (표식으로 가리킨다)
- `tracker` 내용을 볼트로 복제하는 것 (요약만)
- 볼트가 저장소의 상태를 덮어쓰는 것 (흐름은 한 방향)
