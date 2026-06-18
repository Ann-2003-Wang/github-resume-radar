# AI 技术雷达 - 个性化 GitHub 项目推荐系统

上传个人简历（Word/PDF），系统自动提取技术栈，搜索 GitHub 高星仓库，并用大模型进行多维度评分与中文解读，结果每日自动写入飞书多维表格。

## 功能特性
- 支持上传 PDF/Word 简历或纯文本粘贴
- DeepSeek 大模型提取核心技术关键词
- GitHub Search API 搜索相关高星仓库
- AI 翻译描述并生成亮点解读
- 多维度评估（技术栈匹配、领域相关、项目影响力、学习价值）
- 结果自动追加至飞书多维表格，历史可追溯
- 通过 GitHub Actions 每日定时运行，无需服务器

## 项目结构
\```
├── config.py            # 环境变量管理
├── feishu.py            # 飞书开放平台 API 封装
├── resume_analyzer.py   # 简历关键词提取
├── github_searcher.py   # GitHub 仓库搜索
├── ai_processor.py      # AI 文本加工（翻译、解读）
├── evaluator.py         # 多维度评估
├── main.py              # 主流程编排
└── requirements.txt     # 依赖清单
\```

## 快速开始
1. 在飞书多维表格中创建包含 `简历附件`、`简历文本`、`仓库名`、`描述`、`Star数`、`AI解读`、`捕捉时间`、`推荐指数` 等列。
2. 设置环境变量：`FEISHU_APP_ID`、`FEISHU_APP_SECRET`、`FEISHU_BITABLE_ID`、`DEEPSEEK_API_KEY`。
3. 安装依赖：`pip install -r requirements.txt`
4. 运行：`python main.py`

## 作品截图

<img width="2147" height="904" alt="image" src="https://github.com/user-attachments/assets/117ffb6d-2648-4de7-bd1c-e9a45a0210f3" />

