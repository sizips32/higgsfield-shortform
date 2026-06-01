# higgsfield-shortform

한 줄 로그라인에서 **숏폼/릴스(15~60초 세로형)** 영상을 기획부터 완성 직전까지 안내하는 Claude Code 플러그인. 허준호 감독의 7단계 AI 영상 파이프라인 + harness engineering 방법론.

## 철학
- **"AI가 가짜라도 이야기는 진짜여야 한다"** — 훅·정서 우선.
- **스마트 게이트** — 기계적 단계는 자동, 창작 판단(기획·시나리오·톤·렌더비용·큐레이션)은 사용자 승인 강제.
- **인간 안목** — 최종 컷 선별은 AI가 대신 하지 않는다.

## 요건
- `higgsfield` CLI 설치·인증 (`higgsfield auth login`). 크레딧 필요(렌더 단계).
- Python 3.12+ (state 헬퍼, 외부 의존성 없음).

## 사용법
```
/short "지하철에서 우산을 건네는 낯선 사람"     # 신규 프로젝트 시작
/short --resume <slug>                          # 중단 지점부터 재개
```

## 7단계 파이프라인
| # | 단계 | 게이트 | 비용 |
|---|---|---|---|
| 1 | 기획 (컨셉·훅) | 승인 | 무료 |
| 2 | 시나리오 (샷리스트) | 승인 | 무료 |
| 3 | 스타일·키프레임 | 톤 확인 | 소액(이미지) |
| 4 | 영상 프롬프트 | 자동 | 무료 |
| 5 | 렌더 | **비용 게이트** | 크레딧(영상) |
| 6 | 큐레이션 | **인간 안목** | virality 소액(옵션) |
| 7 | 후반 체크리스트 | 없음 | 무료 |

옵션: `short-consistency`(soul-id) — 반복 인물 얼굴 일관성.

## 상태·재개
프로젝트별 워크스페이스 `projects/<slug>/`에 상태(`state.json`)와 산출물(`briefs/`, `assets/`)이 저장된다. 게이트 승인·단계 전이는 `lib/state.py`가 강제한다(마크다운이 우회 불가). 세션이 끊겨도 `--resume`으로 이어간다.

## 구조
```
.claude-plugin/plugin.json   commands/short.md
lib/state.py                 skills/short-{ideate,script,style,prompt,render,curate,post,consistency}/
```
