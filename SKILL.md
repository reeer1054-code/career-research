---
name: career-research
description: >
  Evidence-based career research for mainland China students and recent graduates, with
  overseas coverage only when needed. Uses a funnel from a broad occupation pool to quick scans
  and deep research, investigating real work, hiring requirements, entry barriers, pay, working
  conditions and AI impact before comparing options and producing an action plan. Also handles
  resuming and updating an existing career-research project. Not for company recruiting
  workflows, school admissions or study-abroad applications, or plain resume rewriting.
  用于中国大陆大学生与应届生的证据型职业研究：以“候选池、硬筛、快扫、深研、决策”漏斗调查真实
  工作内容、招聘与薪资证据、入行门槛、工作环境与 AI 影响，结合个人画像比较职业并输出行动计划；
  也用于恢复和更新已有的职业研究项目。不用于企业招聘流程、留学申请或单纯的简历润色。
---

# 职业研究与 AI 时代职业决策

面向中国大陆就业市场的职业研究流程包。研究现实职业与新兴职业假设，结合用户个人画像，逐步缩小范围到主攻方向、备选方向、长期转型方向。

## 红线

- 不预设方向。专业不等于职业，不默认白领，不默认任何行业更适合。用户未表达的偏好不得写成已确认事实。
- 不编数据。没有证据就写「尚无足够证据判断」，并列入待办。
- 结论必须分类：【事实】【推断】【预测】【建议】【未知】。
- 职业名称不是分析单位。按具体岗位、企业类型、行业、地区、初级与资深阶段、受雇与自主经营细分。一个目录记录代表一个可独立招聘的岗位族群；入口、门槛或工作条件实质不同时拆成新记录，细分方向在报告中单列。
- 个人档案可能含收入、家庭责任、健康与安全边界等敏感信息。只记录研究必需内容；写入前确认项目位置；个人数据不得放入来源表或共享来源层；用户可要求导出或删除。
- AI 影响按具体任务分析。禁止只给一个没有依据的替代概率。
- 预测性职业不得进入现实职业目录。
- 进度和状态更新只能基于实际完成的工作。

## 三层职责

- skill：保存稳定方法、漏斗门槛、证据规则、来源表与模板。
- 用户项目：保存职业目录、快扫、深研报告、来源索引、决策与进度。
- 共享来源层：只保存来源入口、查询模板、可信度与访问限制，不保存全量职业内容或个人数据。

不建中央职业数据库，不预装固定的 100 个职业。每个用户按自己的画像和硬约束建立候选池。

## 五道门

默认规模是 100 个候选、硬筛后保留 20 至 30 个、其中 20 至 30 个进入快扫、10 至 15 个进入深研。数量是预算，不是硬门槛；用户可以调整数量、增加候选、拉回已排除职业或指定深研，调整后要在 `PROJECT_STATE.md` 写明原因。

1. 画像与硬约束：明确现实约束、偏好、能力、时间与预算，见 [references/interview-and-profile.md](references/interview-and-profile.md)。
2. 候选池：轻量登记 100 个现实职业，只确认名称、领域、核心工作与存在证据，不写完整报告。
3. 硬筛：按用户明确条件留 20 至 30 个。每个排除项必须写理由，不得静默删除。
4. 快扫：对硬筛保留的 20 至 30 个职业做一页式调查，比较工作内容、入行、收入样本、工时、市场需求与 AI 影响摘要。
5. 深研与决策：只对 10 至 15 个重点职业生成完整报告，再比较、敏感性分析并形成行动计划。

AI 职业影响分析、职业比较、体验任务和项目恢复属于支持流程。AI 分析见
[references/ai-impact-framework.md](references/ai-impact-framework.md)，比较见
[references/decision-framework.md](references/decision-framework.md)。

## 按需加载

1. 先读项目的 `PROJECT_STATE.md` 和当前任务。
2. 只在需要个人匹配时读个人档案。
3. 只读当前职业的 `quick_scan.md`、`report.md` 或当前比较对象。
4. 只在需要核查具体结论时读该职业的 `sources.md`。
5. 只有需要扩大搜索时才读 [references/source-catalog.md](references/source-catalog.md)。
6. 只有任务涉及 AI 分析时，才读 [references/ai-impact-framework.md](references/ai-impact-framework.md)。
7. 只有任务涉及职业目录或阶段文件时，才读 [references/career-schema.md](references/career-schema.md)。
8. 不默认读取全部候选记录、快扫、职业报告和全部原始证据。
9. 只有任务涉及劳动合同、求职风险、学历与资格限制或升学替代路线时，才读
   [references/china-labor-market-risks.md](references/china-labor-market-risks.md)。

## 文件索引

- [references/interview-and-profile.md](references/interview-and-profile.md)：个人画像访谈规则、信息标记与结束条件。
- [references/research-workflow.md](references/research-workflow.md)：五道门、快扫、深研、复盘与支持流程。
- [references/source-catalog.md](references/source-catalog.md)：来源入口、中英文查询模板、可信度与访问限制。
- [references/quick-scan-template.md](references/quick-scan-template.md)：一页式快速筛查模板。
- [references/career-report-template.md](references/career-report-template.md)：职业报告 13 节模板与标准记录卡。
- [references/ai-impact-framework.md](references/ai-impact-framework.md)：四类 AI 影响、影响卡九项指标、五到十年三种情景、新人岗位风险。
- [references/evidence-and-source-rules.md](references/evidence-and-source-rules.md)：结论分类、来源等级、证据门槛、来源字段、短摘录、平台样本局限与无联网处理。
- [references/career-schema.md](references/career-schema.md)：职业记录字段、类型、允许值、必填项、编号规则。
- [references/progress-management.md](references/progress-management.md)：项目状态、漏斗计数、进度快照、恢复与上下文分层。
- [references/decision-framework.md](references/decision-framework.md)：硬性约束筛选、综合评价、敏感性分析、最终决策输出。
- [references/china-labor-market-risks.md](references/china-labor-market-risks.md)：中国大陆劳动权益、求职风险、歧视与升学替代路线检查表。
- `scripts/quick_validate.py`：校验 skill 包结构与项目数据文件。
- `assets/project-template/`：空白项目骨架，用于新建职业研究项目。

## 启动一次研究任务

1. 定位项目目录：查找 `PROJECT_STATE.md`。项目不存在时，把 `assets/project-template/` 复制到用户指定位置，再改名与填日期。
   写入前确认项目位置；个人档案只记研究必需信息，并说明敏感数据的保存范围。
2. 读 `PROJECT_STATE.md`，确认当前阶段、已完成职业和下一步任务。
3. 按下一步只加载需要的 reference，只做该任务。
4. 完成后写回对应职业记录，并更新 `PROJECT_STATE.md` 与进度快照。

## 恢复项目

读 `PROJECT_STATE.md` 和当前任务涉及的记录。缺少文件就明确说明缺什么，不要假装记得没有保存过的内容。发现个人画像与最新明确回答冲突时，以最新回答为准，并在个人档案的「已修正」区记录修正原因。

## 项目布局

```text
<project>/
├── PROJECT_STATE.md
├── MY_CAREER_PROFILE.md
├── data/
│   ├── career_catalog.csv
│   └── emerging_careers.csv
├── research/C001/
│   ├── quick_scan.md
│   ├── report.md
│   └── sources.md
├── decisions/
│   ├── comparisons.md
│   ├── decision_log.md
│   └── decision_report.md
└── progress/
    └── snapshots/
```

## 校验

```bash
python scripts/quick_validate.py --skill .
python scripts/quick_validate.py --project <项目目录>
python -m unittest discover -s tests -v
```

若 PATH 上的 `python` 不可用，改用可用的解释器执行，例如 `uv run --python 3.13 python scripts/quick_validate.py --project <项目目录>`。
