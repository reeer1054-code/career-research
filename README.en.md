![Skill](https://img.shields.io/badge/Skill-2f81f7?style=flat-square)

# career-research

<span>English</span> | <a href="./README.md">中文</a>

`career-research` is a skill for evidence-based career research. It is written
for students and recent graduates in mainland China and can also cover overseas
markets when a project needs them.

The skill helps you move from a broad list of possible occupations to a smaller
set worth investigating, then to detailed reports and a practical decision. It
does not assume that one occupation fits everyone, and it does not fill gaps
with invented salary, hiring, or AI-replacement figures.

## How it works

The process runs through five stages:

1. Build a profile and record hard constraints.
2. Collect a lightweight pool of real occupations.
3. Filter the pool against the user's stated conditions.
4. Quick-scan the remaining occupations.
5. Deep-research the strongest options and compare them before making a
   decision.

The default budget is 100 candidates, 20 to 30 after the hard filter, and 10 to
15 for deep research. These numbers are a planning guide, not a rule that should
override the user's needs.

Evidence is graded A to D. Important claims must show their source, date, region,
sample size, and limits. If live search is unavailable, the skill records the
gap instead of pretending the research is complete.

## What is included

```text
career-research/
├── SKILL.md                     Main instructions and workflow
├── agents/openai.yaml           Codex display metadata
├── references/                  Detailed research rules and templates
├── scripts/quick_validate.py    Skill and project validator
├── tests/                       Validator tests
└── assets/project-template/     Empty career-project skeleton
```

The skill keeps its method separate from the user's project. Personal profiles
and career records stay in the project directory. The shared source catalog only
contains search entry points and query templates.

## Install in Codex

Link this repository into the Codex skills directory:

```powershell
New-Item -ItemType Junction `
  -Path "$HOME\.codex\skills\career-research" `
  -Target "<path to this repository>"
```

Codex can then discover the skill automatically. You can also invoke it
explicitly with `$career-research`.

## Start a project

Copy `assets/project-template/` to a new project folder. Fill in
`PROJECT_STATE.md` with the start date and current goal, then record only
information the user has actually provided in `MY_CAREER_PROFILE.md`.

When continuing an existing project, read `PROJECT_STATE.md` first. Load only the
references needed for the next task.

## Validate

Run the validator from the repository root:

```bash
python scripts/quick_validate.py --skill .
python -m unittest discover -s tests -v
```

The scripts use only the Python standard library. If `python` is unavailable,
use a working interpreter, for example:

```bash
uv run --python 3.13 python scripts/quick_validate.py --skill .
```

## Scope

This skill is not a recruiting workflow, an admissions or study-abroad service,
or a general resume-rewriting tool.
