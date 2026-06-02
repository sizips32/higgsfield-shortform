---
name: bible-higgsfield-production
description: 성경 쇼츠 시나리오를 Higgsfield MCP 이미지/영상 생성 계획, 캐릭터 시트, GPT Image 2 웹툰형 키프레임 프롬프트, 한국어 전용 영상 프롬프트, 비용 승인 게이트로 변환한다. "Higgsfield", "힉스필드", "MCP 제작", "렌더", "키프레임", "GPT Image 2", "웹툰", "한국어 프롬프트", "영상 프롬프트", "캐릭터 일관성" 요청이면 반드시 사용한다.
allowed-tools: Read, Write, mcp__higgsfield.generate_image, mcp__higgsfield.generate_video, mcp__higgsfield.virality_predictor, mcp__higgsfield.media_upload, mcp__higgsfield.media_confirm, mcp__higgsfield.show_generations, mcp__higgsfield.show_medias
---

# bible-higgsfield-production

## 목적
성경 쇼츠 대본과 샷리스트를 실제 생성 가능한 MCP 전용 제작 계획으로 바꾼다. MCP 도구가 없으면 렌더를 실행하지 않고, 프롬프트 패키지와 중단 사유를 남긴다.

## 고정 제작 규칙
- 키프레임 이미지는 기본적으로 **GPT Image 2**를 사용한다. 도구 호출 시 모델 id는 `gpt_image_2`를 우선한다.
- 모든 키프레임은 **한국 웹툰 형식**으로 설계한다: 세로 9:16, 선명한 선화, 따뜻한 채색, 컷툰/웹툰식 표정 연기, 모바일에서 읽히는 큰 제스처.
- 사용자에게 보이는 산출물, `visual-bible.md`, `higgsfield-plan.md`, `prompts.json`의 프롬프트 문장은 **한국어만 사용**한다.
- 이미지나 영상 모델이 영어 프롬프트를 더 잘 이해할 수 있더라도, 이 하네스에서는 영어 프롬프트를 작성하지 않는다. 필요한 시각 정보는 한국어로 구체화한다.
- 영상 모델은 계속 Seedance 2.0을 기본으로 쓰되, `prompt_language`를 지정할 수 있으면 `ko` 또는 Korean에 해당하는 값을 사용한다.
- 화면 안 텍스트가 필요한 컷은 한국어만 넣고, 모델이 임의 영어/중국어/가짜 문자를 만들지 않도록 "화면 속 글자는 한국어 외 금지"를 프롬프트에 포함한다.

## 워크플로우
1. `script.md`와 `shotlist.md`를 읽는다.
2. `visual-bible.md`를 작성한다: 캐릭터, 장소, 색, 조명, 카메라, 자막 안전 영역.
3. 컷별 GPT Image 2 웹툰 키프레임 프롬프트와 한국어 영상 프롬프트를 만든다.
4. 비용이 발생하는 생성은 먼저 비용 산정 계획을 작성하고 사용자 승인을 요구한다.
5. 렌더 완료 후 `higgsfield-plan.md` 또는 `clips.json`에 결과를 기록한다.

## Higgsfield MCP 전용 도구
- 이미지 생성: `mcp__higgsfield.generate_image`가 있으면 키프레임에 사용한다. `model: "gpt_image_2"`를 기본값으로 사용한다.
- 영상 생성: `mcp__higgsfield.generate_video`를 사용한다. `get_cost: true`로 비용을 먼저 확인한다. 프롬프트는 한국어로 작성한다.
- 사용자 제공 파일: `mcp__higgsfield.media_upload` 후 업로드 명령 실행, `mcp__higgsfield.media_confirm`.
- 클립 평가: `mcp__higgsfield.virality_predictor`를 선택적으로 사용한다.
- 기존 결과 재사용: `mcp__higgsfield.show_generations` 또는 `show_medias`.

## MCP 미가용 처리
MCP가 없거나 실패하면 Higgsfield 생성을 실행하지 않는다.
- `higgsfield-plan.md`에 미가용 사유, 필요한 MCP 도구, 재시도 계획을 기록한다.
- 컷별 키프레임/영상 프롬프트는 계속 한국어 패키지로 남긴다.
- 비용 승인과 MCP 도구가 모두 준비된 뒤에만 실제 생성 단계로 재개한다.

## 산출물
`projects/<slug>/briefs/visual-bible.md`:
- 캐릭터 고정 정보.
- 장소별 무드.
- 컷별 화면 구도.
- 자막 위치와 여백.

`projects/<slug>/briefs/higgsfield-plan.md`:
- 사용할 모델과 이유.
- 컷별 GPT Image 2 웹툰 키프레임 프롬프트.
- 컷별 한국어 영상 프롬프트.
- 비용 게이트 체크리스트.
- 실패 시 재시도/단순화 계획.

## 비용 게이트
사용자 승인 전에는 실제 생성 작업을 시작하지 않는다. 승인 요청에는 다음을 포함한다.
- 생성할 컷 수.
- 모델.
- 예상 크레딧 또는 비용 확인 결과.
- 재시도 가능성.
- 비용을 줄이는 옵션.

## 관련 참조
모델 선택과 MCP 사용 세부 기준은 `references/higgsfield-mcp.md`를 읽는다.
