#!/usr/bin/env python3
"""根据小说整体设定和指定章节描述生成章节正文。

用法：
  python generate_chapter.py --num 1
  python generate_chapter.py --num 2

环境变量：
  OPENAI_API_KEY   必填
  OPENAI_MODEL     必填，模型名称
  OPENAI_BASE_URL  可选，OpenAI 兼容接口地址
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from openai import OpenAI


ROOT = Path(__file__).resolve().parent
NOVEL_CONFIG_PATH = ROOT / "config" / "novel_config.json"
CHAPTERS_PATH = ROOT / "config" / "chapters.json"
OUTPUT_DIR = ROOT / "output" / "chapters"


def load_json(path: Path) -> Any:
    if not path.is_file():
        raise FileNotFoundError(f"配置文件不存在：{path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON 格式错误：{path}，第 {exc.lineno} 行：{exc.msg}") from exc


def find_chapter(chapters_data: dict[str, Any], number: int) -> dict[str, Any]:
    chapters = chapters_data.get("chapters")
    if not isinstance(chapters, list):
        raise ValueError("chapters.json 必须包含 chapters 数组")

    for chapter in chapters:
        if isinstance(chapter, dict) and chapter.get("number") == number:
            description = str(chapter.get("description", "")).strip()
            if not description:
                raise ValueError(f"第 {number} 章的 description 为空，请先在 chapters.json 中填写本章内容梗概")
            return chapter

    raise ValueError(f"chapters.json 中不存在第 {number} 章")


def build_prompt(novel_config: dict[str, Any], chapter: dict[str, Any]) -> str:
    novel_json = json.dumps(novel_config, ensure_ascii=False, indent=2)
    chapter_title = chapter.get("title") or f"第{chapter['number']}章"
    description = str(chapter["description"]).strip()

    return f"""你是一名专业的中文长篇小说作家。请根据小说整体设定，创作指定章节的完整正文。

【小说整体设定】
以下 JSON 是小说的全局设定，包含小说类型、世界观和人物设定。它是创作时必须遵守的事实依据：
{novel_json}

【本章信息】
章节：{chapter_title}
本章内容梗概：
{description}

【写作要求】
1. 严格遵守整体设定。人物身份、关系、经历、世界规则不得擅自修改；设定中没有说明的内容，不要当作既定事实。
2. 以本章内容梗概为剧情依据，扩写成完整、连贯、有场景、有行动、有对话的章节正文。不得偏离梗概的核心事件和因果关系，不要擅自引入会改变主线的新事件。
3. **突出人物性格是首要要求。** 不要只用旁白给人物贴性格标签，要通过人物的措辞、语气、思考方式、行为选择、下意识反应和与他人的互动体现性格。
4. 不同人物必须有可区分的说话方式和行为逻辑。对话要符合人物身份、经历和当下情境，避免所有人物说话像同一个人，避免生硬说教和模板化对白。
5. 人物行为必须有动机，并与其已知性格和处境一致。不要为了推动剧情让人物突然做出缺乏依据的决定。
6. 采用自然、具体、有画面感的中文叙事。合理安排动作、环境、心理和对话，不要堆砌形容词，不要反复解释读者已经知道的信息。
7. 控制叙事节奏：场景转换清楚，事件之间衔接自然；重要情节充分展开，次要过程简洁处理。
8. 不要在正文中解释创作过程，不要输出大纲、分析、设定复述或写作说明。
9. 直接输出章节正文，并以章节标题开头。"""


def main() -> int:
    parser = argparse.ArgumentParser(description="根据章节梗概生成小说正文")
    parser.add_argument("--num", type=int, required=True, help="要生成的章节编号，例如 --num 1")
    args = parser.parse_args()

    try:
        novel_config = load_json(NOVEL_CONFIG_PATH)
        chapters_data = load_json(CHAPTERS_PATH)
        chapter = find_chapter(chapters_data, args.num)

        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        model = os.getenv("OPENAI_MODEL", "").strip()
        base_url = os.getenv("OPENAI_BASE_URL", "").strip()

        if not api_key:
            raise ValueError("请设置环境变量 OPENAI_API_KEY")
        if not model:
            raise ValueError("请设置环境变量 OPENAI_MODEL")

        client_args: dict[str, str] = {"api_key": api_key}
        if base_url:
            client_args["base_url"] = base_url
        client = OpenAI(**client_args)

        prompt = build_prompt(novel_config, chapter)
        print(f"正在生成第 {args.num} 章，使用模型：{model}", flush=True)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "你是严谨的中文小说作家。优先保证人物性格鲜明、人物行为合理、剧情符合设定。",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
        )

        content = response.choices[0].message.content
        if not content or not content.strip():
            raise RuntimeError("模型返回了空内容")

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = OUTPUT_DIR / f"chapter_{args.num:03d}.md"
        output_path.write_text(content.strip() + "\n", encoding="utf-8")
        print(f"生成完成：{output_path.relative_to(ROOT)}")
        return 0

    except Exception as exc:
        print(f"生成失败：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
