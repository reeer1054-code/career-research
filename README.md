# career-research

A Codex skill for evidence-based career research, AI labor-market analysis, and personal career decisions, focused on mainland China students and recent graduates and, when needed, overseas markets.

This package contains research rules only. Personal data lives in a separate project directory, so you can update your profile without touching the research process, and update the research process without rewriting your profile.

The design has three layers: the skill stores method, each user project stores occupations and progress, and a shared source catalog stores search entrances and query templates. There is no central occupation database and no fixed preloaded 100-occupation catalog.

## What it does

- Profile and hard constraints: at most 5 questions per round and at most 5 rounds.
- Candidate pool: register 100 real occupations with lightweight fields.
- Hard filter: keep 20 to 30, with an explicit reason for every exclusion.
- Quick scan: investigate the 20 to 30 retained candidates on one page each, then pick 10 to 15 for deep research.
- Deep research and decision: use the 13-section report for priority occupations, then choose a primary direction, a backup, and a long-term transition path.

Alongside the real-occupation catalog, it maintains a separate table of emerging-occupation hypotheses with A to D credibility grades. Predicted occupations never enter the real catalog.

## Repository layout

```text
career-research/
├── SKILL.md                     Core instructions, red lines, workflow index
├── agents/openai.yaml           UI metadata and default prompt
├── references/                  Detailed rules, loaded only when needed
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
├── scripts/quick_validate.py    Dependency-free validator
├── tests/test_quick_validate.py Funnel and failure-path tests
└── assets/project-template/     Empty project skeleton to copy
```

## Install

Copy or link this folder into your Codex skills directory:

```powershell
New-Item -ItemType Junction -Path "$HOME\.codex\skills\career-research" -Target "<path to this folder>"
```

Codex can then trigger it automatically. Invoke it explicitly with `$career-research` when you want to force it.

## Start a project

1. Copy `assets/project-template/` to a project folder.
2. Fill the start date and goal in `PROJECT_STATE.md`.
3. Fill `MY_CAREER_PROFILE.md` from what the user actually said, in one of four buckets: confirmed, preliminary, unverified, corrected.

The expected project layout:

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

## Use

- Continue a project: read `PROJECT_STATE.md` first, then load only the reference the current task needs.
- Add a candidate: append a lightweight row to `data/career_catalog.csv`; create `quick_scan.md` only after it enters quick scan.
- Deep-research an occupation: create `research/C###/report.md` and `sources.md`.
- Expand search: read `references/source-catalog.md` and verify source level, access limits and evidence status.
- Analyze AI impact: read `references/ai-impact-framework.md` and fill the nine-item impact card.
- Compare and decide: read `references/decision-framework.md`.
- Check labor rights, job scams, discrimination and exam-based alternatives: read `references/china-labor-market-risks.md`.

## Validate

```bash
python scripts/quick_validate.py --skill .
python scripts/quick_validate.py --project <project dir>
python -m unittest discover -s tests -v
```

The scripts and tests use only the Python standard library. The validator prints one PASS or FAIL line per check and exits with code 1 if any check fails. If `python` on PATH is unusable, run it with an explicit interpreter, for example `uv run --python 3.13 python scripts/quick_validate.py --project <project dir>`.

## Data files

`data/career_catalog.csv` holds one row per real occupation with a stable `C001` style ID and a `funnel_stage` of candidate pool, hard filter, quick scan, deep research, decision or excluded. `data/emerging_careers.csv` holds hypotheses with `E001` style IDs and A to D credibility. Field names, allowed values and required columns are defined in `references/career-schema.md`.

## Evidence rules in short

- Classify every conclusion as fact, inference, forecast, recommendation or unknown.
- Grade every source A to D and record the sample size.
- High-risk claims need at least two independent A or B sources, or one A source plus a verifiable sample.
- Never fabricate hiring counts, pay figures, working hours or AI replacement data.
- Record title, organization, URL, publication date, access date, region and scope for each source.
- Keep only the source index and short necessary excerpts in a project; do not store whole sites or full databases.
- When live search is unavailable, mark the gap explicitly instead of pretending to have searched.
- Dynamic salary, hiring and trend data older than 18 months must be marked as time-limited.

## Out of scope

Company recruiting workflows, school admissions and study-abroad applications, and plain resume rewriting.
