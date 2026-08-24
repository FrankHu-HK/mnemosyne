# 部署到 GitHub 操作手册 / Deploy to GitHub Runbook

本目录 `Mnemosyne7.0.0_GitHub` 已是 **v7.0.0 全量升级后的 GitHub 仓库内容**，可直接推送到 `https://github.com/FrankHu-HK/mnemosyne`（全量替换旧版 `Mnemosyne Memory v5.1.4 20260814/` 内容）。

## 前置条件
- 已安装 `git`（带 PATH）。
- 已配置 GitHub 凭证（SSH key 或 `gh` 登录：`gh auth login`）。
- 本地已切换代理（如需访问外网）：`export https_proxy=http://127.0.0.1:7897 http_proxy=http://127.0.0.1:7897`。

## 步骤（一次性全量替换远程仓库）
```bash
# 1. 进入本目录
cd "C:/Users/hu_ji/Desktop/Mnemosyne7.0.0最终产品包/Mnemosyne7.0.0_GitHub"

# 2. 初始化并拉取远程（保留历史）
git init -q
git remote add origin https://github.com/FrankHu-HK/mnemosyne.git
git fetch origin
git checkout -b main origin/main || git checkout -b main

# 3. 清空旧跟踪文件（保留 .git）
git rm -r --cached -q . >/dev/null 2>&1
# 若远程仅有旧子目录，先删除远程旧文件：
# git rm -r --cached -q "Mnemosyne Memory v5.1.4 20260814" >/dev/null 2>&1

# 4. 加入 v7.0.0 全部文件
git add -A

# 5. 提交
git commit -m "Mnemosyne OS 7.0.0 — full upgrade: zero-dependency AI memory, MCP/API/CLI/Python, MIT, PyPI"

# 6. 强制覆盖远程（全量替换旧版）
git push -f origin main
```

> ⚠️ 第 6 步 `git push -f` 会覆盖远程全部历史内容，符合“全量替换”要求；执行前请确认备份需求。

## 验证（推送后）
- 仓库根目录应直接包含：`README.md`、`README_CN.md`、`LICENSE`、`setup.py`、`mnemosyne.py`、`mnemosyne/`、`docs/` 等，**不再出现** `Mnemosyne Memory v5.1.4 20260814/` 或任何 v5.1.4 描述。
- 徽章：PyPI / MIT / Python 3.8+ / MCP 13 Tools / 中文 均已在 README 顶部渲染。
- 旧仓库描述（"9.58/10 Hindsight. 85% Session Recall..."）需在 GitHub 仓库 Settings → About 中手动改为：
  `Mnemosyne OS 7.0.0 — zero-dependency, local-first AI memory system (MCP / API / CLI / Python). MIT.`

## 标识清单（已落实）
- ✅ MIT 许可证（`LICENSE` 文件 + 徽章 + 文末声明）
- ✅ PyPI 标识（`pip install mnemosyne-os` + PyPI 徽章）
- ✅ 接口标识：MCP（13 tools）、API（HTTP / REST）、CLI、Python（库 / Async）
- ✅ 中英文切换按钮：README.md ↔ README_CN.md 互链徽章
- ✅ 100% 沿用 hermes-agent 的 README 版式（居中 banner、徽章行、特性表、语言切换）
