import argparse
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastmcp import Client

from cnki_mcp_server import mcp


def normalize(result):
    if getattr(result, "data", None) is not None:
        return result.data
    output = []
    for item in getattr(result, "content", []):
        text = getattr(item, "text", None)
        if text:
            try:
                output.append(json.loads(text))
            except json.JSONDecodeError:
                output.append(text)
    return output[0] if len(output) == 1 else output


async def run(query: str | None, paper: str | None, fulltext: bool, sort: str, start_char: int, bibtex: bool) -> int:
    async with Client(mcp) as client:
        tools = await client.list_tools()
        print(json.dumps({"tool_count": len(tools), "tools": [tool.name for tool in tools]}, ensure_ascii=False))
        status = normalize(await client.call_tool("get_login_status", {}))
        print(json.dumps({"login_status": status}, ensure_ascii=False))
        if query:
            search = normalize(
                await client.call_tool(
                    "search_cnki",
                    {"query": query, "search_type": "主题", "pages": 1, "sort": sort},
                )
            )
            print(json.dumps({"search": search}, ensure_ascii=False))
        if paper:
            detail = normalize(await client.call_tool("get_paper_detail", {"paper": paper}))
            print(json.dumps({"detail": detail}, ensure_ascii=False))
            if fulltext:
                article = normalize(
                    await client.call_tool(
                        "read_paper_fulltext",
                        {"paper": paper, "start_char": start_char, "max_chars": 3000},
                    )
                )
                print(json.dumps({"fulltext": article}, ensure_ascii=False))
            if bibtex:
                citation = normalize(await client.call_tool("get_paper_bibtex", {"paper": paper}))
                print(json.dumps({"bibtex": citation}, ensure_ascii=False))
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query")
    parser.add_argument("--paper")
    parser.add_argument("--fulltext", action="store_true")
    parser.add_argument("--sort", default="相关度")
    parser.add_argument("--start-char", type=int, default=0)
    parser.add_argument("--bibtex", action="store_true")
    args = parser.parse_args()
    raise SystemExit(asyncio.run(run(args.query, args.paper, args.fulltext, args.sort, args.start_char, args.bibtex)))


if __name__ == "__main__":
    main()
