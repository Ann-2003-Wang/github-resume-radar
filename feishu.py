# feishu.py - 封装飞书开放平台所有 API 调用，包括获取 Token、多维表格记录读写、
# 附件下载与简历解析等，对外隐藏底层 HTTP 细节。

import requests
import os
from io import BytesIO
import docx
import PyPDF2
from config import FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_BITABLE_ID, TABLE_ID


def get_tenant_access_token():
    """获取飞书 tenant_access_token，用于后续 API 认证。"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}
    r = requests.post(url, json=payload)
    r.raise_for_status()
    return r.json()["tenant_access_token"]


def add_record(token, fields):
    """向多维表格指定表格新增一条记录。"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_BITABLE_ID}/tables/{TABLE_ID}/records"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = {"fields": fields}
    r = requests.post(url, headers=headers, json=body)
    return r.json()


def get_first_record(token):
    """获取表格第一条记录的所有字段（通常用于读取简历）。"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_BITABLE_ID}/tables/{TABLE_ID}/records"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page_size": 1}
    r = requests.get(url, headers=headers, params=params)
    items = r.json().get("data", {}).get("items", [])
    if not items:
        return {}
    return items[0]["fields"]


def get_last_record(token):
    """获取表格最后一条记录的所有字段（用于定位简历行）。"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_BITABLE_ID}/tables/{TABLE_ID}/records"
    headers = {"Authorization": f"Bearer {token}"}
    all_records = []
    page_token = None
    while True:
        params = {"page_size": 500}
        if page_token:
            params["page_token"] = page_token
        r = requests.get(url, headers=headers, params=params)
        data = r.json().get("data", {})
        items = data.get("items", [])
        all_records.extend(items)
        if not data.get("has_more", False):
            break
        page_token = data.get("page_token")
    if not all_records:
        return {}
    return all_records[-1]["fields"]


def delete_all_except_first(token):
    """删除表格中除第一条外的所有记录（可选，用于刷新推荐）。"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_BITABLE_ID}/tables/{TABLE_ID}/records"
    headers = {"Authorization": f"Bearer {token}"}
    all_records = []
    page_token = None
    while True:
        params = {"page_size": 500}
        if page_token:
            params["page_token"] = page_token
        r = requests.get(url, headers=headers, params=params)
        data = r.json().get("data", {})
        items = data.get("items", [])
        all_records.extend(items)
        if not data.get("has_more", False):
            break
        page_token = data.get("page_token")
    if len(all_records) <= 1:
        return
    ids_to_delete = [item["record_id"] for item in all_records[1:]]
    delete_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_BITABLE_ID}/tables/{TABLE_ID}/records/batch_delete"
    for i in range(0, len(ids_to_delete), 500):
        batch = ids_to_delete[i:i+500]
        requests.delete(delete_url, headers=headers, json={"records": batch})


def download_and_parse_attachment(token, file_token, file_name):
    """从飞书下载附件（Word/PDF）并提取纯文本内容。"""
    download_url = f"https://open.feishu.cn/open-apis/drive/v1/medias/{file_token}/download"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(download_url, headers=headers)
    if r.status_code != 200:
        raise Exception(f"文件下载失败，状态码：{r.status_code}")
    file_bytes = BytesIO(r.content)
    ext = os.path.splitext(file_name)[1].lower()
    text = ""
    if ext == ".docx":
        doc = docx.Document(file_bytes)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif ext == ".pdf":
        reader = PyPDF2.PdfReader(file_bytes)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    else:
        raise Exception(f"不支持的文件格式：{ext}，目前仅支持 docx 和 pdf")
    return text.strip()


def get_resume_from_bitable(token):
    """
    从飞书表格最后一条记录中读取简历内容。
    优先读取“简历附件”中的文件（Word/PDF），若无则读取“简历文本”列。
    """
    fields = get_last_record(token)
    print("调试信息：最后一条记录所有字段：", fields)

    # 检查附件列
    attachments = fields.get("简历附件")
    if attachments and isinstance(attachments, list) and len(attachments) > 0:
        first_file = attachments[0]
        file_token = first_file.get("file_token")
        file_name = first_file.get("name", "resume")
        print(f"发现附件：{file_name}，正在下载解析...")
        return download_and_parse_attachment(token, file_token, file_name)
    # 否则读取文本列
    text = fields.get("简历文本", "").strip()
    if text:
        print("使用文本列中的简历内容。")
        return text
    return None