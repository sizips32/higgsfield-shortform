---
description: 숏폼/릴스 영상 7단계 파이프라인 오케스트레이터 (M1: 1·2단계). 한 줄 로그라인으로 기획·시나리오를 진행하고 게이트에서 승인받는다.
argument-hint: "\"<로그라인>\" | --resume <slug>"
allowed-tools: Bash, Read, Write, Skill
---

# /short — 숏폼 파이프라인 오케스트레이터

상태 헬퍼: `python3 lib/state.py` (프로젝트 루트에서 실행). 절대 state.json을 직접 편집하지 말 것 — 모든 상태 전이는 헬퍼로만.

## 라우팅

- 인자가 `--resume <slug>` → **재개 모드**
- 인자가 따옴표 로그라인 → **신규 모드**
- 인자 없음 → 사용법 안내

## 신규 모드

1. 로그라인에서 slug 생성 (영문 소문자·하이픈, 예: "지하철 우산" → `subway-umbrella` 또는 음역). 비어있거나 200자 초과면 거부.
2. `python3 lib/state.py init <slug> --logline "<로그라인>"` 실행. 종료코드 1(이미 존재)이면 다른 slug 제안 또는 `--resume` 안내.
3. **1단계로 진입** (아래 "단계 실행" 참조).

## 재개 모드

1. `python3 lib/state.py resume <slug>` 실행 → `STEP\tNAME\tSTATUS` 파싱.
2. 종료코드 2면 "프로젝트 없음" 안내 후 종료.
3. 해당 currentStep부터 "단계 실행".

## 단계 실행 (M1 구현: 1·2단계)

### currentStep == 1 (기획)
1. `Skill` 도구로 `short-ideate` 호출 (slug, 로그라인 전달).
2. 스킬이 `projects/<slug>/briefs/concept.md`를 쓰고 사용자 선택을 받는다.
3. 선택 확정 후: `python3 lib/state.py set-output <slug> 1 --file briefs/concept.md`
4. 사용자 승인 시: `python3 lib/state.py approve <slug> 1`
5. `python3 lib/state.py advance <slug>` → 종료코드 0이면 2단계로. 코드 3이면 "게이트 미승인" — 진행 차단, 사용자에게 재확인.

### currentStep == 2 (시나리오)
1. `Skill` 도구로 `short-script` 호출.
2. 스킬이 `projects/<slug>/briefs/shotlist.md`를 쓰고 승인을 받는다.
3. `python3 lib/state.py set-output <slug> 2 --file briefs/shotlist.md`
4. 승인 시: `python3 lib/state.py approve <slug> 2`
5. `python3 lib/state.py advance <slug>`.

### currentStep == 3 (스타일·키프레임)
1. `Skill` 도구로 `short-style` 호출 (slug 전달).
2. 스킬이 비용을 고지하고 사용자 승인 후 키프레임을 생성, `projects/<slug>/assets/keyframes.json`을 쓴다.
3. 톤 확정 후: `python3 lib/state.py set-output <slug> 3 --file assets/keyframes.json`
4. 사용자 승인 시: `python3 lib/state.py approve <slug> 3`
5. `python3 lib/state.py advance <slug>` → 코드 0이면 4단계로. 코드 3이면 차단.

### currentStep == 4 (영상 프롬프트 — 자동, 게이트 없음)
1. `Skill` 도구로 `short-prompt` 호출 (slug 전달).
2. 스킬이 `projects/<slug>/briefs/prompts.json`을 쓴다.
3. `python3 lib/state.py set-output <slug> 4 --file briefs/prompts.json`
4. `python3 lib/state.py advance <slug>` (4단계는 gate=false라 approve 불필요).

### currentStep == 5 (영상 렌더 — 비용 발생)
1. `Skill` 도구로 `short-render` 호출 (slug 전달).
2. 스킬이 Higgsfield MCP 비용 조회로 총 비용을 고지하고 **사용자 승인 후에만** 렌더, `projects/<slug>/assets/clips.json`을 쓴다.
3. 렌더 완료 후: `python3 lib/state.py set-output <slug> 5 --file assets/clips.json`
4. 사용자 승인 시: `python3 lib/state.py approve <slug> 5`
5. `python3 lib/state.py advance <slug>` → 코드 0이면 6단계로. 코드 3이면 차단.

### currentStep == 6 (큐레이션 — 인간 안목 강제)
1. `Skill` 도구로 `short-curate` 호출 (slug 전달).
2. 스킬이 virality 점수를 참고로 제시하고, **사용자가 직접 최종 컷을 선별**해 `projects/<slug>/briefs/selects.md`를 쓴다.
3. 선별 후: `python3 lib/state.py set-output <slug> 6 --file briefs/selects.md`
4. 사용자 승인 시: `python3 lib/state.py approve <slug> 6`
5. `python3 lib/state.py advance <slug>`.

### currentStep == 7 (후반 체크리스트 — 게이트 없음, 종결)
1. 7단계가 이미 done이면 "파이프라인 완료"로 간주한다(아래 완료 안내).
2. 아니면 `Skill` 도구로 `short-post` 호출 (slug 전달).
3. 스킬이 `projects/<slug>/briefs/post-checklist.md`를 쓴다.
4. `python3 lib/state.py set-output <slug> 7 --file briefs/post-checklist.md`
5. **파이프라인 완료 안내**:
   > "🎬 파이프라인 완료. 산출물: `projects/<slug>/` (concept·shotlist·keyframes·prompts·clips·selects·post-checklist). 사운드·컬러·업스케일은 체크리스트대로 외부 NLE에서 마감하세요. 반복 인물 일관성이 필요하면 `short-consistency` 스킬로 MCP 참조 미디어를 준비할 수 있습니다."

## 완료 후
모든 단계가 끝나면 산출물 위치를 요약하고 종료한다. 추가 단계 없음.

## 규칙
- 한 단계 끝나면 반드시 `advance`로 게이트를 통과해야 다음 단계로 간다.
- `advance` 종료코드 3 = 차단. 절대 우회하지 말 것.
- 비용 발생 단계(5)는 반드시 Higgsfield MCP 비용 게이트와 사용자 승인을 통과해야 한다.
