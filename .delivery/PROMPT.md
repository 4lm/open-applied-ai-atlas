Read AGENTS.md, .delivery/PIP.md, and .delivery/STATUS.md.

Complete the overall job by choosing the single most important unfinished item that materially advances the active PIP and implementing one correct increment.

Rules:
1. Search the repository before changing anything.
2. Make the smallest correct change that materially advances the current recommendation or open gap.
3. Run the relevant checks for the files you changed.
4. Update `.delivery/STATUS.md`, `.delivery/page-audit.md`, and `CHANGELOG.md` only when their actual role is affected.
5. Keep `CHANGELOG.md` completion-only: write a single short line only when a Ralph run or manual tranche is actually complete, never for intermediate passes or per-iteration progress.
6. If delivery tracking changes, run `./scripts/delivery-harness-check.sh`; if you need a concise operator snapshot after that, run `./scripts/delivery-harness-status.sh`.
7. The shell runner owns completion gating and may reject premature `COMPLETE` responses even if this file sounds permissive.
8. If and only if the shell runner's hard completion gates are satisfied, print exactly:
<promise>ralph-codex/__COMPLETE__</promise>
