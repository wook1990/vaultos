# Products Dashboard

`07_PRODUCTS`에 등록된, 실제로 떠 있는 제품·자동화 현황이다. 개발 진행 상태는 [[05_OPERATIONS/dashboard/10_projects|Projects Dashboard]]에서 본다 — 여기는 운영 상태만 본다.

```dataviewjs
const rows = [];
for (const p of dv.pages()) {
  if (!p.file.path.includes("07_PRODUCTS/")) continue;
  if (p.file.name !== "product") continue;
  rows.push([p.file.link, p.type, p.status?.state ?? "-", p.status?.last_verified ?? "-"]);
}
dv.table(["제품/자동화", "type", "상태", "마지막 확인"], rows);
```

> Dataview는 `.yaml`을 직접 읽지 못한다. 제품 수가 늘면 각 항목에 짧은 `.md` 인덱스 노트를 추가하거나, 이 블록을 지우고 `07_PRODUCTS/`를 직접 연다. **대시보드가 안 돌아간다고 시스템이 멈추지는 않는다.**

## 점검 리듬

- `status.state: live`인데 `last_verified`가 오래됐으면 한 번 확인한다
- 서비스를 내렸으면 지우지 말고 `retired`로 바꾼다

기준: [[07_PRODUCTS/README|07_PRODUCTS]]
