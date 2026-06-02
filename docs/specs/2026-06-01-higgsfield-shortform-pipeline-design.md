# Higgsfield 숏폼 영상 제작 파이프라인 플러그인 — 설계 문서

- **작성일**: 2026-06-01
- **상태**: 승인됨 (브레인스토밍 완료)
- **출처 영감**: 허준호 감독 「AI 영상 제작 노하우」 (티타임즈TV) — 7단계 AI 영화 제작 파이프라인
- **방법론**: harness-engineering (구조가 모델 품질을 이긴다)

---

## 1. 목표 (Goal)

한 줄 로그라인 입력만으로 **숏폼/릴스(15~60초 세로형)** 영상을 기획부터 완성까지 안내하는
**엔드투엔드 오케스트레이터 플러그인**을 만든다. 허준호 감독의 7단계 제작 철학을 숏폼에 맞게
재구성하고, 각 단계를 Claude Code 스킬로 모듈화하며, 기계적 작업은 자동화하되 **창작 판단 단계는
인간 안목 게이트로 강제**한다.

### 핵심 원칙
1. **"AI가 가짜라면, 이야기만큼은 진짜여야 한다"** — 스토리텔링·훅 중심.
2. **스마트 게이트** — 기계적 단계는 자동, 창작 판단(컨셉·시나리오·큐레이션)은 사용자 승인 필수.
3. **하네스 레이어** — 각 창작 스킬에 5기둥 구조를 주입해 AI를 "신중한 협업자"로 만든다.
4. **MCP 단일화** — Higgsfield 생성, 비용 조회, 업로드, 큐레이션은 MCP 도구로만 수행하고 별도 명령줄 경로를 두지 않는다.

---

## 2. 스코프 결정 (브레인스토밍 합의)

| 항목 | 결정 | 근거 |
|---|---|---|
| 범위 | **풀 파이프라인 오케스트레이터** | 7단계 전체를 하나의 진입점으로 |
| 자동화 | **하이브리드 스마트 게이트** | 기계적=자동, 창작판단=강제 게이트 |
| 산출물 | **숏폼/릴스 15~60초 세로형** | 훅·리텐션 중심, virality predictor 직결 |
| 중국어 압축 프롬프트 | **제외** | 단편영화용 고밀도 기법, 숏폼엔 과함 |

### Out of Scope (YAGNI)
- 4000자 중국어 압축 프롬프트 엔진
- 단편영화/롱폼 포맷
- 실제 후반작업(NLE 편집·컬러그레이딩) 자동 실행 — 7단계는 **체크리스트 안내만**
- 멀티에이전트 병렬 팬아웃 (선형+인간게이트 파이프라인과 충돌)

---

## 3. 연동 사실 (검증됨)

| 항목 | 실제 상태 |
|---|---|
| Higgsfield 연동 | **Higgsfield MCP 전용**. 이미지, 영상, 업로드, 큐레이션을 MCP 도구로 호출한다. |
| 주요 MCP 도구 | `mcp__higgsfield.generate_image`, `mcp__higgsfield.generate_video`, `mcp__higgsfield.media_upload`, `mcp__higgsfield.media_confirm`, `mcp__higgsfield.virality_predictor`, `mcp__higgsfield.show_generations`, `mcp__higgsfield.show_medias` |
| Virality Predictor | `mcp__higgsfield.virality_predictor` — 훅 강도·어텐션·리텐션·산만도·창의 점수 |
| 기존 스킬 | 단계별 `short-*` 스킬은 MCP 도구 호출 지침을 담는 하네스 레이어로 사용한다. |
| 기존 harness-engineering | 5기둥 시스템 프롬프트 빌더 (정체성·환경·워크플로우·검증·보고) |

> MCP 연결과 크레딧이 필요하다. 렌더 단계는 비용 발생 — 게이트에서 MCP 비용 조회 결과를 사용자에게 고지한다.

---

## 4. 파이프라인 매핑 (허준호 7단계 → 숏폼)

| # | 단계 | 게이트 | 주요 도구 | 산출물 |
|---|---|---|---|---|
| 1 | **기획** 로그라인→컨셉·훅 | 🚪 승인 | LLM | `briefs/concept.md` |
| 2 | **시나리오** 15~60s 비트시트·샷리스트 | 🚪 승인 | LLM | `briefs/shotlist.md` |
| 3 | **스타일·키프레임 이미지** | 자동→🚪 톤 확인 | `mcp__higgsfield.generate_image` (GPT Image 2, 웹툰형) | `assets/keyframes/` |
| 4 | **샷별 영상 프롬프트 설계** | 자동 | LLM (한국어만, CN 없음) | `briefs/prompts.json` |
| 5 | **영상 생성** i2v 다중 클립 | 자동 (사전 비용 고지) | `mcp__higgsfield.generate_video` (Seedance 2.0 / Kling 3.0) | `assets/clips/` |
| 6 | **큐레이션·선별** | 🚪 **인간 안목 강제** | `mcp__higgsfield.virality_predictor` + 사용자 | `briefs/selects.md` |
| 7 | **후반 체크리스트** 사운드·컬러·업스케일 | 가이드 | 외부툴 안내 | `briefs/post-checklist.md` |

- **일관성**: 인물 등장 시 MCP 참조 미디어와 캐릭터 시트로 얼굴·의상 정보를 반복 주입한다. 공간/사물 상대위치는 프롬프트 템플릿에 명세.
- **게이트 정의**: 🚪 = 사용자 승인 없이 다음 단계 진행 불가. 자동 = 사용자 개입 없이 진행하되 결과는 state에 기록.

---

## 5. 아키텍처

### 5.1 선택안: 오케스트레이터 커맨드 + 단계별 서브스킬 (1안)
`/short` 커맨드가 상태머신을 구동한다. 7단계 각각은 독립 스킬이며 단독 호출도 가능하다.
오케스트레이터는 `state.json`을 읽어 현재 단계를 파악하고, 다음 단계 스킬을 실행한 뒤
게이트에서 멈춰 사용자 승인을 기다린다.

**기각된 대안**
- 2안 멀티에이전트 팬아웃: 선형+인간게이트와 충돌. 과설계.
- 3안 오케스트레이터 없는 스킬 모음: 엔드투엔드 목표 상실.

### 5.2 플러그인 구조
```
my_higgsfield/
  plugin.json                 # 플러그인 매니페스트
  commands/
    short.md                  # 오케스트레이터 진입점 (/short)
  skills/
    short-ideate/SKILL.md     # 1단계 기획
    short-script/SKILL.md     # 2단계 시나리오
    short-style/SKILL.md      # 3단계 스타일·키프레임
    short-prompt/SKILL.md     # 4단계 영상 프롬프트
    short-render/SKILL.md     # 5단계 렌더 (Higgsfield MCP)
    short-curate/SKILL.md     # 6단계 큐레이션 (virality+게이트)
    short-post/SKILL.md       # 7단계 후반 체크리스트
  lib/
    state.py                  # state 헬퍼 CLI (read/write/gate-check) — Python 3.12
    state_schema.md           # state.json 스키마 문서
  docs/specs/                 # 본 설계 문서 위치
```

> **런타임 결정**: state 로직은 **스크립트 기반**(`lib/state.py`, Python 3.12.9). 마크다운 스킬/커맨드는 신뢰성이 필요한 원자적 쓰기·손상 복구·게이트 차단을 보장할 수 없으므로, LLM은 창작 콘텐츠만 담당하고 상태 전이는 헬퍼가 담당한다. Higgsfield 생성 경로는 MCP로만 연결한다.

### 5.3 상태 저장 (멀티세션 대응)
프로젝트별 워크스페이스를 작업 디렉토리 하위에 둔다.
```
projects/<slug>/
  state.json     # { slug, currentStep, steps:{1..7:{status, gateApproved, output}}, createdAt }
  briefs/        # concept.md, shotlist.md, prompts.json, selects.md, post-checklist.md
  assets/        # keyframes/, clips/
```
- 오케스트레이터는 매 호출 시 `python lib/state.py read <slug>`로 재개 지점을 결정한다.
- 게이트 통과는 `state.py approve <slug> <step>` → `gateApproved: true` 기록. 세션이 끊겨도 승인 이력 보존.
- **게이트 강제**: 다음 단계 진입 전 `state.py can-advance <slug> <step>`가 직전 게이트 승인 여부를 검사해 미승인 시 비정상 종료코드 반환 → 오케스트레이터가 진행 차단. (마크다운 honor-system 아님.)
- **불변성·원자성**: `state.py`가 새 객체로 작성 후 temp→rename 원자적 쓰기. 매 쓰기 전 `state.json.bak` 백업. 손상 시 백업 복구.
- **헬퍼 인터페이스(M1 확정)**: `init|read|set-output|approve|can-advance|resume` 서브커맨드. 표준 라이브러리만 사용, 외부 의존성 없음.

### 5.4 하네스 레이어 (차별점)
각 **창작 단계 스킬**(1·2·4·6)은 harness-engineering 5기둥 구조를 내장한다:
1. **정체성** — 사용자=감독/매니저, AI=숏폼 전문 작가·연출.
2. **환경** — 출력 형식, `[확인 필요]` 태그, 시스템 프롬프트 누설 금지.
3. **워크플로우** — 단계별 질문·산출 절차.
4. **검증** — 산출물 자가 점검(훅 존재? 길이 적정? 일관성?).
5. **보고** — state 기록 + 게이트 요약 제시.

---

## 6. 데이터 흐름 (예시: 1회 실행)

```
사용자: /short "지하철에서 우산을 건네는 낯선 사람"
 → [1 기획] 컨셉·훅 3안 제시 → 🚪 사용자 선택/수정
 → [2 시나리오] 6컷 비트시트·샷리스트 → 🚪 승인
 → [3 스타일] 키프레임 이미지 자동 생성 → 🚪 톤 확인
 → [4 프롬프트] 샷별 i2v 프롬프트 자동 설계
 → [5 렌더] 비용 고지 → 클립 N개 자동 생성
 → [6 큐레이션] virality 점수 + 사용자 선별 🚪 (인간 안목 강제)
 → [7 후반] 사운드·컬러·업스케일 체크리스트 안내
```

각 화살표 후 `state.json` 갱신. 중단 시 `/short --resume <slug>`로 재개.

---

## 7. 에러 처리

| 상황 | 처리 |
|---|---|
| Higgsfield MCP 미가용 | 필요한 MCP 도구 목록을 안내하고 생성 없이 프롬프트 패키지까지만 제공 |
| MCP 인증/권한 문제 | 연결 상태 확인을 요청하고 게이트에서 중단 |
| 크레딧 부족 | 렌더 게이트에서 비용 고지·중단, 충전 안내 |
| 렌더 job 실패/타임아웃 | MCP 결과 조회로 상태 확인, 재시도 옵션, state에 실패 기록 |
| state.json 손상 | 백업(`state.json.bak`)에서 복구 시도, 불가 시 사용자에게 단계 재확인 |
| 사용자 입력 검증 | 로그라인 빈값·과길이 거부, slug 충돌 시 경고 |

---

## 8. 테스트 전략

- **단위**: state 스키마 읽기/쓰기/재개 로직(원자적 쓰기, 손상 복구).
- **계약**: 각 스킬의 입출력(브리프 파일 생성, state 갱신) 검증 — 실제 MCP 호출은 mock.
- **게이트**: 승인 전 다음 단계 진입 차단 확인.
- **스모크(수동)**: 인증된 환경에서 1·2단계(비용 없음)까지 실제 실행.
- **MCP 비용 게이트**: 영상 생성은 `get_cost: true` 비용 조회와 명시적 사용자 승인 뒤에만 실행.

---

## 9. 마일스톤 (구현 순서 제안)

1. **M1 골격**: `plugin.json` + `/short` 오케스트레이터 + state 스키마 + 1·2단계(LLM, 비용無).
2. **M2 비주얼**: 3단계(키프레임) + 4단계(프롬프트) + MCP 이미지 생성 연동.
3. **M3 렌더·큐레이션**: 5단계(렌더·비용게이트) + 6단계(virality+선별) + MCP 참조 미디어 일관성.
4. **M4 마감**: 7단계 체크리스트 + `--resume` + 에러처리 + 문서.

---

## 10. 미해결/추후 결정

- 워크스페이스 위치: 작업 디렉토리 하위 `projects/` 기본 — 사용자별 경로 설정 옵션은 추후.
- 기본 모델: 영상 Seedance 2.0, 이미지 GPT Image 2(`gpt_image_2`) 가정. 기본 비주얼은 한국 웹툰형이며 프롬프트는 한국어만 사용한다.
- 후반(7단계) 외부툴: DaVinci/Premiere 안내 텍스트 수준 — 자동화는 범위 외.
