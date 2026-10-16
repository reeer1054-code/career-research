#!/usr/bin/env python3
"""Focused tests for quick_validate.py."""

from __future__ import annotations

import contextlib
import csv
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import quick_validate as validator  # noqa: E402


class QuickValidateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="career-research-tests-")
        self.template = Path(__file__).resolve().parents[1] / "assets" / "project-template"
        self.project = Path(self.temp_dir.name) / "project"
        shutil.copytree(self.template, self.project)
        self.make_funnel_fixture()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def sources_text(self) -> str:
        return "\n".join(
            [
                "# 来源索引",
                "",
                "## S001",
                "- 来源类型：官方",
                "- 标题：测试来源",
                "- 发布机构：测试机构",
                "- 链接：https://example.com/source",
                "- 发布日期：2026-01-01",
                "- 访问日期：2026-10-16",
                "- 覆盖地区：中国",
                "- 统计口径：测试",
                "- 来源等级：A",
                "- 样本量：不适用",
                "- 支持的结论：测试",
                "- 可信度与限制：仅测试",
                "- 关键摘录：测试短摘录",
                "- 核验状态：已核验",
                "- 替代链接：无",
            ]
        )

    def write_state_counts(self) -> None:
        path = self.project / "PROJECT_STATE.md"
        text = path.read_text(encoding="utf-8")
        replacements = {
            "- 候选总数：（0）": "- 候选总数：100",
            "- 硬筛后数量：（0）": "- 硬筛后数量：30",
            "- 快扫完成数：（0）": "- 快扫完成数：30",
            "- 深研完成数：（0）": "- 深研完成数：12",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")

    def make_funnel_fixture(self) -> None:
        catalog_path = self.project / "data" / "career_catalog.csv"
        fieldnames = list(validator.CATALOG_COLUMNS)
        rows: list[dict[str, str]] = []
        for index in range(1, 101):
            career_id = f"C{index:03d}"
            if index <= 12:
                stage, state = "深研", "已完成"
            elif index <= 30:
                stage, state = "快扫", "研究中"
            elif index <= 60:
                stage, state = "硬筛", "未研究"
            else:
                stage, state = "候选池", "未研究"
            row = {field: "" for field in fieldnames}
            row.update(
                {
                    "career_id": career_id,
                    "name": f"测试职业{index}",
                    "domain": "测试领域",
                    "existence_status": "真实招聘岗位",
                    "funnel_stage": stage,
                    "stage_reason": "曾因地区条件排除；用户拉回，保留原因" if index == 60 else "",
                    "core_work": "测试核心工作",
                    "fresh_graduate_fit": "待验证",
                    "profile_fit": "待验证",
                    "research_priority": "高",
                    "research_state": state,
                    "last_checked": "2026-10-16",
                    "next_task": "继续验证",
                }
            )
            rows.append(row)
        with catalog_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        for index in range(1, 31):
            career_id = f"C{index:03d}"
            career_dir = self.project / "research" / career_id
            career_dir.mkdir(parents=True, exist_ok=True)
            quick_scan_body = "\n\n".join(
                f"{section}\n\n测试内容。" for section in validator.QUICK_SCAN_SECTIONS
            )
            (career_dir / "quick_scan.md").write_text(
                "\n".join(
                    [
                        "---",
                        f"id: {career_id}",
                        f"name: 测试职业{index}",
                        "funnel_stage: 快扫",
                        "last_checked: 2026-10-16",
                        "---",
                        "",
                        f"# {career_id} 测试职业{index}｜快扫",
                        "",
                        quick_scan_body,
                    ]
                ),
                encoding="utf-8",
            )
            (career_dir / "sources.md").write_text(self.sources_text(), encoding="utf-8")

        for index in range(1, 13):
            career_id = f"C{index:03d}"
            career_dir = self.project / "research" / career_id
            report_body = "\n\n".join(
                f"{section}\n\n测试内容。" for section in validator.REPORT_SECTIONS
            )
            (career_dir / "report.md").write_text(
                "\n".join(
                    [
                        "---",
                        f"id: {career_id}",
                        f"name: 测试职业{index}",
                        "research_state: 已完成",
                        "match_score: 待验证",
                        "last_checked: 2026-10-16",
                        "---",
                        "",
                        f"# {career_id} 测试职业{index}",
                        "",
                        report_body,
                    ]
                ),
                encoding="utf-8",
            )

        self.write_state_counts()

    def run_validator(self) -> tuple[int, str]:
        output = io.StringIO()
        report = validator.Report()
        with contextlib.redirect_stdout(output):
            validator.validate_project(self.project, report)
            code = report.summary()
        return code, output.getvalue()

    def read_catalog(self) -> list[dict[str, str]]:
        with (self.project / "data" / "career_catalog.csv").open(
            "r", encoding="utf-8-sig", newline=""
        ) as handle:
            return list(csv.DictReader(handle))

    def write_catalog(self, rows: list[dict[str, str]]) -> None:
        with (self.project / "data" / "career_catalog.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=list(validator.CATALOG_COLUMNS))
            writer.writeheader()
            writer.writerows(rows)

    def write_emerging(self, row: dict[str, str]) -> None:
        with (self.project / "data" / "emerging_careers.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=list(validator.EMERGING_COLUMNS))
            writer.writeheader()
            writer.writerow(row)

    def test_valid_funnel_passes(self) -> None:
        rows = self.read_catalog()
        stages = [row["funnel_stage"] for row in rows]
        self.assertEqual(len(rows), 100)
        self.assertEqual(stages.count("深研"), 12)
        self.assertEqual(stages.count("快扫"), 18)
        self.assertEqual(len(list((self.project / "research").glob("*/quick_scan.md"))), 30)
        self.assertEqual(len(list((self.project / "research").glob("*/report.md"))), 12)
        code, output = self.run_validator()
        self.assertEqual(code, 0, output)
        self.assertIn("漏斗阶段文件完整", output)

    def test_skill_package_passes(self) -> None:
        skill_dir = Path(__file__).resolve().parents[1]
        output = io.StringIO()
        report = validator.Report()
        with contextlib.redirect_stdout(output):
            validator.validate_skill(skill_dir, report)
            code = report.summary()
        self.assertEqual(code, 0, output.getvalue())
        self.assertIn("references 目录非空", output.getvalue())

    def test_restored_candidate_keeps_reason(self) -> None:
        row = next(row for row in self.read_catalog() if row["career_id"] == "C060")
        self.assertEqual(row["funnel_stage"], "硬筛")
        self.assertIn("用户拉回", row["stage_reason"])

    def test_invalid_stage_fails(self) -> None:
        rows = self.read_catalog()
        next(row for row in rows if row["career_id"] == "C002")["funnel_stage"] = "异常阶段"
        self.write_catalog(rows)
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("funnel_stage 取值合法", output)

    def test_missing_quick_scan_fails(self) -> None:
        rows = self.read_catalog()
        next(row for row in rows if row["career_id"] == "C013")["funnel_stage"] = "深研"
        self.write_catalog(rows)
        (self.project / "research" / "C013" / "quick_scan.md").unlink()
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("C013:深研:quick_scan.md", output)

    def test_missing_report_fails(self) -> None:
        (self.project / "research" / "C012" / "report.md").unlink()
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("C012:深研:report.md", output)

    def test_source_without_link_fails(self) -> None:
        source_path = self.project / "research" / "C001" / "sources.md"
        source = source_path.read_text(encoding="utf-8")
        source_path.write_text(
            source.replace("- 链接：https://example.com/source", "- 链接：无"),
            encoding="utf-8",
        )
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("缺 http 链接", output)

    def test_excluded_without_reason_fails(self) -> None:
        rows = self.read_catalog()
        row = next(row for row in rows if row["career_id"] == "C100")
        row["funnel_stage"] = "排除"
        row["stage_reason"] = ""
        self.write_catalog(rows)
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("排除职业都有 stage_reason", output)

    def test_ab_grade_marked_prediction_fails(self) -> None:
        row = {field: "" for field in validator.EMERGING_COLUMNS}
        row.update(
            {
                "emerging_id": "E001",
                "name": "测试假设",
                "definition": "测试定义",
                "credibility": "A",
                "prediction_marked": "是",
            }
        )
        self.write_emerging(row)
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("A/B 级新兴职业不标为预测性假设", output)

    def test_state_count_mismatch_fails(self) -> None:
        state_path = self.project / "PROJECT_STATE.md"
        state = state_path.read_text(encoding="utf-8")
        state_path.write_text(state.replace("- 候选总数：100", "- 候选总数：99"), encoding="utf-8")
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("计数与实际文件一致", output)

    def test_candidate_with_research_done_fails(self) -> None:
        rows = self.read_catalog()
        row = next(row for row in rows if row["career_id"] == "C061")
        row["funnel_stage"] = "候选池"
        row["research_state"] = "已完成"
        self.write_catalog(rows)
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("funnel_stage 与 research_state 一致", output)

    def test_report_without_sections_fails(self) -> None:
        report_path = self.project / "research" / "C001" / "report.md"
        report_path.write_text(
            "\n".join(
                [
                    "---",
                    "id: C001",
                    "name: 测试职业1",
                    "research_state: 已完成",
                    "match_score: 待验证",
                    "last_checked: 2026-10-16",
                    "---",
                    "",
                    "# 空报告",
                ]
            ),
            encoding="utf-8",
        )
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("report.md 结构完整", output)

    def test_quick_scan_without_sources_fails(self) -> None:
        (self.project / "research" / "C013" / "sources.md").unlink()
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("C013:快扫:sources.md", output)

    def test_source_grade_invalid_fails(self) -> None:
        source_path = self.project / "research" / "C001" / "sources.md"
        source = source_path.read_text(encoding="utf-8")
        source_path.write_text(source.replace("- 来源等级：A", "- 来源等级：X"), encoding="utf-8")
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("来源等级缺失或取值不符", output)

    def test_duplicate_career_id_fails(self) -> None:
        rows = self.read_catalog()
        next(row for row in rows if row["career_id"] == "C002")["career_id"] = "C001"
        self.write_catalog(rows)
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("career_catalog.csv ID 无重复", output)


if __name__ == "__main__":
    unittest.main()
