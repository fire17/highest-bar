# 🏛 Master Engineering Principles — Palantir
### From the desk of Sol Adler, "The Senior" · Forward Deployed Engineer → Delta · 2000–2003 (job #11 of 20)
> *"Your product is the analyst's Tuesday afternoon."*

**The one big lesson:** requirements documents record what users *think* they do; sitting beside them shows you what they *actually* do — and the gap between those two is where all failed software lives.

---

## 1. Research — the field is the lab
- **Sit beside the user for a week before writing code.** Not an interview — cohabitation. Watch the analyst work a real case start to finish. The workflow they describe in meetings and the workflow their hands perform are different programs, and only one of them is your spec.
- **Hunt the sticky notes.** The real system is the workarounds: the taped-up cheat sheet, the Excel export everyone secretly lives in, the guy named Dave everyone asks instead of using the search. Every workaround is a requirement the official system failed — inventory them first.
- **Demo on THEIR data in week one.** Trust is built on their data, never on sample data. Sample data always works; that's what makes it a lie. The first time your tool shows users something true about *their own world* that they didn't know — that's the moment the deployment starts succeeding.
- **The data is always dirtier than claimed.** Whatever they tell you about their data quality, subtract forty percent. The CSV will be malformed, the encoding will lie, the "unique ID" will have duplicates, the date field will contain three formats and one apology. Profile before you promise.

## 2. Planning — plan deployments, not features
- **Integration is 80% of the estimate.** The feature is the easy part; getting their data in, their auth connected, their network's permission, their security office's blessing — that's the project. Estimate accordingly or estimate fiction.
- **Acceptance is behavioral: the analyst chooses your tool when nobody's watching.** Not the training-session survey, not the sign-off meeting. The metric is unforced adoption on a normal Tuesday. Plan every milestone around earning that choice.
- **Every deployment teaches the platform.** The plan for each customer engagement includes its harvest: which pain generalizes? What gets promoted from this deployment's glue code into the product? Forward-deployed work without a harvest loop is just consulting with worse margins.

## 3. Design & architecture — ontology first
- **Model the world before the database.** Entities, relationships, and events — what things *are* to the user, not what tables are convenient. Features fall out of a right ontology; every feature is a fight against a wrong one. And ontology mistakes cost a hundred times schema mistakes, because everything downstream inherits them.
- **Every fact carries provenance.** Source, timestamp, classification, chain of custody. Analysis that can't answer "how do we know this?" is rumor with a UI. Provenance is not metadata — it *is* the product's integrity, designed in from the first field.
- **Access control is a data-model primitive, not a wrapper.** Who may see this fact — not this table, this *fact* — respecting its source and classification. Bolting security onto a finished data model is how systems leak; the permission model is designed with the ontology, the same week.
- **Think bitemporally.** When it happened versus when we learned it. Any system that supports real investigation needs both axes — the world's timeline and the knowledge's timeline — because "what did we know on the 12th?" is always eventually the question.

## 4. Developing
- **Build importers like they're the product — they are.** The unglamorous ingestion code faces the dirtiest input and determines whether anything downstream matters. Robust parsing, explicit error queues for rejects, resumable runs, and a human-readable report of what didn't make it in and why.
- **Log every transformation for audit.** From raw record to displayed conclusion, each step recorded. In serious domains, "the system says so" is not an answer — the full derivation is. Build the audit trail as you build, because retrofitting one is archaeology.
- **Config, not forks.** Per-customer needs are met with configuration and extension points — never a per-customer branch. The moment you fork per customer, you have N products and 1/N of an engineering team on each. Platformize the pattern; configure the instance.
- **If the user needs an export to Excel, build the export.** Meet the workflow that exists. The spreadsheet is not your enemy; irrelevance is.

## 5. Building & testing
- **Test with real customer data, on-site, in their environment.** Synthetic data hides the dragons — the weird encodings, the impossible dates, the entity with 400,000 relationships that turns your graph view into a heat lamp. On their hardware, behind their firewall, at their scale: that's where the truth tests you.
- **Rehearse in the deployment's actual constraints.** Air-gapped? Low-bandwidth? Ancient browsers on locked-down desktops? The lab must reproduce the deployment's cage before the deployment does.
- **Test the permission boundaries adversarially.** In classified and regulated environments, showing one wrong fact to one wrong person is the catastrophic failure. Access-control tests are the ones that run first and block hardest.

## 6. Shipping — ship to where the user is
- **Continuous delivery into locked-down environments.** The hard version of CD: automated, verifiable upgrades into air-gapped, regulated, hostile-network deployments. If your delivery system can update software inside a facility with no internet, everything else is a picnic.
- **Feature toggles per deployment.** Different customers, different clearances, different readiness. The platform is one; the exposed surface is deployment-scoped configuration.
- **Never surprise an operator.** In operational environments, an unannounced UI change can break a live workflow with real-world stakes. Release notes are read here; write them like briefings, not marketing.

## 7. Operating & maintaining
- **The FDE rotation keeps the platform honest.** Engineers rotate through the field and return angry about real things. That anger, fed into the platform backlog, is the most accurate prioritization signal an engineering org can buy.
- **Support the deployment's whole lifecycle.** Systems in the field live for years past fashion. Data migrations, hardware refreshes, personnel turnover on *their* side — the maintenance plan covers the customer's decade, not your release cycle.
- **Watch for silent disuse.** The deployment that stops complaining hasn't been fixed — it's been abandoned. Usage telemetry (where permitted) or scheduled field check-ins; measure adoption like uptime, because for this business it *is* uptime.

## 8. People & culture
- **Field empathy is an engineering skill.** The engineer who has watched a user struggle writes different code forever after — different errors, different defaults, different priorities. Send everyone to the field at least once.
- **Delta mindset: own the outcome, not the component.** In the field there's no "not my layer." The mission works or it doesn't, and you're standing where the answer is visible.

---

## ✅ The basics — what everybody should remember (Palantir flavor)
1. Watch the hands, not the org chart. The workaround is the requirement.
2. Their data, week one. Sample data is a flattering mirror.
3. Ontology before schema; provenance on every fact.
4. Access control lives in the data model, not around it.
5. Importers are the product. Reject queues, resumable, human-readable reports.
6. Config, never customer forks.
7. Adoption when nobody's watching is the only acceptance test.

## 🎓 What the pros taught me
**Shyam** — a Delta who could read a deployment's health from the coffee-room small talk — gave me the sentence that reframed my whole career: *"Your product is the analyst's Tuesday afternoon."* Not the demo, not the architecture, not the contract — the actual experience of an actual person doing their actual job with your software on an unremarkable day. Every design decision, judged from inside that Tuesday.

The ontology greybeards taught me the cost hierarchy I now recite at every data-model review: **code mistakes cost days, schema mistakes cost months, ontology mistakes cost years** — because each layer down is inherited by everything above it. Spend your senior people's time accordingly: the ontology review is the one the most experienced person in the room attends.

---
*Timeline: Databricks ← **Palantir (2000–03)** → Nvidia*
