![Skill](https://img.shields.io/badge/Skill-2f81f7?style=flat-square)

# career-research

<a href="./README.en.md">English</a> | <span>中文</span>

`career-research` 是一个帮助大学生和应届生了解职业、寻找就业方向的 Skill，主要面向中国大陆的就业市场，也可以用来研究海外的职业机会。

它会先通过问卷了解你的兴趣、偏好和实际情况，帮你筛选出值得考虑的职业，再逐步了解这些工作的日常内容、薪资、技能要求和就业前景，最后结合你的个人情况，给出一些实际可行的建议。

它不会因为你学了某个专业，就直接认定你适合做什么工作。对于查不到或缺乏可靠依据的数据，也不会随便编一个数字来凑报告。

## 工作方式

研究按五个阶段推进：

1. 建立个人画像，写清现实中的硬性条件。
2. 先收集一批现实存在的职业。
3. 按用户明确提出的条件做筛选。
4. 对保留的职业做一页式快扫。
5. 深研最有希望的方向，比较后形成决策。

默认预算是 100 个候选、硬筛后保留 20 至 30 个、其中 10 至 15 个进入深研。数字用于控制工作量，不会压过用户的实际需求。

所有来源按 A 至 D 分级。重要结论要记录来源、日期、地区、样本量和局限。无法联网核实时，skill 会明确写下证据缺口，不会假装已经查过。

## 包含内容

```text
career-research/
├── SKILL.md                     核心指令与研究流程
├── agents/openai.yaml           Codex 展示信息
├── references/                  研究规范与模板
├── scripts/quick_validate.py    skill 与项目校验脚本
├── tests/                       校验脚本测试
└── assets/project-template/     空白职业研究项目
```

skill 本身只保存研究方法。个人画像、职业记录和进度放在用户项目里。共享来源层只保存检索入口与查询模板，不放个人资料。

## 安装到 Codex

把仓库链接到 Codex 的 skills 目录：

```powershell
New-Item -ItemType Junction `
  -Path "$HOME\.codex\skills\career-research" `
  -Target "<仓库所在路径>"
```

安装后 Codex 会自动发现这个 skill。也可以输入 `$career-research` 强制调用。

## 开始一个项目

先把 `assets/project-template/` 复制成项目目录。然后在 `PROJECT_STATE.md` 里填写开始日期和当前目标。`MY_CAREER_PROFILE.md` 只记录用户亲口说过的信息，不要把推测写成事实。

继续已有项目时，先读 `PROJECT_STATE.md`。只加载下一步真正需要的参考资料。

## 校验

在仓库根目录运行：

```bash
python scripts/quick_validate.py --skill .
python -m unittest discover -s tests -v
```

这些脚本只使用 Python 标准库。如果 `python` 不可用，可以换一个可用的解释器，例如：

```bash
uv run --python 3.13 python scripts/quick_validate.py --skill .
```

## 不适用范围

这个 skill 不处理企业招聘流程、留学申请或普通的简历润色。
