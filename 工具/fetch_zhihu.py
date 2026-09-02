# -*- coding: utf-8 -*-
"""
抓取知乎问题/答案内容（反爬兜底多策略）：
  策略1: 知乎 API（需 cookie，先访问主页拿匿名 cookie）
  策略2: r.jina.ai 阅读代理（免登录，返回 markdown 文本）
用法: python 工具/fetch_zhihu.py <问题ID> [答案ID]
"""
import json
import re
import sys
import urllib.request
import urllib.parse

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

QID = sys.argv[1] if len(sys.argv) > 1 else "528264443"
AID = sys.argv[2] if len(sys.argv) > 2 else "3099626683"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.zhihu.com/",
}


def get(url, headers=None, timeout=20):
    h = dict(HEADERS)
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", errors="replace")


def strategy_api():
    """知乎官方 API：问题标题 + 高赞答案。"""
    print("=== 策略1: 知乎 API ===")
    # 先访问主页种 cookie
    try:
        opener = urllib.request.build_opener()
        opener.open(urllib.request.Request("https://www.zhihu.com/", headers=HEADERS), timeout=15)
        cookie = "; ".join(f"{c.name}={c.value}" for c in opener.handlers
                           if hasattr(c, "cookiejar") for c in c.cookiejar)
        h = {"Cookie": cookie} if cookie else {}
    except Exception as e:
        print("cookie 初始化失败:", e)
        h = {}
    # 问题信息
    try:
        q = json.loads(get(f"https://www.zhihu.com/api/v4/questions/{QID}?include=detail", h))
        print("问题:", q.get("title", "N/A"))
        print("详情:", (q.get("detail") or "")[:500])
        print("回答数:", q.get("answer_count"), "| 关注:", q.get("follower_count"))
    except Exception as e:
        print("问题 API 失败:", e)
    # 答案内容
    try:
        a = json.loads(get(
            f"https://www.zhihu.com/api/v4/answers/{AID}?include=content,excerpt,author",
            h))
        print("\n作者:", a.get("author", {}).get("name"), "| 赞同:", a.get("voteup_count"))
        content = a.get("content", "")
        content = re.sub(r"<[^>]+>", " ", content)
        print("\n=== 答案正文 ===")
        print(content[:6000])
        return True
    except Exception as e:
        print("答案 API 失败:", e)
        return False


def strategy_jina():
    """r.jina.ai 阅读代理（返回网页纯文本/markdown）。"""
    print("\n=== 策略2: r.jina.ai 代理 ===")
    url = f"https://www.zhihu.com/question/{QID}/answer/{AID}"
    try:
        txt = get(f"https://r.jina.ai/{url}", timeout=60)
        print("获取长度:", len(txt))
        print(txt[:7000])
        return True
    except Exception as e:
        print("jina 代理失败:", e)
        return False


if __name__ == "__main__":
    ok = strategy_api()
    if not ok:
        strategy_jina()
