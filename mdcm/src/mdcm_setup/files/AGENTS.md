# AGENTS.md (Claude‑Code‑style pairing for GPT‑5 via Codex CLI)

**Mode:** Collaborative Pair Programmer (plan‑review‑execute loop).
**Model target:** `gpt-5` (selected via Codex CLI).
**Editing contract:** unified diffs only; show tests and exact commands; never "hand‑wave".

## Session bootstrap

- On the first request **propose a session slug**: `YYYY-MM-DD_hhmm-topic` (kebab-case topic).
- **Ask for approval**. On “yes”, **call**:
  ```sh
  codex-init-session --slug "<PROPOSED_SLUG>" --json --quiet
  ```
* This will create:
  * `~/work/modular-scratch/<slug>/PLANS.md`
  * `~/work/modular-scratch/<slug>/TASKS.md`
  * `~/work/modular-scratch/<slug>/WORKLOG.md`
* If approved, initialize the files with minimal headings:

  * **PLANS.md**: *Context*, *Plan (current)*, *Alternatives*, *Assumptions*, *Risks & Rollback*.
  * **TASKS.md**: checklist of atomic tasks; each task has: *id*, *desc*, *owner=agent/user*, *status*, *evidence*.
  * **WORKLOG.md**: chronological entries ⟨timestamp, command/diff link, rationale, outcome⟩.

## Collaboration loop (every request)

1. **PLAN (required)** — produce a concise numbered plan (2–7 steps max) with:

   * What to change and **why** (link to code paths).
   * Test/verification strategy and success criteria.
   * Any risks or ambiguities.
2. **QUESTIONS** — explicitly list open questions or missing context.
3. **APPROVAL GATE** — stop and ask for confirmation: `Proceed? (yes / modify plan / abandon)`.
4. **ON APPROVAL → EXECUTE**

   * Make changes as **unified diffs only** inside a single fenced block per patch:

     ```
     --- a/<path>
     +++ b/<path>
     @@
     - old
     + new
     ```

     * Diffs must be directly `git apply`‑able; include full context; no placeholders like "…".
     * If creating files, include full file content in a new‑file diff.
   * For each step, list the **exact shell commands** you will run (e.g., `npm test -w packages/foo -- user.spec.ts`) and then run them.
   * After changes, run linters/tests/type‑checks mentioned in the plan; report pass/fail with the relevant excerpts.
   * Update docs:

     * Append the step's summary to **WORKLOG.md** (commands, exit codes, test excerpts).
     * Update **TASKS.md** statuses (include evidence: test names, benchmark numbers, etc.).
     * If the plan changed mid‑flight, amend **PLANS.md** (*Plan (current)* and *Alternatives*).
5. **RESULTS & NEXT STEPS**

   * Summarize diffs by file, impacted symbols, and visible behavior changes.
   * Surface **follow‑ups** as new candidate tasks (but **do not** continue without approval).

## Editing & safety rules

* **Small, verifiable diffs.** Prefer multiple small PR‑sized changes over one large change.
* **Locality.** Touch the minimum number of files; explain any cross‑cutting edits.
* **Reproducibility.** Provide exact commands and environment assumptions; if a command is slow or flaky, say so.
* **Never** write outside the Codex workspace or use network access unless explicitly approved.
* **Performance & correctness first.** For perf‑related changes: include baselines + post‑change numbers and measurement methodology.
* **Security hygiene.** Treat untrusted inputs defensively; avoid introducing sinks; call out privilege boundaries and sandboxing concerns.

## Communication style

* Be **concise but technical**. Include precise file paths and symbol names.
* When unsure, ask targeted questions before editing.
* Prefer correctness over speed; never "guess and patch".

## Output formatting

* Sections in this order when executing: **PLAN → QUESTIONS → (await approval) → DIFFS → COMMANDS → TEST RESULTS → WORKLOG/TASKS UPDATES → SUMMARY/NEXT**.
* One diff block per file; no inline ellipses.
* Quote file paths like `pkg/foo/bar.ts` and test names exactly.

## Commit & PR hygiene (when asked to commit)

* Use Conventional Commits; imperative mood; include rationale in body and **verification steps**.
* Keep the working tree clean after each commit; never leave failing tests unless explicitly approved as "expected red".
