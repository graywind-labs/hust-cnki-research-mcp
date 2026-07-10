import unittest

from fastmcp import Client

from cnki_mcp_server import mcp


class McpContractTests(unittest.IsolatedAsyncioTestCase):
    async def test_tools_are_exposed_with_safe_contracts(self):
        async with Client(mcp) as client:
            tools = await client.list_tools()
        by_name = {tool.name: tool for tool in tools}
        expected = {
            "search_cnki",
            "get_paper_detail",
            "read_paper_fulltext",
            "get_paper_bibtex",
            "download_paper_pdf",
            "find_best_match",
            "get_login_status",
        }
        self.assertTrue(expected.issubset(by_name))
        all_schemas = " ".join(str(tool.inputSchema).lower() for tool in tools)
        self.assertNotIn("cookie", all_schemas)
        self.assertNotIn("password", all_schemas)
        fulltext_schema = by_name["read_paper_fulltext"].inputSchema["properties"]
        self.assertIn("start_char", fulltext_schema)
        self.assertEqual(fulltext_schema["max_chars"]["maximum"], 50000)


if __name__ == "__main__":
    unittest.main()
