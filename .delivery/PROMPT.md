Read AGENTS.md, .delivery/PIP.md, and .delivery/STATUS.md.

Complete the overall job by choosing the single most important unfinished item that materially advances the active PIP and implementing one correct increment.

Rules:
1. Search the repository before changing anything.
2. Make the smallest correct change that materially advances the current recommendation or open gap.
3. Run the relevant checks for the files you changed.
4. Update `.delivery/STATUS.md`, `.delivery/page-audit.md`, `CONTENT_AUDIT_SUMMARY.md`, and `CHANGELOG.md` only when their actual role is affected.
5. If delivery tracking changes, run `./scripts/delivery-harness-check.sh`; if you need a concise operator snapshot after that, run `./scripts/delivery-harness-status.sh`.
6. If the whole job is complete, print exactly:
<promise>COMPLETE</promise>
