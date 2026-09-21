---
type: system
updated: 2026-09-21
---

# Channels

사람이 vault 상태를 폰/메신저로 묻고 답을 받는 면이다.

## 두 종류

| | Message Channels | Orchestration Surface |
|---|---|---|
| 예 | Slack, Telegram | Buzz류의 "사람+에이전트+프로젝트를 한곳에" 서비스 |
| 하는 일 | 텍스트로 묻고 답한다 | `08_DEVICES`/`04_AGENTS`를 직접 보고 여러 device의 에이전트를 하나의 풀로 다룬다 |

메시지 채널은 Query-Response(읽기 전용)부터 시작한다. Orchestration Surface는 그 채널이 실제로 있고 API가 열려 있을 때만 다음 단계다.

## 채널 목록

| 채널 | kind | 상태 |
|---|---|---|
| [[05_OPERATIONS/channels/slack\|Slack]] | message | not_connected |
| [[05_OPERATIONS/channels/telegram\|Telegram]] | message | not_connected |
| [[05_OPERATIONS/channels/openclaw\|OpenClaw]] (예시 — 지식 조사 오케스트레이터류) | message | not_connected |
| [[05_OPERATIONS/channels/buzz\|Orchestration Surface]] (예시 — Buzz류) | orchestration | not_connected |

## 필드 스키마

```yaml
channel: slack
kind: message                    # message | orchestration
status: not_connected            # not_connected | testing | active
scope: personal                  # personal | company | both
direction: [query_response]      # query_response | notify_out | capture_in | command_in
assistant_permission: read_only  # read_only | can_trigger_task | full
secret_ref: SLACK_BOT_TOKEN      # 값이 아니라 참조만 — 01_GOVERNANCE/data-policy §5
```

## 연결 순서

n8n(또는 동등한 자동화 엔진)이 모든 채널과 vault 사이의 접착제다 — Assistant는 채널 API를 직접 호출하지 않는다.

1. 자동화 엔진을 올릴 device 결정 — `08_DEVICES`에서 상시 온라인 후보 확인
2. 메시지 채널 하나를 먼저 `testing`으로 연결, Query-Response 하나만 검증
3. 검증되면 `status: active`로 올리고 다른 채널 진행
4. Orchestration Surface(command_in)는 메시지 채널의 Query-Response가 며칠 안정화된 뒤에만
