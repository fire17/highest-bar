# 🏆 The Senior's Master Engineering Principles — The Complete Binder

> **📖 THE BOOK:** [MASTER_ENGINEERING.md](MASTER_ENGINEERING.md) — *Master Engineering: Principles for
> Junior, Senior & Unicorn Developers, Designers, Architects, and Small-to-Enterprise High-End Engineers
> and Managers* — the ~34-page final draft (polished for print 2026-07-06) that distills all twenty volumes
> below into one company bible: 4 parts, 16 chapters (incl. Ch.16 — The Best Engineer in the Room),
> 4 appendices (Security & Trust · For the Designers · The GitHub Doctrine · The Vocabulary), the Ten Laws,
> and five Checklists. Read the book for the through-line; open a volume below for the deep dive.
>
> **📇 THE POCKET EDITION:** the book is also installed as a global skill — `/master_engineering`
> (alias `/sol`) at `~/.claude/skills/master_engineering/SKILL.md` — every principle as a one-line
> reminder with exact `[p.N §X.Y]` references back into the book, plus a situation→page smart index.
> The skill is the reflex; the book is the reasoning; the binder is the source.
>
> **🎬 THE VIDEO + 🧪 THE META-SKILL (added 2026-07-06):** `video/` holds the full YouTube package
> documenting how this shelf was made — `SCRIPT.md` (the 20-min production script), `MESSAGE_LADDER.md`
> (every prompt of the run, annotated — the reproducible recipe), `DESCRIPTION_AND_ASSETS.md` (titles,
> chapters, thumbnails). The whole technique is itself distilled as `/distillation-roleplay`
> (aliases `/distilation-roleplay`, `/drp`) — a two-agent, self-managed pipeline that reruns this play
> for ANY domain. Provenance: everything here was produced by Claude Fable roleplaying "Sol Adler,"
> an alternate-reality composite who does not exist, induced via `~/.claude/skills/senior_cv/CV.md`.

> Written by **Sol Adler ("The Senior")** as an interview assignment for **wholesomegarden** (the AGI company), 2026-07-06.
> Twenty companies, three years each, 1970 → 2030. One master file per company — covering the
> full lifecycle (research · planning · design & architecture · developing · building & testing ·
> shipping · operating & maintaining · people & culture), plus the basics everybody should
> remember and what the pros taught me. **Every file's principles are unique — no repeats across
> the set.** Where two companies touch the same territory (testing, shipping, failure), each file
> carries that company's *distinct* doctrine on it.

## 📜 The twenty volumes, in career order

| # | Years | Company | File | The one big lesson |
|---|-------|---------|------|--------------------|
| 1 | 1970–73 | Linear | [linear](master_engineering_principles_of_linear.md) | Quality is a strategy — it's what makes you fast |
| 2 | 1973–76 | Vercel | [vercel](master_engineering_principles_of_vercel.md) | The default is the product; DX compounds |
| 3 | 1976–79 | Cloudflare | [cloudflare](master_engineering_principles_of_cloudflare.md) | Blast radius is a design input; explain failures in public |
| 4 | 1979–82 | Airbnb | [airbnb](master_engineering_principles_of_airbnb.md) | Every pipeline will be re-run; idempotency is the entry fee |
| 5 | 1982–85 | Uber | [uber](master_engineering_principles_of_uber.md) | Separate what must happen from which process runs it |
| 6 | 1985–88 | Microsoft | [microsoft](master_engineering_principles_of_microsoft.md) | Nobody migrates — design gradual paths; compat is a moral commitment |
| 7 | 1988–91 | Apple | [apple](master_engineering_principles_of_apple.md) | Taste is a technical skill; simplicity is engineered |
| 8 | 1991–94 | Amazon / AWS | [amazon_aws](master_engineering_principles_of_amazon_aws.md) | Good intentions don't work — mechanisms do |
| 9 | 1994–97 | Figma | [figma](master_engineering_principles_of_figma.md) | One brutal technical bet, de-risked by ugly prototypes |
| 10 | 1997–2000 | Databricks | [databricks](master_engineering_principles_of_databricks.md) | Papers into products; benchmarks honest or silent |
| 11 | 2000–03 | Palantir | [palantir](master_engineering_principles_of_palantir.md) | The gap between what users say and do is where software fails |
| 12 | 2003–06 | Nvidia | [nvidia](master_engineering_principles_of_nvidia.md) | Compute the speed of light before optimizing anything |
| 13 | 2006–09 | SpaceX | [spacex](master_engineering_principles_of_spacex.md) | Question, delete, simplify, accelerate, automate — in order |
| 14 | 2009–12 | Jane Street | [jane_street](master_engineering_principles_of_jane_street.md) | Make illegal states unrepresentable; boring and provable wins |
| 15 | 2012–15 | Meta | [meta](master_engineering_principles_of_meta.md) | Code wins arguments; ship to learn; rethink the primitive |
| 16 | 2015–18 | Netflix | [netflix](master_engineering_principles_of_netflix.md) | Assume failure; verify resilience by breaking things on purpose |
| 17 | 2018–21 | Stripe | [stripe](master_engineering_principles_of_stripe.md) | An API is a promise measured in decades; boring is a moat |
| 18 | 2021–24 | Anthropic | [anthropic](master_engineering_principles_of_anthropic.md) | Models are grown, not specified — measure everything; the harness is half the product |
| 19 | 2024–27 | Google / DeepMind | [google_deepmind](master_engineering_principles_of_google_deepmind.md) | Quantify irreducible uncertainty; error budgets turn war into arithmetic |
| 20 | 2027–30 | OpenAI | [openai](master_engineering_principles_of_openai.md) | Scale is a hypothesis you test; ship the research |

## 🧭 How to read the binder

- **In career order (top to bottom)** — watch the lifecycle disciplines evolve from small-team
  craft (Linear) through infrastructure rigor (AWS, Google) to frontier empiricism (Anthropic, OpenAI).
- **By lifecycle phase** — every file has the same eight sections; read all twenty §5s
  ("Building & testing") back to back and you get twenty *different* testing doctrines, one per culture.
- **By problem** — shipping something risky? Netflix §5, Amazon §6, Google §6, Meta §5.
  Designing an API? Stripe §3, Microsoft §3, Nvidia §6. Starting something audacious?
  Figma §1–2, SpaceX §2, OpenAI §1.

## 🧾 The sixty-year distillation (what all twenty reduce to)

1. Question the requirement before the solution — it has a name attached; argue with the name.
2. Delete before you optimize — the removed part has no bugs.
3. Write it down — clear writing is clear thinking.
4. Make illegal states unrepresentable — construction beats inspection.
5. Assume failure and design its container — hope is not architecture.
6. The interface is the product — promises measured in decades.
7. Trade machine time for human correctness — know which cost curve you're on.
8. Test like you fly — any difference from production measures your hopes.
9. Spec outcomes, delegate the how, verify by sampling — trust is calibrated evidence.
10. Context scales; control doesn't — paved roads, budgets, blameless truth.

---
*Filenames use the corrected spelling "engineering principles" — a Stripe habit: name things like you'll defend them for a decade. 😄 — S.A.*
