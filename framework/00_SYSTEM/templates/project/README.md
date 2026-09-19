# Project Template

## 시작하는 법

```
02_WORKSPACES/personal/projects/<slug>/project.yaml
```

**이 파일 하나면 시작이다.** `project.yaml`을 복사하고 `id` / `name` / `slug` / `mission`만 채운다.

나머지는 **실제로 필요해졌을 때** 추가한다. 미리 만들지 않는다.

## Profile별로 추가되는 것

| Profile | 추가 | 언제 올리는가 |
|---|---|---|
| `personal-light` | 없음. `project.yaml` 하나 | 기본값. 개인 실험은 전부 여기서 시작 |
| `personal-full` | `governance/constitution.md`<br>`requirements/requirements.yaml`<br>`evidence/` | 다른 사람이 쓰기 시작하거나, 되돌리기 어려운 결정이 쌓일 때 |
| `company-standard` | + `architecture/adr/`<br>`status/risks.yaml`<br>`status/decision-log.md` | 회사 업무 전부 |
| `company-strict` | + `logs/events.jsonl`<br>문서별 `classification`<br>Release Approval | 민감 데이터·외부 영향이 있을 때 |

프로필을 올리는 것은 쉽고, 내리는 것도 쉽다. **처음부터 무겁게 시작하지 않는다.**

## repo 연결

코드가 있으면 `repo.url`에 GitHub 주소를 적는다. **이게 프로젝트의 주소다.**

```yaml
repo:
  url: https://github.com/<you>/my-app
  local:
    wsl: /home/<you>/workspace/my-app
    mac: /Users/<you>/workspace/my-app
```

`local`은 기기마다 다르고 정본이 아니다. 비워둬도 된다.
**로컬 절대경로를 정본처럼 쓰지 않는다** — 다른 기기에서 열면 깨진 값이 된다.

## 주의

- 실행 정본(code, tests, `tracker/*.yaml`)은 repo에 둔다. 볼트로 복제하지 않는다.
- 별도 트래킹 표면을 선제적으로 만들지 않는다.
- 회사 프로젝트는 `company/` 아래에만 만들고, 개인 자료를 컨텍스트로 섞지 않는다.

규칙 전문: [[01_GOVERNANCE/project-policy|Project Policy]]
