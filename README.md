# novel-maker

## 章节正文生成

章节梗概放在 `config/chapters.json`，每一项对应一章，`description` 填写该章的剧情内容梗概。小说全局设定读取自 `config/novel_config.json`。

安装依赖：

```bash
pip install openai
```

设置 OpenAI 兼容接口环境变量：

```bash
# 必填
export OPENAI_API_KEY="你的 API Key"
export OPENAI_MODEL="你的模型名称"

# 可选：使用第三方 OpenAI 兼容接口时设置
export OPENAI_BASE_URL="https://你的接口地址/v1"
```

Windows PowerShell 示例：

```powershell
$env:OPENAI_API_KEY="你的 API Key"
$env:OPENAI_MODEL="你的模型名称"
$env:OPENAI_BASE_URL="https://你的接口地址/v1"
```

生成指定章节：

```bash
python generate_chapter.py --num 1
```

生成结果保存到 `output/chapters/chapter_001.md`。再次生成同一章会覆盖该文件。

脚本会把 `novel_config.json` 中的完整小说设定和指定章节的 `description` 一起发送给模型。提示词重点要求通过人物的语言、行为、思维和互动突出人物性格，并保持人物行为与既有设定一致。
