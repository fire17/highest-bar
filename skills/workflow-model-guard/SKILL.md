---
name: workflow-model-guard
description: MANDATORY pre-flight + post-author guard for ANY Workflow/agent spawning — forbids Fable-model subagents; requires explicit model on every agent() call, a model-verification pass, and a big-banner compliance announcement (models + effort levels) BEFORE launch. Load this BEFORE authoring or opening any workflow.
---

# workflow-model-guard — NEVER spawn Fable subagents

**Load and follow this skill BEFORE authoring, opening, resuming, or launching ANY
Workflow script — and apply the same rule to Agent-tool spawns.** (User directive
2026-07-03; standing Tokenomics doctrine.)

## The rule

Subagents must be **Opus 4.8 or below** — NEVER model Fable.

| Tier | Use for |
|---|---|
| `opus` @ high (default) | workhorse: build, validate, review |
| `opus` @ xhigh | design-critical / hardest verify-judge lanes |
| `sonnet` | classic (non-tmux) helper subagents under an opus parent — ≤3 per opus, context only from the opus, opus verifies everything (see `/pyramid`) |
| `haiku` @ xhigh | atomic logistics, cheap mechanical stages |
| **Fable — FORBIDDEN** | never, in any spawn path |

## Why omission is the trap

The **main session may itself run Fable** (`/model fable`). Both spawn paths
**inherit the main-loop model when no model is given**:
- Workflow scripts: `agent(prompt, opts)` with no `opts.model` → inherits → **Fable**.
- Agent tool: no `model` param → inherits → **Fable**.

So an *implicit* model is a violation even if it "usually" resolved to Opus before.

## Procedure (all steps MANDATORY)

**1. While authoring** — every single `agent()` call in the script (and every
Agent-tool spawn) sets an explicit `model: 'opus'` or `model: 'haiku'`. Set
`effort` deliberately (`'low'|'medium'|'high'|'xhigh'`); if omitted it inherits the
session effort — note that in the banner.

**2. VERIFY after creating the workflow (before launch)** — mechanically check,
don't trust memory of what you wrote:
```bash
# every agent( must carry an explicit non-fable model; any hit here = violation
grep -n "agent(" <script> | grep -v "model"        # → must be EMPTY (naked spawns)
grep -ni "fable" <script>                          # → must be EMPTY
```
For `workflow()` sub-calls, verify the child script too. For `agentType` custom
agents, confirm the agent definition's model frontmatter is not Fable.
If ANY check fails → **fix the script first; never launch-then-fix.**

**3. ANNOUNCE with a big banner** — after verification and before/at launch, print:

```
╔══════════════════════════════════════════════════════════════╗
║  ✅ WORKFLOW MODEL GUARD — ALL SUBAGENTS OPUS OR BELOW        ║
║  No Fable subagents. Verified by grep, not assumption.       ║
║  <lane/label> → opus @ high                                   ║
║  <lane/label> → opus @ xhigh                                  ║
║  <lane/label> → haiku @ xhigh                                 ║
╚══════════════════════════════════════════════════════════════╝
```
List every lane/stage with its model **and effort level** (say "effort: inherited
(<session effort>)" when not explicitly set).

**4. Zenith runtime workers** — NOT model-pinned (verified vs disk 2026-07-03:
`~/Creations/.mcp.json` carries no `ANTHROPIC_MODEL`; the checkout only
env-forwards it if present). Zenith workers inherit the host env's model — so when
touching Zenith config or spawning drivers for it, always set an explicit allowed
model (`model: "opus"`); never assume a pin protects you.

**5. Resumes count too** — `resumeFromRunId` re-runs live agents under the CURRENT
session model for any call lacking an explicit model. Re-verify (step 2) before
every resume, not just first launch.
