# ai_processor.py - 封装 DeepSeek 大模型调用，提供翻译、亮点总结等文本加工功能。
# 同时初始化并导出 OpenAI 客户端，供其他模块（如 evaluator）使用。

from openai import OpenAI
from config import DEEPSEEK_API_KEY

# 全局客户端
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")


def translate_to_chinese(text):
    """将英文技术描述翻译为简洁中文，失败时返回原文。"""
    if not text or text.isspace():
        return "无描述"
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": f"请将以下英文技术描述翻译成简洁的中文，只返回译文：\n{text}"}],
            temperature=0.1,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"翻译失败: {e}")
        return text


def ai_summary(repo):
    """为仓库生成一句话（约20字）亮点解读。"""
    prompt = f"""你是一个技术专家，请用一句话（20字左右）点评以下 GitHub 仓库的亮点和用途：
仓库：{repo['full_name']}
描述：{repo['description']}
Star 数：{repo['stars']}"""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=60
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"AI 解读失败: {e}")
        return "解读生成失败"