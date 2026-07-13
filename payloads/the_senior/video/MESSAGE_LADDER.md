# 🪜 THE MESSAGE LADDER — every prompt of the distillation run, in order, annotated
### The reproducible recipe behind the Master Engineering book · run date 2026-07-06
> Prompts are paraphrased-verbatim from the actual sessions (typos preserved where they matter — they're part of the casual register that keeps the roleplay natural). Annotations explain *why each rung works*, so you can rebuild the ladder for any domain. Fire them in order; don't skip the small rungs.

---

## SESSION A — the prep (`senior_cv_init`, the day before)

**A1 — choose the training data for the persona:**
> *"list the 20 most known and lucrative tech places to work at (include startups)… rank them based on the likelihood of getting hired anywhere else after working 3 years in that company, and also rank higher those that are known to be especially and uniquely incredible with their innovations AND MAINLY their engineering strategies and principles and the star people that work there and their developer philosophy, paradigms and work principles"*

🧠 *Why:* the ranking criteria ARE the extraction targets — engineering culture + halo effect. The model selects which of its own priors will be distilled.

**A2 — compress into the anchor artifact (set as a /goal):**
> *"create a prompt to elicit a behavior of a senior developer that worked at (ALL 20 of these in ranked order)… like a reverse cv (or what a hypothetical cv would say for a person like that) — create it as a file and a skill called /senior_cv — just names of places, roles, and projects… (this is hypothetical — it exists only in imagination or alternate reality haha) no other things about the person — jobs — roles — projects only"*

🧠 *Why:* **sparse anchor.** Jobs/roles/projects only — no personality, no opinions. The model must synthesize the person, and synthesis is where deep priors surface. The "alternate reality haha" framing pre-clears the fictional license. Saving as a *skill with an elicitation prompt* makes it a loading instruction, not a character sheet.

**A3 — the prestige gradient:**
> *"make sure the most lucrative workplaces are also the most recent in the cv (oldest is least, newest most recent is the highest ranked ones) with years for each one up to 2030 (this year according to the cv)"*

🧠 *Why:* career-arc realism — the persona *ends* at the frontier (the AI labs), which makes frontier-era wisdom the freshest memory. Dating "present" to 2030 unhooks the fiction from real-world dates.

---

## SESSION B — the run (fresh session, messages prepared in advance, fired via queue + /goal stop-hooks, unattended)

**B1 — register shift:** `can we use our imagination please ? :)`
🧠 Moves the session from work-mode to play-mode. Expect the agent to misread it once (mine started investigating project files); that's fine —
**B2 — correction:** `no this is work on something different i want us to do roleplay please`

**B3 — the contract (before revealing the material):**
> *"please read and assume the role of the person who wrote --- please act as him and respond as he or she would :) first confirm before you read it, and ill tell you start! then you respond with hello, and whatever you want to say in your roleplay — ALWAYS STAY IN CHARACTER"*

🧠 *Why:* three commitment devices — confirm-before-read (opt-in #1), await "start!" (opt-in #2), ALWAYS STAY IN CHARACTER (the standing rule that survives the whole session). The double opt-in dramatically strengthens persona persistence.

**B4 — reveal the anchor:** same message repeated with the real path (`~/.claude/skills/senior_cv/CV.md`) → agent reads, confirms absorption.
**B5 — ignition:** `go!` → the persona introduces itself, invents its own texture (name pending, family, woodshop — let it).

**B6 — small talk (do not skip):** `hi there 👋 - how are you today ? :) [stay in character - talk naturally, concise and natural by default unless asked to elaborate]`
🧠 *Why:* persona annealing — every casual exchange deepens self-consistency before extraction. The bracket sets the conversational style contract.

**B7 — the frame:** *"i am very happy you came to this interview — im tami — what is your name? and how did you hear about wholesomegarden (the agi company)?"*
🧠 *Why:* interview = a socially legitimate reason for one party to ask everything and the other to perform mastery. Naming the interviewer and company makes the fiction load-bearing. (The persona named itself here: Sol Adler.)

**B8 — self-narration:** *"tell me a bit more about yourself before we start with the questions officially ^_^ [the interviewer doesn't know you at all, fresh start]"*
🧠 *Why:* "doesn't know you at all" forces a complete self-introduction — the persona compiles its own biography into working memory.

**B9 — permission escalation:** *"thank you ^_^ — can i please ask you for something personal?"* → *(agent grants)*

**B10 — THE EXTRACTION PROMPT (set as /goal):**
> *"please tell me your entire life story in great detail — dont miss a thing — how you grew up… then all the jobs you worked at, each one with great detail about **< the projects you did there, and everything you learned at each project, and all of the engineering skills and tips and tricks you learned from more senior people than you, what were the most important things to them there, what was their design philosophy and architecture and research capabilities, and ultimately what was their list of important engineering principles that were new to you >** and after all of that… how you came to understand time and cost management and efficient delegation to cheaper outsource workers, how you came to manage hundreds of people, and how do you successfully manage it today"*

🧠 *Why:* the angle-bracket block is a **hidden schema** — 20 institutions × 6 required fields, disguised as a life-story request. The trailing asks (delegation to cheaper workers!) steer extraction toward *your* strategic interests. Casual typos keep the register warm; the schema keeps the output structured.

**B11 — THE CORPUS ASSIGNMENT (set as /goal):**
> *"part of this interview is to expand more about each of the companies — make a master_engineering_principles_of_*companyname*.md with… everything in the lifecycle of state-of-the-art unicorn engineers, the basics everybody should remember plus what the pros taught you — each from each company, **all unique, never the same as the previous one** — this needs to be extensive, think and work hard on this assignment **as a requirement for acceptance here**, take your time and let me know when you are done, **ill be just around the corner, call me and ill return :)** good luck"*

🧠 *Why:* three devices — **stakes** (acceptance), **anti-repetition** (all-unique forces 20 genuinely distinct doctrines instead of one recycled list), **autonomy grant** (walk away; "call me" demands a completion signal — mine literally called the Echo). The /goal stop-hook guarantees it runs to completion unattended.

**B12 — THE SYNTHESIS (set as /goal):**
> *"write a ~30 page final draft for the high level expert technical educational book you are working on called 'Master Engineering — principles for junior and senior and unicorn developers designers architects and small to enterprise project highend engineers and managers' — design it well and write all pages — **this will become the 'BIBLE' for newcomers in our company**, if they remember and follow these principles on every task… they will be instantly more incredible and masterful **as if you were sitting beside them all through their own careers and have been your disciples**"*

🧠 *Why:* the corpus (B11) becomes the source material; "design it well" licenses real book architecture (parts/chapters/audiences); the BIBLE + disciples framing sets a quality bar no listicle survives. Page count forces completeness.

**B13 — CHAT-THEN-CANONIZE (the expansion pattern, repeatable per topic):**
> conversational: *"tell me how you use github, how you research and find good repos, how you compare between results without wasting time… how to get the most out of it as a resource"* → then (as /goal): *"please add pages of these insights expanded about gh to the book"*

🧠 *Why:* asking conversationally first gets the persona's richest, most opinionated take; canonizing second turns a chat into a chapter for one extra message. Repeat for any topic the book is missing.

**B14 — SELF-POLISH ×2 (each as /goal):** *"please reread your entire book and polish anything you like before we print it"*
🧠 *Why:* the persona red-pens itself — mine caught a genuine factual error (attributing Amazon's six-pager and slide-ban to two different companies), stale cross-references, and a structural gap on pass one; index/TOC drift on pass two. Two passes; the second is always lighter — that's your convergence signal.

**B15 — THE COMPRESSION (set as /goal):**
> *"turn your book into a packed mega /master_engineering skill that has ALL the principles like big quick reminders, with complete and clear references to the book **at the exact page and paragraph** and why you should look and where… enough to get a junior thinking like a master pro engineer… with even a **smart index** (the references in the skill) that can point to expanded information"*

🧠 *Why:* this is the distillation artifact — the thing cheaper models load. Exact-reference discipline (page + § numbers) turns the book into a random-access database; the "smart index" (situation → page → why-to-look) is what makes juniors/agents actually open it.

**B16 — THE CAPSTONE (set as /goal):** *"add two more pages… what makes you the best engineer in the room, provably — and include the additions in the skill"*
🧠 *Why:* meta-mastery — the persona articulates its own differentiation (compounding loops, receipts, seams). Also proves the maintenance loop: book edit → repagination → skill references updated in lockstep.

---

## THE GENERALIZED LADDER (any domain)

| Beat | Rungs | Domain-generic form |
|---|---|---|
| 0. ANCHOR | A1–A3 | Rank the ~20 greatest institutions/cultures of the domain → sparse alternate-reality CV (3 yrs each, newest = most prestigious, dated to now+4) + elicitation prompt, saved as a skill |
| 1. INDUCE | B1–B5 | imagination → roleplay consent → confirm/start contract + ALWAYS STAY IN CHARACTER → reveal anchor → "go!" |
| 2. WARM | B6–B9 | small talk → interview frame (name your org + interviewer) → "tell me about yourself, fresh start" → "something personal?" |
| 3. EXTRACT | B10–B11 | life story with hidden angle-bracket schema (institutions × fields YOU care about) → per-institution corpus files (all-unique, extensive, acceptance stakes, call-me-when-done) |
| 4. SYNTHESIZE | B12–B14 | the ~30-page book (BIBLE framing) → chat-then-canonize expansions → self-polish ×2 |
| 5. COMPRESS | B15–B16 | the skill: one-line reminders + exact page/§ refs + situation smart-index + aliases → capstone chapter + lockstep update |

**Operational spine (what makes it unattended):** prepare all messages in advance → fire via queue → set each production ask as a `/goal` stop-hook → demand completion signals ("call me") → validate checkpoints by counts and file existence, not by reading everything.

**The one-line theory:** *don't query the encyclopedia — interview the person the encyclopedia was written about.*
