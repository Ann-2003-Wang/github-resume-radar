# config.py - 读取并校验所有必需的环境变量，统一提供给其他模块使用。

import os

FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID")
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET")
FEISHU_BITABLE_ID = os.environ.get("FEISHU_BITABLE_ID")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
TABLE_ID = "tblHwyHQmp9WW4UI"   # 固定表格 ID

# 启动前检查
_missing = []
if not FEISHU_APP_ID: _missing.append("FEISHU_APP_ID")
if not FEISHU_APP_SECRET: _missing.append("FEISHU_APP_SECRET")
if not FEISHU_BITABLE_ID: _missing.append("FEISHU_BITABLE_ID")
if not DEEPSEEK_API_KEY: _missing.append("DEEPSEEK_API_KEY")
if _missing:
    raise EnvironmentError(f"缺少必需的环境变量: {', '.join(_missing)}")