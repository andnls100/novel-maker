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
```

生成结果保存到 `output/chapters/chapter_001.md`。再次生成同一章会覆盖该文件。

脚本会把 `novel_config.json` 中的完整小说设定和指定章节的 `description` 一起发送给模型。提示词重点要求通过人物的语言、行为、思维和互动突出性格，并保持人物行为与既有设定一致。
