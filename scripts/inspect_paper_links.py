import asyncio
import json
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cnki_mcp_server import BrowserPool, paper_registry


async def run(label: str, follow_ai: bool = False, follow_html: bool = False):
    pool = BrowserPool()
    page = await pool.get_page()
    captured = []
    capture_tasks = []

    async def capture_response(response):
        parsed = urlparse(response.url)
        if any(word in parsed.path.lower() for word in ("segmentstream", "getdocbysession", "chatdocs/article/permission")):
            post_data = response.request.post_data
            post_keys = []
            if post_data:
                try:
                    payload = json.loads(post_data)
                    if isinstance(payload, dict):
                        post_keys = list(payload.keys())
                except json.JSONDecodeError:
                    pass
            body_preview = ""
            body_chars = None
            try:
                body = await response.body()
                body_chars = len(body)
                body_preview = body[:500].decode("utf-8", errors="replace")
            except Exception:
                pass
            captured.append({
                "host": parsed.hostname,
                "path": parsed.path,
                "method": response.request.method,
                "status": response.status,
                "post_keys": post_keys,
                "body_bytes": body_chars,
                "body_preview": body_preview,
            })

    page.on("response", lambda response: capture_tasks.append(asyncio.create_task(capture_response(response))))
    try:
        url = paper_registry.resolve(label)
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        anchors = await page.locator("a").evaluate_all(
            """els => els.map(a => ({
                text: (a.innerText || a.textContent || '').trim(),
                href: a.href || '',
                id: a.id || '',
                className: a.className || ''
            }))"""
        )
        selected = []
        for anchor in anchors:
            marker = " ".join(str(anchor.get(key, "")) for key in ("text", "id", "className")).lower()
            if any(word in marker for word in ("阅读", "html", "pdf", "caj", "下载", "read")):
                parsed = urlparse(urljoin(page.url, anchor.get("href") or ""))
                selected.append(
                    {
                        "text": anchor.get("text"),
                        "id": anchor.get("id"),
                        "class": anchor.get("className"),
                        "host": parsed.hostname,
                        "path": parsed.path,
                        "has_query": bool(parsed.query),
                    }
                )
        print(json.dumps(selected, ensure_ascii=False, indent=2))
        if follow_ai:
            ai_link = page.get_by_text("CNKI AI阅读").first
            if await ai_link.count():
                ai_href = await ai_link.get_attribute("href")
                await page.goto(urljoin(page.url, ai_href), wait_until="domcontentloaded", timeout=60000)
                await page.wait_for_timeout(7000)
                if capture_tasks:
                    await asyncio.gather(*capture_tasks, return_exceptions=True)
                parsed = urlparse(page.url)
                body = (await page.locator("body").inner_text()).strip()
                resources = await page.evaluate(
                    "performance.getEntriesByType('resource').map(e => e.name)"
                )
                resource_paths = []
                for resource in resources:
                    item = urlparse(resource)
                    marker = (item.path or "").lower()
                    if any(word in marker for word in ("api", "paper", "article", "content", "chapter", "read", "study")):
                        resource_paths.append({"host": item.hostname, "path": item.path})
                print(json.dumps({
                    "final_host": parsed.hostname,
                    "final_path": parsed.path,
                    "title": await page.title(),
                    "body_chars": len(body),
                    "body_preview": body[:800],
                    "resource_paths": resource_paths[:80],
                    "captured_api": captured,
                }, ensure_ascii=False, indent=2))
        if follow_html:
            html_link = page.get_by_text("HTML阅读").first
            if await html_link.count():
                popup_task = asyncio.create_task(page.wait_for_event("popup", timeout=10000))
                await html_link.click()
                try:
                    reader_page = await popup_task
                except Exception:
                    reader_page = page
                await reader_page.wait_for_load_state("domcontentloaded", timeout=60000)
                await reader_page.wait_for_timeout(5000)
                parsed = urlparse(reader_page.url)
                body = (await reader_page.locator("body").inner_text()).strip()
                frames = [{"host": urlparse(frame.url).hostname, "path": urlparse(frame.url).path} for frame in reader_page.frames]
                print(json.dumps({
                    "html_final_host": parsed.hostname,
                    "html_final_path": parsed.path,
                    "html_title": await reader_page.title(),
                    "html_body_chars": len(body),
                    "html_body_preview": body[:1000],
                    "frames": frames,
                }, ensure_ascii=False, indent=2))
    finally:
        await page.close()
        await pool.close()


if __name__ == "__main__":
    asyncio.run(run(
        sys.argv[1],
        "--follow-ai" in sys.argv[2:],
        "--follow-html" in sys.argv[2:],
    ))
