# evaluator.py - 从四个维度（技术栈匹配、领域相关、项目影响力、学习价值）
# 评估仓库与简历的匹配度，输出结构化评分及综合推荐指数。

import json

def evaluate_dimensions(repo, resume_text, client):
    """
    利用 DeepSeek 输出 JSON 格式的四维评分，计算平均分后返回字典。
    需要外部传入已初始化的 OpenAI client。
    """
    prompt = f"""你是一名资深技术招聘专家。请根据简历摘要和开源项目信息，从以下四个维度
分别给出1-10的整数评分，最终输出一个严格的JSON对象，不要任何其他文字。

维度说明：
- stack_match：项目技术栈与候选人技能的重合度（语言、框架、工具链）。
- domain_relevance：项目业务方向与候选人目标岗位的相关性。
- project_influence：基于Star数、社区活跃度等指标的项目行业影响力。
- learning_value：项目是否适合候选人当前阶段学习、提升技能。

简历摘要：
{resume_text[:1000]}

开源项目：
- 名称：{repo['full_name']}
- 描述：{repo['description']}
- 主题标签：{', '.join(repo.get('topics', []))}
- Star数：{repo['stars']}

输出格式示例：
{{"stack_match": 8, "domain_relevance": 7, "project_influence": 6, "learning_value": 9}}
"""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=150
        )
        result_text = response.choices[0].message.content.strip()
        scores = json.loads(result_text)
        avg = round(sum(scores.values()) / len(scores), 1)
        scores["average"] = avg
        return scores
    except Exception as e:
        print(f"多维度评估失败: {e}")
        return {"stack_match":5, "domain_relevance":5, "project_influence":5, "learning_value":5, "average":5.0}