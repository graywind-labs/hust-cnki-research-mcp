# HUST CNKI Research MCP

让 Codex、Claude Code 或 WorkBuddy 帮你检索、阅读和引用中国知网论文。

本项目适用于华中科技大学机构统一认证（HUST SSO）。它会使用一个独立的 Chrome 用户目录保存登录状态；通常只需登录一次，之后重启 Agent 也能继续使用。

> 本文先给出 Windows 10/11 的小白安装方法。熟悉 Python 的用户可直接跳到最后的[手动安装](#手动安装源码开发者)。

## 极简安装：直接让 Agent 帮你装

如果你已经装好了 **Codex、Claude Code、WorkBuddy 或其他支持 MCP 的 Agent**，不需要自己阅读后面的安装步骤。直接把下面这句话完整复制给它：

```text
帮我安装 https://github.com/graywind-labs/hust-cnki-research-mcp.git 并接入这个 MCP，同时安装所有所需依赖。请自动识别当前 Agent 所需的 MCP 配置方式，完成安装、配置和连接验证；需要我在 Chrome 中登录华中科技大学统一认证和知网时，再提示我操作。
```

也就是告诉它：帮我安装 [graywind-labs/hust-cnki-research-mcp](https://github.com/graywind-labs/hust-cnki-research-mcp.git)、接入 MCP，并安装全部依赖。

接下来只需：

1. Agent 请求执行安装命令时，确认允许；
2. Agent 打开专用 Chrome 窗口后，由你本人完成学校统一认证；
3. 等 Agent 告诉你 MCP 已连接并验证成功。

如果 Agent 无法自动完成，再按照下方的“小白分步安装”操作。

## 可以做什么

- 按主题、关键词、篇名、作者、机构、基金、摘要、DOI 等字段检索论文；
- 按期刊、作者筛选，并按相关度、时间、被引量或下载量排序；
- 获取题名、作者、机构、摘要、关键词、来源、年份、卷期页、DOI、基金等信息；
- 获取 CNKI 官方 BibTeX；
- 分段读取机构授权的在线正文，避免一次占满 Agent 上下文；
- 下载机构已授权的 PDF；
- 保存论文标签和浏览器登录状态。

## 小白分步安装：先准备环境

只需要以下三样：

1. **Python 3.10 或更高版本**：用于运行本 MCP；
2. **Google Chrome**：用于登录学校 SSO 和访问知网；
3. **一个支持 MCP 的 Agent**：Codex、Claude Code 或 WorkBuddy 等，任选其一。

另外，你需要能正常访问华中科技大学统一认证和学校已订阅的知网资源。校外访问是否可用取决于学校当前的访问政策。

### 1. 安装 Python

打开 Windows 的“终端”或 PowerShell，粘贴下面这行并回车：

```powershell
winget install -e --id Python.Python.3.11
```

安装完成后，**关闭并重新打开终端**，再检查：

```powershell
py -3.11 --version
```

看到 `Python 3.11.x` 就说明成功。如果电脑没有 `winget`，请从 [Python 官网](https://www.python.org/downloads/windows/)下载安装，并在安装界面勾选 **Add Python to PATH**。

### 2. 安装 Chrome

在 PowerShell 中运行：

```powershell
winget install -e --id Google.Chrome
```

也可以直接从 [Chrome 官网](https://www.google.com/chrome/)下载安装。安装后正常打开一次 Chrome 即可，**不需要**安装任何 Chrome 扩展，也不需要下载 Playwright 自带的 Chromium。

### 3. 安装一个 Agent

- **Codex**：使用 Codex CLI、IDE 扩展或 ChatGPT 桌面版均可；它们共享同一份 MCP 配置。参见 [Codex 快速开始](https://learn.chatgpt.com/codex/quickstart)。
- **Claude Code**：Windows PowerShell 可运行 `irm https://claude.ai/install.ps1 | iex`，然后运行 `claude` 登录。参见 [Claude Code 官方安装文档](https://code.claude.com/docs/en/installation)。
- **WorkBuddy**：从腾讯 WorkBuddy 官网下载安装并登录。参见 [WorkBuddy Windows 安装文档](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Installation-Win-Guide)。

已有其中一个 Agent 的话，不必安装其他两个。

## 第一步：安装本 MCP

在 PowerShell 中复制并运行这一整行：

```powershell
py -3.11 -m pip install --user --upgrade "https://github.com/graywind-labs/hust-cnki-research-mcp/archive/refs/heads/main.zip"
```

等待命令执行完成。以后项目更新时，再运行一次相同命令即可升级。

## 第二步：登录知网

运行：

```powershell
py -3.11 -m cnki_mcp_server --login
```

随后会打开一个专用 Chrome 窗口：

1. 在知网页面选择机构“华中科技大学”；
2. 在学校统一认证页面完成登录；
3. 登录后回到知网页面；
4. 回到终端，按提示确认完成。

这个专用窗口使用独立登录档案，不会修改你平时使用的 Chrome 资料。登录档案默认保存在 `%LOCALAPPDATA%\CNKIResearchMCP\browser-profile`。如果以后登录过期，只需重新执行上面的登录命令。

## 第三步：接入你的 Agent

下面三种方式只需选择一种。

### Codex

在 PowerShell 中运行：

```powershell
codex mcp add cnki -- py -3.11 -m cnki_mcp_server
```

然后重启 Codex。在 Codex 中输入 `/mcp`，看到 `cnki` 即表示接入成功。也可以在终端运行 `codex mcp list` 检查。

这条命令适用于 Codex CLI；Codex CLI、IDE 扩展和 ChatGPT 桌面版会共享 MCP 配置。配置格式来自 [Codex 官方 MCP 文档](https://learn.chatgpt.com/codex/extend/mcp)。

### Claude Code

在 PowerShell 中运行：

```powershell
claude mcp add --transport stdio --scope user cnki -- py -3.11 -m cnki_mcp_server
```

然后重新打开 Claude Code，输入 `/mcp`，看到 `cnki` 且状态正常即表示成功。终端中也可以运行 `claude mcp list` 检查。

这里使用 `user` 范围，所以所有项目都能使用；命令格式来自 [Claude Code 官方 MCP 文档](https://code.claude.com/docs/en/mcp)。

### WorkBuddy

WorkBuddy 官方文档目前使用 URL 添加 MCP，因此要先启动本机服务。

1. 打开 PowerShell，运行下面命令，并让这个窗口保持打开：

   ```powershell
   py -3.11 -m cnki_mcp_server --http
   ```

2. 打开 WorkBuddy，进入 **Settings（设置）→ MCP**；
3. 点击 **Add MCP Server（添加 MCP 服务器）**；
4. 名称填写 `cnki`，地址填写：

   ```text
   http://127.0.0.1:8000/mcp
   ```

5. 本地服务不需要填写认证信息，保存后确认连接状态正常。

每次使用 WorkBuddy 前都要先运行第 1 步；关闭那个 PowerShell 窗口后，本机 MCP 服务也会停止。服务默认只监听 `127.0.0.1`，局域网和互联网中的其他电脑无法访问。界面步骤依据 [WorkBuddy 官方 MCP 文档](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/MCP-Guide)。

## 试着问一句

接入完成后，可以直接对 Agent 说：

> 检查我的知网登录状态，然后检索近五年关于“大语言模型学术写作”的中文论文，按被引量排序。

如果 Agent 能调用 `get_login_status` 和 `search_cnki`，说明安装成功。

## 常见问题

### 提示 `No module named cnki_mcp_server`

通常是安装 MCP 时使用了另一套 Python。重新执行：

```powershell
py -3.11 -m pip install --user --upgrade "https://github.com/graywind-labs/hust-cnki-research-mcp/archive/refs/heads/main.zip"
```

### 没有弹出 Chrome，或提示找不到 Chrome

先确认 Chrome 已安装并能正常打开。若必须改用 Edge，可先在当前 PowerShell 中运行：

```powershell
$env:CNKI_BROWSER_CHANNEL = "msedge"
py -3.11 -m cnki_mcp_server --login
```

也可以通过 `CNKI_BROWSER_EXECUTABLE` 指定浏览器程序的绝对路径。

### 登录过期或工具提示未登录

关闭 Agent，再运行一次：

```powershell
py -3.11 -m cnki_mcp_server --login
```

登录完成后重启 Agent。

### WorkBuddy 连接不上

确认运行 `--http` 的 PowerShell 窗口仍然打开，并确认地址是 `http://127.0.0.1:8000/mcp`。如果 8000 端口已被占用，可在启动前更换端口：

```powershell
$env:CNKI_MCP_PORT = "8001"
py -3.11 -m cnki_mcp_server --http
```

此时 WorkBuddy 地址也要改为 `http://127.0.0.1:8001/mcp`。

### 开着代理软件时无法登录

本项目默认让 CNKI 和学校 SSO 的专用浏览器直连。如果你的网络必须经过代理，请在启动或登录前运行：

```powershell
$env:CNKI_DIRECT = "false"
```

## 可用工具

| 工具 | 用途 |
|---|---|
| `search_cnki` | 多字段检索、作者/期刊筛选、多页和排序 |
| `get_paper_detail` | 获取完整题录、摘要和可用权限入口 |
| `read_paper_fulltext` | 分段读取机构授权的在线正文 |
| `get_paper_bibtex` | 获取并补充 CNKI 官方 BibTeX |
| `download_paper_pdf` | 下载机构授权 PDF |
| `find_best_match` | 根据标题核验并匹配文献 |
| `get_login_status` | 检查会话状态，不返回认证秘密 |

## 登录与安全

MCP 没有读取或设置 Cookie 的工具，也不会把 Cookie、令牌、账号或密码返回给模型。所有网页导航均限制为 HTTPS 的 `*.cnki.net` 域名。机构或知网主动让会话失效时需要再次登录，这是 SSO 本身的安全规则。

WorkBuddy 的 HTTP 模式默认仅监听本机地址。请勿将监听地址改成 `0.0.0.0` 或直接暴露到公网，除非你清楚如何为 MCP 服务增加认证和网络访问控制。

## 手动安装（源码开发者）

手动方式放在这里，普通用户不需要执行。

```powershell
git clone https://github.com/graywind-labs/hust-cnki-research-mcp.git
cd hust-cnki-research-mcp
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
```

登录：

```powershell
.\.venv\Scripts\python.exe -m cnki_mcp_server --login
```

STDIO 模式启动：

```powershell
.\.venv\Scripts\python.exe -m cnki_mcp_server
```

WorkBuddy 所需的本机 HTTP 模式：

```powershell
.\.venv\Scripts\python.exe -m cnki_mcp_server --http
```

macOS 或 Linux 可使用 `python3` 和 `.venv/bin/python` 替换上述 Windows 命令。Chrome 可从 [Google Chrome 官网](https://www.google.com/chrome/)安装。

## 来源与许可

项目基于 [NoFixedPoint/cnki-mcp](https://github.com/NoFixedPoint/cnki-mcp) 增强，底座项目使用 MIT 许可证。本项目只访问当前用户和机构已经获得授权的内容，不提供绕过订阅、验证码或访问控制的能力。请遵守学校、数据库和版权方的使用规则，避免高频批量下载。
