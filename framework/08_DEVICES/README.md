---
type: system
updated: 2026-09-21
---

# 08_DEVICES

**지금 뭐가 어디서 돌고 있는가.** `02_WORKSPACES`가 "무엇을 만들고 있는가", `07_PRODUCTS`가 "무엇이 배포됐는가"라면, 여기는 그것들이 **물리적으로 어느 기기 위에서** 돌아가는지를 기록한다.

## 구조

```text
08_DEVICES/
├── personal/
│   └── <device-slug>/
│       └── device.yaml
└── company/
    └── <device-slug>/
        └── device.yaml
```

Personal/Company를 물리적으로 분리한다 — `02_WORKSPACES`, `07_PRODUCTS`와 같은 이유. 회사 업무용 기기가 생기면 `company/`에 등록한다.

## device.yaml

템플릿: `00_SYSTEM/templates/device/device.yaml`

## 원칙

- **기기 개수에 의존하지 않는다.** 몇 대든 등록 방식은 같다
- `runs.products`로 `07_PRODUCTS`를 참조만 한다 — 제품 상태를 여기 복제하지 않는다
- `last_seen`은 사람이 세션 끝에 손으로 갱신한다. 자동 heartbeat는 아직 안 만든다(MVP 원칙)
- 구독 계정으로 도는 CLI 코딩 에이전트(Claude Code, Codex CLI, Gemini CLI 등)는 API 키가 아니라 로그인 세션으로 돈다 — 그래서 에이전트는 항상 여기 등록된 특정 기기에 묶여 실행된다(`runs.agents`)

## 새 기기 등록

1. `00_SYSTEM/templates/device/device.yaml`을 복사해 `08_DEVICES/<personal|company>/<slug>/device.yaml`로 저장
2. 필드를 채운다 (없어도 되는 필드는 비워둔다)
3. `05_OPERATIONS/dashboard/40_devices.md`에 한 줄 추가
