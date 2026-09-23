#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mnemosyne OS -- documentation consistency gate
==============================================

Every language edition of the README, and every overview document, has to state
the *same* product facts about the *same* release.  This script is the machine
check for that.  Run it before tagging a release; wire it into CI if you want
the guarantee to hold without anyone remembering to look.

It checks six things:

1. **Edition parity** -- every ``README.*.md`` mirrors the canonical ``README.md``
   in structure: same heading levels, same capability-table rows, same number of
   code fences, same number of table rows.

2. **Required facts** -- each edition states the release version, the MCP tool
   count, the provider counts, the benchmarks and the zero-dependency claim.

3. **Forbidden strings** -- stale badges, retired tool counts, the old brand
   spelling and references to code that no longer ships.

4. **Declared version** -- every *declaration* of the version (``__version__``,
   ``VERSION``, ``setup.py``, plugin manifests, pyproject) reads 8.0.0.  A
   version number in *prose* is left alone in the documents that record defect
   history: those numbers say *when a fix landed*, and rewriting them would
   falsify the record.  See ``scripts/bump_version.py`` for the same policy.

5. **Link and path targets** -- markdown links and backticked repository paths
   point at files that exist.

6. **MCP tool inventory** -- the tool count and the *names* an edition lists are
   read back against the MCP server source.  A headline number that agrees with
   the code while the table below it names a different set is still a lie, so
   both the total and the membership are checked.

Exit status is 0 only when everything passes.

Usage::

    python scripts/verify_docs_consistency.py
    python scripts/verify_docs_consistency.py --root .
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from typing import Dict, List, Tuple

ROOT_DEFAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = frozenset({".git", "__pycache__", ".pytest_cache", ".mypy_cache",
                       "node_modules", "dist", "build", ".venv", "venv"})

VERSION = "8.0.0"

#: The canonical edition plus every translated one.
EDITIONS = ["README.md", "README_CN.md", "README_TW.md", "README.de.md",
            "README.es.md", "README.ja.md", "README.ko.md", "README.ru.md",
            "README.th.md"]

#: Facts every edition must state identically.  Keep this list in step with the
#: canonical README: a number that is not here is a number nobody is checking.
REQUIRED_FACTS: List[Tuple[str, str]] = [
    ("release version", r"8\.0\.0"),
    ("MCP badge shows 31 Tools", r"MCP-31%20Tools"),
    ("MCP tool count 31 (prose)", r"\b31\b"),
    ("Python floor", r"Python 3\.8\+"),
    ("install command", r"pip install mnemosyne-os"),
    ("provider total (72)", r"\b72\b"),
    ("provider split (20 LLM / 13 embedder)", r"\b20\b[\s\S]{0,400}?\b13\b"),
    ("benchmark LongMemEval", r"96\.2"),
    ("benchmark LoCoMo", r"94\.8"),
    ("benchmark BEAM 1M", r"68\.5"),
    ("benchmark BEAM 10M", r"53\.9"),
    ("zero-dependency claim", r"install_requires"),
    ("ledger hash", r"SHA-256"),
    ("score scale", r"\b100\b"),
]

#: High-signal strings that must never come back.  Deliberately precise: a broad
#: "20 <tool-word>" rule would fire on the correct phrasing "31 tools -- 20 native
#: plus 11 compatible", which every edition is supposed to contain.
FORBIDDEN: List[Tuple[str, str]] = [
    ("stale MCP badge", r"MCP-20%20Tools"),
    ("stale MCP total in Simplified Chinese", r"20 个工具"),
    ("stale MCP total in Traditional Chinese", r"20 個工具"),
    ("stale MCP total in the runbook", r"MCP[（(]20 tools[）)]"),
    ("brand: lowercase mnemosyne OS", r"(?<![A-Za-z-])mnemosyne OS(?!-)"),
    ("brand: caduceus glyph", r"☤"),
    ("stale provider count (67)", r"\b67\b"),
    ("removed context_engine package", r"(?<![A-Za-z_])context_engine/"),
    ("stale release-folder reference", r"Mnemosyne ?8\.0\.0/"),
    ("deleted comparison.md", r"comparison\.md"),
    ("deleted COMPLIANCE.md", r"COMPLIANCE\.md"),
    ("deleted tests/ suite", r"\btests/test_"),
]

#: Documents whose *prose* version numbers are historical records, not claims
#: about the current release.  A 7.0.2 here means "this defect was fixed in
#: 7.0.2" and is correct as written.
HISTORY_FILES = frozenset({
    "CHANGELOG.md",
    "docs/KNOWN_DEFECTS.md",
    "docs/ACCEPTANCE_GUIDE.md",
    "docs/DEPLOY_DEEPSEEK_HARNESS.md",
    "docs/RECALL_STRATEGY.md",
    "scripts/bump_version.py",
})

#: Declaration shapes that must read 8.0.0.
DECLARATIONS: List[Tuple[str, str]] = [
    ("__version__", r'__version__\s*=\s*"([^"]+)"'),
    ("VERSION", r'(?m)^VERSION\s*=\s*"([^"]+)"'),
    ("setup.py version", r'(?<![_a-z])version\s*=\s*"([^"]+)"'),
    ("JSON version field", r'"version"\s*:\s*"([^"]+)"'),
]

PROSE_VERSION_RE = re.compile(r"(?<![\d.])\d+\.\d+\.\d+(?![\d.])")
#: A version preceded (within a short window) by one of these is a third-party
#: version -- a vector store release, an interpreter, a placeholder -- and is
#: none of this script's business.
THIRD_PARTY_CTX = re.compile(
    r"qdrant|n8n|dify|vercel|langchain|llama|node|python|proxy|127\.0\.0\.1"
    r"|npm|pip|docker|x\.y\.z"
    # the v5 predecessor was a different product with its own version line
    r"|mnemosyne memory",
    re.I,
)
#: A version that appears inside this window of the product name *is* a claim
#: about the product, wherever it lives.
PRODUCT_CTX = re.compile(r"mnemosyne", re.I)

#: Phrasings that assert the *current* release.  Checked everywhere -- including
#: the defect-history documents, which are otherwise allowed to carry old version
#: numbers because those record when a fix landed.
CURRENT_VERSION_RE = re.compile(
    r"(?:当前版本|目前版本|current version|aktuelle Version|versión actual"
    r"|現在のバージョン|현재 버전|текущая версия|เวอร์ชันปัจจุบัน)"
    r"\s*[（(]?\s*(\d+\.\d+\.\d+)",
    re.I,
)

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#\s]+)\)|href=\"([^\"#\s]+)\"")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
PATHISH_RE = re.compile(r"^(?:\./)?(?:[\w.\-]+/)+[\w.\-]+/?$")
CODE_EXT = frozenset({".py", ".md", ".json", ".toml", ".sh", ".yml", ".yaml",
                      ".cfg", ".ini", ".txt", ".js", ".html", ".css"})
#: Prefixes that mark a reference as living outside this repository: the user's
#: own client configuration, or a runtime data directory.
PREFIX_IGNORE = re.compile(r"^(?:\.[\w.\-]+/|data/|~/|/etc/|/usr/)")
#: Tokens that look path-like but are not repository paths.
PATH_IGNORE = re.compile(
    r"^(?:/|~"
    r"|mnemosyne\.[a-z_]+(?:\.[a-z_]+)*"        # dotted python module path
    r"|[\w.\-]+/[\w.\-]+\.(?:db|sqlite|log)"    # runtime artefacts
    r"|--?[\w\-]+/[\w\-]+"                      # CLI flags: --from/--to
    r"|(?:try|except|high|medium|low|and|or)(?:/[\w\-]+)+"
    r")$"
)


#: ---- MCP tool inventory ----------------------------------------------------
#: Read from source rather than by importing the server: the gate must run in CI
#: with no brain directory, no side effects and no import cost.  The count a
#: document states is checked *against this*, never against a constant that both
#: sides can drift from together.
TOOL_SRC = "mnemosyne/webui/mcp_server.py"
TOOL_API_SRC = "mnemosyne/webui/mcp_api.py"
#: The native table is one compact dict per line; the compatibility module uses a
#: spaced, multi-line layout.
NATIVE_TOOL_RE = re.compile(r'\{"name":"([A-Za-z0-9_/\-]+)"')
API_TOOL_RE = re.compile(r'"name":\s*"([A-Za-z0-9_/\-]+)"')
#: A capability-table row whose first cell is a tool name.
TOOL_CELL_RE = re.compile(r"(?m)^\|\s*`([A-Za-z0-9_/\-]+)`\s*\|")
#: The badge every edition carries.
TOOL_BADGE_RE = re.compile(r"MCP-(\d+)%20Tools")


def walk(root: str, exts: Tuple[str, ...]) -> List[str]:
    out: List[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.endswith(exts):
                out.append(os.path.join(dirpath, name))
    return sorted(out)


def read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def shape(text: str) -> Dict[str, int]:
    return {
        "h2": len(re.findall(r"(?m)^##\s", text)),
        "h3": len(re.findall(r"(?m)^###\s", text)),
        "tr": len(re.findall(r"<tr>", text)),
        "rows": len(re.findall(r"(?m)^\|", text)),
        "fences": len(re.findall(r"(?m)^```", text)),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=ROOT_DEFAULT)
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    failures: List[str] = []
    md_files = walk(root, (".md",))

    def rel_of(p: str) -> str:
        return os.path.relpath(p, root).replace(os.sep, "/")

    # ---------------------------------------------------------------- 1 + 2
    canon_path = os.path.join(root, EDITIONS[0])
    if not os.path.exists(canon_path):
        print(f"FATAL: canonical {EDITIONS[0]} not found under {root}")
        return 2
    canon_shape = shape(read(canon_path))

    print("=" * 74)
    print(f"1. EDITION PARITY  (canonical: {EDITIONS[0]}, release {VERSION})")
    print("=" * 74)
    keys = list(canon_shape)
    print(f"  {'edition':<16} " + " ".join(f"{k:>7}" for k in keys))
    print(f"  {EDITIONS[0]:<16} " + " ".join(f"{canon_shape[k]:>7}" for k in keys))
    for ed in EDITIONS[1:]:
        p = os.path.join(root, ed)
        if not os.path.exists(p):
            failures.append(f"{ed}: edition missing")
            print(f"  {ed:<16} MISSING")
            continue
        s = shape(read(p))
        print(f"  {ed:<16} " + " ".join(f"{s[k]:>7}" for k in keys))
        for k in keys:
            if s[k] != canon_shape[k]:
                failures.append(
                    f"{ed}: structure drift -- {k}={s[k]}, README.md={canon_shape[k]}")

    print()
    print("=" * 74)
    print("2. REQUIRED FACTS PER EDITION")
    print("=" * 74)
    for ed in EDITIONS:
        p = os.path.join(root, ed)
        if not os.path.exists(p):
            continue
        text = read(p)
        missing = [lbl for lbl, pat in REQUIRED_FACTS if not re.search(pat, text)]
        if missing:
            failures.append(f"{ed}: missing facts -- {', '.join(missing)}")
        print(f"  {ed:<16} {'OK' if not missing else 'MISSING: ' + ', '.join(missing)}")

    # ---------------------------------------------------------------- 3
    print()
    print("=" * 74)
    print("3. FORBIDDEN STRINGS")
    print("=" * 74)
    hits = 0
    for path in md_files:
        rel = rel_of(path)
        if rel == "CHANGELOG.md":
            continue
        text = read(path)
        for lbl, pat in FORBIDDEN:
            for m in re.finditer(pat, text):
                lineno = text[:m.start()].count("\n") + 1
                failures.append(
                    f"{rel}:{lineno}: forbidden -- {lbl} :: {m.group(0)!r}")
                hits += 1
    print(f"  violations: {hits}")

    # ---------------------------------------------------------------- 4
    print()
    print("=" * 74)
    print("4. DECLARED VERSION")
    print("=" * 74)
    decl_ok = 0
    for path in walk(root, (".py", ".json", ".toml")):
        rel = rel_of(path)
        text = read(path)
        for lbl, pat in DECLARATIONS:
            for m in re.finditer(pat, text):
                val = m.group(1)
                if not re.fullmatch(r"\d+\.\d+\.\d+", val):
                    continue
                if val != VERSION:
                    lineno = text[:m.start()].count("\n") + 1
                    failures.append(
                        f"{rel}:{lineno}: declared {lbl}={val}, expected {VERSION}")
                    print(f"  {rel:<44} {lbl:<20} {val}  <- WRONG")
                else:
                    decl_ok += 1
    print(f"  declarations reading {VERSION}: {decl_ok}")

    print()
    print("  explicit current-version claims (checked in every document):")
    claims = 0
    bad_claims = 0
    for path in md_files:
        rel = rel_of(path)
        if rel == "CHANGELOG.md":
            continue
        text = read(path)
        for m in CURRENT_VERSION_RE.finditer(text):
            claims += 1
            if m.group(1) != VERSION:
                lineno = text[:m.start()].count("\n") + 1
                failures.append(
                    f"{rel}:{lineno}: current-version claim reads {m.group(1)}, "
                    f"expected {VERSION}")
                bad_claims += 1
    print(f"  claims: {claims}   wrong: {bad_claims}")

    print()
    print("  prose version numbers that claim the product version:")
    drift = 0
    for path in md_files:
        rel = rel_of(path)
        if rel in HISTORY_FILES or rel == "CHANGELOG.md":
            continue
        text = read(path)
        for m in PROSE_VERSION_RE.finditer(text):
            val = m.group(0)
            if val == VERSION or val == "127.0.0.1":
                continue
            ctx = text[max(0, m.start() - 60):m.end() + 60]
            if THIRD_PARTY_CTX.search(ctx):
                continue
            # a stray version next to unrelated prose is not a product claim
            if not PRODUCT_CTX.search(text[max(0, m.start() - 40):m.start()]):
                continue
            lineno = text[:m.start()].count("\n") + 1
            failures.append(f"{rel}:{lineno}: prose version {val} is not {VERSION}")
            drift += 1
    print(f"  drift: {drift}")

    # ---------------------------------------------------------------- 5
    print()
    print("=" * 74)
    print("5. LINK AND PATH TARGETS")
    print("=" * 74)
    dead_links = 0
    for path in md_files:
        rel = rel_of(path)
        base = os.path.dirname(path)
        text = read(path)
        for m in LINK_RE.finditer(text):
            target = m.group(1) or m.group(2) or ""
            if not target or target.startswith(("http://", "https://", "mailto:",
                                               "#", "data:")):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(base, target))):
                lineno = text[:m.start()].count("\n") + 1
                failures.append(f"{rel}:{lineno}: dead link -> {target}")
                dead_links += 1

    dead_paths = 0
    checked = 0
    for path in md_files:
        rel = rel_of(path)
        if rel == "CHANGELOG.md":
            continue
        base = os.path.dirname(path)
        for lineno, line in enumerate(read(path).splitlines(), 1):
            for m in BACKTICK_RE.finditer(line):
                tok = m.group(1).strip()
                if not tok or tok.startswith(("http://", "https://", "file://")):
                    continue
                if PATH_IGNORE.match(tok) or PREFIX_IGNORE.match(tok):
                    continue
                if not PATHISH_RE.match(tok):
                    continue
                bare = tok.rstrip("/")
                ext = os.path.splitext(bare)[1].lower()
                is_dir_ref = tok.endswith("/")
                if ext:
                    if ext not in CODE_EXT:
                        continue
                elif not is_dir_ref:
                    # "memory/export-v1" -- an identifier that happens to carry a
                    # slash, not a claim about a path.  Documentation states
                    # directories with a trailing slash and files with a source
                    # extension; anything else is a name (an MCP tool, a flag).
                    continue
                if len(tok) > 120:
                    continue
                checked += 1
                if not (os.path.exists(os.path.normpath(os.path.join(root, bare)))
                        or os.path.exists(os.path.normpath(os.path.join(base, bare)))):
                    failures.append(f"{rel}:{lineno}: dead path -> `{tok}`")
                    dead_paths += 1
    print(f"  dead markdown links : {dead_links}")
    print(f"  paths checked       : {checked}")
    print(f"  dead paths          : {dead_paths}")

    # ---------------------------------------------------------------- 6
    print()
    print("=" * 74)
    print("6. MCP TOOL INVENTORY  (documented vs. implemented)")
    print("=" * 74)
    server_text = read(os.path.join(root, TOOL_SRC))
    # everything before the compatibility divider is the native table
    native_tools = NATIVE_TOOL_RE.findall(server_text.split("# ---- client API tools")[0])
    api_tools = API_TOOL_RE.findall(read(os.path.join(root, TOOL_API_SRC)))
    all_tools = native_tools + api_tools
    total = len(all_tools)
    tool_set = set(all_tools)
    if len(tool_set) != total:
        dupes = sorted({n for n in all_tools if all_tools.count(n) > 1})
        failures.append(f"{TOOL_SRC}: duplicate MCP tool name(s) -- {', '.join(dupes)}")
    print(f"  implemented : {len(native_tools)} native + {len(api_tools)} "
          f"client-compatible = {total}")
    print(f"  {'edition':<16} {'badge':<8} named")
    for ed in EDITIONS:
        p = os.path.join(root, ed)
        if not os.path.exists(p):
            continue
        text = read(p)
        badge = TOOL_BADGE_RE.search(text)
        listed = {n for n in TOOL_CELL_RE.findall(text) if n in tool_set}
        problems: List[str] = []
        if not badge:
            problems.append("no MCP badge")
        elif int(badge.group(1)) != total:
            problems.append(f"badge states {badge.group(1)}, code has {total}")
        missing = [n for n in all_tools if n not in listed]
        if missing:
            problems.append(f"table omits {len(missing)}: {', '.join(missing[:4])}")
        if problems:
            failures.append(f"{ed}: tool inventory -- {'; '.join(problems)}")
        print(f"  {ed:<16} {(badge.group(1) if badge else '-'):<8} "
              f"{len(listed):>2}/{total}   {'OK' if not problems else 'MISMATCH'}")

    # ---------------------------------------------------------------- verdict
    print()
    print("=" * 74)
    if failures:
        print(f"FAIL -- {len(failures)} problem(s)")
        print("=" * 74)
        for f in failures:
            print(f"  ! {f}")
        return 1
    print(f"PASS -- all {len(EDITIONS)} editions state the same {VERSION} facts")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
