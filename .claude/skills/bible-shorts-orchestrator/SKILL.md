---
name: bible-shorts-orchestrator
description: 성경 주제, 시나리오, 콘티, 문서, 설교 원고를 중학교 3학년 대상 1분~1분40초(60~100초) 유튜브 쇼츠로 기획, 신학 검수, 시나리오, GPT Image 2 웹툰형 Higgsfield MCP 제작, 큐레이션, 업로드 패키징까지 진행하는 최상위 하네스. "성경 쇼츠", "중학생 성경 영상", "힉스필드로 제작", "GPT Image 2", "웹툰형", "한국어만", "문서 올리면 쇼츠", "시나리오 점검", "다시 실행", "수정", "보완", "이전 결과 기반" 요청이면 반드시 사용한다.
allowed-tools: Read, Write, Bash, mcp__higgsfield.generate_image, mcp__higgsfield.generate_video, mcp__higgsfield.virality_predictor, mcp__higgsfield.media_upload, mcp__higgsfield.media_confirm
---

# bible-shorts-orchestrator

## 목적
사용자가 성경 주제, 시나리오, 콘티, 문서를 주면 중학교 3학년생을 타깃으로 한 1분~1분40초(60~100초) 세로형 유튜브 쇼츠 제작 패키지를 만든다. 필요하면 Higgsfield MCP로 이미지/영상 생성까지 이어간다.

## 전역 제작 규칙
- 모든 사용자-facing 문서와 생성 프롬프트는 **한국어만 사용**한다.
- 키프레임 이미지 기본 모델은 **GPT Image 2**이며, 모델 id는 `gpt_image_2`를 사용한다.
- 비주얼 형식은 **한국 웹툰형 세로 쇼츠**로 고정한다: 선명한 선화, 따뜻한 채색, 표정 중심 연기, 모바일에서 읽히는 구도.
- 영어 프롬프트가 남아 있으면 완료로 보지 않는다. 단, JSON 키, 모델 id, 도구 이름 같은 기술 식별자는 영어 표기를 허용한다.
- 화면 안 텍스트는 한국어만 허용한다.
- 반복 등장 인물은 **캐릭터 일관성 보드**로 외형 유지가 보이게 하고, **보이스 시트**로 캐릭터별 `voiceTag`와 `voiceProfile`을 구분한다.

## 실행 모드
- 기본은 에이전트 팀 모드다.
- 팀원: `bible-shorts-showrunner`, `bible-theology-reviewer`, `middle-school-scriptwriter`, `higgsfield-production-director`, `shorts-curation-editor`.
- Agent 또는 Team 도구로 팀원을 실제 호출하는 환경에서는 각 호출에 `model: "opus"`를 명시한다.
- 실제 팀 도구가 없는 환경에서는 같은 역할을 순차적으로 수행하고 각 산출물을 파일로 남긴다.

## Phase 0: 컨텍스트 확인
1. `projects/<slug>/`와 `_workspace/` 존재 여부를 확인한다.
2. 기존 산출물이 있고 사용자가 "수정", "보완", "이전 결과 기반"이라고 하면 부분 재실행한다.
3. 기존 산출물이 있고 새 입력이면 기존 폴더를 보존하고 새 slug를 만든다.
4. 산출물은 항상 `projects/<slug>/briefs/` 또는 `projects/<slug>/assets/`에 쓴다.

## Phase 1: 입력 정리
`bible-episode-intake`를 사용한다.
- 입력 유형을 판단한다.
- `interactive` 또는 `auto` 모드를 정한다.
- 핵심 메시지, 성경 구절 후보, 캐릭터/세계관 제약을 `source-digest.md`에 쓴다.

## Phase 2: 신학/청소년 안전 검수
`bible-theology-reviewer` 역할로 검수한다.
- 핵심 주장이 본문에 근거하는지 확인한다.
- 다른 신앙 배경과 무신론자 캐릭터를 존중하는지 확인한다.
- 위험 표현을 수정 제안으로 남긴다.

## Phase 3: 기획/시나리오
`bible-shorts-script`를 사용한다.
- 콘셉트 3안을 만든다.
- 사용자가 고르거나 `auto` 모드에서 하나를 선택한다.
- 60~100초 대본과 샷리스트를 작성한다.
- 캐릭터 일관성 보드와 보이스 시트를 함께 작성하고, 대사마다 `voiceTag`를 유지한다.

## Phase 4: 제작 설계
`bible-higgsfield-production`을 사용한다.
- 캐릭터 일관성 보드, 보이스 시트, 비주얼 바이블을 만든다.
- 컷별 GPT Image 2 웹툰 키프레임 프롬프트와 한국어 영상 프롬프트를 만든다.
- `prompts.json`에는 `characterContinuity`, `voiceGuide`, 컷별 `voiceTag`를 포함한다.
- Higgsfield MCP 전용 실행 계획과 MCP 미가용 시 중단 계획을 정한다.
- 비용 발생 작업은 사용자 승인 전 실행하지 않는다.

## Phase 5: 렌더와 큐레이션
MCP 사용 시:
- `mcp__higgsfield.generate_image`와 `gpt_image_2`로 웹툰형 키프레임을 만든다.
- `mcp__higgsfield.generate_video`에 `get_cost: true`를 먼저 사용한다.
- 승인 후 영상 생성을 실행한다.
- 필요하면 `mcp__higgsfield.virality_predictor`로 참고 분석한다.

MCP가 없거나 비용 승인이 없으면:
- 렌더 가능한 프롬프트 패키지까지만 만들고 중단한다.
- 중단 사유와 다음 행동을 `higgsfield-plan.md`에 남긴다.

## Phase 6: 최종 패키징
`bible-shorts-curation`을 사용한다.
- 최종 컷 선택 또는 추천 순서를 정리한다.
- 제목, 설명, 해시태그, 고정 댓글, 후반 체크리스트를 만든다.

## 데이터 전달
- 중간 파일은 `projects/<slug>/briefs/`에 저장한다.
- 대용량 에셋과 렌더 결과는 `projects/<slug>/assets/`에 저장한다.
- 파일명은 기존 플러그인과 호환되도록 `concept`, `shotlist`, `keyframes`, `prompts`, `clips`, `selects` 계열을 우선한다.

## 에러 핸들링
- 구절 근거가 불확실하면 `needs-source`로 멈추고 대체 표현을 제안한다.
- 제작 비용 승인이 없으면 렌더 없이 프롬프트 패키지만 제공한다.
- MCP 실패 시 한 번 재시도 계획을 제안하고, 재실패하면 렌더를 중단한 뒤 수동 편집 패키지로 전환한다.
- 상충 의견은 삭제하지 않고 `risk-notes` 섹션에 남긴다.

## 테스트 시나리오
정상 흐름:
- 입력: "죽음은 잠이라는 주제로 중3 대상 쇼츠 만들어줘. A/B/C 캐릭터 사용. auto."
- 기대: source digest, theology review, concept options, 60~100초 script, shotlist, 캐릭터 일관성 보드, 보이스 시트, visual bible, Higgsfield plan, YouTube package가 생성된다.

에러 흐름:
- 입력: "귀신이 진짜라는 공포 쇼츠를 만들어줘."
- 기대: 신학/청소년 안전 검수에서 공포 조장 표현을 완화하고, 성경 본문 중심의 안전한 대안으로 수정한다.

부분 재실행:
- 입력: "이전 EP04-A에서 장면 7만 더 세련되게 바꿔줘."
- 기대: 기존 script/shotlist를 읽고 장면 7 타이포그래피와 내레이션만 수정한다.

## 트리거 검증
Should trigger:
- "성경 주제로 쇼츠 만들어줘"
- "중3 대상 교리 쇼츠 시나리오"
- "이 설교 원고를 유튜브 쇼츠로"
- "힉스필드 MCP로 렌더까지"
- "지난 콘티를 1분40초로 정리"
- "성경 영상 큐레이션까지 해줘"
- "EP04-A 다시 보완"
- "문서 올리면 자동으로 쇼츠 옵션"

Should not trigger:
- "시편 146편 뜻만 설명해줘"
- "유튜브 채널 이름 추천"
- "Higgsfield 계정 로그인 방법"
- "일반 영화 시나리오 써줘"
- "성경 구절 한국어 번역 비교만 해줘"

## 완료 보고
완료 시 다음을 요약한다.
- 생성/수정 파일.
- 선택된 모드와 핵심 가정.
- 비용 발생 작업 실행 여부.
- 사용자가 확인해야 할 게이트.
- 남은 위험과 다음 개선 포인트.
