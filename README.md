# HUST CNKI Research MCP

适用于华中科技大学机构统一认证（HUST SSO）的中国知网学术研究 MCP。项目基于
[NoFixedPoint/cnki-mcp](https://github.com/NoFixedPoint/cnki-mcp) 增强，使用独立、持久的
Chrome 档案保存机构统一认证（SSO）会话，并补充机构授权的在线正文分段读取。

## 能力

- 按主题、关键词、篇名、作者、机构、基金、摘要、DOI 等字段检索；
- 按期刊、作者筛选，并按相关度、时间、被引量、下载量排序；
- 获取题名、作者、机构、摘要、关键词、来源、年份、卷期页、DOI、基金等元数据；
- 获取 CNKI 官方 BibTeX；
- 读取机构订阅范围内允许在线阅读的正文，并按段返回，避免一次塞满模型上下文；
- 下载机构已授权的 PDF；
- 论文标签与浏览器登录态均跨 Codex 重启保留。

## 登录与安全

首次运行 `cnki-research-login` 会打开专用 Chrome 窗口。选择机构“华中科技大学”，在学校
统一认证页面登录，返回知网后完成确认。后续 MCP 使用同一浏览器档案，不再要求日常重复登录。

登录档案默认位于 `%LOCALAPPDATA%\CNKIResearchMCP\browser-profile`。MCP 没有读取或设置 Cookie
的工具，也不会把 Cookie、令牌、账号或密码返回给模型。所有网页导航均限制为 HTTPS 的
`*.cnki.net` 域名。机构或知网主动让会话失效时，需要再次运行登录程序，这是 SSO 本身的安全规则。

## 工具

| 工具 | 用途 |
|---|---|
| `search_cnki` | 多字段检索、作者/期刊筛选、多页和排序 |
| `get_paper_detail` | 获取完整题录、摘要和可用权限入口 |
| `read_paper_fulltext` | 分段读取机构授权的在线正文 |
| `get_paper_bibtex` | 获取并补充 CNKI 官方 BibTeX |
| `download_paper_pdf` | 下载机构授权 PDF |
| `find_best_match` | 根据标题核验并匹配文献 |
| `get_login_status` | 检查会话状态，不返回任何认证秘密 |

## 本地安装

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install "fastmcp==2.14.5" "playwright>=1.61.0"
```

默认复用系统 Chrome，不需要下载 Playwright 自带的 Chromium。如需改用其他通道，可设置
`CNKI_BROWSER_CHANNEL=msedge`；也可以用 `CNKI_BROWSER_EXECUTABLE` 指定浏览器程序的绝对路径。
在本机开着代理软件时，默认让 CNKI 与学校 SSO 浏览器直连；如机构网络必须经过代理，可设置
`CNKI_DIRECT=false`。

启动 MCP：

```powershell
.\.venv\Scripts\python.exe .\cnki_mcp_server.py
```

首次机构登录：

```powershell
.\.venv\Scripts\python.exe .\cnki_mcp_server.py --login
```

## 来源与许可

底座项目使用 MIT 许可证。本项目仅访问当前用户和机构已经获得授权的内容，不提供绕过订阅、
验证码或访问控制的能力。请遵守学校、数据库和版权方的使用规则，避免高频批量下载。
