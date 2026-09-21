---
type: channel
channel: buzz
kind: orchestration
status: not_connected
scope: personal
direction: []
assistant_permission: read_only
secret_ref: null
updated: 2026-09-21
---

# Orchestration Surface Channel (example: Buzz)

**목표 지점의 실제 UI.** 사람이 채널에서 "오늘 상황 정리해줘" → 답을 받고 → "그럼 진행해"라고 하면 여러 device의 에이전트가 동시에 움직이는 것 — 이걸 가능하게 하는 채널은 단순 메시지 채널(Slack/Telegram)과 다르다. `08_DEVICES` + `04_AGENTS`를 직접 참조해서 여러 device의 에이전트를 하나의 풀로 다룰 수 있어야 한다.

이런 도구(예: Buzz — "Your people, your agents, your project — all in one place" 류의 서비스)를 실제로 쓸 계획이 있다면 이 파일 이름과 `channel:` 값을 바꿔서 쓴다.

## 지금 하는 것

자리만 만든다. `status: not_connected` 유지 — 아직 API가 없거나 검증 전이면 먼저 만들지 않는다.

## 연결되면 할 것

1. `08_DEVICES`의 온라인 device 목록을 이 채널이 읽을 수 있게 연동
2. Query-Response부터 Slack/Telegram과 같은 패턴으로 검증
3. `command_in`(실제 작업 트리거)은 Query-Response가 며칠 안정화된 뒤 별도로 설계 — 한 번에 다 열지 않는다

## 참고

베타/미검증 서비스에 먼저 하네스를 맞추지 않는다 — `08_DEVICES`/`04_AGENTS`를 명확하게 만들어두는 것 자체가 이미 이 채널을 위한 준비다.
