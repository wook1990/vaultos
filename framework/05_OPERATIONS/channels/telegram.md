---
type: channel
channel: telegram
kind: message
status: not_connected
scope: personal
direction: [query_response, capture_in]
assistant_permission: read_only
secret_ref: TELEGRAM_BOT_TOKEN
updated: 2026-09-21
---

# Telegram Channel

두 가지 독립 기능을 겸할 수 있다 — **섞지 않는다.** "인입과 분석을 분리한다" 원칙: 캡처와 분석 트리거는 항상 별도 흐름이다.

- **Query-Response**: slack.md와 같은 흐름. 질문 → Assistant → 답장
- **Capture-in**: 링크/텍스트를 보내면 `03_KNOWLEDGE/00_inbox`에 저장. 분석은 자동으로 이어지지 않는다 — 사람이 별도로 요청해야 한다. 이 둘을 하나로 합쳐서 "메시지가 오면 자동으로 분석까지 끝난다"로 만들지 않는다 — caution 없이 대량 처리되는 위험이 생긴다

## Query-Response 설정 체크리스트

1. **BotFather로 봇 생성**, 토큰 발급
2. **개인 Chat ID 확인**
3. `.env` 또는 n8n Secret에 `TELEGRAM_BOT_TOKEN`으로 저장
4. n8n에 Telegram Trigger 노드 → Assistant 질의 → Telegram 응답 워크플로 하나 구성 (slack.md와 동일한 패턴)

## Capture-in 설정 체크리스트

1. Telegram Trigger(n8n) 또는 Webhook으로 메시지를 받는다
2. `03_KNOWLEDGE`의 Inbox 규격(frontmatter)대로 `.md` 파일을 만들어 `03_KNOWLEDGE/00_inbox`에 쓴다
3. Obsidian은 클라우드 API가 아니므로 파일 쓰기는 로컬 스크립트/Local REST API 플러그인/git 커밋 중 하나를 거쳐야 한다
4. 분석 트리거(사람이 직접 요청, 또는 나중에 스케줄)는 별도 워크플로로 둔다 — 캡처 워크플로에 합치지 않는다

## 연결되면 바꿀 것

`status: not_connected` → `testing` → `active`로 이 파일 frontmatter를 갱신한다. Query-Response와 Capture-in을 각각 언제 켰는지 `direction` 배열로 구분해서 남긴다.
