import json
import tempfile
import unittest
from pathlib import Path

from cnki_mcp_server import PaperRegistry, _clean_article_html, _is_cnki_url, _online_read_params


class CoreTests(unittest.TestCase):
    def test_cnki_url_allowlist(self):
        self.assertTrue(_is_cnki_url("https://kns.cnki.net/kcms2/article/abstract?v=1"))
        self.assertFalse(_is_cnki_url("http://kns.cnki.net/example"))
        self.assertFalse(_is_cnki_url("https://cnki.net.evil.example/"))

    def test_registry_survives_restart_without_secrets(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            url = "https://kns.cnki.net/kcms2/article/abstract?v=test"
            label = PaperRegistry(path).register(url, "作者", "2026", "标题")
            self.assertTrue(label.startswith("cnki:"))
            self.assertEqual(PaperRegistry(path).resolve(label), url)
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertNotIn("cookie", json.dumps(payload).lower())

    def test_article_html_cleanup(self):
        value = "<h2>第一节</h2><p>正文&nbsp;内容</p><script>ignore()</script>"
        cleaned = _clean_article_html(value)
        self.assertIn("第一节", cleaned)
        self.assertIn("正文 内容", cleaned)
        self.assertNotIn("<p>", cleaned)
        self.assertNotIn("ignore()", cleaned)

    def test_online_reader_params(self):
        params = _online_read_params([
            "https://kns.cnki.net/nzkhtml/read?fileName=A&tableName=CJFD&dbCode=CJFD&invoice=token"
        ])
        self.assertEqual(params["filename"], "A")
        self.assertEqual(params["invoice"], "token")


if __name__ == "__main__":
    unittest.main()
