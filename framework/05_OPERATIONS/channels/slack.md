---
type: channel
channel: slack
kind: message
status: not_connected
scope: personal
direction: [query_response]
assistant_permission: read_only
secret_ref: SLACK_BOT_TOKEN
updated: 2026-09-21
---

# Slack Channel

Query-Response 전용으로 시작한다. 예약 알림(Notify-out)은 나중 선택지다 — 아쉬워지면 그때 별도로 설계한다. 처음부터 둘 다 만들지 않는다.

## 목표 흐름

```
[폰 Slack] "F-018 어디까지 됐어?"
      │
      ▼
   Slack Incoming Webhook → n8n
      │  scope(personal) 확인
      ▼
   n8n → 08_DEVICES에서 온라인 device 확인 → 그 device의 Assistant 하네스 세션에 질문 전달
      │  Assistant가 project.yaml / dashboard / 08_DEVICES / 07_PRODUCTS 읽음 (read_only)
      ▼
   n8n → Slack으로 답장
```

## 설정 체크리스트 (사용자가 직접 해야 하는 것)

1. **Slack App 생성** — [api.slack.com/apps](https://api.slack.com/apps)에서 새 앱, 워크스페이스 선택 (개인 워크스페이스 또는 기존 워크스페이스 안 비공개 채널 `#ops-me`)
2. **Bot Token Scopes** — 최소 `chat:write`, 메시지 수신을 위해 Event Subscriptions에서 `message.channels` 또는 `message.im` 구독
3. **Incoming Webhook 활성화** — 응답 전송용
4. **Bot Token 발급** — `.env` 또는 n8n Secret에 `SLACK_BOT_TOKEN`으로 저장. **이 문서나 다른 vault 문서에 직접 쓰지 않는다** ([[01_GOVERNANCE/data-policy|data-policy]] §5)
5. **n8n에 Webhook 노드 + Slack 노드 워크플로 하나 구성** — 위 "목표 흐름" 그대로
6. 질문 1개("오늘 뭐 해야 돼?")로 끝까지 테스트

## 참고

- Slack의 공식 문서를 직접 확인하고 시작한다(Incoming Webhooks, Event Subscriptions) — API 세부사항은 자주 바뀐다
- `reminders.add` 류의 축소/퇴역 방향 API에 핵심 기능을 의존하지 않는다

## 연결되면 바꿀 것

`status: not_connected` → `testing` → `active`로 이 파일 frontmatter를 갱신한다.
