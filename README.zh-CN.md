# career-research

一个用于职业研究、AI 时代劳动力市场分析与个人职业决策的 Codex skill，主要面向中国大陆大学生与应届生，必要时覆盖海外。

本包只包含研究规则，不含任何个人数据。个人画像单独放在项目目录中，更新研究流程不必重写个人资料，更新个人资料也不必改动研究流程。

结构是三层：skill 管方法，用户项目存职业记录与进度，共享来源表提供检索入口和查询模板。不建中央职业数据库，也不预装固定的 100 个职业。

## 能力范围

- 画像与硬约束：结构化访谈，每轮最多 5 问，最多 5 轮。
- 候选池：轻量登记 100 个现实职业。
- 硬筛：按明确条件留 20 至 30 个；排除必须写理由。
- 快扫：对硬筛保留的 20 至 30 个候选各做一页式调查，再选出 10 至 15 个深研。
- 深研与决策：对重点职业使用 13 节报告模板，再比较并形成主攻、备选、长期路线和行动计划。

现实职业目录之外，另建新兴职业假设观察表，用 A 到 D 分级。预测性职业不得混入现实职业目录。

## 目录结构

```text
career-research/
├── SKILL.md                     核心指令、红线、流程索引
├── agents/openai.yaml           前端展示信息与默认提示词
├── references/                  详细规范，按需加载
│   ├── interview-and-profile.md
│   ├── research-workflow.md
│   ├── source-catalog.md
│   ├── quick-scan-template.md
│   ├── career-report-template.md
│   ├── ai-impact-framework.md
│   ├── evidence-and-source-rules.md
│   ├── career-schema.md
│   ├── progress-management.md
│   └── decision-framework.md
├── scripts/quick_validate.py    无第三方依赖的校验脚本
├── tests/test_quick_validate.py 漏斗与失败路径测试
└── assets/project-template/     空白项目骨架
```

## 安装

把本目录链接或复制到 Codex 技能目录：

```powershell
New-Item -ItemType Junction -Path "$HOME\.codex\skills\career-research" -Target "<本目录路径>"
```

安装后 Codex 可自动触发；需要强制触发时用 `$career-research`。

## 新建项目

1. 把 `assets/project-template/` 复制为项目目录。
2. 在 `PROJECT_STATE.md` 填启动日期与目标。
3. 在 `MY_CAREER_PROFILE.md` 只写用户实际说过的信息，分入已确认、初步判断、尚待验证、已修正四个区。

项目目录结构：

```text
<project>/
├── PROJECT_STATE.md
├── MY_CAREER_PROFILE.md
├── data/career_catalog.csv
├── data/emerging_careers.csv
├── research/C###/{quick_scan.md,report.md,sources.md}
├── decisions/{comparisons.md,decision_log.md,decision_report.md}
└── progress/snapshots/
```

## 使用

- 继续项目：先读 `PROJECT_STATE.md`，再只加载当前任务需要的 reference。
- 新增候选：先向 `data/career_catalog.csv` 追加轻量记录；进入快扫后再建 `quick_scan.md`。
- 深研职业：生成 `research/C###/report.md` 与 `sources.md`。
- 扩大搜索：读 `references/source-catalog.md`，按来源等级和访问限制核验。
- 分析 AI 影响：读 `references/ai-impact-framework.md`，填九项影响卡。
- 比较与决策：读 `references/decision-framework.md`。
- 核查劳动权益、求职风险、歧视与升学替代路线：读 `references/china-labor-market-risks.md`。

## 校验

```bash
python scripts/quick_validate.py --skill .
python scripts/quick_validate.py --project <项目目录>
python -m unittest discover -s tests -v
```

脚本和测试只用 Python 标准库，每项检查打印一行 PASS 或 FAIL，任一项失败时退出码为 1。若 PATH 上的 `python` 不可用，改用可用解释器，例如 `uv run --python 3.13 python scripts/quick_validate.py --project <项目目录>`。

## 数据文件

`data/career_catalog.csv` 一行一个现实职业，编号形如 `C001`，并用 `funnel_stage` 记录候选池、硬筛、快扫、深研、决策或排除。`data/emerging_careers.csv` 存放形如 `E001` 的假设，带 A 到 D 可信度。字段名、允许值与必填列见 `references/career-schema.md`。

## 证据规则要点

- 每条重要结论标注为事实、推断、预测、建议或未知。
- 每条来源标 A 至 D 等级，并记录样本量。
- 薪资、招聘需求、入行门槛与 AI 替代等高风险结论，至少两个独立 A 或 B 级来源，或一个 A 级来源加可复核样本。
- 不编造招聘数量、薪资、工作时间或 AI 替代数据。
- 每条来源记录标题、机构、原始 URL、发布日期、访问日期、地区与统计口径。
- 项目内只保存来源索引与必要短摘录，不保存整站或全量数据库。
- 无联网检索时明确写出证据缺口，不伪装成已经检索。
- 招聘、薪资与趋势数据超过 18 个月未更新时标记「时效受限」。

## 不适用范围

企业招聘流程、留学申请、单纯的简历润色。
