---
type: system
updated: 2026-09-21
---

# 07_PRODUCTS

**프로젝트가 아니라, 프로젝트에서 나와 지금 실제로 떠 있는 것을 관리하는 곳이다.**

`02_WORKSPACES`가 "무엇을 만들고 있는가"라면, `07_PRODUCTS`는 "무엇이 지금 돌아가고 있는가"다. 개발 진행 상태(Requirement, Task, CR, ADR)는 여전히 그 프로젝트의 `02_WORKSPACES/<workspace>/projects/<slug>/`에 남는다 — 여기로 옮기지 않는다. 여기 있는 건 **운영 상태 요약**뿐이다.

## 왜 필요한가

[[01_GOVERNANCE/aipm-trace|aipm-trace]]의 Project Lifecycle은 `RELEASE → MAINTENANCE → ARCHIVE`로 끝난다. 지금까지 VaultOS엔 RELEASE 이후를 위한 자리가 없었다 — 프로젝트 문서 안에 그대로 남거나, 아무 데도 기록되지 않았다. `07_PRODUCTS`는 그 자리다.

여기 등록되는 두 가지:

- **배포된 서비스/제품**: 프로젝트가 RELEASE에 도달해서 실제로 사용자가 쓰는 것
- **운영 중인 자동화**: 일회성 Task가 아니라 계속 돌아가는 프로세스 (스케줄러, 봇, 파이프라인) — 반드시 `02_WORKSPACES` 프로젝트에서 나올 필요는 없다

주의: `06_AUTOMATIONS`(아직 미생성)와 다른 것이다. `06_AUTOMATIONS`는 VaultOS **자신**을 검사·관리하는 내부 도구용(drift-detector 등)이고, `07_PRODUCTS`는 **사용자의** 제품·자동화를 위한 것이다.

## 구조

```text
07_PRODUCTS/
├── personal/
│   └── <product-slug>/
│       └── product.yaml
└── company/
    └── <product-slug>/
        └── product.yaml
```

`02_WORKSPACES`와 같은 이유로 personal/company를 물리적으로 분리한다 — [[01_GOVERNANCE/data-policy|Data Policy]].

## product.yaml

템플릿: `00_SYSTEM/templates/product/product.yaml`

최소 필드만 가진다 — task 목록이나 로그를 여기로 복제하지 않는다. 실제 헬스체크·로그·알림은 그 제품의 repo 또는 외부 모니터링 도구에 있다. 여기는 **"이게 지금 살아있는가, 어디서 왔는가"만** 요약한다.

## 언제 등록하는가

프로젝트가 `RELEASE`에 도달하면 등록한다. `status.phase`가 `maintenance`인 동안 유지하고, 서비스를 내리면 `status.state: retired`로 바꾸고 (지우지 않는다) `99_ARCHIVE`로 옮기지 않는다 — retired도 "한때 무엇이 떠 있었는가"의 기록이다.

## 지금 하지 않는 것

이 볼트는 운영되지 않는 구조를 미리 만들어두고 방치한 이력이 있다 ([[01_GOVERNANCE/vaultos-health|vaultos-health]] §5). 그래서 지금은 다음을 만들지 않는다.

- 별도 대시보드 자동화·알림 파이프라인 — 실제로 제품이 2~3개 등록되고 나서 필요하면 만든다
- incidents/, monitoring/ 같은 하위 폴더 — 실제로 장애가 나거나 모니터링 연동이 생기면 그때 추가한다

지금 있는 건 [[05_OPERATIONS/dashboard/30_products|Products Dashboard]] 하나뿐이다.
