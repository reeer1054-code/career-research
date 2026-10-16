# 职业数据结构

机器可读的数据分四处保存：目录表、快扫、职业报告 frontmatter、来源索引。字段定义与允许值必须一致，修改前先改本文件。

## 一、编号规则

- 现实职业：`C001` 起，三位数字，格式 `^C\d{3}$`。
- 新兴职业假设：`E001` 起，格式 `^E\d{3}$`，只出现在 `data/emerging_careers.csv`。
- 编号一经分配不再改变。删除职业时编号作废，不回收、不复用。
- 目录中同名或高度重叠的岗位不得重复计数。名称不同但工作内容相同的岗位合为一条，并在「常见招聘名称」中列出别名。
- 一个目录记录代表一个可独立招聘的岗位族群。入口、学历与资格要求、工作条件或收入结构实质不同时，拆成新记录；仅细分方向不同则在报告第 1、2、9 节分别说明。

## 二、目录表 data/career_catalog.csv

一行一个职业，列名固定为下列顺序。除标「必填」外，未研究阶段允许留空。100 个候选先进入「候选池」，不是每个候选都需要完整报告。

| 列名 | 中文含义 | 类型 | 允许值或格式 | 必填 |
| --- | --- | --- | --- | --- |
| career_id | 职业 ID | 文本 | `C001` 格式 | 是 |
| name | 职业名称 | 文本 | 稳定中文名称 | 是 |
| common_titles | 常见招聘名称 | 文本 | 分号分隔 | 否 |
| domain | 所属领域 | 文本 | 推荐领域见下，可新增 | 是 |
| existence_status | 现实存在状态 | 枚举 | 成熟职业、真实招聘岗位、新兴岗位 | 是 |
| funnel_stage | 漏斗阶段 | 枚举 | 候选池、硬筛、快扫、深研、决策、排除 | 是 |
| stage_reason | 阶段理由 | 文本 | 排除时必填；其他阶段可写保留或推进理由 | 否 |
| core_work | 核心工作内容 | 文本 | 一句话到一段 | 是 |
| typical_employers | 典型雇主 | 文本 | 分号分隔 | 否 |
| typical_regions | 常见工作地区 | 文本 | 分号分隔 | 否 |
| entry_roles | 典型入门岗位 | 文本 | 分号分隔 | 否 |
| education_and_qualification | 学历与资格要求 | 文本 | 硬性要求与常见要求分开写 | 否 |
| skills_and_qualifications | 技能与证书要求 | 文本 | 分号分隔 | 否 |
| fresh_graduate_fit | 应届生适配情况 | 枚举 | 适合、有条件适合、通常不适合、待验证 | 否 |
| profile_fit | 个人匹配度 | 枚举 | 1、2、3、4、5、待验证 | 否 |
| research_priority | 研究优先级 | 枚举 | 高、中、低、待定 | 是 |
| research_state | 研究状态 | 枚举 | 未研究、研究中、已完成、待补充证据、已排除 | 是 |
| last_checked | 最后核查日期 | 日期 | `YYYY-MM-DD`，未核查留空 | 否 |
| evidence_gap | 证据缺口 | 文本 | 缺少哪类证据、缺哪个年份或地区 | 否 |
| next_task | 下一步研究任务 | 文本 | 一个具体动作 | 否 |

推荐领域：信息技术与软件、工程与制造、医疗健康、教育、金融与财会、法律与公共安全、公共服务与公共管理、商业与销售、市场与内容、设计与创意、交通与物流、建筑与房地产、能源与环保、农业与食品、旅游与酒店、生活服务与个人服务、科研与技术、体育与艺术、社区与社会服务、其他。可新增，但同一职业只填一个主领域。

漏斗阶段规则：

- `候选池`：只登记轻量候选。
- `硬筛`：正在按硬约束筛选。
- `快扫`：已决定进入一页式调查，必须有 `quick_scan.md` 与至少一个来源条目的 `sources.md`。
- `深研`：已完成快扫并决定深研，必须有 `quick_scan.md`、`report.md` 与 `sources.md`。
- `决策`：参与最终比较，必须有 `quick_scan.md`、`report.md` 与 `sources.md`。
- `排除`：必须有 `stage_reason`；历史文件保留，用户可以拉回。

`research_state` 表示研究完成度；`funnel_stage` 表示在漏斗中的位置。两者不得互相替代。

## 三、新兴职业表 data/emerging_careers.csv

一行一个假设，列名固定。

| 列名 | 中文含义 | 类型 | 允许值或格式 | 必填 |
| --- | --- | --- | --- | --- |
| emerging_id | 假设 ID | 文本 | `E001` 格式 | 是 |
| name | 假设名称 | 文本 | 稳定名称 | 是 |
| definition | 职业定义 | 文本 | 工作内容与出现原因 | 是 |
| related_real_evidence | 已有相关证据 | 文本 | 相近岗位、业务或产品 | 否 |
| demand_and_payer | 真实需求与付费方 | 文本 | 谁付费、解决什么问题 | 否 |
| potential_employers | 潜在雇主 | 文本 | 分号分隔 | 否 |
| entry_skills_and_cost | 入行技能与成本 | 文本 | 分号分隔 | 否 |
| income_sources | 可能收入来源 | 文本 | 分号分隔 | 否 |
| self_automation_risk | AI 自身替代风险 | 枚举 | 低、中、高、未知 | 否 |
| transitory_risk | 过渡岗位风险 | 枚举 | 低、中、高、未知 | 否 |
| credibility | 可信度分级 | 枚举 | A、B、C、D，定义见下 | 是 |
| prediction_marked | 是否标注为预测性假设 | 枚举 | 是、否 | 是 |
| last_checked | 最后核查日期 | 日期 | `YYYY-MM-DD` | 否 |
| next_task | 下一步研究任务 | 文本 | 一个具体动作 | 否 |

可信度定义：

| 等级 | 含义 | 最低证据 |
| --- | --- | --- |
| A | 已核验的现实职业需求 | 多个独立来源显示稳定付费需求，且有持续招聘岗位或稳定交易记录 |
| B | 初步现实需求 | 有真实招聘样本或付费案例，但样本少、地区有限或岗位名称不稳定 |
| C | 预测性假设 | 只有相邻岗位、单一案例或行业推断，尚无可核验的稳定招聘与付费证据 |
| D | 概念性预测 | 只有技术可能性或趋势推断，无现实需求证据 |

一致性规则：可信度为 C 或 D 时，`prediction_marked` 必须是「是」。A 或 B 时为「否」。

预测性职业禁止写入 `career_catalog.csv`。

## 四、职业报告 research/C###/report.md

只有进入深研或决策阶段的职业才需要 `report.md`。快扫阶段使用
[quick-scan-template.md](quick-scan-template.md) 生成 `quick_scan.md`，不提前生成深研报告。

frontmatter 只放五个字段，避免与目录表重复维护。

```yaml
---
id: C001
name: 职业名称
research_state: 研究中
match_score: 待验证
last_checked: 2026-10-16
---
```

约束：

- `id` 必须与所在目录名一致，且必须存在于目录表。
- `name`、`research_state`、`match_score` 必须与目录表对应行一致。
- `match_score` 的取值与 `profile_fit` 相同：1 到 5 或「待验证」。
- `last_checked` 未核查时写「未核查」，已核查写 `YYYY-MM-DD`。
- 深研报告正文必须包含 [career-report-template.md](career-report-template.md) 的 13 个编号小节。
- 正文结构见 [career-report-template.md](career-report-template.md)。

## 五、来源索引 research/C###/sources.md

每个来源一个二级标题块，块内字段固定。

```markdown
## S001
- 来源类型：
- 标题：
- 发布机构：
- 链接：
- 发布日期：
- 访问日期：
- 覆盖地区：
- 统计口径：
- 来源等级：
- 样本量：
- 支持的结论：
- 可信度与限制：
- 关键摘录：
- 核验状态：
- 替代链接：
```

约束：

- `链接` 必须是以 `http` 开头的原始 URL，不得填写搜索页或平台首页。
- `访问日期` 必须为 `YYYY-MM-DD`。
- `发布日期` 未知时写「未知」，不得留空或编造。
- `来源等级` 只能是 `A`、`B`、`C` 或 `D`，定义见 [evidence-and-source-rules.md](evidence-and-source-rules.md)。
- `样本量` 写样本数量与范围；没有样本概念时写「不适用」，不得留空。
- 每条来源必须写清它支持哪个具体结论。
- `关键摘录` 只保留判断所需的最小片段；无法保存时写「无可用短摘录」。
- `核验状态` 只能是 `已核验`、`部分核验`、`待核验` 或 `已失效`。
- `替代链接` 没有时写「无」。
- GitHub 仓库完成 README、数据、许可和更新时间核验前，只能写为线索。

## 六、核心 24 个字段落在何处

| 字段 | 存放位置 |
| --- | --- |
| 1 职业 ID | 目录表 career_id，报告 frontmatter id |
| 2 职业名称 | 目录表 name，报告 frontmatter name |
| 3 常见招聘名称 | 目录表 common_titles |
| 4 所属领域 | 目录表 domain |
| 5 现实存在状态 | 目录表 existence_status |
| 6 官方职业分类信息 | 报告正文第 1 节 |
| 7 核心工作内容 | 目录表 core_work，报告正文第 2 节 |
| 8 典型雇主 | 目录表 typical_employers |
| 9 常见工作地区 | 目录表 typical_regions |
| 10 典型入门岗位 | 目录表 entry_roles |
| 11 应届生适配情况 | 目录表 fresh_graduate_fit |
| 12 学历与专业要求 | 目录表 education_and_qualification，报告正文第 4 节 |
| 13 技能与资格要求 | 目录表 skills_and_qualifications，报告正文第 4 节 |
| 14 薪资样本及统计口径 | 报告正文第 5 节，来源写进 sources.md |
| 15 工作环境 | 报告正文第 7 节 |
| 16 职业发展路径 | 报告正文第 8 节 |
| 17 AI 影响卡 | 报告正文第 9 节 |
| 18 新人就业风险 | 报告正文第 9 节 |
| 19 个人匹配度 | 目录表 profile_fit，报告 frontmatter match_score |
| 20 证据列表 | sources.md |
| 21 证据缺口 | 目录表 evidence_gap |
| 22 研究状态 | 目录表 research_state，报告 frontmatter research_state |
| 23 最后核查日期 | 目录表 last_checked，报告 frontmatter last_checked |
| 24 下一步研究任务 | 目录表 next_task |

`funnel_stage` 与 `stage_reason` 是漏斗控制字段，不计入核心 24 字段；它们决定当前需要哪些阶段文件。

项目级最终决策写入 `decisions/decision_report.md`，不重复写进单个职业报告。
