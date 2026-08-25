#!/usr/bin/env python3
"""anti-asu-skills 静态校验器。

检查内容：
  1. 每个 skills/<name>/ 下存在 SKILL.md
  2. frontmatter 可解析，含 name 与 description
  3. frontmatter 的 name 与目录名一致
  4. description 非空且长度合理
  5. SKILL.md 与 references/ 中引用的本地 .md 路径真实存在
  6. .claude-plugin/*.json 为合法 JSON
  7. evals/evals.json 合法，且引用的 fixture 文件存在
  8. 隐私红线：不得出现手机号、邮箱等真实个人信息形态

退出码 0 表示全部通过。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

DESC_MIN, DESC_MAX = 40, 1200

# 隐私红线：公开仓库中不应出现的形态
PHONE_RE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
EMAIL_ALLOW = re.compile(r"(example|xyz|fake|test|noreply|your)", re.I)

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """解析简单的 YAML frontmatter（只需 key: value，值可跨行）。"""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    body = text[3:end].strip("\n")
    data: dict[str, str] = {}
    key = None
    for line in body.split("\n"):
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            data[key] = m.group(2).strip()
        elif key and line.strip():
            data[key] += " " + line.strip()
    return data


def check_skill(d: Path) -> None:
    sk = d / "SKILL.md"
    if not sk.exists():
        err(f"{d.name}: 缺少 SKILL.md")
        return

    text = sk.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        err(f"{d.name}: frontmatter 无法解析（需以 --- 开头并以 --- 结束）")
        return

    name = fm.get("name", "")
    if not name:
        err(f"{d.name}: frontmatter 缺少 name")
    elif name != d.name:
        err(f"{d.name}: frontmatter name='{name}' 与目录名不一致")

    desc = fm.get("description", "")
    if not desc:
        err(f"{d.name}: frontmatter 缺少 description")
    elif not (DESC_MIN <= len(desc) <= DESC_MAX):
        warn(f"{d.name}: description 长度 {len(desc)}，建议 {DESC_MIN}-{DESC_MAX}")


def check_links(md: Path) -> None:
    """校验 markdown 中形如 [text](path.md) 的本地链接。"""
    text = md.read_text(encoding="utf-8")
    for target in re.findall(r"\]\(([^)#]+\.md)\)", text):
        if target.startswith(("http://", "https://")):
            continue
        if not (md.parent / target).resolve().exists():
            err(f"{md.relative_to(ROOT)}: 引用的文件不存在 -> {target}")


def check_privacy(md: Path) -> None:
    text = md.read_text(encoding="utf-8")
    rel = md.relative_to(ROOT)
    for hit in PHONE_RE.findall(text):
        err(f"{rel}: 疑似手机号 {hit[:3]}****{hit[-2:]}")
    for hit in EMAIL_RE.findall(text):
        if not EMAIL_ALLOW.search(hit):
            err(f"{rel}: 疑似真实邮箱 {hit}")


def main() -> int:
    if not SKILLS.is_dir():
        err("缺少 skills/ 目录")
        return report()

    skill_dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    if not skill_dirs:
        err("skills/ 下没有任何 skill")

    for d in skill_dirs:
        check_skill(d)

    md_files = sorted(ROOT.rglob("*.md"))
    for md in md_files:
        if ".git" in md.parts:
            continue
        check_links(md)
        check_privacy(md)

    for p in sorted((ROOT / ".claude-plugin").glob("*.json")):
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(f"{p.relative_to(ROOT)}: JSON 非法 -> {e}")

    evals = ROOT / "evals" / "evals.json"
    if evals.exists():
        try:
            data = json.loads(evals.read_text(encoding="utf-8"))
            for ev in data.get("evals", []):
                for f in ev.get("files", []):
                    if not (ROOT / "evals" / f).exists() and not (ROOT / f).exists():
                        err(f"evals.json: eval {ev.get('id')} 引用的文件不存在 -> {f}")
                if not ev.get("assertions"):
                    warn(f"evals.json: eval {ev.get('id')} 没有断言")
        except json.JSONDecodeError as e:
            err(f"evals/evals.json: JSON 非法 -> {e}")

    print(f"已检查 {len(skill_dirs)} 个 skill、{len(md_files)} 个 markdown 文件。")
    return report()


def report() -> int:
    for w in warnings:
        print(f"  warn  {w}")
    for e in errors:
        print(f"  ERROR {e}")
    if errors:
        print(f"\n校验失败：{len(errors)} 个错误、{len(warnings)} 个警告。")
        return 1
    print(f"\n校验通过{'（' + str(len(warnings)) + ' 个警告）' if warnings else ''}。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
