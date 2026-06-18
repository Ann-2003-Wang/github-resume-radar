# resume_analyzer.py - 利用 DeepSeek 大模型从简历文本中提取核心技术栈，
# 并转换为 GitHub 搜索语法，供后续仓库搜索使用。

from openai import OpenAI
from config import DEEPSEEK_API_KEY

# 初始化 DeepSeek 客户端（也可从 ai_processor 引用，这里独立使用）
_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")


def extract_keywords_from_resume(resume_text):
    """
    输入简历文本，返回最多 5 个 GitHub 搜索查询字符串（topic 组合）。
    """
    prompt = f"""你是一个技术招聘专家。请根据以下简历内容，提炼出3~5个核心技术方向或技术栈，
并用GitHub搜索语法表示（使用 topic: 前缀）。每个方向写成一个单独的搜索查询字符串，
查询中可以组合多个关键词。要求：
- 每个查询字符串应能筛选出与该方向高度相关的仓库。
- 只返回查询字符串，一行一个，不要额外解释。
- 示例输出格式：
topic:python topic:fastapi stars:>50
topic:kubernetes topic:microservice

简历：
{resume_text[:2000]}
"""
    try:
        response = _client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=300
        )
        lines = response.choices[0].message.content.strip().split("\n")
        return [line.strip().lstrip("- ").strip() for line in lines if line.strip()][:5]
    except Exception as e:
        print(f"关键词提取失败: {e}")
        return ["topic:python stars:>100"]