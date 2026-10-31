# novel-maker

## 章节正文生成

章节梗概放在 `config/chapters.json`，每一项对应一章，`description` 填写该章的剧情内容梗概。小说全局设定读取自 `config/novel_config.json`。

API 参数统一配置在 `config/api_config.json`：

```json
{
  "api_key": "你的 API Key",
  "model": "模型名称",
  "base_url": "https://你的接口地址/v1"
}
```

安装依赖：

```bash
pip install openai
```

生成指定章节：

```bash
python generate_chapter.py --num 1
python generate_chapter.py --num 2
```

生成结果保存到 `output/chapters/chapter_001.md` 等对应文件。再次生成同一章会覆盖该文件。

生成第 2 章及之后的章节时，脚本会自动读取上一章正文（例如生成第 2 章时读取 `output/chapters/chapter_001.md`），并将完整正文一并发送给模型，用于保持人物状态、剧情事件、时间线和场景衔接。必须先生成上一章；如果上一章文件不存在或为空，脚本会报错。

脚本会把 `novel_config.json` 中的完整小说设定、指定章节的 `description`，以及（第 2 章起）上一章完整正文一起发送给模型。提示词重点要求通过人物的语言、行为、思维和互动突出性格，并保持人物行为与既有设定一致。
