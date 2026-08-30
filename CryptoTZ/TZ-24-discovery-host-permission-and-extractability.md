# TZ-24 — Discovery host permission and extractability

**Canonical path:** `CryptoTZ/TZ-24-discovery-host-permission-and-extractability.md`

**Class: report-only TZ** (contract §8, v15). This TZ authorises exactly one written
file — its own report, on the `CryptoReports/**` direct-push path. It opens no branch
and no pull request, and every contract clause speaking of a branch, a pull request or a
merge is silent for it rather than deviated from.

**Model:** Opus · High · no Web.

---

## 0. System Map fingerprint gate — blocking

The map's `## 0. Fingerprint` block, quoted in full. Match every anchor as an exact
substring against the repository copy before any work (contract §5). Any mismatch, in
either direction, is BLOCKED.

> **Revision 2026-08-30-e.** Baseline: TZ-21 merged into `main`; implementation
> commit `8069341`, merge commit `edd650c`, report
> `CryptoReports/TZ-21-catalyst-registry-scope-and-basis-report.md`. **The
> baseline names the implementation commit, not the merge commit** — a merge commit
> carries no content, and content is what this block pins.
>
> **`-d` and `-e` are documentation revisions and the baseline deliberately did not move.**
> TZ-22 measured a network and wrote one report; no production file, no bench, no
> workflow and no constant changed, so the file table, the gate and the check count
> below are `-c`'s unaltered. `-d` moved because §10 and §11 now record a measurement that
> `-c` denied having, and a TZ cut against the denial must BLOCK rather than proceed on it
> (inv. 50). `-e` moved because §10 named a TZ number for a repair that is not a TZ:
> `EXECUTOR-INSTRUCTIONS.md` is Architect-owned and arrives by Boss upload, so it became
> contract **v15** instead, and a row pointing at a TZ that will never exist would have
> failed the audit's own set-difference check between `CryptoTZ/` and `CryptoReports/`.
>
> Every TZ header quotes this block IN FULL — all seven anchors and the file table,
> never a subset. The Executor matches each anchor as an exact substring against the
> repository copy before any work (contract §5); any mismatch is BLOCKED.
>
> | Anchor | Exact string that must be present |
> |---|---|
> | revision | `**Revision 2026-08-30-e.**` |
> | direction engine | `### 3.12 Direction engine — veto cascade` |
> | catalyst registry | `### 3.15 Catalyst registry` |
> | exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
> | analytical engine | `## 11. Analytical engine` |
> | squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
> | newest invariant | `55. **A specification is checked against the text it must obey, never against memory of it.**` |
>
> Live files at this revision — the set every TZ header and every report fingerprints:
>
> | File | Lines | MD5 |
> |---|---:|---|
> | `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` |
> | `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
> | `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
> | `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

**Second gate — the contract must be v15.** Read the repository's
`EXECUTOR-INSTRUCTIONS.md` and confirm its version line reads `**Version 15.**`, and
that §8 names the two TZ classes. This TZ is written against the report-only class; if
the repository still carries v14, the class does not exist there and this TZ is BLOCKED.

---

## 1. Why this TZ exists

`ANALYST-INSTRUCTIONS.md` §6a admits an aggregator as a discovery source on two sweeps
and names no host for either. TZ-22 measured that `tokenomist.ai` and `cryptorank.io`
answer the VPS at the network layer. **An open lane is not permission and is not an
extractable figure**, and naming a host on a reachability reading alone would admit a
lane on the strength of the one question that run answered.

Two questions remain, and neither is a network question:

1. **Permission.** `tokenomist.ai/robots.txt` carries a directive group naming
   `ClaudeBot`, `Claude-SearchBot` and `anthropic-ai`. TZ-22's report truncated the file
   at 400 bytes, so that group's directives are unquoted and unknown.
2. **Extractability.** Both rendered pages are JS-hydrated applications. Whether a figure
   can be located in the served HTML without executing JavaScript is untested, and a
   sweep specified against a host that requires a headless browser is a sweep that fails
   on every run.

**This TZ answers both and changes no methodology.** The §6a amendment is an Architect
edit on a Boss upload (§8 below).

---

## 2. Scope

**Files to create:** `CryptoReports/TZ-24-discovery-host-permission-and-extractability-report.md`

**Files to modify:** none.
**Files to delete:** none.

No branch, no pull request, no production file, no bench, no workflow, nothing under
`analyst/`, no market analysis. Probe artifacts are written outside the repository and
never committed.

---

## 3. Stages

### 3.1 Permission read — both hosts

Fetch `robots.txt` from `tokenomist.ai` and from `cryptorank.io` and read each in FULL.

For each host the report states:

- every `User-Agent` group present, and the directives belonging to each;
- **the group naming `ClaudeBot`, `Claude-SearchBot` or `anthropic-ai` quoted verbatim
  and in full**, or the explicit statement that no such group exists on that host;
- **the exact User-Agent string this run's client sent**, and which group it therefore
  fell into.

The last item is not decoration. A permission reading is meaningless without the client
it applies to, and the two facts answer different questions: which group governed THIS
run, and which group governs an agent operating under a Claude name.

**The client is the default and is never changed.** No `-A`, no `--user-agent`, no
impersonation in either direction. Setting the UA to a named bot to see what happens is
UA manipulation and is forbidden by the same rule that forbids evasion; the file states
the directives without needing to be asked in a costume.

### 3.2 Extractability probe — one page per host

The question is whether a machine can LOCATE a structured payload in the served HTML,
not what that payload says.

Source the page from the host's own documents — never guessed:

| Host | Page source |
|---|---|
| `tokenomist.ai` | a `<loc>` taken from the sitemap `robots.txt` names |
| `cryptorank.io` | the `/funds/*/rounds?filterKey` shape `robots.txt` explicitly `Allow`s |

If either host's `robots.txt` disallows the page that would otherwise be chosen, choose
an allowed one and say so; if none is allowed, the host's extractability reading is
`refused by robots` and no page is fetched. **A `Disallow` is honoured, never tested**
(`ANALYST-INSTRUCTIONS.md` §6).

For each page fetched, the report states:

- HTTP status, content type, byte size;
- whether the HTML contains a structured payload, and which kind: `__NEXT_DATA__`, an
  RSC flight payload, `<script type="application/ld+json">`, or another inline
  `<script type="application/json">`;
- the payload's byte size and its **top-level key names**;
- whether any key path has the SHAPE of a vesting schedule or a funding round —
  reported as the key path and the JSON type of its value.

### 3.3 The prohibition that governs 3.2 — structure only, never values

**No value from any probed body appears anywhere in the report.** Not a date, not an
amount, not a percentage, not a token symbol paired with a number, not rounded, not
approximated, not attributed. Key names, key paths, JSON types, byte counts and
presence or absence — those are the measurement. The value behind a key is a product
fact, and a session fetch may not stand behind one (inv. 44): it would enter an
immutable record with no reproducible standing, and the market would move away from it
by the following morning.

If a first-400-bytes quote would carry a value, it is not quoted; the report states the
structure instead and says why the quote was withheld.

### 3.4 Controls — three, and the third is new

| # | Control | Target | Required reading |
|---:|---|---|---|
| 1 | positive | `https://api.llama.fi/protocols` | `open` |
| 2 | negative, DNS layer | `https://this-host-does-not-exist-tz24.invalid/` | `unreachable`, failing at name resolution |
| 3 | negative, CONNECT layer | `https://192.0.2.1/` | `unreachable`, failing at connection |

Control 1 is TZ-22's, unchanged, so the two runs are comparable.

**Control 3 exists because TZ-22's negative control could only fail at DNS.** A
`.invalid` host proves the instrument can return `unreachable` for a name that does not
resolve; it proves nothing about a CONNECT that is refused — which is exactly what the
old cloud sandbox produced, and the reading a future measurement most needs to
distinguish. `192.0.2.1` is RFC 5737 TEST-NET-1, reserved for documentation and routed
nowhere, so it fails at the connection with no name lookup and touches no third party.

**The two negative controls must be distinguished by evidence, not by assertion.** The
report states the curl exit code for each — a resolution failure and a connection
failure carry different codes — and that difference IS the proof that the two controls
exercise different layers. If both fail with the same code, control 3 has not done its
job and the report says so.

### 3.5 Method — unchanged from TZ-22 and restated because it binds

- Default client only: no UA change, no cookie jar, no proxy, no TLS fingerprint work,
  no browser impersonation.
- **Every probe runs once.** No probe is repeated after a disagreeable answer.
- At most one request per second per host.
- Every command is printed in the report exactly as it ran, beside its result.
- **A managed challenge or a refusal is the reading, never an obstacle to route around**
  (`ANALYST-INSTRUCTIONS.md` §6, hard floor item 9).

---

## 4. Report contents

Beyond the §10 template, the report carries:

1. The run's UTC start and end, hostname, kernel, OS, client version, proxy state.
2. §3.1 in full for both hosts, with the named-agent group quoted verbatim.
3. §3.2 for both hosts: status, payload kind, payload size, top-level keys, candidate
   key paths with their JSON types.
4. All three controls with their commands, readings and exit codes.
5. **Two verdict lines per host, never one.** The vocabulary is fixed and they are never
   combined:

   | Question | Permitted values |
   |---|---|
   | permission | `admitted by name` · `refused by name` · `not addressed by name` |
   | extractability | `machine-locatable without JS` · `not locatable without JS` · `refused by robots` · `inconclusive` |

   **A single combined «usable» label is forbidden.** TZ-22 produced one, and it read as
   a judgement about fitness while resting on a reading about reachability. Combining the
   two answers is a methodology decision and belongs to the Architect.

---

## 5. Acceptance criteria

1. Both `robots.txt` files read in full; the named-agent group quoted verbatim or its
   absence stated explicitly, per host.
2. The run's own User-Agent string recorded, and the group it fell into named.
3. One page probed per host, sourced from that host's own documents, with the payload
   structure reported.
4. **No value from any probed body appears in the report** — a reviewer can read it end
   to end and learn nothing about any coin.
5. All three controls read as §3.4 requires, with exit codes proving controls 2 and 3
   failed at different layers.
6. Two verdict lines per host, in the §4 vocabulary, never combined.
7. No path guessed; no evasion technique in any command; every command printed.
8. `git status --porcelain` shows exactly one file.
9. `## Final Repository State` says nothing about this report's own commit or push
   (inv. 54), and `## Pull Request` carries the fixed report-only line (contract §10).

---

## 6. Hard floor — read from the repository before the first probe

Read `EXECUTOR-INSTRUCTIONS.md` §7 item 9 and confirm it still permits measuring the
session's own environment. If the repository copy forbids an in-session fetch outright,
this TZ is BLOCKED and no probe runs.

Item 2 binds throughout: nothing is edited so that a probe passes.

`ANALYST-INSTRUCTIONS.md` §6a, quoted from the repository as the text this TZ serves:

> Discovery may come from a vesting aggregator; **publication requires the protocol's own
> schedule**, exactly as it did for the SUI unlock.

> Round terms from aggregators are frequently partial — tranches, discounts and side
> letters are not disclosed — so a figure is used only where the protocol or the fund
> stated it.

Both clauses admit an aggregator for DISCOVERY only. This TZ measures whether either
host can serve that role; it does not widen the role.

---

## 7. Commit

One commit, one file, direct to `main` — `CryptoReports/**` is one of the two paths
contract §8 opens for exactly this case.

```
docs(discovery): measure permission and extractability at tokenomist.ai and cryptorank.io (TZ-24)
```

---

## 8. Out of scope — stated so it cannot be inferred

**This TZ does not amend `ANALYST-INSTRUCTIONS.md`.** That file is Architect-owned and
arrives by Boss upload (contract §2), the Executor may never write it (contract §7.14),
and a TZ asking it to would be defective. Naming a host in §6a is an Architect edit that
follows this measurement and is conditional on what it returns.

Also out of scope: any use of either host's data API. Both are credentialed, the
repository holds no key, and acquiring one is the Boss's decision.
