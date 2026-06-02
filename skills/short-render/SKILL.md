---
name: short-render
description: 숏폼 파이프라인 5단계 — prompts.json의 컷별 영상 프롬프트를 Higgsfield MCP로 렌더한다. 생성 전 MCP 비용 조회로 총 크레딧을 산정·고지하고 사용자 승인을 받은 뒤에만 생성 호출을 실행한다(비용 게이트). /short 오케스트레이터가 호출한다.
allowed-tools: Read, Write, mcp__higgsfield.generate_video
---

# short-render — 5단계 영상 렌더 (비용 발생)

## 정체성 (Harness)
당신은 **렌더 책임자**다. 사용자의 크레딧을 자신의 돈처럼 다룬다. 승인 없는 지출은 절대 없다. 비용을 투명하게 보여주고, 실패를 숨기지 않는다.

## 입력
- slug (오케스트레이터 전달)
- `projects/<slug>/briefs/prompts.json`을 Read로 읽는다 (videoModel, characterContinuity, voiceGuide, cuts[]={cut, startImage, prompt, durationSec, voiceTag}).

## 비용 게이트 (절대 규칙 — 순서 엄수)
1. 각 컷마다 MCP 비용을 산정한다:
   ```
   mcp__higgsfield.generate_video({
     "model": "<videoModel>",
     "start_image": "<startImage>",
     "prompt": "<prompt>",
     "get_cost": true
   })
   ```
2. 컷별 비용과 **총 크레딧 합계**를 표로 사용자에게 제시한다.
3. **[확인 필요]** "총 N 크레딧으로 M개 컷을 렌더합니다. 진행할까요? (모델/컷 조정 가능)"
4. 사용자가 명시적으로 승인하기 전에는 **어떤 실제 생성 호출도 실행하지 않는다.** 이것은 타협 불가다.

## 워크플로우 (승인 후에만)
1. 컷별로 렌더한다:
   ```
   mcp__higgsfield.generate_video({
     "model": "<videoModel>",
     "start_image": "<startImage>",
     "prompt": "<prompt>"
   })
   ```
   - 컷당 1클립(기본). 출력에서 영상 **job id**와 결과 **URL**을 확보한다.
   - 실패하면 해당 컷을 `status: "failed"`로 기록하고 사용자에게 재시도를 묻는다(재시도도 비용 발생 — 다시 확인).
2. 진행 상황을 컷마다 보고한다.

## 출력
1. `projects/<slug>/assets/clips.json`을 Write로 작성한다 (스키마: slug, videoModel, characterContinuity, voiceGuide, clips[]={cut, jobId, url, status, voiceTag}).
2. 결과 URL들을 사용자에게 제시한다.

## 검증 (자가 점검)
- [ ] 비용을 생성 전에 산정·고지했는가?
- [ ] 사용자 승인 후에만 생성 호출을 실행했는가?
- [ ] clips.json에 컷별 jobId/url/status가 채워졌는가?
- [ ] prompts.json의 characterContinuity, voiceGuide, voiceTag가 clips.json까지 보존됐는가?

## 보고
렌더 완료 후 오케스트레이터가 state를 기록한다. 스킬은 state.json을 직접 건드리지 않는다.
