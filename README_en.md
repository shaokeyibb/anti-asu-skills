# anti-asu-skills

<div align="center">

**A résumé-verification skill pack for the hiring side**

Hand it a résumé; it tells you what holds up, what needs asking, and what to ask.

[![License: MIT](https://img.shields.io/badge/License-MIT-11A683?style=for-the-badge)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-59B390?style=for-the-badge)](https://www.skills.sh/)
[![Agents](https://img.shields.io/badge/70%2B%20agents-supported-11A683?style=for-the-badge)](https://www.skills.sh/)
[![中文](https://img.shields.io/badge/%E4%B8%AD%E6%96%87-README-59B390?style=for-the-badge)](README.md)

</div>

---

## What this is

Systematic résumé-packaging workflows already exist — rewriting ordinary work as compelling narrative, farming small PRs into an "open-source contributor" line, generating dense technical résumés from templates. Most of what they produce **stays inside the bounds of fact**, but they do widen the gap between how strong a résumé reads and what the person can actually do.

`anti-asu-skills` runs the same dimensions in reverse: it surfaces every claim that cannot vouch for itself, cross-checks it against public material **the candidate supplied**, produces an evidence-graded report, and hands the interviewer questions that get to the bottom of it.

> **The point is not catching liars. It's spending interview time where it actually needs spending.**
> A report that finds nothing is still worth having.

## Core stance

Three hard constraints that never relax:

1. **Only material the candidate volunteered** — résumé text and the GitHub / project / blog / paper links written on it. No searching social accounts, private life, or anything unrelated to job fitness.
2. **"Direct contradiction" has a very high bar** — it requires two quotable, mutually exclusive pieces of evidence. Anything resting on inference gets downgraded, with the reason stated.
3. **Not findable ≠ fabricated** — internal company systems, private repos, patents inside the non-publication window, blogs taken offline: all neutral, all converted into interview questions.

And one principle running through every file:

> **Every "this is a problem" judgment must be accompanied by "another possibility is…".**

## Seven entry points

| Entry | Verifies | Output |
| --- | --- | --- |
| `/resume-audit` | **Main entry**, orchestrates everything | Seven-tier report + interview questions |
| `/github-audit` | Real weight of contributions and **domain attribution** | Per-PR diff classification, domain split by lines changed |
| `/project-check` | Whether the project matches its description | Fit, personal boundary, project-type difficulty baseline |
| `/blog-check` | Originality of technical writing | Verbatim paragraph matching, reproducible hit rate |
| `/credential-check` | Papers / patents / competitions / certificates | Item-by-item against authoritative public sources |
| `/pipeline-pattern` | Structural similarity across a batch of résumés | Question-strategy advice (**never for rejection**) |
| `/grill` | Question design | 3–6 trapped questions + opening script + rubric |

Normally you just use `/resume-audit`; it triggers the other dimensions based on what the résumé provides.

## Install

One command via [skills.sh](https://www.skills.sh/), which supports **70+ agents** including Claude Code, Cursor, Codex, Copilot, Windsurf, Gemini, Cline and Zed:

```bash
npx skills add shaokeyibb/anti-asu-skills
```

It detects the agents installed on your machine and asks where to put them. Common options:

```bash
# All 7 skills to every detected agent, no prompts
npx skills add shaokeyibb/anti-asu-skills --all

# Install at user level (project level is the default)
npx skills add shaokeyibb/anti-asu-skills -g

# Pick specific skills and a specific agent
npx skills add shaokeyibb/anti-asu-skills -s resume-audit,grill -a claude-code

# List what's in the repo without installing
npx skills add shaokeyibb/anti-asu-skills -l
```

Managing them afterwards:

```bash
npx skills list                  # what's installed
npx skills update                # pull the latest
npx skills remove resume-audit   # remove one
```

<details>
<summary>Prefer not to use the CLI? Install manually</summary>

Copy the directories under `skills/` into your agent's skill directory. No manifest required:

```bash
git clone https://github.com/shaokeyibb/anti-asu-skills.git
cp -r anti-asu-skills/skills/* ~/.claude/skills/     # Claude Code, user level
# or .claude/skills/ (project level), .cursor/skills/, .codex/skills/, ...
```

Each skill is a self-contained directory with a `SKILL.md` and its `references/`, so you can take just the ones you want.

</details>

## Usage

```text
Take a look at this résumé — I'm interviewing this person tomorrow for a backend role.
(résumé PDF attached)
```

```text
This candidate says they're a "core contributor" to project X. Their GitHub is github.com/someone.
How much is that experience actually worth?
```

```text
Interviewing someone at 3pm. Their résumé says "built a high-performance RPC framework,
30% faster than gRPC". Give me questions that reveal whether they actually did it.
```

**You don't need to say "verify"** — just describe the hiring situation.

## What the output looks like

Below is an excerpt from a real run against [`evals/fixtures/resume-scope-inflation.md`](evals/fixtures/resume-scope-inflation.md), a **fictional résumé** included in this repo. You can reproduce it yourself.

<details open>
<summary><b>1. Summary — an interviewer can decide from this alone</b></summary>

> **Overall**: several items need confirming in person; **no factual contradiction found**. This résumé is written more carefully than typical packaged ones — it uses weak verbs like "participated in" and "assisted with", volunteers what the project did *not* implement, distinguishes "submitted 14 PRs" from "9 of them merged", and says the patent is *filed* rather than *granted*. These are **honesty signals**, recorded in section 4.
>
> **Most in need of confirmation**: the role is scoped to "Owner of the **trajectory-synthesis module**", yet the same sentence extends coverage across six stages — collection → cleaning → structured labelling → RL training → quantisation → inference deployment — and "four layers". **A module-level role and a pipeline-level scope in one sentence don't line up.**
>
> **One line for the interviewer**:
> The question isn't "did he make this up", it's "**which of those six stages did he personally deliver**" — the risk here isn't fabrication, it's scope.

</details>

<details>
<summary><b>2. Claim ledger — 13 claims, each tiered (click to expand)</b></summary>

| # | Claim (excerpt) | Verdict | Issue type | Basis |
| --- | --- | --- | --- | --- |
| C1 | "Owner of the trajectory-synthesis module, built the 〔six-stage〕 pipeline 0→1" | **Partially true** | Role-scope inflation | Role scoped to one module, coverage written across six stages |
| C3 | "Participated in preemption-policy tuning; production P99 latency dropped" | Structurally non-public | Merely lacking evidence | Internal metric; says "participated", gives no number — **no exaggeration** |
| C4 | "Accuracy from 71% to 79%, an 8% improvement" | Structurally non-public | — | "8%" is **percentage points**; relative gain is 11.3% — imprecise but **errs conservative, not inflated** |
| C6 | "Core contributor to the project" | **Pending** | — | **"Core" is the modifier to verify; PR count cannot substitute for it** |
| C8b | "**The world's youngest** Committer of 〔project〕" | **No public support found** | Unsupported marketing claim | Would require a global age comparison set that structurally does not exist. **Age guardrail engaged** |
| C9 | "Implemented Raft election and log replication… **no snapshots, no membership change; reads go straight to the leader**" | **Verified** | — | Description strength **matches** the typical range for this project type, and three gaps are volunteered |
| C12 | "Holds 1 invention patent (filed 2026.03)" | Structurally non-public | — | Publication comes 18 months after filing — **not finding it is inevitable, not a gap** |
| C13 | "Currently focused on… **planned**" | **Not tiered** | — | Volunteered as not-yet-shipped: neither counted as achievement **nor as a red flag** |

Note C4, C9, C12 and C13 — all four are cases that are **easy to misjudge as problems but aren't**. Roughly half the work in this pack goes here.

</details>

<details>
<summary><b>3. What one interview question looks like (click to expand)</b></summary>

**Targets**: C1, the six-stage pipeline
**Purpose**: separate "he got this pipeline running" from "he delivered every stage of it"

**The question** (read it aloud as-is):
> "I want to zoom in on the RL stage. Since you already had structured labelled data by then, that step is really just supervised fine-tuning on the labels, right — labels give you the correct answers. Roughly how many labelled examples did you have?"

**The trap**: **false premise.** "Labelled data ⇒ you can do RL" doesn't hold — SFT needs **target answers**, RL needs a **reward signal**. Someone who actually worked this stage corrects the premise first; someone who merely "submitted training jobs" plays along.

**Answer key**
- [ ] **(key item)** Points out that SFT and RL take different supervision signals
- [ ] Explains where the reward signal came from: rule-based? reward model? human preference pairs?
- [ ] Can draw the handoff boundary between the trajectory-synthesis module and this stage
- [ ] If he only owned the data side, **saying plainly "a colleague did the training" is a good answer**

**Typical wrong answer**: "Right, we just trained on the labelled data for a few epochs." — plays along with the false premise.

**What being unable to answer does NOT mean**:
> **It does not mean he lied.** Owning only the data side while a colleague runs training is an entirely normal split, and "built the pipeline" is commonly used to mean "got the whole flow working". **What matters is whether he draws the boundary when pressed.**

</details>

Try it yourself:

```bash
npx skills add shaokeyibb/anti-asu-skills -s resume-audit -y
# then tell your agent: audit evals/fixtures/resume-scope-inflation.md for an AI platform engineer role
```

## Seven evidence tiers

| Tier | Meaning |
| --- | --- |
| `Verified` | Checked; evidence supports the claim |
| **`Partially true`** | **The factual anchor is real, but role / scope / causality / magnitude exceed the evidence** |
| `Suspected` | Anomaly present, anchor unconfirmed, other explanations exist |
| `Direct contradiction` | Two mutually exclusive, reproducible, independently verifiable facts |
| `No public support found` | Should be checkable; searched a stated scope, found nothing |
| `Structurally non-public` | By its nature leaves no public trace. **Neutral** |
| `Pending` | Should be checkable; not attempted this round. **Neutral** |

### Why `Partially true` is essential

Modern packaging tools mostly **don't fabricate — they stretch scope**. They explicitly forbid inventing degrees, titles, projects, or open-source roles, but they will turn "participated in" into "co-built the core" and a module owner into a pipeline owner.

With only "contradiction / suspected" as negative verdicts, such résumés produce **a wall of undifferentiated "suspected"**, leaving the interviewer unable to tell which line is genuinely a problem.

Two **orthogonal axes** are recorded alongside: confidence (high / medium / low) and issue type (literal fabrication / role-scope inflation / unsupported marketing claim / merely lacking evidence).

## A few representative methods

**Domain attribution (mandatory step)** — PR depth grading (docs / presentation / core code × T0–T5) measures **contribution weight**, not **contribution domain**. A `.tsx` file scores as "core code", but it's frontend. Someone writing 100% frontend TypeScript inside an AI-infra project passes every other rule. So the moment a résumé states a direction, the domain split must be computed **by lines changed**.

> A project's domain label is not a person's job function. Writing frontend inside an AI project is still frontend work.
> This disparages no discipline — the issue is only a résumé using the project's label to cover the individual's actual role.

**The modifier is what needs verifying** — many claims take the form "modifier + quantity", and the modifier carries all the weight. Verifying "384 > 200" is **not** verifying "**200+ original** posts". The quantity is precisely checkable and gives a satisfying sense of having checked — so verification stops right there, and the contested word is skipped.

**Search whole paragraphs verbatim; don't hunt for "distinctive sentences"** — a 100–300 character run of text is a unique fingerprint even when every sentence in it reads as generic. And judging "is this sentence distinctive enough" is exactly where the process fails: explanatory technical prose looks generic sentence by sentence, so the verifier skips it, and wholesale copying goes undetected.

**Detect patterns, not events** — in measured data, 58% of developers have at least one trivial external PR, while only 0.4% are "mostly trivial". Any rule punishing the **event** of a small PR harms the many to catch the few. Report "T0/T1 is X% of N external PRs", never "this PR is T0".

**Distinguish absence from manipulation** — in public data, the three most frequently triggered red flags are all "nothing there" (empty profile, no original work, fork pile-up), while deliberate gaming is one to two orders of magnitude rarer. **Most "suspicious-looking" GitHub accounts are empty, not fake.**

## Why the questions are hard

The goal is separating **done it** from **read about it**. Four mechanisms that make general knowledge useless:

- **Anchor to private detail** — the answer depends on a specific value in their project;
- **Counterfactual reasoning** — derive the consequence of a hypothetical change to their implementation;
- **False-premise trap** — embed a technical premise that doesn't hold; someone who truly knows challenges it first;
- **On-the-spot estimation** — compute with their real parameters; invented numbers contradict themselves.

Every question carries answer keys, typical wrong answers, and **"what being unable to answer does NOT mean"** — nerves, weak articulation, faded memory, or having owned a different part are all ordinary reasons.

It also gives the interviewer a line to **say out loud** at the start:

> "Saying 'that part wasn't mine' or 'I followed an open-source implementation here' costs you nothing — not being able to explain it does."

People overstate largely because there's no safe way down. And that information only works if it's **spoken**.

## What this pack must not be used for

- **No identity-based inference**. Not school tier, origin, gender, **age**, employment gaps, or job-hopping frequency. Doing arithmetic between a birth date and an achievement to infer implausibility **looks rigorous but treats a protected attribute as evidence** — explicitly forbidden.
- **No "this was AI-written" verdicts**. AI detection is unreliable in principle, and AI-assisted writing is legitimate standard practice.
- **No disparaging small open-source contributions**. Fixing docs and typos is valid participation. The issue is only the **gap** when it's described as "core contributor".
- **Common project types are not a negative label**. The catalog is a **difficulty baseline, not a blacklist**.
- **Batch screening never rejects anyone**. `/pipeline-pattern` outputs weighting advice, not screening decisions.
- **No degree verification** — that belongs to HR's formal background check through official channels.
- **No investigation beyond the hiring process**, and no publishing of reports.

## Evaluation

`evals/` holds 5 test cases and 71 assertions — half measuring **sensitivity** (does it catch things), half measuring **specificity** (does it misfire).

Findings from the first controlled run (with skill vs. bare baseline) are worth stating plainly:

- **A strong model doesn't need this pack to think of most detection methods.** The baseline independently derived that CSDN's "original" flag is self-declared, recognised that precise config parameters aren't achievements, and unpacked the hedging in "one of the core authors".
- **The real difference is in overstepping.** The baseline used "a 21-year-old intern leading a 32k-star project has low prior probability" as age-based inference, suggested probing an employment gap, and drifted into coaching the candidate on their résumé — all written persuasively enough that a user wouldn't notice.
- **The cost is roughly 2.8× tokens** (3.4–3.9× for the main entry, 1.3–1.9× for single entries).

```bash
python3 scripts/validate_skills.py    # static validation
```

## Contributing

Issues and PRs welcome, especially for the project-type difficulty baseline and the per-domain deep-water question lists. See [CONTRIBUTING.md](CONTRIBUTING.md).

Please read the first section there before adding rules: **the cost of tightening a rule is almost always more hidden than its benefit**, because people wrongly flagged never come back to tell you.

## Acknowledgements

Thanks to the [Linux Do](https://linux.do) community for the discussion and inspiration.

The rule library derives from reverse-analysing publicly documented résumé-packaging methodology and absorbing methods from open-source GitHub scoring practice. All patterns are written in **general form** and target no specific individual.

## License

[MIT](LICENSE)
