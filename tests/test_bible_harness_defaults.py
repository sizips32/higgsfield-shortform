from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_bible_harness_uses_gpt_image_2_webtoon_korean_only():
    orchestrator = (ROOT / ".claude/skills/bible-shorts-orchestrator/SKILL.md").read_text()
    production = (ROOT / ".claude/skills/bible-higgsfield-production/SKILL.md").read_text()
    director = (ROOT / ".claude/agents/higgsfield-production-director.md").read_text()
    reference = (
        ROOT / ".claude/skills/bible-higgsfield-production/references/higgsfield-mcp.md"
    ).read_text()

    combined = "\n".join([orchestrator, production, director, reference])

    assert "gpt_image_2" in combined
    assert "웹툰" in combined
    assert "한국어만" in combined
    assert "영어 프롬프트를 기본" not in combined


def test_short_pipeline_defaults_match_bible_harness():
    style = (ROOT / "skills/short-style/SKILL.md").read_text()
    prompt = (ROOT / "skills/short-prompt/SKILL.md").read_text()

    assert '기본 `<imageModel>` = `gpt_image_2`' in style
    assert "한국 웹툰형" in style
    assert "한국어 이미지 프롬프트" in style
    assert '"promptLanguage": "ko"' in prompt
    assert "한국어 i2v 프롬프트" in prompt


def test_higgsfield_production_paths_are_mcp_only():
    active_paths = [
        "README.md",
        ".claude-plugin/plugin.json",
        "commands/short.md",
        "skills/short-style/SKILL.md",
        "skills/short-render/SKILL.md",
        "skills/short-curate/SKILL.md",
        "skills/short-consistency/SKILL.md",
        "skills/short-post/SKILL.md",
        ".claude/skills/bible-shorts-orchestrator/SKILL.md",
        ".claude/skills/bible-higgsfield-production/SKILL.md",
        ".claude/skills/bible-higgsfield-production/references/higgsfield-mcp.md",
        ".claude/agents/bible-shorts-showrunner.md",
        ".claude/agents/higgsfield-production-director.md",
        "docs/specs/2026-06-01-higgsfield-shortform-pipeline-design.md",
    ]
    combined = "\n".join((ROOT / path).read_text() for path in active_paths)

    assert "mcp__higgsfield.generate_image" in combined
    assert "mcp__higgsfield.generate_video" in combined
    assert "higgsfield generate" not in combined
    assert "higgsfield upload" not in combined
    assert "higgsfield soul-id" not in combined
    assert "higgsfield CLI" not in combined
    assert "`higgsfield` CLI" not in combined
    assert "CLI 폴백" not in combined
    assert "CLI 래핑" not in combined
    assert "generate cost" not in combined
    assert "generate create" not in combined
