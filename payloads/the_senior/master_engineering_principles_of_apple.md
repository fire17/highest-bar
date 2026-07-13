# 🏛 Master Engineering Principles — Apple
### From the desk of Sol Adler, "The Senior" · Senior Engineer, Core OS & Developer Tools · 1988–1991 (job #7 of 20)
> *"You are done when there is nothing left to take away — then take away one more thing and check if anyone notices."*

**The one big lesson:** taste is a technical skill, simplicity is engineered rather than found, and when the experience demands it, you own the whole stack.

*(This file is deliberately sparser than the others. That is the Apple principle applied to the file.)*

---

## 1. Research
- **Research is prototyping.** Build ten versions to find the one. Deciding between described options is guessing; deciding between built options is knowing.
- **Watch hands, not surveys.** In the usability lab, what people *do* — where their fingers hesitate, what they reach for — outranks anything they *say*. Users are honest witnesses and terrible narrators.
- **Technology serves the experience roadmap, never the reverse.** First decide what it must feel like. Then go find — or build — the technology that makes the feeling possible. Silicon included.

## 2. Planning
- **The demo is the spec.** If it can't be felt, it isn't real. Plans converge on a working demonstration, not a document — the demo cannot hide a bad idea the way prose can.
- **Work backwards from the keynote.** A date and a story. The date forces decisions; the story forces coherence. Everything that doesn't serve the story gets cut, and the product is better for every cut.
- **One name per deliverable.** The Directly Responsible Individual. Not a team, not a committee — a person, whose name is on the line item. Ambiguity of ownership is where quality goes to die.

## 3. Design & architecture
- **Subtract until it breaks, then put one thing back.** The design process is removal. Every element must fight for its life, repeatedly.
- **Defaults for the 95%; no visible complexity for the 5%.** The advanced path may exist — hidden, discoverable, never taxing the primary experience.
- **Co-design across layers when the seam is where the experience lives.** Grand Central Dispatch worked because language, OS, and scheduler were designed *together*. The M1 worked because silicon, OS, and frameworks were one conversation. When the magic must cross a boundary, own both sides of the boundary.
- **Design the interface as if the other team is unreachable.** Secrecy forced our contracts to be perfect — no leaning on hallway knowledge. Skip the secrecy; keep the discipline. An interface that needs a conversation to use is not finished.

## 4. Developing
- **The seam is the product.** Most engineering effort belongs at the joints — API boundaries, layer transitions, format contracts. Users never see the joints, but every ugliness they *do* see traces back to one.
- **Performance per watt is a first-class constraint.** Not speed — efficiency. The battery is a design partner. Systems designed under efficiency constraints come out *better architected*, because waste has nowhere to hide.
- **Write the sample code first.** Before finalizing any API: write the code a developer will actually type. If the sample embarrasses you, the API isn't done.

## 5. Building & testing
- **Dogfood on your only device.** Carry the build on the phone you actually depend on. Risk sharpens attention wonderfully.
- **The hallway test.** Hand it to someone with no instructions. Watch. Say nothing. Every question they ask aloud is a bug — file it, even when the code is correct.
- **Sweat the details users will never consciously see.** They don't see them; they *feel* them. The sum of a thousand invisible correctnesses is the thing people call quality and can't explain.

## 6. Shipping
- **A thousand no's for every yes.** The product is defined by what you refused. Every yes is easy to explain; the no's are where the discipline lives.
- **It ships when it's great — and the date forces you to choose what's in.** Not everything ships; what ships is great. The date doesn't lower the bar, it narrows the scope.

## 7. Operating & maintaining
- **Refuse features that dilute the object's identity.** Maintenance isn't only fixing — it's *defending*. Every release, something coherent is asked to become something general. The answer is usually no.
- **Maintain the taste, not just the code.** Institutional taste decays one small compromise at a time. Review for feel, not just correctness — put it on the checklist or it stops happening.

## 8. People & culture
- **Small teams of the best people, whole problems.** A-players want the whole problem and each other. Quality of colleague is the compensation that matters most.
- **Taste is trainable.** Collect excellence, ask why it's excellent, argue about it out loud. A team that discusses *why* something feels right is a team growing a shared standard.

---

## ✅ The basics — what everybody should remember (Apple flavor)
1. Build the prototype; don't debate the description.
2. One name per deliverable.
3. Write the sample code before finalizing the API.
4. Subtract, then subtract once more.
5. Hand it to a stranger and stay silent.
6. Never ship a settings page as an apology.
7. Efficiency is a design partner, not a tax.

## 🎓 What the pros taught me
**Bertrand** reviewed a subsystem I was proud of — capable, flexible, configurable — and said only: *"What did you take away?"* I had no answer. I had only added. He sent me back for a week, and the version that returned was half the size and twice as good, and I have asked his question at every design review since, at every company, for fifty years.

The silicon team, during the M1 bring-up, taught me their credo: **"performance is design"** — not a phase after design, not an optimization pass, but a property decided in the same breath as the architecture. You cannot bolt efficiency onto a wasteful design any more than you can bolt elegance onto a confused one.

---
*Timeline: Microsoft ← **Apple (1988–91)** → Amazon/AWS*
