# Bridge Promotion Rules

이 문서는 ProjectOS와 KnowledgeOS를 연결하는 승격 규칙입니다.

## 허용되는 이동

- project artifact -> permanent note
- knowledge note -> project reference

## 허용되지 않는 이동

- project tracker -> permanent note 직접 이동
- workspace mirror -> permanent note 직접 이동
- LLM 초안 -> permanent note 직접 이동

## 승격 시 메타데이터

- `voBridge: promoted_from_project`
- `voDomain: knowledge`
- 가능하면 `origin_project` 또는 `linked_project` 기록

## 참조 시 메타데이터

- project 문서는 필요하면 `voBridge: referenced_by_project`
- knowledge note는 원본 위치를 유지
