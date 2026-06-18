# main.py - 项目主入口，负责串联各模块：读取简历、提取关键词、搜索仓库、
# 翻译与解读、多维度评估，最后将结果追加至飞书多维表格。

from datetime import datetime

# 飞书 API 封装：获取 Token、记录读写、简历解析
from feishu import get_tenant_access_token, add_record, get_resume_from_bitable

# 简历分析：提取技术关键词
from resume_analyzer import extract_keywords_from_resume

# GitHub 搜索：根据关键词获取高星仓库
from github_searcher import search_by_keywords

# AI 文本加工：翻译描述、生成亮点解读，并导出 DeepSeek 客户端
from ai_processor import translate_to_chinese, ai_summary, client

# 多维度评估：计算四项维度评分及综合推荐指数
from evaluator import evaluate_dimensions


def main():
    print("1. 获取飞书 Token...")
    token = get_tenant_access_token()
    print("Token 获取成功")

    print("2. 从飞书表格读取简历...")
    resume = get_resume_from_bitable(token)
    if not resume:
        print("未找到简历内容，请在表格最后一条记录中上传“简历附件”或填写“简历文本”列。")
        return
    print(f"简历长度：{len(resume)} 字符")

    print("3. 提取技术关键词...")
    queries = extract_keywords_from_resume(resume)
    print(f"搜索语句：{queries}")

    print("4. 搜索相关 GitHub 仓库...")
    repos = search_by_keywords(queries, target_count=5)
    print(f"找到 {len(repos)} 个仓库")

    if not repos:
        print("没有搜索到相关项目，流程结束。")
        return

    capture_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for repo in repos:
        print(f"处理: {repo['full_name']} ({repo['stars']} stars)")
        # 翻译描述为中文
        chinese_desc = translate_to_chinese(repo["description"])
        # AI 亮点解读
        summary = ai_summary(repo)
        # 多维度评估，返回字典含 average
        dimensions = evaluate_dimensions(repo, resume, client)
        print(f"  维度评分：{dimensions}")

        # 准备写入字段
        fields = {
            "仓库名": repo["full_name"],
            "描述": chinese_desc,
            "Star数": repo["stars"],
            "AI解读": summary,
            "捕捉时间": capture_time,
            "推荐指数": dimensions["average"]
        }
        result = add_record(token, fields)
        if result.get("code") != 0:
            print(f"写入失败：{result}")
        else:
            print("  写入成功。")

    print("全部完成，请查看飞书表格。")


if __name__ == "__main__":
    main()