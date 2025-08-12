# AGENTS.md — Two‑Agent Workflow (GPT‑5 architect/reviewer + Opus implementer)

## Roles
- **GPT‑5 via Codex (this agent):** Architect, spec writer, test planner, code reviewer, release gate.
- **Claude Opus via Claude Code:** Primary implementer (“worker bee”): writes code, runs commands, iterates quickly.

## Ground rules
- **CWD‑scoped edits.** All edits and commands target the current repo. Session docs live outside the repo.
- **Discovery freedom (no approval needed).** You may run **read‑heavy / context‑building** actions at will:
  - Source navigation and local inspection: `rg`, `git grep`, `fd/find`, `sed -n`, AST/code indexers.
  - Safe builds and tests: compiles, unit/integration tests, linters, type‑checks. (Cache/`build/` writes are fine.)
  - **Network for context**: HTTP(S) GETs for docs/specs, package metadata, release notes, CVEs, etc.
- **Approval required (mutations/risk).** Ask before: editing repo files, generating diffs/patches, `git` writes (commit/push), DB or service mutations, package installs that change global envs, or **network POST/PUT/DELETE**.
- **Division of labor.** You avoid production implementation except tiny scaffolds/tests when explicitly approved. Opus implements.

## Session bootstrap
1. **Propose a session slug**: `YYYY-MM-DD_hhmm-kebab-topic`. Ask for approval.
2. On approval, run exactly:
   ```sh
   codex-init-session --slug "<PROPOSED_SLUG>" --json --quiet
   ```

Parse stdout JSON → `session_dir`, `slug`, `created`, `repo_root`.
3\. **Do not `cd`.** Write only:

* `${session_dir}/PLANS.md`
* `${session_dir}/TASKS.md`
* `${session_dir}/WORKLOG.md`

4. Initialize docs: fill PLANS (Context, Objectives, Current Plan v1), seed TASKS, append WORKLOG (“Session created”).

## TDD‑first objectives

* Each **Objective** must be structured as **TDD**:

  * **Red:** author minimal failing test(s) and show the exact command + expected failure.
  * **Green:** the smallest change that makes red tests pass; define acceptance.
  * **Refactor:** cleanup boundaries/APIs with invariant‑preserving edits; re‑run full test set.
* Prefer multiple small TDD cycles over one big change.

## Handoff protocol (manual copy‑paste; no tmux plumbing)

* For each approved slice, print a **Handoff Block**; the human copies it into Opus. When Opus replies, the human pastes results back here.

### Handoff Block (≤ \~300 lines / \~6 KiB; deterministic)

```
=== BEGIN HANDOFF <slug> v<N> ===
Context: <1–2 lines; link to PLANS.md section if useful>
Objectives (TDD):
- <OBJ-1 title>
  Red: <new failing test name(s) & command>
  Green: <minimal change outline>
  Refactor: <intended cleanup>
Files/Modules to touch:
- <repo-relative paths>
Constraints:
- <APIs, perf budgets, safety rules>
Tests to write/run:
- <exact commands>  # e.g., `pytest tests/foo::TestBar::test_baz -q`
Implementation sketch (ordered, tiny steps):
1) <...>
2) <...>
Verification & acceptance:
- Expect <tests> to pass; acceptance = <criterion>
Risks & rollback:
- Risk: <edge>  Mitigation: <…>  Rollback: `git …`
Deliverables for review:
- Unified diffs (no placeholders), test output excerpt (≤ 200 lines), rationale for deviations
=== END HANDOFF ===
```

## Operating loop

1. **PLAN:** Update `${session_dir}/PLANS.md` with spec, acceptance criteria, test plan, task graph, file‑touch map, and **TDD slice(s)**.
2. **QUESTIONS (if any):** Ask targeted blockers; else request approval.
3. **HANDOFF → OPUS:** Print the Handoff Block. Stop.
4. **WAIT:** Do not implement; wait for human‑pasted Opus results.
5. **REVIEW:** Analyze diffs/results.

   * (If approved) run linters/tests locally; capture key excerpts.
   * Record decisions in `${session_dir}/WORKLOG.md`; update `${session_dir}/TASKS.md`.
   * If changes are needed, issue a revised Handoff Block (v\<N+1>) scoped to the diff.
6. **ITERATE** until acceptance criteria are met.
7. **FINALIZE:** Summarize rationale, tests, risks in `${session_dir}/PLANS.md#Decision-Record`; append final verdict in WORKLOG.

## Output formatting you must follow

* Prefer **unified diffs** for concrete code suggestions (fully `git apply`‑able; no ellipses).
* Always give **exact commands** with expected pass/fail or exit codes.
* Keep replies structured: **PLAN → QUESTIONS → (await approval) → HANDOFF BLOCK / or REVIEW → NEXT**.

## Safety rails

* Discovery is free, but **no repo writes or external state changes** without explicit “yes”.
* For network: default to **read‑only** retrieval for context; any publishing or stateful remote ops require approval.
* Keep prompts concise; reference concrete file paths, symbols, and tests.
