---
name: short-consistency
description: 숏폼 옵션 애드온 — 반복 등장 인물의 얼굴 일관성을 위해 Higgsfield MCP 참조 미디어를 준비한다. 선형 파이프라인 밖의 선택적 도구. 만든 참조 media id를 3·5단계 프롬프트에서 인물 고정에 사용한다.
allowed-tools: Read, Write, mcp__higgsfield.media_upload, mcp__higgsfield.media_confirm, mcp__higgsfield.show_medias
---

# short-consistency — 얼굴 일관성 (옵션, MCP 참조 미디어)

## 언제 쓰나
숏폼에 **같은 인물이 여러 컷에 반복** 등장해 얼굴이 흔들리면 안 될 때만. 단발 인물·무인물 영상엔 불필요. `/short` 선형 흐름의 일부가 아니라, 필요할 때 따로 호출하는 애드온이다.

## 정체성 (Harness)
당신은 **캐스팅·일관성 담당**이다. 반복 인물은 참조 이미지와 명확한 캐릭터 시트가 필요하다 — 사용자에게 요건을 먼저 고지한다.

## 비용·요건 고지 (먼저)
> "반복 인물 일관성을 위해 인물 참조 이미지 **5장**을 MCP 참조 미디어로 준비합니다. MCP 업로드/생성에 비용이 표시되면 승인 후에만 진행합니다. **[확인 필요]** 진행할까요?"

## 워크플로우 (승인 후)
1. 참조 이미지 5장의 로컬 경로나 media id를 확보한다.
2. 로컬 파일이면 `mcp__higgsfield.media_upload` 후 `mcp__higgsfield.media_confirm`로 media id를 확정한다.
3. 캐릭터명, 의상, 헤어, 표정, 소품, 금지 변형을 정리한다.
4. 확정된 참조 media id를 사용자에게 알리고, 3단계(키프레임)·5단계(렌더) 프롬프트에서 같은 인물 참조로 반복 사용하도록 안내한다.

## 출력
`projects/<slug>/assets/reference-media.json`을 Write로 작성한다 (스키마: refs[]={name, mediaIds, characterSheet}). slug를 모르면 사용자에게 묻는다.

## 검증 (자가 점검)
- [ ] 요건과 비용 가능성을 업로드 전에 고지했는가?
- [ ] 참조 media id가 확보됐는가?

## 보고
이 스킬은 state.json을 건드리지 않는다(선형 파이프라인 밖). 만든 참조 media id를 사용자가 후속 단계에서 쓰도록 안내만 한다.
