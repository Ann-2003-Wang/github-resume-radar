# github_searcher.py - 根据关键词列表调用 GitHub Search API 获取高星仓库，
# 合并去重后按 Star 数降序返回指定数量。

import requests
import time


def search_by_keywords(queries, target_count=5):
    """
    对每个查询字符串分别搜索，汇总去重，按 Star 数降序排序，返回前 target_count 个仓库信息。
    每个仓库包含 full_name, description, stars, topics, url。
    """
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"}
    repo_map = {}
    for q in queries:
        url = "https://api.github.com/search/repositories"
        params = {"q": q, "sort": "stars", "order": "desc", "per_page": 5}
        try:
            r = requests.get(url, headers=headers, params=params, timeout=15)
            if r.status_code == 200:
                for item in r.json().get("items", []):
                    name = item["full_name"]
                    if name not in repo_map:
                        repo_map[name] = {
                            "full_name": name,
                            "description": item.get("description", ""),
                            "stars": item.get("stargazers_count", 0),
                            "topics": item.get("topics", []),
                            "url": item.get("html_url", "")
                        }
            time.sleep(2)   # 搜索 API 频率限制：每分钟最多 10 次
        except Exception as e:
            print(f"搜索异常: {q}, {e}")
    sorted_repos = sorted(repo_map.values(), key=lambda x: x["stars"], reverse=True)
    return sorted_repos[:target_count]