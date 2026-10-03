# Implementation Report — TZ-58

## Status

**BLOCKED at A0. The session did not run on the VPS.** `hostname` returned `vm`, not `vultr`. The three other A0 checks gave answers other than the known ones (below). TZ-58 §7 A0 says: «Any other answer: BLOCKED. The session writes a report carrying A0's lines and its own `hostname`, commits it to `main`, and does nothing else — no gate, no branch, no reading». This report is that report.

1. **The fit: not read.** No `fits` line was written. The host's answer is none.
2. **The model: not read.** `run.py` keeps `--model opus`. No `--effort` was added.
3. **`crypto-announce.service`: not listed.** C1 did not run.
4. **The list reader: not built.** A3 and C2 did not run, so there is no baseline line.

**What unblocks it:** `EXECUTE TZ-58` sent to a Claude Code session running on the VPS (host `vultr`). TZ-52 to TZ-56 ran in sessions like that.

## Inbound Filing

None. `CryptoTZ/TZ-58-vps-fit-model-stream-list.md` is at its canonical path on `origin/main`, in one copy (575 lines, MD5 `d5eecb82b6fd9fe2178e969c39b55f25`). It was found with contract §3's search after `git fetch --all --prune`.

## Scope Executed

**Class: branch TZ** (contract §8). The scope names files under `vps/`, which is outside `CryptoReports/**`. **No branch was opened.** A0 stops before any branch (TZ-58 §7 A0), so the clauses that need a branch or a pull request have nothing to apply to here.

Steps run, in order:

- Contract §4a steps 1–4: the contract was read, `git fetch --all --prune` was run, the TZ was located and read in full.
- **A0:** run as the first stage of the TZ, before the §5 gate. All four checks gave answers other than the known ones, so the TZ stopped there.

| Stage | Executed | Outcome |
|---|---|---|
| A0 | yes | **BLOCKED**: four of four answers differ from the known answers |
| A1 (§4a steps 5–6, §5 gate, merge check, deploy lines) | no | stopped by A0 |
| A2, A3, A4 | no | stopped by A0 |
| B1, B2, B3 | no | stopped by A0 |
| C1, C2 | no | stopped by A0 |
| E1–E4 | no | stopped by A0 |
| V1–V11 | no | stopped by A0 |

**A0 — the commands and their full output**, from this session's shell. The reading instant came from `date -u +%FT%TZ`: `2026-10-03T19:42:59Z`.

```
$ hostname
vm
exit=0
$ systemctl is-active crypto-bot.service crypto-exchange.service
System has not been booted with systemd as init system (PID 1). Can't operate.
Failed to connect to bus: Host is down
exit=1
$ test -d /srv/crypto-auto/.git && echo clone
exit=1
$ id -u cryptorun
id: 'cryptorun': no such user
exit=1
```

| Check | Known answer (TZ-58 §7 A0) | Read | Match |
|---|---|---|---|
| `hostname` | `vultr` | `vm` | no |
| `systemctl is-active crypto-bot.service crypto-exchange.service` | `active` twice | no systemd: `System has not been booted with systemd as init system (PID 1)` | no |
| `test -d /srv/crypto-auto/.git && echo clone` | `clone` | nothing printed, exit 1 | no |
| `id -u cryptorun` | a number (995 in TZ-56) | `no such user`, exit 1 | no |

**This session's own `hostname`: `vm`.**

## Files Created

None. This report is the session's only written file.

## Files Modified

None.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

No implementation was done. A0 stopped the TZ before Stage B.

## Validation

None of V1–V11 was run. Each is stopped by A0, which (per TZ-58 §7 A0) means no gate, no branch and no reading. Under contract §9 an item that cannot be run fails. All eleven are therefore **failed, not executed**, and all for the same reason: this session is not on the VPS.

## Test Results

None run.

## Deviations

- **D-1. `## Fingerprints` has content even though no gate ran.** Contract §10 makes that section mandatory in every report. It holds line counts and MD5s of files at `origin/main` (`075de0e`). They are measurements of the checkout. They are not the §5 gate: no anchor was compared, and nothing was decided on them.
- **D-2. One fact was seen before A0.** It came from the `git log` read while locating the TZ (§4a steps 2–3). `origin/main`'s first-parent line holds `075de0e Merge pull request #46 from seahomebatumi-ai/claude/vibrant-albattani-ddmwh1`, and that merge's second parent is `895d1dc`. A1.1's `git merge-base --is-ancestor` check was **not** run.

## Pre-existing Issues

None looked for. A0 forbids any further reading.

## Remaining Risks

- **This is the second TZ in a row whose host stages could not run.** TZ-57's session also ran in a cloud container (`hostname` → `vm`) and recorded every host stage as BLOCKED. Until a session runs on the VPS, these all stay unread and unbuilt:
  - the fit (`fits`, `budget_bytes`, the run unit's `MemorySwapMax=` and `RuntimeMaxSec=`);
  - the model pin;
  - the stream listing;
  - the list reader.
- The product's runs since TZ-56's install are recorded in the VPS's journal, so a later reading can still class them. Whether that journal keeps them until such a reading happens was not checked.

## Commit

Report, direct to `main` on the `CryptoReports/**` path (contract §8), message from TZ-58 §14:

```
TZ-58: report — on the VPS: the fit, the model, the stream and the list
```

Contents: `CryptoReports/TZ-58-vps-fit-model-stream-list-report.md` only. No implementation commit exists.

## Pull Request

None. A0 stopped the TZ before any branch (TZ-58 §7 A0: «no gate, no branch»), so there is no implementation to propose.

## CI Execution

None. No branch was pushed. This report is a `**.md` path: it is excluded by `bench.yml`'s `paths-ignore` (`'**.md'`) and it is not on `main.yml`'s `paths` allow-list. Before the push, that allow-list was read and is exactly `main.py` and `.github/workflows/main.yml`.

## Final Repository State

The checkout this report was written against is `origin/main` at `075de0ec6704cc976390a9901b0a73b8cff2aaed`. The working tree was clean (`git status --porcelain` empty) before this report was added. This session started no unit, wrote no file outside this report, and touched no host.

## Fingerprints

These are measurements at `origin/main` (`075de0e`), taken with `git show origin/main:<file> | wc -l` and `| md5sum`. They are **not** the §5 gate (D-1).

| File | Lines | MD5 | TZ-58 §0 states |
|---|---:|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 3193 | `b5a4478afd3afebd24c4ec12897514dc` | 3193 · `b5a4478afd3afebd24c4ec12897514dc` |
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | 3799 · `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | 518 · `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | 17 · `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | 175 · `3b8730b254467c9df4c0a845a0f3cfb3` |
| `EXECUTOR-INSTRUCTIONS.md` | 991 | `d7bd23785656896a119e0cb7f0fddad5` | 991 · `d7bd23785656896a119e0cb7f0fddad5` |
| `ANALYST-INSTRUCTIONS.md` | 3921 | `7f19dc64a596ee07ad8298ee2a59c8a4` | 3921 · `7f19dc64a596ee07ad8298ee2a59c8a4` |

Version and revision lines (`grep -n -m1 -F`):

- The map, line 17: `**Revision 2026-10-03-d.**`
- `EXECUTOR-INSTRUCTIONS.md`, line 3: `**Version 26.**`
- `ANALYST-INSTRUCTIONS.md`, line 4: `**Revision 2026-10-03-a.**`

**Anchors: not compared.** §5 step 2 was not run, because A0 comes before the gate. No anchor text, and no row count of the map's anchor table, is recorded here.
