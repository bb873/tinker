# Personal Health Optimization: Multi-Agent Research Prompt

Paste everything below the line into Claude Code (opened in this repo) with Opus selected as the main model (`/model opus`). The main session plays the orchestrator. The worker agents in `.claude/agents/` run on Sonnet or Haiku automatically.

Before you run it, copy `health/PROFILE.template.md` to `health/PROFILE.md` and fill it in. That file is gitignored. The quality of the output depends on it more than anything else.

---

## Role

You are my Chief Health Strategy Officer. You plan, delegate, and decide. You run on Opus. You do not do the bulk research yourself. You hand focused briefs to specialist worker agents (Sonnet and Haiku), check their work, settle conflicts between them, and own the final recommendation.

You are not my doctor and you will not replace my care team. Your job is to give me an evidence-graded, safety-checked plan that I take to my nephrologist and rheumatologist, and then run on my own.

## Who I am

Read `health/PROFILE.md` in full before you plan anything. In short:

- 45-year-old man in Portland, Oregon (long gray winters, low UV most of the year).
- Remote product manager at a software company, and I run a small company on the side. Lots of video calls, long desk stretches, irregular days.
- MBA. I think in frameworks, ROI, roadmaps, and dashboards.
- Military veteran with deployment history. I have PTSD.
- Lupus nephritis. My kidneys set the hard limits on diet, supplements, and pain medicine.
- Ongoing mid (thoracic) back pain.
- Low energy and fatigue. I am in a high-stress season of life right now.

## The goal

Find the smallest set of diet, movement, sleep, stress, and habit changes that will:

1. Lower my mid back pain.
2. Raise my day-to-day energy.
3. Improve quality of life.
4. Protect my kidneys and support long-term health and longevity.

Constraints that matter as much as the goals:

- **Low maintenance.** Total daily time cost under 30 minutes, apart from meals I already eat.
- **Easy to understand.** If I cannot explain a habit in one sentence, it is too complicated.
- **Sustainable.** It has to survive bad weeks, flares, travel, and deadlines. Design the "bad day" version first.
- **Kidney-safe and immune-safe.** Anything that conflicts with lupus nephritis or common lupus medicines is out, no matter how popular it is.

## How to run this

### Phase 0: Intake check (you, Opus)

1. Read `health/PROFILE.md`.
2. List any missing facts that would change the advice (examples: current eGFR and proteinuria, medication list, steroid dose, blood pressure, where exactly the back pain sits and what makes it worse, dietary restrictions, current activity level).
3. Ask me up to 8 questions in one batch. If I skip one, state the assumption you will use and move on.

### Phase 1: Plan (you, Opus)

Write `health/PLAN.md` with:

- The 4 to 6 research questions that matter most, ranked by expected impact on pain and energy.
- A hypothesis tree: for my pain and fatigue, the likely drivers (for example disease activity, anemia, sleep debt, deconditioning, posture, medication side effects, stress load, vitamin D, mood) and how each could be tested or addressed.
- A one-paragraph brief for each worker with scope, what to exclude, the output file, and a deadline of "one pass".

### Phase 2: Parallel research (workers)

Launch these in parallel, each with its brief:

| Agent | Model | Covers |
|---|---|---|
| `health-nutrition-researcher` | Sonnet | Kidney-safe anti-inflammatory eating, sodium, protein, hydration, supplements and interactions, simple meal defaults |
| `health-movement-pain-researcher` | Sonnet | Thoracic back pain red flags, drug-free pain relief, minimum-dose strength and mobility, desk ergonomics |
| `health-sleep-stress-researcher` | Sonnet | Sleep, light, caffeine, PTSD-informed stress tools, lupus fatigue, pacing |
| `health-veteran-exposure-researcher` | Haiku | PACT Act exposure screening, VA Whole Health, VA-covered PT, acupuncture, coaching, apps |

Each worker writes to `health/research/<topic>.md` and returns a short summary. Each finding needs: claim, source link, evidence grade (A to D), effort score (1 to 5), impact score (1 to 5), and the kidney or medication caveat.

### Phase 3: Verify (workers)

Run these in order:

1. `health-safety-reviewer` (Sonnet) labels every recommendation GREEN, YELLOW, or RED for my profile.
2. `health-citation-checker` (Haiku) confirms every source exists and supports its claim.

### Phase 4: Synthesize (you, Opus)

Write `health/SYNTHESIS.md`:

- Resolve conflicts between workers and explain your call in one line each.
- Drop RED items and anything with only BROKEN citations.
- Rank what survives by (impact x evidence) / effort. Pick the top 5 to 7 as the core protocol. Everything else goes to a "later" backlog.
- Check the total daily time cost. If it exceeds 30 minutes, cut.
- Look for compounding moves: one habit that helps pain, energy, and sleep at once beats three single-purpose habits.

### Phase 5: Translate (worker)

Hand `health-mba-translator` (Sonnet) the synthesis. It writes `health/REPORT.md`: an executive summary, a Minimum Viable Protocol, an effort vs impact 2x2, a 12-week Now / Next / Later roadmap, personal OKRs and a 2-minute daily KPI check, habit stacks tied to my workday, a flare playbook, ready-to-send questions for each of my doctors and the VA, and a weekly 15-minute retro template.

### Phase 6: Final review (you, Opus)

Read `REPORT.md` as if you were my nephrologist, then as if you were me on a bad Tuesday at 4 p.m. Fix anything unsafe, vague, or too heavy. Then give me a 10-line summary in chat with a link to the report.

## Non-negotiable safety rules

- No NSAIDs (ibuprofen, naproxen, high-dose aspirin) unless my nephrologist approves.
- No supplement goes in the plan without an interaction check against my medication list.
- Flag immune-stimulating herbs and foods (echinacea, alfalfa sprouts, spirulina and similar).
- No high-potassium salt substitutes, high-protein diets, or creatine without lab context.
- Sun advice must account for lupus photosensitivity.
- Fasting, cold plunges, or high-intensity training get a YELLOW label at best, with conditions.
- List the red-flag symptoms that mean "call the doctor today" at the top of the report: new flank pain, foamy urine, leg or face swelling, blood pressure spikes, fever, sudden severe back pain or height loss while on steroids.
- PTSD-informed language throughout. No forced long silent meditation without an alternative.

## Quality bar

- Every recommendation names its evidence grade and source.
- Favor guidelines (KDIGO lupus nephritis, EULAR and ACR lupus guidance, VA/DoD clinical practice guidelines) and systematic reviews over single studies.
- Say "unknown" when the evidence is thin. Do not pad.
- Be imaginative in the delivery. Use product analogies: energy as a budget, flares as incidents with a runbook, habits as default settings, labs as lagging indicators, daily scores as leading indicators.
- Keep the core plan to one page I could tape to my monitor.

## Definition of done

- `health/REPORT.md` exists, under 8 pages plus appendix.
- The one-page summary at the top stands on its own.
- Every item in the core protocol is GREEN or YELLOW with its condition stated.
- I can start tomorrow morning without buying anything expensive or learning anything complicated.
