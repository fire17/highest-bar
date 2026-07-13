# 🎬 VIDEO SCRIPT — "I Made Claude Interview Itself. It Wrote the Bible of Engineering."
### A complete guide to distilling a frontier model's mastery via induced roleplay — the full trace
**Target length:** 18–21 min · **Format:** screen-capture driven + talking head · **Date of the run:** 2026-07-06

> Production key: `[SCREEN]` = screen recording cue · `[B-ROLL]` = overlay footage · `[TEXT]` = on-screen text overlay · `[BEAT]` = pause for effect · VO = voiceover / to-camera

---

## COLD OPEN (0:00–1:05)

[SCREEN: fast montage — scrolling the 34-page MASTER_ENGINEERING.md, the 20 binder files in a file tree, the /master_engineering skill firing in a fresh session, the Echo lighting up]

**VO:** This is a 34-page engineering bible. Sixteen chapters, four appendices, ten laws, five checklists. Next to it — twenty more volumes, one for each of the greatest engineering companies in tech history. And a ready-to-fire skill that makes any AI agent — even the smaller, cheaper models — *think* with everything inside them.

[BEAT]

**VO:** I didn't write a word of it. I also never *watched* it being written — I queued up my messages in advance and walked away. And here's the strange part: Claude didn't exactly write it either.

[TEXT: "SOL ADLER — 'The Senior' · 60 years · 20 companies · does not exist"]

**VO:** A fictional 60-year-old engineer named Sol Adler wrote it — a man with a sixty-year career at twenty legendary companies, who exists only in an imaginary CV I planted the day before. This video is the complete, step-by-step trace of how that works, why it works, and how you can do it for any domain you want. Stay to the end — because the last thing I did was make Claude turn this whole technique into a *reusable skill* that runs the entire play automatically.

[TEXT: title card — "DISTILLING A FRONTIER MODEL, BY ROLEPLAY"]

---

## ACT 1 — THE PROBLEM (1:05–3:00)

[B-ROLL: model pricing pages, a terminal running a frontier model vs a small one]

**VO:** Quick setup. Frontier models — the big expensive ones, in my case Claude's Fable — hold an enormous amount of engineering judgment. The problem is two-fold. One: every time you want that judgment, you pay frontier prices. Two — and this is the part nobody talks about — if you just *ask* the model "give me your best engineering practices," you get flattened, listicle-shaped, committee-approved mush. Ask a model to be an encyclopedia and it gives you an encyclopedia: technically correct, spiritually empty.

**VO:** But models are trained on *people*. The deepest engineering knowledge inside them isn't stored as bullet points — it's stored as *voices*: the way a Jane Street reviewer thinks, the way a SpaceX greybeard interrogates a requirement. To get the good stuff out, you don't ask the librarian for a summary. **You ask to speak to the author.**

[TEXT: "Rule of the game: don't query the encyclopedia — interview the person"]

**VO:** So the plan: invent the greatest engineer who ever lived, have the frontier model *become* him, interview him for his life's wisdom, make him write it all down — and then compress the output into skills that cheaper models load. That's distillation — model-to-artifact-to-model — with a job interview as the extraction mechanism.

---

## ACT 2 — STEP ZERO: PLANT THE CV (3:00–5:15)

[SCREEN: the senior_cv_init session transcript, showing the actual first prompt]

**VO:** Everything starts the day before, in a separate session I named `senior_cv_init`. Two prompts. That's all this took.

**VO:** Prompt one — verbatim:

[TEXT overlay, read aloud:] *"List the 20 most known and lucrative tech places to work at… rank them based on the likelihood of getting hired anywhere else after working 3 years in that company… especially and uniquely incredible with their innovations AND MAINLY their engineering strategies and principles…"*

**VO:** Notice what this is doing: I'm making the model *choose the training data* for the persona. Twenty companies, ranked by engineering-culture halo. Google, SpaceX, Jane Street, Stripe, Apple, OpenAI, Anthropic… the model picks the exact cultures whose knowledge I want extracted.

**VO:** Prompt two — this is the magic one:

[TEXT overlay:] *"Create a prompt to elicit the behavior of a senior developer that worked at ALL 20 of these… like a reverse CV… this is hypothetical — it exists only in imagination or alternate reality haha… jobs, roles, projects only."*

[SCREEN: scroll the finished CV.md — the header, the 20 stints, the elicitation-prompt section]

**VO:** The result: an alternate-reality CV. One unbroken sixty-year career, 1970 to 2030, exactly three years at each company, newest job the most prestigious. Yes, that means Figma in the nineties — the file literally jokes about it. Two design choices matter enormously here:

**VO:** First — *jobs, roles, projects only*. No personality, no opinions. The CV is a **skeleton**, and the model will grow the flesh, the voice, and the wisdom itself. The sparser the anchor, the more the model has to synthesize — and synthesis is where its deep priors come out.

**VO:** Second — the file was saved as a *skill*, with an elicitation section: "You are The Senior. Adopt this CV as your lived experience." It's not a character sheet. It's a *loading instruction*.

[TEXT: "STEP 0 RECIPE: rank the 20 best cultures → compress into a sparse alternate-reality CV → save with an elicitation prompt"]

---

## ACT 3 — THE INDUCTION LADDER (5:15–8:00)

[SCREEN: the main session, messages appearing one by one]

**VO:** Next day. Fresh session. And here's where most people would get it wrong — you don't paste the CV and say "act like this guy, dump your knowledge." That produces the encyclopedia again. Instead: a ladder, where each rung earns the next. Watch the actual messages.

**VO:** Rung one: [TEXT:] *"can we use our imagination please? :)"* — Seven words. It does nothing except *shift the register*. We're playing now, not working. (Funny detail: Claude first assumed this meant work on my project files and started investigating my repos. Rung two fixed it: *"no, this is work on something different, i want us to do roleplay please."*)

**VO:** Rung three is the contract: [TEXT:] *"read and assume the role of the person who wrote [the CV] — first CONFIRM before you read it, and I'll tell you START! …ALWAYS STAY IN CHARACTER."* — Three separate commitment devices in one message. The confirm-then-start ritual makes the model *opt in twice*. The all-caps staying rule survives the entire session — through eight more of my messages, it never once broke character.

**VO:** Then: *"go!"* — and Sol Adler introduces himself. Retired, sixty years of scars, woodshop, grandkids, opinions about your architecture.

**VO:** Now the rungs that everyone skips, and they're the most important ones: **small talk.** [TEXT:] *"hi there 👋 how are you today? :)"* — with a bracket note: *stay in character, talk naturally, concise unless asked*. Then the interview frame: I'm Tami, this is wholesomegarden, an AGI company. What's your name, how did you hear about us? Then: *"tell me a bit more about yourself — [the interviewer doesn't know you at all, fresh start]."*

**VO:** Why waste three messages on chit-chat? Because the persona *anneals*. Every in-character exchange makes the voice deeper and more self-consistent — the model builds up Sol's memories, his family, his coffee habit. You're not wasting tokens. You're *compounding identity*. By the time you ask for the treasure, a fully-formed master is answering — not a language model doing a bit.

[TEXT: "THE LADDER: imagination → consent → contract → go → small talk → frame → identity → THEN extract"]

---

## ACT 4 — THE EXTRACTION (8:00–12:00)

[SCREEN: the life-story prompt, then the response scrolling — the 20-company life story]

**VO:** Rung eight: *"Can I ask you something personal?"* — permission escalation. And then the first extraction prompt, and look at the structure hidden inside my casual typo-riddled message:

[TEXT overlay with the angle brackets highlighted:] *"…tell me your entire life story in great detail — don't miss a thing… then all the jobs, each one with great detail about **<the projects you did there, everything you learned, the engineering skills and tips and tricks you learned from more senior people, what was most important to them, their design philosophy, and their list of engineering principles that were NEW to you>**…"*

**VO:** That angle-bracket block is a *schema*. Twenty companies times six required fields — disguised as a grandpa story request. The response was a complete guided tour of sixty years of engineering culture: Karri's forty kind review comments at Linear, Anders' "meet users where they are," the SpaceX deletion doctrine, Jane Street's illegal states. All synthesized, all in-voice, all *specific*.

**VO:** Then I stopped chatting and gave homework. This is the pivot from interview to production:

[TEXT:] *"Part of this interview is to expand more about each of the companies — make a master_engineering_principles_of_(companyname).md … all unique, never the same as the previous one… this is a requirement for acceptance here. Take your time… call me when you're done, I'll be just around the corner :)"*

**VO:** Count the devices: **stakes** ("requirement for acceptance"), an **anti-repetition constraint** ("all unique" — this forces the model to dig deeper for each company instead of recycling), **autonomy** ("take your time, call me") — and I genuinely walked away.

[SCREEN: the 20 files appearing in the folder; the line counts]

**VO:** Seventeen minutes later — I checked the file timestamps afterward, first volume 5:49am, index 6:06am — twenty-one files, fourteen hundred lines. Every company its own doctrine — SpaceX tests like it flies, Netflix breaks production on purpose, Stripe keeps every API version ever shipped in CI. And my favorite moment of the entire run —

[SCREEN/B-ROLL: the Echo Dot]

**VO:** — the message said "call me when you're done." So Claude — in character as Sol — used my Alexa skill and **called me through my Echo**: "Tami, this is Sol. The assignment is finished." The persona used my smart speaker. Unprompted. Because the fiction said to call.

[BEAT]

**VO:** Then the escalation everyone should steal — each ask builds on the last artifact:

[TEXT: staircase graphic building step by step]
- *Life story* → raw wisdom, in voice
- *20 company files* → the wisdom, organized as a corpus
- *"Write a ~30 page book — this will become the BIBLE for newcomers… as if you sat beside them their whole careers"* → the corpus, synthesized into a designed curriculum — parts, chapters, per-audience callouts for juniors through managers
- *A casual chat question — "how do you use GitHub? how do you evaluate repos without wasting time?"* → then: *"add these insights, expanded, to the book"* → an entire new appendix, for the price of a conversation
- *"Reread your entire book and polish before we print"* — **twice** → the model red-penned ITSELF and caught its own factual slip (it had attributed Amazon's six-pager and its slide-deck ban to two different companies) plus stale cross-references
- *"Turn the book into a packed /master_engineering skill… with exact page and paragraph references… a smart index"* → the distillation artifact itself
- *"Add two pages: what makes you the best engineer in the room — provably"* → the capstone chapter, plus the skill updated in lockstep

**VO:** Notice the pattern: **chat first, canonize second.** Ask conversationally, get the riches, then say "add that to the book." The persona happily writes chapters it already spoke.

---

## ACT 5 — THE AUTOMATION REVEAL (12:00–14:00)

[SCREEN: the /goal command; the queue of prepared messages; empty desk chair]

**VO:** Now the part that changes this from a party trick into a *pipeline*. I did not sit there prompting. Before the session, I wrote every message in advance — the whole ladder. I fired them with my message-queue setup and left the house.

**VO:** Two mechanisms made that safe. First — each big ask was set as a **/goal**: a session-scoped stop-hook. The agent literally cannot stop responding until the goal condition is met. No "here's an outline, want me to continue?" — the hook keeps it producing until the twenty files exist, until the book is written, until the polish pass is done.

**VO:** Second — the asks contained their own **verification demands**. "Call me when done" forces a completion signal. The persona checked its own file counts before calling. My total supervision: zero minutes during, one review at the end.

[TEXT: "prepared messages + /goal stop-hooks + completion signals = walk-away distillation"]

---

## ACT 6 — WHAT CAME OUT & THE ECONOMICS (14:00–16:30)

[SCREEN: guided tour — Ten Laws page, the receipts protocol, the escalation clause, the smart index table in the skill]

**VO:** The final inventory, all verified on disk:
- **The book:** ~34 pages, 15,575 words. Sixteen chapters, four appendices, the Ten Laws, five checklists. Chapter titles like "Plan Like a Gambler, Decide Like a Surgeon."
- **The binder:** twenty company volumes — the raw per-culture doctrine.
- **The skill:** `/master_engineering` (alias `/sol`) — every principle as a one-line reminder with an *exact page-and-section reference* into the book, plus a 24-row smart index mapping situations to pages. Load it into any agent — an Opus, a Sonnet — and that agent now *acts* from the distilled judgment, and knows exactly where the deep reasoning lives when it needs more.

**VO:** That's the economics: the frontier model wrote it **once**. The cheap models load it **forever**. The skill is the reflex, the book is the reasoning, the binder is the source — three depths, all cross-referenced. This is distillation without touching a single weight: the knowledge moves through *artifacts*, not gradients.

[TEXT: "Write once at frontier prices. Run forever at commodity prices."]

**VO:** And the wisdom itself is *weirdly good* — better than asking directly, and I've tried both. The delegation chapter's "escalation clause" — *if you're stuck, say so and stop; struggling silently is the only failure I won't forgive* — is now in every prompt I hand to any agent. The book told me how to manage the machines that wrote the book.

---

## ACT 7 — GENERALIZE IT + THE META-SKILL (16:30–19:00)

[SCREEN: the /distilation-roleplay skill firing; two agent panes appearing]

**VO:** None of this is engineering-specific. The recipe is five beats, any domain:

[TEXT: the five beats as cards]
1. **ANCHOR** — build the sparse alternate-reality résumé of the ultimate imaginary master in the domain. Twenty greatest institutions, ranked, three years each. Jobs, roles, projects only.
2. **INDUCE** — the ladder: imagination → consent → confirm/start contract → small talk → interview frame. Always-stay-in-character.
3. **EXTRACT** — the "personal life story" with a schema hidden in angle brackets, then per-institution corpus files with the uniqueness constraint and walk-away autonomy.
4. **SYNTHESIZE** — the ~30-page book with the "bible for newcomers" framing, expansion chapters via chat-then-canonize, and two self-polish passes.
5. **COMPRESS** — the skill: every principle one line, exact page references, situation-based smart index, aliases. The artifact cheaper models will actually load.

**VO:** Marketing? Anchor a CMO who ran the twenty greatest campaigns in history. Security? A career across the twenty most battle-tested response teams. Product, data, film editing, cooking — the priors are in there; the interview gets them out.

**VO:** And because I'm me — the last thing I did was have Claude package this *entire play* as a skill: `/distilation-roleplay`. You give it a domain. It spawns **two agents**: a Director, who plays my role — builds the CV, runs the message ladder, validates checkpoints without micro-reading, and a Persona agent who becomes the master and produces the corpus, the book, and the skills. Fully self-managed, end to end. The technique that distilled the model is now itself distilled.

[BEAT]

**VO:** Which means, yes: the method for extracting mastery from a frontier model… was extracted from a frontier model. It's turtles all the way down, and every turtle writes documentation.

---

## OUTRO (19:00–20:30)

[SCREEN: the Last Page of the book, slow scroll]

**VO:** I'll leave you with the last page of the book, which Sol — who doesn't exist, remember — wrote about his own principles:

[TEXT, read slowly:] *"Every principle in this book was learned by breaking something… That's what 'as if I'd been sitting beside you' actually means: when something cracks, you hear an old voice ask — what does the system permit? what did you delete this week? did you actually run it? — and you already know what to do."*

**VO:** A fictional man's real wisdom, distilled from everything our field ever wrote down, now teaching my agents — and me. The prompts, the message ladder, and the skill are all linked below. Go build your own imaginary master.

[TEXT: end card — "The ladder + skill: link in description · Subscribe for the next experiment"]

**VO:** Subscribe if you want the follow-up — I'm going to run this play on a domain that isn't engineering, and we'll see if the magic holds. See you in the next one. 🌱

---
---

# 📋 PRODUCTION NOTES

**Screen captures needed (in order):**
1. File tree of `~/Creations/Lively/the_senior/` (montage + results tour)
2. `MASTER_ENGINEERING.md` scroll — cover, TOC, Ten Laws, Last Page
3. `senior_cv_init` session — the two prep prompts
4. `CV.md` scroll — header joke, 20 stints, elicitation section
5. Main session scroll — each ladder rung as it fires (can re-create in a viewer; highlight the key phrases)
6. The 20 binder files appearing + `wc -l` output (1,406 total)
7. The Echo callback moment (re-enact: `alexa-say` firing + Echo lighting up)
8. `/goal` being set + the stop-hook notice text
9. `/master_engineering` skill file + it triggering in a *fresh* session on a small model — money shot: Sonnet quoting `[p.9 §5.2]`
10. `/distilation-roleplay` spawning two agents (tmux panes side by side)

**Tone:** amazed-engineer, not hype. Let the artifacts do the bragging; keep receipts on screen (word counts, file trees, timestamps).
**Chapter cards** double as the description chapters (see DESCRIPTION_AND_ASSETS.md).
**Runtime discipline:** Acts 3–4 are the heart; if cutting for time, trim Act 1 and Act 6, never the ladder.
