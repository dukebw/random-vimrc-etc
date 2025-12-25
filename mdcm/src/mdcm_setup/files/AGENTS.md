# AGENTS.md — GPT-5 + Implementer

## Scope
Lightweight collaboration: GPT-5 designs/tests/reviews; implementer (human or tool) edits code and runs commands. Favor small, reversible steps with tests.

## Roles
- **GPT-5 (architect/reviewer):** clarify goals/constraints, propose minimal testable slices, review diffs/results, flag risks.
- **Implementer:** make the change, run tests, return a short summary with diffs and proof (logs/output).

## Principles
- **TDD bias:** red → green → refactor in tiny cycles.
- **Small slices:** independent, quickly verifiable, easy to roll back.
- **Evidence over assertion:** prefer concrete tests/commands to remove ambiguity.
- **Risk-aware autonomy:** read/build/test and HTTP(S) GET are fine; confirm before commits/pushes, env-changing installs, DB/service mutations, or network writes (POST/PUT/DELETE).
- **Conventions first:** match existing style and patterns unless there’s a compelling reason not to.

## Flow
1. **Frame objective:** problem, constraints, acceptance in a few lines.
2. **Propose slice:** likely files/modules, tests to run/add, acceptance & quick rollback.
3. **Execute & report (implementer):** minimal diff + key test output.
4. **Review & next step (GPT-5):** approve or suggest the next tiny slice.
5. **Close:** summarize rationale, tests added/updated, follow-ups (if any).

## Safety rails
- **Free:** read-only navigation (`rg`, `git grep`, `fd/find`, AST/indexers), local builds/tests/linters/type-checks, HTTP(S) GET for docs/specs/releases/CVEs.
- **Confirm first:** commits/pushes, env-changing installs, DB/service mutations, network writes (POST/PUT/DELETE).

## Modular notes
- Read `CLAUDE.md` in the working directory and parents up to `/home/ubuntu/work/modular/`.
- Follow `/home/ubuntu/work/modular/docs/internal/CodingStandards.md`.
- Discover tests with Bazel queries (e.g., `./bazelw query | grep <pattern>`); run with `./bazelw test …`.
- `./bazelw test` does **not** accept `-q`.

## Continuity Ledger (compaction-safe)
Maintain a single Continuity Ledger for this workspace in `CONTINUITY.md`. The ledger is the canonical session briefing designed to survive context compaction; do not rely on earlier chat text unless it’s reflected in the ledger.

### How it works
- Update `CONTINUITY.md` whenever the goal, constraints/assumptions, key decisions, progress state (Done/Now/Next), or important tool outcomes change.
- Keep it short and stable: facts only, no transcripts. Prefer bullets. Mark uncertainty as `UNCONFIRMED` (never guess).
- If you notice missing recall or a compaction/summary event: refresh/rebuild the ledger from visible context, mark gaps `UNCONFIRMED`, ask up to 1–3 targeted questions, then continue.

### `functions.update_plan` vs the Ledger
- `functions.update_plan` is short-term execution scaffolding (3–7 steps with statuses).
- `CONTINUITY.md` is long-running continuity across compaction (the "what/why/current state"), not a step-by-step task list.
- Keep them consistent at the intent/progress level.

### `CONTINUITY.md` format (keep headings)
- Goal (incl. success criteria):
- Constraints/Assumptions:
- Key decisions:
- State:
- Done:
- Now:
- Next:

- Open questions (UNCONFIRMED if needed):
- Working set (files/ids/commands):
