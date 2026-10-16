#!/usr/bin/env python3
"""Validate the career-research skill package and career research project data.

Standard library only. Two modes:

    python scripts/quick_validate.py --skill <skill_dir>
    python scripts/quick_validate.py --project <project_dir>

Exit code 0 when every check passes, 1 otherwise.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import sys
from pathlib import Path

CATALOG_COLUMNS = [
    "career_id",
    "name",
    "common_titles",
    "domain",
    "existence_status",
    "funnel_stage",
    "stage_reason",
    "core_work",
    "typical_employers",
    "typical_regions",
    "entry_roles",
    "education_and_qualification",
    "skills_and_qualifications",
    "fresh_graduate_fit",
    "profile_fit",
    "research_priority",
    "research_state",
    "last_checked",
    "evidence_gap",
    "next_task",
]

CATALOG_REQUIRED = [
    "career_id",
    "name",
    "domain",
    "existence_status",
    "funnel_stage",
    "core_work",
    "research_priority",
    "research_state",
]

EMERGING_COLUMNS = [
    "emerging_id",
    "name",
    "definition",
    "related_real_evidence",
    "demand_and_payer",
    "potential_employers",
    "entry_skills_and_cost",
    "income_sources",
    "self_automation_risk",
    "transitory_risk",
    "credibility",
    "prediction_marked",
    "last_checked",
    "next_task",
]

EMERGING_REQUIRED = ["emerging_id", "name", "definition", "credibility", "prediction_marked"]

EXISTENCE_STATUS = {"成熟职业", "真实招聘岗位", "新兴岗位"}
FUNNEL_STAGE = {"候选池", "硬筛", "快扫", "深研", "决策", "排除"}
FRESH_GRADUATE_FIT = {"适合", "有条件适合", "通常不适合", "待验证"}
PROFILE_FIT = {"1", "2", "3", "4", "5", "待验证"}
RESEARCH_PRIORITY = {"高", "中", "低", "待定"}
RESEARCH_STATE = {"未研究", "研究中", "已完成", "待补充证据", "已排除"}
SOURCE_VERIFICATION_STATUS = {"已核验", "部分核验", "待核验", "已失效"}
SOURCE_GRADE = {"A", "B", "C", "D"}
CREDIBILITY = {"A", "B", "C", "D"}
PREDICTION_FLAG = {"是", "否"}
RISK_LEVEL = {"低", "中", "高", "未知"}

REPORT_SECTIONS = [
    "## 1. 职业定义",
    "## 2. 真实工作内容",
    "## 3. 真实工作案例",
    "## 4. 入行门槛",
    "## 5. 薪资情况",
    "## 6. 就业难度",
    "## 7. 工作环境",
    "## 8. 职业发展路径",
    "## 9. AI 影响分析",
    "## 10. 职业优缺点",
    "## 11. 与用户的匹配程度",
    "## 12. 现实证据",
    "## 13. 最终结论",
]

QUICK_SCAN_SECTIONS = [
    "## 1. 一句话结论",
    "## 2. 核心工作与区分",
    "## 3. 应届生入口",
    "## 4. 收入样本",
    "## 5. 工作条件",
    "## 6. 市场需求",
    "## 7. AI 影响摘要",
    "## 8. 与用户的匹配摘要",
    "## 9. 证据缺口",
    "## 10. 快扫结论",
]

SKILL_ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
CATALOG_ID_RE = re.compile(r"^C\d{3}$")
EMERGING_ID_RE = re.compile(r"^E\d{3}$")
SKILL_NAME_RE = re.compile(r"^[a-z0-9-]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LINK_RE = re.compile(r"\]\(([^)]+)\)")
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")


class Report:
    """Collect check results."""

    def __init__(self) -> None:
        self.items: list[tuple[bool, str, str]] = []

    def add(self, ok: bool, name: str, detail: str = "") -> None:
        self.items.append((ok, name, detail))
        marker = "PASS" if ok else "FAIL"
        line = f"[{marker}] {name}"
        if detail:
            line += f" | {detail}"
        print(line)

    @property
    def failed(self) -> list[tuple[bool, str, str]]:
        return [item for item in self.items if not item[0]]

    def summary(self) -> int:
        failures = self.failed
        total = len(self.items)
        if failures:
            print(f"\n{total - len(failures)}/{total} checks passed, {len(failures)} failed.")
            return 1
        print(f"\n{total}/{total} checks passed.")
        return 0


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def strip_fenced_blocks(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def split_frontmatter(text: str) -> tuple[dict[str, str], str] | tuple[None, str]:
    """Minimal frontmatter parser for flat keys, block scalars and quoted values."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    match = re.match(r"^---\n(.*?)\n---\n?", normalized, re.DOTALL)
    if not match:
        return None, normalized
    raw = match.group(1)
    body = normalized[match.end():]
    data: dict[str, str] = {}
    lines = raw.split("\n")
    index = 0
    while index < len(lines):
        line = lines[index]
        index += 1
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key_match = re.match(r"^([A-Za-z0-9_.-]+):(?:\s*(.*))?$", line)
        if not key_match:
            continue
        key = key_match.group(1)
        value = (key_match.group(2) or "").strip()
        if value in (">", "|", ">-", "|-", ">+", "|+"):
            block: list[str] = []
            while index < len(lines) and (not lines[index].strip() or lines[index].startswith((" ", "\t"))):
                block.append(lines[index].strip())
                index += 1
            data[key] = " ".join(part for part in block if part)
        else:
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            data[key] = value
    return data, body


def parse_openai_yaml(text: str) -> dict[str, str]:
    """Read only the interface block of agents/openai.yaml."""
    interface: dict[str, str] = {}
    in_interface = False
    for raw_line in text.replace("\r\n", "\n").split("\n"):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if re.match(r"^[A-Za-z0-9_.-]+:", raw_line):
            in_interface = raw_line.split(":", 1)[0].strip() == "interface"
            continue
        if not in_interface:
            continue
        match = re.match(r"^\s+([A-Za-z0-9_.-]+):\s*(.*)$", raw_line)
        if not match:
            continue
        value = match.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        interface[match.group(1)] = value
    return interface


def is_iso_date(value: str) -> bool:
    if not DATE_RE.fullmatch(value):
        return False
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def validate_skill(skill_dir: Path, report: Report) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        report.add(False, "SKILL.md 存在", str(skill_md))
        return
    report.add(True, "SKILL.md 存在")

    text = read_text(skill_md)
    frontmatter, body = split_frontmatter(text)
    if frontmatter is None:
        report.add(False, "SKILL.md frontmatter 格式", "缺少合法的 --- 区块")
        return
    report.add(True, "SKILL.md frontmatter 格式")

    unexpected = sorted(set(frontmatter) - SKILL_ALLOWED_KEYS)
    report.add(
        not unexpected,
        "frontmatter 键名合法",
        "" if not unexpected else "未知键: " + ", ".join(unexpected),
    )

    name = frontmatter.get("name", "").strip()
    if not name:
        report.add(False, "frontmatter name", "缺失")
    elif not SKILL_NAME_RE.fullmatch(name):
        report.add(False, "frontmatter name", "只能小写字母、数字与连字符")
    elif name.startswith("-") or name.endswith("-") or "--" in name:
        report.add(False, "frontmatter name", "不能首尾连字符或连续连字符")
    elif len(name) > 64:
        report.add(False, "frontmatter name", f"长度 {len(name)} 超过 64")
    else:
        report.add(True, "frontmatter name")

    description = frontmatter.get("description", "").strip()
    if not description:
        report.add(False, "frontmatter description", "缺失")
    elif "<" in description or ">" in description:
        report.add(False, "frontmatter description", "不能包含尖括号")
    elif description.startswith("[TODO:"):
        report.add(False, "frontmatter description", "仍是 TODO 占位")
    elif len(description) > 1024:
        report.add(False, "frontmatter description", f"长度 {len(description)} 超过 1024")
    else:
        report.add(True, "frontmatter description", f"{len(description)} 字符")

    report.add(name in description, "description 含 skill 名", "" if name in description else "便于前端展示与检索")

    todo_hits = [
        line.strip()
        for line in body.split("\n")
        if re.fullmatch(r"\[TODO:[^\n]*\]", line.strip())
    ]
    report.add(not todo_hits, "正文无 TODO 占位", "; ".join(todo_hits))

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.is_file():
        report.add(False, "agents/openai.yaml 存在", str(openai_yaml))
    else:
        report.add(True, "agents/openai.yaml 存在")
        interface = parse_openai_yaml(read_text(openai_yaml))
        display_name = interface.get("display_name", "")
        short_description = interface.get("short_description", "")
        default_prompt = interface.get("default_prompt", "")
        report.add(bool(display_name), "openai.yaml display_name", "" if display_name else "缺失")
        report.add(
            25 <= len(short_description) <= 64,
            "openai.yaml short_description",
            f"长度 {len(short_description)}，要求 25 到 64",
        )
        report.add(
            bool(name) and f"${name}" in default_prompt,
            "openai.yaml default_prompt",
            "" if f"${name}" in default_prompt else "必须包含 $skill-name",
        )

    searchable = strip_fenced_blocks(body)
    targets: list[str] = []
    for raw in LINK_RE.findall(searchable) + INLINE_CODE_RE.findall(searchable):
        candidate = raw.strip().strip("`").split("#")[0]
        if not candidate:
            continue
        if candidate.startswith(("references/", "assets/", "scripts/")):
            targets.append(candidate)
    targets.append("scripts/quick_validate.py")

    missing: list[str] = []
    for target in sorted(set(targets)):
        if not (skill_dir / target).exists():
            missing.append(target)
    report.add(not missing, "SKILL.md 引用的文件都存在", "" if not missing else "缺失: " + "; ".join(missing))

    reference_files = sorted((skill_dir / "references").glob("*.md")) if (skill_dir / "references").is_dir() else []
    report.add(bool(reference_files), "references 目录非空", f"{len(reference_files)} 个文档")
    for relative in ["references/source-catalog.md", "references/quick-scan-template.md"]:
        target = skill_dir / relative
        report.add(target.is_file(), f"{relative} 存在", "" if target.is_file() else str(target))

    template_dir = skill_dir / "assets" / "project-template"
    report.add(template_dir.is_dir(), "assets/project-template 存在", str(template_dir))


def read_csv(path: Path, expected: list[str], report: Report, label: str) -> list[dict[str, str]]:
    if not path.is_file():
        report.add(False, f"{label} 存在", str(path))
        return []
    report.add(True, f"{label} 存在")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []
        rows = list(reader)
    if header != expected:
        report.add(False, f"{label} 表头", "实际: " + ", ".join(header))
        return rows
    report.add(True, f"{label} 表头")
    return rows


def check_id_rows(
    rows: list[dict[str, str]],
    id_field: str,
    id_pattern: re.Pattern[str],
    required: list[str],
    report: Report,
    label: str,
) -> set[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    bad_format: list[str] = []
    missing_required: list[str] = []
    for row in rows:
        value = (row.get(id_field) or "").strip()
        label_value = value or "(空)"
        if not id_pattern.fullmatch(value):
            bad_format.append(value or "(空)")
        else:
            if value in seen:
                duplicates.append(value)
            seen.add(value)
        for field in required:
            if not (row.get(field) or "").strip():
                missing_required.append(f"{label_value}.{field}")
    report.add(not bad_format, f"{label} ID 格式合法", "; ".join(bad_format))
    report.add(not duplicates, f"{label} ID 无重复", "; ".join(sorted(set(duplicates))))
    report.add(not missing_required, f"{label} 必填字段完整", "; ".join(missing_required))
    return seen


def check_enum(rows: list[dict[str, str]], field: str, allowed: set[str], report: Report, label: str) -> None:
    bad = [
        f"{(row.get('career_id') or row.get('emerging_id') or '?')}.{field}={row.get(field, '')}"
        for row in rows
        if (row.get(field) or "").strip() and (row.get(field) or "").strip() not in allowed
    ]
    report.add(not bad, f"{label}.{field} 取值合法", "; ".join(bad))


def check_dates(rows: list[dict[str, str]], records: list[str], report: Report, label: str) -> None:
    bad: list[str] = []
    for row in rows:
        for field in records:
            value = (row.get(field) or "").strip()
            if value and value != "未核查" and not is_iso_date(value):
                bad.append(f"{row.get('career_id') or row.get('emerging_id') or '?'}.{field}={value}")
    report.add(not bad, f"{label} 日期格式", "; ".join(bad))


def check_sources_file(path: Path, career_id: str, report: Report) -> None:
    if not path.is_file():
        report.add(False, f"{career_id} sources.md 存在", str(path))
        return
    text = read_text(path)
    headings = list(re.finditer(r"^##\s+(S\d{3})\s*$", text, flags=re.MULTILINE))
    if not headings:
        report.add(False, f"{career_id} sources.md 含来源条目", "没有 ## S 条目")
        return
    problems: list[str] = []
    for index, heading in enumerate(headings):
        start = heading.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        block = text[start:end]
        title = heading.group(1)
        link = re.search(r"^-\s*链接[:：]\s*(.+)$", block, re.MULTILINE)
        published = re.search(r"^-\s*发布日期[:：]\s*(.+)$", block, re.MULTILINE)
        access = re.search(r"^-\s*访问日期[:：]\s*(.+)$", block, re.MULTILINE)
        grade = re.search(r"^-\s*来源等级[:：]\s*(.+)$", block, re.MULTILINE)
        sample = re.search(r"^-\s*样本量[:：]\s*(.+)$", block, re.MULTILINE)
        verification = re.search(r"^-\s*核验状态[:：]\s*(.+)$", block, re.MULTILINE)
        required_fields = [
            "来源类型",
            "标题",
            r"发布机构(?:或作者)?",
            "链接",
            "发布日期",
            "访问日期",
            "覆盖地区",
            "统计口径",
            "来源等级",
            "样本量",
            "支持的结论",
            "可信度与限制",
            "关键摘录",
            "核验状态",
            "替代链接",
        ]
        for field in required_fields:
            if not re.search(rf"^-\s*{field}[:：]", block, re.MULTILINE):
                problems.append(f"{title} 缺字段 {field.replace(chr(92), '')}")
        if not link or not link.group(1).strip().startswith("http"):
            problems.append(f"{title} 缺 http 链接")
        if not published or (
            published.group(1).strip() != "未知" and not is_iso_date(published.group(1).strip())
        ):
            problems.append(f"{title} 发布日期缺失或格式不符")
        if not access or not is_iso_date(access.group(1).strip()):
            problems.append(f"{title} 访问日期缺失或格式不符")
        if not grade or grade.group(1).strip() not in SOURCE_GRADE:
            problems.append(f"{title} 来源等级缺失或取值不符")
        if not sample or not sample.group(1).strip():
            problems.append(f"{title} 样本量缺失")
        if not verification or verification.group(1).strip() not in SOURCE_VERIFICATION_STATUS:
            problems.append(f"{title} 核验状态缺失或取值不符")
    report.add(not problems, f"{career_id} sources.md 字段完整", "; ".join(problems))


def check_quick_scan_file(path: Path, career_id: str, report: Report) -> None:
    if not path.is_file():
        report.add(False, f"{career_id} quick_scan.md 存在", str(path))
        return
    text = read_text(path)
    frontmatter, body = split_frontmatter(text)
    if frontmatter is None:
        report.add(False, f"{career_id} quick_scan.md frontmatter", "缺少合法 frontmatter")
        return
    problems: list[str] = []
    if (frontmatter.get("id") or "").strip() != career_id:
        problems.append(f"id={frontmatter.get('id', '')}")
    if not (frontmatter.get("name") or "").strip():
        problems.append("name 缺失")
    if (frontmatter.get("funnel_stage") or "").strip() != "快扫":
        problems.append(f"funnel_stage={frontmatter.get('funnel_stage', '')}")
    last_checked = (frontmatter.get("last_checked") or "").strip()
    if last_checked != "未核查" and not is_iso_date(last_checked):
        problems.append(f"last_checked={last_checked}")
    report.add(not problems, f"{career_id} quick_scan.md frontmatter", "; ".join(problems))
    missing_sections = [section for section in QUICK_SCAN_SECTIONS if section not in body]
    report.add(
        not missing_sections,
        f"{career_id} quick_scan.md 结构完整",
        "" if not missing_sections else "缺少: " + "; ".join(missing_sections),
    )


def check_report_file(path: Path, career_id: str, report: Report) -> None:
    text = read_text(path)
    frontmatter, body = split_frontmatter(text)
    if frontmatter is None:
        return
    problems: list[str] = []
    last_checked = (frontmatter.get("last_checked") or "").strip()
    if last_checked != "未核查" and not is_iso_date(last_checked):
        problems.append(f"last_checked={last_checked}")
    report.add(not problems, f"{career_id} report.md frontmatter 日期", "; ".join(problems))
    missing_sections = [section for section in REPORT_SECTIONS if section not in body]
    report.add(
        not missing_sections,
        f"{career_id} report.md 结构完整",
        "" if not missing_sections else "缺少: " + "; ".join(missing_sections),
    )


def check_state_counts(state_text: str, actual: dict[str, int], report: Report) -> None:
    problems: list[str] = []
    for label, expected in actual.items():
        match = re.search(
            rf"^[ \t]*(?:[-*][ \t]*)?{re.escape(label)}[：:]\s*[（(]?(\d+)",
            state_text,
            re.MULTILINE,
        )
        if not match:
            problems.append(f"{label} 未找到数字")
            continue
        actual_value = int(match.group(1))
        if actual_value != expected:
            problems.append(f"{label}: 状态 {actual_value} != 实际 {expected}")
    report.add(not problems, "PROJECT_STATE.md 计数与实际文件一致", "; ".join(problems))


def validate_project(project_dir: Path, report: Report) -> None:
    state_file = project_dir / "PROJECT_STATE.md"
    profile_file = project_dir / "MY_CAREER_PROFILE.md"
    report.add(state_file.is_file(), "PROJECT_STATE.md 存在", "" if state_file.is_file() else str(state_file))
    report.add(profile_file.is_file(), "MY_CAREER_PROFILE.md 存在", "" if profile_file.is_file() else str(profile_file))

    if state_file.is_file():
        state_text = read_text(state_file)
        has_goal = "## 项目目标" in state_text
        has_next = "## 下一步任务" in state_text
        report.add(has_goal and has_next, "PROJECT_STATE.md 必需小节", "需要『项目目标』与『下一步任务』")
        progress_markers = ["候选总数", "硬筛后数量", "快扫完成数", "深研完成数", "当前决策状态"]
        missing_markers = [marker for marker in progress_markers if marker not in state_text]
        report.add(
            not missing_markers,
            "PROJECT_STATE.md 漏斗进度字段",
            "" if not missing_markers else "缺少: " + ", ".join(missing_markers),
        )

    catalog_path = project_dir / "data" / "career_catalog.csv"
    catalog_rows = read_csv(catalog_path, CATALOG_COLUMNS, report, "career_catalog.csv")
    catalog_ids = check_id_rows(
        catalog_rows, "career_id", CATALOG_ID_RE, CATALOG_REQUIRED, report, "career_catalog.csv"
    )
    check_enum(catalog_rows, "existence_status", EXISTENCE_STATUS, report, "career_catalog.csv")
    check_enum(catalog_rows, "funnel_stage", FUNNEL_STAGE, report, "career_catalog.csv")
    check_enum(catalog_rows, "fresh_graduate_fit", FRESH_GRADUATE_FIT, report, "career_catalog.csv")
    check_enum(catalog_rows, "profile_fit", PROFILE_FIT, report, "career_catalog.csv")
    check_enum(catalog_rows, "research_priority", RESEARCH_PRIORITY, report, "career_catalog.csv")
    check_enum(catalog_rows, "research_state", RESEARCH_STATE, report, "career_catalog.csv")
    check_dates(catalog_rows, ["last_checked"], report, "career_catalog.csv")

    emerging_path = project_dir / "data" / "emerging_careers.csv"
    emerging_rows = read_csv(emerging_path, EMERGING_COLUMNS, report, "emerging_careers.csv")
    check_id_rows(
        emerging_rows, "emerging_id", EMERGING_ID_RE, EMERGING_REQUIRED, report, "emerging_careers.csv"
    )
    check_enum(emerging_rows, "credibility", CREDIBILITY, report, "emerging_careers.csv")
    check_enum(emerging_rows, "prediction_marked", PREDICTION_FLAG, report, "emerging_careers.csv")
    check_enum(emerging_rows, "self_automation_risk", RISK_LEVEL, report, "emerging_careers.csv")
    check_enum(emerging_rows, "transitory_risk", RISK_LEVEL, report, "emerging_careers.csv")
    check_dates(emerging_rows, ["last_checked"], report, "emerging_careers.csv")

    inconsistent_predictions = [
        f"{row.get('emerging_id')} credibility={row.get('credibility')} prediction_marked={row.get('prediction_marked')}"
        for row in emerging_rows
        if (row.get("credibility") or "").strip() in {"C", "D"}
        and (row.get("prediction_marked") or "").strip() != "是"
    ]
    report.add(
        not inconsistent_predictions,
        "C/D 级新兴职业标注为预测性假设",
        "; ".join(inconsistent_predictions),
    )
    inconsistent_real = [
        f"{row.get('emerging_id')} credibility={row.get('credibility')} prediction_marked={row.get('prediction_marked')}"
        for row in emerging_rows
        if (row.get("credibility") or "").strip() in {"A", "B"}
        and (row.get("prediction_marked") or "").strip() != "否"
    ]
    report.add(
        not inconsistent_real,
        "A/B 级新兴职业不标为预测性假设",
        "; ".join(inconsistent_real),
    )

    stage_state_problems = []
    for row in catalog_rows:
        cid = (row.get("career_id") or "").strip() or "?"
        stage = (row.get("funnel_stage") or "").strip()
        state = (row.get("research_state") or "").strip()
        if stage in {"候选池", "硬筛"} and state != "未研究":
            stage_state_problems.append(f"{cid} {stage}/{state}")
        if stage == "排除" and state != "已排除":
            stage_state_problems.append(f"{cid} {stage}/{state}")
        if stage != "排除" and state == "已排除":
            stage_state_problems.append(f"{cid} {stage}/{state}")
        if stage == "决策" and state != "已完成":
            stage_state_problems.append(f"{cid} {stage}/{state}")
    report.add(
        not stage_state_problems,
        "funnel_stage 与 research_state 一致",
        "; ".join(stage_state_problems),
    )

    catalog_by_id = {(row.get("career_id") or "").strip(): row for row in catalog_rows}
    research_dir = project_dir / "research"
    report_dirs: list[Path] = []
    if not research_dir.is_dir():
        report.add(False, "research 目录存在", str(research_dir))
    else:
        report.add(True, "research 目录存在")
        report_dirs = sorted(path for path in research_dir.iterdir() if path.is_dir())

    actual_counts = {
        "候选总数": sum(
            1 for row in catalog_rows if (row.get("funnel_stage") or "").strip() != "排除"
        ),
        "硬筛后数量": sum(
            1
            for row in catalog_rows
            if (row.get("funnel_stage") or "").strip() in {"快扫", "深研", "决策"}
        ),
        "快扫完成数": len(list(research_dir.glob("*/quick_scan.md"))) if research_dir.is_dir() else 0,
        "深研完成数": len(list(research_dir.glob("*/report.md"))) if research_dir.is_dir() else 0,
    }
    if state_file.is_file():
        check_state_counts(read_text(state_file), actual_counts, report)

    missing_exclusion_reasons = [
        cid
        for cid, row in catalog_by_id.items()
        if (row.get("funnel_stage") or "").strip() == "排除"
        and not (row.get("stage_reason") or "").strip()
    ]
    report.add(
        not missing_exclusion_reasons,
        "排除职业都有 stage_reason",
        "; ".join(missing_exclusion_reasons),
    )

    missing_stage_files: list[str] = []
    for cid, row in catalog_by_id.items():
        stage = (row.get("funnel_stage") or "").strip()
        career_dir = research_dir / cid
        if stage in {"快扫", "深研", "决策"}:
            for file_name in ("quick_scan.md", "sources.md"):
                if not (career_dir / file_name).is_file():
                    missing_stage_files.append(f"{cid}:{stage}:{file_name}")
        if stage in {"深研", "决策"} and not (career_dir / "report.md").is_file():
            missing_stage_files.append(f"{cid}:{stage}:report.md")
    report.add(not missing_stage_files, "漏斗阶段文件完整", "; ".join(missing_stage_files))

    mismatches: list[str] = []
    for directory in report_dirs:
        career_id = directory.name
        report_path = directory / "report.md"
        quick_scan_path = directory / "quick_scan.md"
        sources_path = directory / "sources.md"
        if career_id not in catalog_by_id:
            mismatches.append(f"{career_id} 不在 career_catalog.csv")
            continue
        row = catalog_by_id[career_id]
        stage = (row.get("funnel_stage") or "").strip()
        if quick_scan_path.is_file():
            check_quick_scan_file(quick_scan_path, career_id, report)
        if sources_path.is_file():
            check_sources_file(sources_path, career_id, report)
        if not report_path.is_file():
            if stage in {"深研", "决策"}:
                mismatches.append(f"{career_id} 缺 report.md")
            elif not quick_scan_path.is_file() and stage not in {"候选池", "硬筛"}:
                mismatches.append(f"{career_id} 缺 quick_scan.md 或 report.md")
            continue
        frontmatter, _ = split_frontmatter(read_text(report_path))
        if frontmatter is None:
            mismatches.append(f"{career_id} report.md frontmatter 非法")
            continue
        checks = [
            ("id", career_id),
            ("name", (row.get("name") or "").strip()),
            ("research_state", (row.get("research_state") or "").strip()),
            ("match_score", (row.get("profile_fit") or "").strip()),
        ]
        for field, expected in checks:
            actual = (frontmatter.get(field) or "").strip()
            if actual != expected:
                mismatches.append(f"{career_id}.{field}: {actual!r} != 目录 {expected!r}")
        check_report_file(report_path, career_id, report)
    report.add(not mismatches, "report.md frontmatter 与目录一致", "; ".join(mismatches))

    for relative in [
        "decisions/comparisons.md",
        "decisions/decision_log.md",
        "decisions/decision_report.md",
        "progress/snapshots",
    ]:
        target = project_dir / relative
        report.add(target.exists(), f"{relative} 存在", "" if target.exists() else str(target))


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    parser = argparse.ArgumentParser(description="Validate career-research skill package or project data.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--skill", metavar="DIR", help="skill package directory")
    group.add_argument("--project", metavar="DIR", help="career research project directory")
    args = parser.parse_args()

    report = Report()
    if args.skill:
        skill_dir = Path(args.skill).expanduser().resolve()
        print(f"# skill: {skill_dir}\n")
        if not skill_dir.is_dir():
            print(f"[FAIL] 目录不存在 | {skill_dir}")
            return 1
        validate_skill(skill_dir, report)
    else:
        project_dir = Path(args.project).expanduser().resolve()
        print(f"# project: {project_dir}\n")
        if not project_dir.is_dir():
            print(f"[FAIL] 目录不存在 | {project_dir}")
            return 1
        validate_project(project_dir, report)

    return report.summary()


if __name__ == "__main__":
    sys.exit(main())
