# Changelog

This file is a completion-only root ledger. Active operator context belongs in the durable root docs and explicitly referenced `pips/` artifacts, not here.

| Date | Completed Outcome |
| --- | --- |
| 2026-04-19 | Tightened Ralph's default unattended sandbox posture to `workspace-write`, added opt-in `dangerously-unrestricted` profile mode, and documented the resulting access model in the repo. |
| 2026-04-19 | Added tracked Ralph example prompt/profile fixtures, established explicit PIP status frontmatter, and closed the non-`docs/` repo consistency gaps captured in `GAP_FIX_PROPOSALS.md`. |
| 2026-04-19 | Hardened `scripts/ralph-codex.py` so the documented direct CLI entrypoint is executable, app-server failures surface as bounded errors instead of hangs, and completion rejection state is persisted consistently with the live controller state. |
| 2026-04-19 | Replaced the shell-era Ralph loop with a plan-aware `scripts/ralph-codex.py` app-server controller, added stdlib unittest coverage, and removed shell-era Ralph references and artifact naming. |
| 2026-04-19 | Kept `pips/PIP_001.md` as the live PIP board and aligned the repo's root guidance and completion ledger around that live-plan posture. |
| 2026-04-18 | Hardened `scripts/ralph-codex.sh` into a shell-gated Ralph loop that overrides prompt completion policy and refuses premature completion without hard verification. |
| 2026-04-18 | Simplified delivery tracking by moving the repository-wide audit snapshot into `.delivery/STATUS.md`, removing the duplicate root audit-summary file, and keeping `CHANGELOG.md` as a completion-only ledger. |
| 2026-04-17 | Initial repository implementation for Open Applied AI Atlas, including root governance docs, taxonomy foundation, topic corpus, and cleanup discipline. |
