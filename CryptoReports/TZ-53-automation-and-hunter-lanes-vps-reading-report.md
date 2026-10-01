# Implementation Report — TZ-53

## Status

**COMPLETED.** Report-only TZ. Stages A–E ran from this session's own machine on 01.10.2026:
the local reads from 08:02:39Z, the B6 unit from 08:03:47Z to 08:03:54Z, and **41 requests, one
per URL, strictly sequential, all in rule 1's form**, from 08:06:55Z to 08:08:11Z. Every stage
attempted at least one read and every request was answered with an HTTP status (V3). **V1** printed
4, 0 and 1. **V5**: 8 of 8 known answers match and no host changed. On the iShares row the as-of
date read is one day later than the Architect's. V2, V4, V6 and V7 pass. Nothing was built,
installed, enabled or admitted.

- **A** — The payload is `ts` 2026-09-30T22:14:24+04:00, `src` `fapi`, `n` 31. `c` holds 31 rows
  of 9 keys. `x` holds 787 rows, and every row carries `x[0]`'s 16 keys. The session runs as
  `root` (uid 0), with `CLAUDECODE` set, in harness worktree
  `/root/crypto-auto/.claude/worktrees/bridge-cse_01D6P1U4thNUnBuHuwmJe2eS`.
- **B** — Ubuntu 24.04.4 LTS on kernel 6.8.0-136-generic, `systemd-detect-virt` `microsoft`,
  PID 1 `systemd`, up since 2026-08-02 07:24:32. It has 1 CPU and 955 MB of memory, of which 74 MB
  was available, plus 3 099 MB of swap; the disk shows 30G with 12G free. The clock is Etc/UTC,
  NTP-synchronised. The hosting lookup reads `AS20473 The Constant Company, LLC`. systemd 255
  reports `running` and `cron` is `active`; root's `crontab -l` exits 1 with 0 lines.
  The toolchain is Python 3.12.3, node v22.23.1, npm 10.9.8, git 2.43.0, jq 1.7, gh 2.45.0
  (`gh auth status` exit 0), `tmux` and `/usr/bin/claude` 2.1.282. The credentials file is present
  and `ANTHROPIC_API_KEY` is unset. `origin` is an SSH remote and no credential helper is set.
  **B6: one transient system unit ran the probe in 7.000 s, and `systemd-run` exited 0.** All four
  `.rc` files read 0. The headless run returned `result` equal to `HEADLESS-OK` exactly, with
  `is_error` false, `num_turns` 1 and `duration_ms` 2792. Six of the seven named options occur in
  `--help`; `--max-turns` does not. The dry-run push authenticated
  (`To github.com:seahomebatumi-ai/crypto-auto.git`), and no `tz-53-*` ref exists on the remote.
- **C** — All eleven `fapi` and `api` reads answered 200. The clock skew is −127 ms. The 24-hour
  ticker's 788-row key set is **equal** to `x[0]`'s. `premiumIndex` carries `markPrice` and
  `lastFundingRate`. **`exchangeInfo` carries both dates:** 15 symbols have an `onboardDate` in the
  seven days before the read, and 3 trading perpetuals carry a `deliveryDate` of 2026-10-05. On the
  announcement site, the list API is `refused on permission` (`Disallow: */bapi/`) while
  `/sitemap_output/` is allowed. The English child sitemap's 4 973 URLs all carry **one**
  `lastmod`, 2026-09-30T00:00:00+00:00, 32.12 h older than the read. The first announcement page
  answered **405 with `x-amzn-waf-action: captcha`**.
- **D** — `api.telegram.org/` answered 302 to `https://core.telegram.org/bots`. `getMe` on an
  invalid token answered 401 with the expected body, byte for byte.
- **E** — FRED answered 4 of 4 CSVs (last observations 2026-09-23 ×3, 2026-09-30). The FOMC
  calendar lists **8** meetings under «2026 FOMC Meetings», and H.4.1's release date is
  September 24, 2026. Fiscal Data's newest `record_date` is 2026-09-29. DefiLlama listed 429
  `peggedAssets` and a chart to 2026-10-01T00:00:00Z. **iShares** IBIT and ETHA both carry the datum, as of
  Sep 30, 2026, and **Bitwise** carries it with «Data as of 09/29/2026». **Grayscale** answered
  429 with a Vercel Security Checkpoint, on its robots.txt too. **Farside** answered 403 with
  `cf-mitigated: challenge` and no `<table`. Coinbase answered 2 of 2, with body times 0.37 s and
  0.69 s before the read.

The previous TZ, TZ-52, was report-only: its report commit is `435c441` on `main`, and it had no
branch to merge.

---

## Inbound Filing

`CryptoTZ/TZ-53-automation-and-hunter-lanes-vps-reading.md` arrived under its canonical name in the
Boss's upload commit `97c8372`, the only commit touching a `*TZ-53*` path on any ref:

```
$ git log --all --format='%h' --name-only -- '*TZ-53*' '*TZ 53*' '*TZ_53*' | sort --unique

97c8372
CryptoTZ/TZ-53-automation-and-hunter-lanes-vps-reading.md
[exit 0]
```

(The empty first line is `--name-only`'s separator, sorted first.) Nothing was moved or renamed.

---

## Scope Executed

**Class: report-only TZ** (contract §8). The TZ's `## Scope` names one written file, this report,
on the `CryptoReports/**` direct-push path. Its Files to Modify and Files to Delete are both
`none`.

Run order under contract §4a:

1. Contract v23 was read in full: 864 lines, MD5 `02abb1969626d2af150a0d1f6e02f2a7`.
2. `git fetch origin main` showed the harness worktree at `424d79a`, behind `origin/main` at
   `97c8372`. `git merge --ff-only origin/main` brought it there with no merge commit.
   `git rev-parse --is-shallow-repository` printed `false`, `git fetch --all --prune` exited 0,
   `git rev-parse HEAD origin/main` printed `97c837275ea578d7ff6d20ef8348172b0dd2692d` twice, and
   `git status --porcelain` printed nothing.
3. The TZ was found in `CryptoTZ/` on `origin/main` and read in full.
4. **The fingerprint gate (contract v23 §5) passed.** The anchor list was cut from the map's own
   table by its structure. The table carries 7 rows and 7 were compared. All 7 appear in the TZ
   header as identical rows, and all 7 are exact substrings of the map. The evidence block is
   under `## Fingerprints`.
5. The seven blockquotes under «Contract text this TZ obeys» were checked against their sources,
   whitespace-normalised, because the sources wrap their lines. **All 7 are verbatim**, each
   inside the section it names:

```
$ python3 - <<'PY'
import re
tz = open('CryptoTZ/TZ-53-automation-and-hunter-lanes-vps-reading.md').read()
sec = tz.split('## Contract text this TZ obeys')[1].split('\n## Scope')[0]
quotes = [' '.join(l[2:] for l in b.strip().split('\n')) for b in re.findall(r'((?:^> .*\n?)+)', sec, re.M)]
norm = lambda s: re.sub(r'\s+', ' ', s).strip()
srcs = ('EXECUTOR-INSTRUCTIONS.md', 'SYSTEM-MAP-CRYPTOCALCUL.md', 'ANALYST-INSTRUCTIONS.md')
for q in quotes:
    where = []
    for f in srcs:
        raw = open(f).read()
        if norm(q) in norm(raw):
            line = next(n + 1 for n, l in enumerate(raw.split('\n')) if norm(q)[:40] in norm(l))
            head = [l for l in raw.split('\n')[:line] if re.match(r'#{2,3} ', l)][-1]
            where.append('%s:%d (under "%s")' % (f, line, head[:60]))
    print('%-50s -> %s' % (norm(q)[:50], '; '.join(where) or 'NOT FOUND'))
print('quotes: %d; found verbatim (whitespace-normalised): %d' % (len(quotes), sum(1 for q in quotes if any(norm(q) in norm(open(f).read()) for f in srcs))))
PY
**Never commit secrets.** Credentials live only in -> EXECUTOR-INSTRUCTIONS.md:501 (under "## 7. Hard floor — binding regardless of what a TZ says")
7. The client-side password is decoration. Secrets -> SYSTEM-MAP-CRYPTOCALCUL.md:2057 (under "## 4. Invariants — DO NOT BREAK")
**Measuring the session's own environment is a DIF -> EXECUTOR-INSTRUCTIONS.md:518 (under "## 7. Hard floor — binding regardless of what a TZ says")
**Permitted in a session** — measuring the session -> SYSTEM-MAP-CRYPTOCALCUL.md:2094 (under "## 4. Invariants — DO NOT BREAK")
A **report-only TZ** authorises exactly one writte -> EXECUTOR-INSTRUCTIONS.md:631 (under "## 8. GitHub rules")
**The command is part of the channel.** A host ans -> ANALYST-INSTRUCTIONS.md:2450 (under "### 6a. The supply scan — mandatory, cached, never re-derive")
**TZ-54 waits on one floor edit** (inv. 59): contr -> SYSTEM-MAP-CRYPTOCALCUL.md:2817 (under "## 10. Open queue and gates")
quotes: 7; found verbatim (whitespace-normalised): 7
[exit 0]
```

6. Repository state: `git log --oneline --graph --all` runs to 833 lines. No `tz-52` or `tz-53`
   branch exists on any ref. `main.yml` is still a `paths` allow-list of exactly `main.py` and
   `.github/workflows/main.yml`, read before the first push as contract §8 requires (block under
   `## CI Execution`).
7. Stages A–E ran, then V1–V7.

**Not done, because the scope forbids it.** Nothing was written under `analyst/`, to
`catalysts.json`, or to any production, bench, workflow or contract file. Nothing was installed,
enabled or configured: no package, service, timer, crontab line or git setting. No branch, ref or
remote was created; the dry-run push and V6 prove the remote has no `tz-53-*` ref. No credential
file's content was read. **`claude` was never run inside this session**; it ran only inside the
B6 unit. No date, figure or event read here entered any file except this report.

**Network traffic, all of it:**
- the 41 `curl` reads of B2–E, listed under `### Reading ledger`;
- inside the B6 unit, the headless `claude` call and the dry-run push over SSH to `github.com`;
- `git fetch` and `git merge --ff-only` against this repository's own remote;
- two `git ls-remote origin 'refs/heads/tz-53-*'` reads, one after B6 and one in V6.

No request was retried, and no user-agent, header, proxy or cookie was set.

---

## Files Created

- `CryptoReports/TZ-53-automation-and-hunter-lanes-vps-reading-report.md` — this report.

## Files Modified

None.

## Files Renamed

None.

## Files Deleted

None.

---

## Implementation Summary

### Instrument

Everything lived in `/tmp/tz53/`, outside the repository, and V7 removed it.

- **`mask.sed`, `leak.re`, `fixture.txt` and `unit/probe.sh`** were not typed. They were cut by
  code from the TZ's own fenced blocks, and they compare byte for byte with those blocks
  (block below the list).
- **`run.sh`** holds the local-read helper. It prints `$ <command>`, the combined output and
  `[exit N]`, all piped through `mask.sed`. Every local block below was produced by it.
- **`probe.py`** (622 lines, MD5 `9ce3c167ab5898cd9500f233cc05ab4c`) holds the network layer:
  - `fetch()` runs rule 1's form as an argv list, so no shell parses a URL taken from a page.
  - A URL already in the append-only ledger is returned from the ledger and never requested
    again.
  - One process at a time ran it, so reads were sequential.
  - Consecutive reads to one host stood at least 1 s apart: FRED's own `Crawl-delay: 1`, applied
    to every host as a courtesy.
  - `robots.txt` follows RFC 9309. The product token `curl` falls back to `*`. The longest match
    wins and `Allow` wins a tie. A 4xx file imposes no restriction, as rule 3 states, and a 5xx or
    unreachable file is a complete disallow.
  - Every body and header dump was kept. With `TZ53_OFFLINE=1`, any URL not already in the ledger
    aborts the run.
- **`extra.py`**, **`v34.py`**, **`selftest.py`** and **`blocks.py`** are offline. They read saved
  bodies or the ledger, and make no request.
- **`report.py`** fills this report's blocks from the saved outputs and runs the local re-runnable
  commands it quotes. It makes no request apart from V6's `git ls-remote`.

The four dictated scratch files against the TZ's blocks:

```
$ python3 /tmp/tz53/blocks.py
TZ code block 1 of 5 vs /tmp/tz53/mask.sed: identical
TZ code block 2 of 5 vs /tmp/tz53/unit/probe.sh: identical
TZ code block 4 of 5 vs /tmp/tz53/leak.re: identical
TZ code block 5 of 5 vs /tmp/tz53/fixture.txt: identical
[exit 0]
```

The robots decision was tested offline before any external request:

```
$ python3 /tmp/tz53/selftest.py
/bapi/composite/v1/public/cms/article/list/query     expected False got False PASS
/bapi/fe/x                                           expected True  got True  PASS
/sitemap_output/                                     expected True  got True  PASS
/en/private                                          expected False got False PASS
/en/private2                                         expected True  got True  PASS
/x/                                                  expected True  got True  PASS
/robots.txt                                          expected True  got True  PASS
/en/bapi/                                            expected False got False PASS
governing group *; 8 of 8 PASS
[exit 0]
```

**The client** (local reads, taken when this report was generated):

```
$ curl --version | head --lines=1
curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13 zlib/1.3 brotli/1.1.0 zstd/1.5.5 libidn2/2.3.7 libpsl/0.21.2 (+libidn2/2.3.7) libssh/0.10.6/openssl/zlib nghttp2/1.59.0 librtmp/2.3 OpenLDAP/2.6.10
[exit 0]
$ env | grep --ignore-case --count --extended-regexp '^(https?_proxy|no_proxy|all_proxy)='
0
[exit 1]
$ ls ~/.curlrc /etc/curlrc
ls: cannot access '/root/.curlrc': No such file or directory
ls: cannot access '/etc/curlrc': No such file or directory
[exit 2]
```

So no `curlrc` and no proxy variable alter rule 1's client.

### Stage A — Baseline

| Item | Reading |
|---|---|
| A1 | contract §4a steps 1–6 done (Scope Executed); §5 gate passed, 7 table rows, 7 compared; 4 of 4 map files and 2 of 2 contract files match (`## Fingerprints`) |
| A2 top-level keys | `c`, `n`, `src`, `ts`, `x` |
| A2 `ts` · `src` · `n` | `2026-09-30T22:14:24+04:00` · `fapi` · `31` |
| A2 `c` | length 31; key set of `c[0]` `chg`, `fr`, `h`, `l`, `mark`, `oi`, `p`, `qv`, `s`; 31 of 31 rows carry exactly it |
| A2 `x` | length 787; key set of `x[0]`, 16 keys (below); 787 of 787 rows carry exactly it |
| A3 user | `root`, uid `0` |
| A3 `CLAUDECODE` | set |
| A3 toplevel | `/root/crypto-auto/.claude/worktrees/bridge-cse_01D6P1U4thNUnBuHuwmJe2eS` |

```
## A2
$ date -u '+%Y-%m-%dT%H:%M:%SZ'
2026-10-01T08:02:49Z
[exit 0]
$ python3 -c 'import json; d=json.load(open("analyst/live.json")); c=d["c"]; x=d["x"]; print("top-level keys:", sorted(d)); print("ts:", d["ts"]); print("src:", d["src"]); print("n:", d["n"]); print("c: len", len(c), "| key set of c[0]:", sorted(c[0]), "| rows with that key set:", sum(sorted(r) == sorted(c[0]) for r in c)); print("x: len", len(x), "| key set of x[0] (" + str(len(x[0])) + " keys):", sorted(x[0]), "| rows with that key set:", sum(sorted(r) == sorted(x[0]) for r in x))'
top-level keys: ['c', 'n', 'src', 'ts', 'x']
ts: 2026-09-30T22:14:24+04:00
src: fapi
n: 31
c: len 31 | key set of c[0]: ['chg', 'fr', 'h', 'l', 'mark', 'oi', 'p', 'qv', 's'] | rows with that key set: 31
x: len 787 | key set of x[0] (16 keys): ['closeTime', 'count', 'firstId', 'highPrice', 'lastId', 'lastPrice', 'lastQty', 'lowPrice', 'openPrice', 'openTime', 'priceChange', 'priceChangePercent', 'quoteVolume', 'symbol', 'volume', 'weightedAvgPrice'] | rows with that key set: 787
[exit 0]
## A3
$ id -un
root
[exit 0]
$ id -u
0
[exit 0]
$ [ -n "${CLAUDECODE+x}" ] && echo "CLAUDECODE: set" || echo "CLAUDECODE: unset"
CLAUDECODE: set
[exit 0]
$ git rev-parse --show-toplevel
/root/crypto-auto/.claude/worktrees/bridge-cse_01D6P1U4thNUnBuHuwmJe2eS
[exit 0]
```

### Stage B — The machine and its scheduler

| Item | Reading |
|---|---|
| B1 OS · kernel | Ubuntu 24.04.4 LTS · 6.8.0-136-generic |
| B1 `systemd-detect-virt` | `microsoft`, exit 0 |
| B1 PID 1 · up since | `systemd` · 2026-08-02 07:24:32 |
| B1 CPUs · memory | 1 · total 955 MB, available 74 MB; swap total 3 099 MB (1 543 MB in use) |
| B1 `/` | 30G size, 12G available |
| B1 clock | `Timezone=Etc/UTC`, `NTPSynchronized=yes` |
| B2 hosting (ipinfo `/org`) | `AS20473 The Constant Company, LLC` — the address was never requested |
| B3 oldest reflog entry of A3's checkout | `424d79a HEAD@{2026-10-01 07:59:30 +0000}` |
| B3 `.git` of A3's checkout | a **regular file** (a worktree pointer), born and modified 2026-10-01 07:59:30 |
| B3 (extra) common git directory | `/root/crypto-auto/.git`, a directory born 2026-08-29 19:37:14; oldest reflog entry `clone: from https://github.com/seahomebatumi-ai/crypto-auto.git` at 2026-08-29 19:37:15; 68 worktrees registered |
| B4 `systemctl --version` | `systemd 255 (255.4-1ubuntu8.17)` |
| B4 `is-system-running` | `running`, exit 0 |
| B4 user-manager reads | not run: A3's user is root (uid 0), and the TZ asks them for a non-root user only |
| B4 `is-active cron` | `active`, exit 0 |
| B4 `crontab -l` | exit 1; 0 non-empty, non-comment lines (lines never printed) |
| B5 toolchain | Python 3.12.3 · node v22.23.1 · npm 10.9.8 · git 2.43.0 · jq-1.7 · gh 2.45.0 · tmux `/usr/bin/tmux` |
| B5 `claude` | `command -v` → `/usr/bin/claude`, a symlink to a 238 767 288-byte x86-64 ELF executable (extra read); `~/.local/bin/claude` and `/usr/local/bin/claude` absent |
| B5 `gh auth status` | exit 0 |
| B5 `~/.claude/.credentials.json` | present (content not read) |
| B5 `ANTHROPIC_API_KEY` | unset |
| B5 `origin` | `git@github.com:seahomebatumi-ai/crypto-auto.git` (SSH, nothing to mask) |
| B5 `credential.helper` | none set (exit 1, empty) |
| B6 `systemd-run` | exit 0; `Finished with result: success`; runtime 7.000 s; CPU 1.512 s; `Memory peak: 512.0K` |
| B6 `.rc` | version 0 · help 0 · headless 0 · push 0 |
| B6 `version.out` | `2.1.282 (Claude Code)` |
| B6 options in `help.out` | `--output-format` yes · `--permission-mode` yes · `--allowedTools` yes · **`--max-turns` no** · `--append-system-prompt` yes · `--mcp-config` yes · `--dangerously-skip-permissions` yes |
| B6 `headless.json` | an object of 25 keys (below); `is_error` false; `num_turns` 1; `duration_ms` 2792; `result` equals `HEADLESS-OK` exactly: **true** |
| B6 `push.err` line 1 | `To github.com:seahomebatumi-ai/crypto-auto.git` |
| B6 afterwards | `tz53-*` units 0; remote `refs/heads/tz-53-*` none |

```
## B1
$ grep '^PRETTY_NAME=' /etc/os-release
PRETTY_NAME="Ubuntu 24.04.4 LTS"
[exit 0]
$ uname -r
6.8.0-136-generic
[exit 0]
$ systemd-detect-virt; echo "exit $?"
microsoft
exit 0
[exit 0]
$ cat /proc/1/comm
systemd
[exit 0]
$ uptime -s
2026-08-02 07:24:32
[exit 0]
$ nproc
1
[exit 0]
$ free -m
               total        used        free      shared  buff/cache   available
Mem:             955         881          77           0         139          74
Swap:           3099        1543        1556
[exit 0]
$ df -h --output=size,avail,target /
 Size Avail Mounted on
  30G   12G /
[exit 0]
$ timedatectl show -p Timezone -p NTPSynchronized
Timezone=Etc/UTC
NTPSynchronized=yes
[exit 0]
## B3
$ git reflog --date=iso | tail -1
424d79a HEAD@{2026-10-01 07:59:30 +0000}: 
[exit 0]
$ stat -c '%w | %y' .git
2026-10-01 07:59:30.963130269 +0000 | 2026-10-01 07:59:30.963130269 +0000
[exit 0]
$ stat -c '%F' .git
regular file
[exit 0]
## B4
$ systemctl --version | head -1
systemd 255 (255.4-1ubuntu8.17)
[exit 0]
$ systemctl is-system-running; echo "exit $?"
running
exit 0
[exit 0]
$ systemctl is-active cron; echo "exit $?"
active
exit 0
[exit 0]
$ crontab -l >/tmp/tz53/crontab.txt 2>/tmp/tz53/crontab.err; echo "exit $?"; echo "non-empty, non-comment lines: $(grep -cvE '^[[:space:]]*(#|$)' /tmp/tz53/crontab.txt)"
exit 1
non-empty, non-comment lines: 0
[exit 0]
```

B2 is a network read and its line is in the Stage C log below, which starts with it.

```
## B3 (extra: the common git directory this worktree shares)
$ git rev-parse --git-common-dir
/root/crypto-auto/.git
[exit 0]
$ git -C /root/crypto-auto reflog --date=iso | tail -1
de62002 HEAD@{2026-08-29 19:37:15 +0000}: clone: from https://github.com/seahomebatumi-ai/crypto-auto.git
[exit 0]
$ stat -c '%F | %w | %y' /root/crypto-auto/.git
directory | 2026-08-29 19:37:14.070108104 +0000 | 2026-09-30 18:42:37.851895468 +0000
[exit 0]
$ git worktree list | wc -l
68
[exit 0]
## B5
$ python3 --version
Python 3.12.3
[exit 0]
$ node --version
v22.23.1
[exit 0]
$ npm --version
10.9.8
[exit 0]
$ git --version
git version 2.43.0
[exit 0]
$ jq --version
jq-1.7
[exit 0]
$ gh --version | head -1
gh version 2.45.0 (2025-07-18 Ubuntu 2.45.0-1ubuntu0.3)
[exit 0]
$ command -v tmux
/usr/bin/tmux
[exit 0]
$ command -v claude
/usr/bin/claude
[exit 0]
$ for p in ~/.local/bin/claude /usr/local/bin/claude /usr/bin/claude; do [ -e "$p" ] && echo "$p: exists" || echo "$p: absent"; done
/root/.local/bin/claude: absent
/usr/local/bin/claude: absent
/usr/bin/claude: exists
[exit 0]
$ gh auth status >/dev/null 2>&1; echo "exit $?"
exit 0
[exit 0]
$ [ -e "$HOME/.claude/.credentials.json" ] && echo "credentials.json: present" || echo "credentials.json: absent"
credentials.json: present
[exit 0]
$ [ -n "${ANTHROPIC_API_KEY+x}" ] && echo "ANTHROPIC_API_KEY: set" || echo "ANTHROPIC_API_KEY: unset"
ANTHROPIC_API_KEY: unset
[exit 0]
$ git remote get-url origin
git@github.com:seahomebatumi-ai/crypto-auto.git
[exit 0]
$ git config --get credential.helper
[exit 1]
```

```
## B5 (extra: what the binary is)
$ ls -l /usr/bin/claude
lrwxrwxrwx 1 root root 60 Sep 24 21:21 /usr/bin/claude -> ../lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe
[exit 0]
$ readlink -f /usr/bin/claude
/usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe
[exit 0]
$ file -L /usr/bin/claude | cut -c1-160
/usr/bin/claude: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[
[exit 0]
$ stat -L -c '%s bytes' /usr/bin/claude
238767288 bytes
[exit 0]
```

**B6, the unit.** `probe.sh` is byte-identical to the TZ's block (Instrument). Starting it
required the execute bit, which `chmod +x` set on that scratch file. The `--setenv` values were
expanded from this session: `HOME` and `PATH` from its environment, `CLAUDE_BIN` from B5, and
`REPO` from A3.

```
## B6 (before)
$ systemctl list-units --all 'tz53-*' --no-legend | wc -l
0
[exit 0]
$ stat -c '%y' ~/.claude.json
2026-10-01 07:59:32.442142261 +0000
[exit 0]
$ ls ~/.claude/projects | wc -l
74
[exit 0]
$ ls -d ~/.claude/projects/-tmp-tz53-unit 2>&1
ls: cannot access '/root/.claude/projects/-tmp-tz53-unit': No such file or directory
[exit 2]
$ chmod +x /tmp/tz53/unit/probe.sh && stat -c '%A %n' /tmp/tz53/unit/probe.sh
-rwxr-xr-x /tmp/tz53/unit/probe.sh
[exit 0]
```

```
## B6 (unit)
$ date -u "+%Y-%m-%dT%H:%M:%SZ"
2026-10-01T08:03:47Z
[exit 0]
$ timeout 330 systemd-run --unit=tz53-probe --wait --collect --property=RuntimeMaxSec=300 --setenv=HOME="$HOME" --setenv=PATH="$PATH" --setenv=CLAUDE_BIN="/usr/bin/claude" --setenv=REPO="/root/crypto-auto/.claude/worktrees/bridge-cse_01D6P1U4thNUnBuHuwmJe2eS" /tmp/tz53/unit/probe.sh; echo "systemd-run exit $?"
Running as unit: tz53-probe.service; invocation ID: 1627a9896bb14da894eaa01c412fb295
Finished with result: success
Main processes terminated with: code=exited/status=0
Service runtime: 7.000s
CPU time consumed: 1.512s
Memory peak: 512.0K
Memory swap peak: 0B
systemd-run exit 0
[exit 0]
$ date -u "+%Y-%m-%dT%H:%M:%SZ"
2026-10-01T08:03:54Z
[exit 0]
```

```
## B6 (readings)
$ cd /tmp/tz53/unit && for f in version help headless push; do echo "$f.rc: $(cat $f.rc)"; done
version.rc: 0
help.rc: 0
headless.rc: 0
push.rc: 0
[exit 0]
$ cat /tmp/tz53/unit/version.out
2.1.282 (Claude Code)
[exit 0]
$ cd /tmp/tz53/unit && for o in --output-format --permission-mode --allowedTools --max-turns --append-system-prompt --mcp-config --dangerously-skip-permissions; do printf "%s: %s\n" "$o" "$(grep -c -- "$o" help.out)"; done
--output-format: 5
--permission-mode: 1
--allowedTools: 1
--max-turns: 0
--append-system-prompt: 3
--mcp-config: 3
--dangerously-skip-permissions: 1
[exit 0]
$ python3 -c "import json; d=json.load(open(\"/tmp/tz53/unit/headless.json\")); print(\"type:\", type(d).__name__); print(\"key set:\", sorted(d)); print(\"is_error:\", d.get(\"is_error\")); print(\"num_turns:\", d.get(\"num_turns\")); print(\"duration_ms:\", d.get(\"duration_ms\")); print(\"result == HEADLESS-OK exactly:\", d.get(\"result\") == \"HEADLESS-OK\")"
type: dict
key set: ['api_error_status', 'duration_api_ms', 'duration_ms', 'fast_mode_disabled_reason', 'fast_mode_state', 'first_content_frame_ms', 'is_error', 'modelUsage', 'num_turns', 'permission_denials', 'queued_turn_count', 'result', 'result_index', 'session_id', 'stop_reason', 'subagent_stats', 'subtype', 'terminal_reason', 'time_to_request_ms', 'total_cost_usd', 'ttft_ms', 'ttft_stream_ms', 'type', 'usage', 'uuid']
is_error: False
num_turns: 1
duration_ms: 2792
result == HEADLESS-OK exactly: True
[exit 0]
$ head -1 /tmp/tz53/unit/push.err
To github.com:seahomebatumi-ai/crypto-auto.git
[exit 0]
$ cd /tmp/tz53/unit && wc -c version.err help.err headless.err push.out
0 version.err
0 help.err
0 headless.err
0 push.out
0 total
[exit 0]
```

```
## B6 (readings, extra)
$ cd /tmp/tz53/unit && for o in --output-format --permission-mode --allowedTools --max-turns --append-system-prompt --mcp-config --dangerously-skip-permissions; do printf "%s: %s\n" "$o" "$(grep -cE -- "(^|[[:space:],])${o}([[:space:],=<]|\$)" help.out)"; done
--output-format: 5
--permission-mode: 1
--allowedTools: 1
--max-turns: 0
--append-system-prompt: 2
--mcp-config: 3
--dangerously-skip-permissions: 1
[exit 0]
$ cat /tmp/tz53/unit/push.err
To github.com:seahomebatumi-ai/crypto-auto.git
 * [new branch]      HEAD -> tz-53-push-probe
[exit 0]
## B6 (after)
$ systemctl list-units --all 'tz53-*' --no-legend | wc -l
0
[exit 0]
$ git ls-remote origin 'refs/heads/tz-53-*'
[exit 0]
$ stat -c '%y' ~/.claude.json
2026-10-01 08:03:48.791332667 +0000
[exit 0]
$ ls ~/.claude/projects | wc -l
75
[exit 0]
$ ls ~/.claude/projects/-tmp-tz53-unit | wc -l; du -sb ~/.claude/projects/-tmp-tz53-unit
2
180846	/root/.claude/projects/-tmp-tz53-unit
[exit 0]
```

```
## B6 (extra: what the unit's memory figure measures)
$ stat -fc %T /sys/fs/cgroup
cgroup2fs
[exit 0]
$ systemctl show --property=DefaultMemoryAccounting
DefaultMemoryAccounting=yes
[exit 0]
$ systemctl --version | grep -o 'default-hierarchy=[a-z]*'
default-hierarchy=unified
[exit 0]
```

The second option count matches whole options only. It differs from the TZ's plain occurrence
count only on `--append-system-prompt`, 3 lines against 2, because one line carries a longer
option starting with the same text. The B6-extra block shows that memory accounting was on for
the unit (cgroup v2, `DefaultMemoryAccounting=yes`), so `Memory peak: 512.0K` is printed as
systemd reported it. It is not offered as the headless run's footprint (`## Remaining Risks`).

### Stage C — Binance: the payload and the listing state

| Reading | Result |
|---|---|
| C1 ping · time | 200 `{}` · 200, key set `serverTime`; skew = serverTime − local epoch ms at return = **−127 ms** |
| C2 `ticker/24hr` | 200, 292 784 bytes, 788 rows, 16 keys on all 788; **equal** to A2's `x[0]` key set |
| C3 `premiumIndex` | 200, 923 rows, 8 keys on all 923; `markPrice` yes, `lastFundingRate` yes |
| C4 `openInterest` | 200, key set `openInterest`, `symbol`, `time` |
| C5 `exchangeInfo` | 200, 1 142 974 bytes, **920 symbols**; contractType PERPETUAL 703 · TRADIFI_PERPETUAL 213 · CURRENT_QUARTER 2 · NEXT_QUARTER 2; status TRADING 788 · SETTLING 131 · PENDING_TRADING 1 |
| C5 PERPETUAL `deliveryDate`, five most frequent | 2100-12-25 ×569 · 2026-03-24 ×6 · 2025-04-14 ×5 · 2026-02-06 ×4 · 2026-05-19 ×4 (68 distinct values) |
| C5 `onboardDate` in the 7 days before the read | **15** symbols, listed in the log |
| C5 (extra) PERPETUAL `deliveryDate` after the read and not 2100-12-25 | **3**, all 2026-10-05, all TRADING: `1000000BOBUSDT`, `PROMPTUSDT`, `PUMPBTCUSDT`; 131 rows dated before the read, all SETTLING |
| C6 positioning | 4 of 4 answered 200 with 2 rows; key sets in the log |
| C7 spot ping | 200 |
| C8 `robots.txt` | 200; governing group `*`, 28 rule lines, 15 `Sitemap` lines |
| C8 `/bapi/composite/v1/public/cms/article/list/query` | **disallowed** — matching `Allow: /` and `Disallow: */bapi/`, deciding `Disallow: */bapi/` → `refused on permission`, not requested |
| C8 `/sitemap_output/` | **allowed** — deciding `Allow: */sitemap_output/` |
| C8 index | 200, 13 536 bytes, 75 children, one ending `_en_0.xml` |
| C8 English child | 200, 754 121 bytes; **4 973 URLs, 4 973 with `lastmod`, 1 distinct value, 1 distinct date**; newest `2026-09-30T00:00:00+00:00`, **32.12 h** before the read |
| C8 first `/support/announcement/` `<loc>` | **405**, 2 225 bytes, `text/html; charset=UTF-8` — `x-amzn-waf-action: captcha`, title «Human Verification» |

```
=== B2
READ r01 [B2] curl -sS -L -m 20 -o /tmp/tz53/body/r01 -D /tmp/tz53/hdr/r01 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://ipinfo.io/org'
     -> 200 34 text/html; charset=utf-8 https://ipinfo.io/org | curl exit 0 | hops 200 | 2026-10-01T08:06:55Z .. 2026-10-01T08:06:56Z (0.19 s)
B2 body line: AS20473 The Constant Company, LLC
COUNT [B2] attempted 1, answered 1
=== C1
READ r02 [C1] curl -sS -L -m 20 -o /tmp/tz53/body/r02 -D /tmp/tz53/hdr/r02 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/ping'
     -> 200 2 application/json https://fapi.binance.com/fapi/v1/ping | curl exit 0 | hops 200 | 2026-10-01T08:06:56Z .. 2026-10-01T08:06:56Z (0.28 s)
C1 ping body: {}
READ r03 [C1] curl -sS -L -m 20 -o /tmp/tz53/body/r03 -D /tmp/tz53/hdr/r03 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/time'
     -> 200 28 application/json https://fapi.binance.com/fapi/v1/time | curl exit 0 | hops 200 | 2026-10-01T08:06:57Z .. 2026-10-01T08:06:57Z (0.28 s)
C1 time: key set ['serverTime']; serverTime 1790842017511; local epoch ms at return 1790842017638; skew serverTime - local = -127 ms
COUNT [C1] attempted 2, answered 2
=== C2
READ r04 [C2] curl -sS -L -m 20 -o /tmp/tz53/body/r04 -D /tmp/tz53/hdr/r04 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/ticker/24hr'
     -> 200 292784 application/json https://fapi.binance.com/fapi/v1/ticker/24hr | curl exit 0 | hops 200 | 2026-10-01T08:06:58Z .. 2026-10-01T08:06:58Z (0.28 s)
C2 rows 788; row key set (16 keys, 788 rows carry exactly it): ['closeTime', 'count', 'firstId', 'highPrice', 'lastId', 'lastPrice', 'lastQty', 'lowPrice', 'openPrice', 'openTime', 'priceChange', 'priceChangePercent', 'quoteVolume', 'symbol', 'volume', 'weightedAvgPrice']
C2 row key set vs A2 x[0] key set: equal
COUNT [C2] attempted 1, answered 1
=== C3
READ r05 [C3] curl -sS -L -m 20 -o /tmp/tz53/body/r05 -D /tmp/tz53/hdr/r05 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/premiumIndex'
     -> 200 204789 application/json https://fapi.binance.com/fapi/v1/premiumIndex | curl exit 0 | hops 200 | 2026-10-01T08:07:00Z .. 2026-10-01T08:07:00Z (0.29 s)
C3 rows 923; row key set (8 keys, 923 rows carry exactly it): ['estimatedSettlePrice', 'indexPrice', 'interestRate', 'lastFundingRate', 'markPrice', 'nextFundingTime', 'symbol', 'time']
C3 markPrice among keys: True; lastFundingRate among keys: True
COUNT [C3] attempted 1, answered 1
=== C4
READ r06 [C4] curl -sS -L -m 20 -o /tmp/tz53/body/r06 -D /tmp/tz53/hdr/r06 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT'
     -> 200 68 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT | curl exit 0 | hops 200 | 2026-10-01T08:07:01Z .. 2026-10-01T08:07:01Z (0.28 s)
C4 key set: ['openInterest', 'symbol', 'time']
COUNT [C4] attempted 1, answered 1
=== C5
READ r07 [C5] curl -sS -L -m 20 -o /tmp/tz53/body/r07 -D /tmp/tz53/hdr/r07 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/exchangeInfo'
     -> 200 1142974 application/json https://fapi.binance.com/fapi/v1/exchangeInfo | curl exit 0 | hops 200 | 2026-10-01T08:07:02Z .. 2026-10-01T08:07:03Z (0.40 s)
C5 top-level key set: ['assets', 'exchangeFilters', 'futuresType', 'rateLimits', 'serverTime', 'symbols', 'timezone']
C5 symbols 920; per contractType {'PERPETUAL': 703, 'TRADIFI_PERPETUAL': 213, 'CURRENT_QUARTER': 2, 'NEXT_QUARTER': 2}; per status {'TRADING': 788, 'SETTLING': 131, 'PENDING_TRADING': 1}
C5 PERPETUAL rows 703; distinct deliveryDate values 68; five most frequent (ISO UTC date, count): [('2100-12-25', 569), ('2026-03-24', 6), ('2025-04-14', 5), ('2026-02-06', 4), ('2026-05-19', 4)]
C5 onboardDate within the 7 days before the read (2026-09-24T08:07:03Z .. 2026-10-01T08:07:03Z): 15 symbol(s): [('2026-09-25T08:00Z', 'BTCUSDT_270326'), ('2026-09-25T08:00Z', 'ETHUSDT_270326'), ('2026-09-28T09:00Z', 'OKLOUSDT'), ('2026-09-28T09:05Z', 'TWSTUSDT'), ('2026-09-28T09:10Z', 'CVNAUSDT'), ('2026-09-28T09:15Z', 'RUMUSDT'), ('2026-09-28T09:20Z', 'XOMUSDT'), ('2026-09-29T09:00Z', 'CRMLUSDT'), ('2026-09-29T09:05Z', 'BWETUSDT'), ('2026-09-29T09:10Z', 'ACNUSDT'), ('2026-09-29T09:15Z', 'MPUSDT'), ('2026-09-29T09:20Z', 'SECZUSDT'), ('2026-09-29T09:25Z', 'UNHUSDT'), ('2026-09-29T09:30Z', 'NKEUSDT'), ('2026-10-01T07:45Z', 'CTUSDT')]
COUNT [C5] attempted 1, answered 1
=== C6
READ r08 [C6] curl -sS -L -m 20 -o /tmp/tz53/body/r08 -D /tmp/tz53/hdr/r08 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/futures/data/topLongShortPositionRatio?symbol=BTCUSDT&period=1h&limit=2'
     -> 200 241 application/json;charset=UTF-8 https://fapi.binance.com/futures/data/topLongShortPositionRatio?symbol=BTCUSDT&period=1h&limit=2 | curl exit 0 | hops 200 | 2026-10-01T08:07:04Z .. 2026-10-01T08:07:04Z (0.29 s)
C6 topLongShortPositionRatio: status 200; rows 2; key set ['longAccount', 'longShortRatio', 'shortAccount', 'symbol', 'timestamp']
READ r09 [C6] curl -sS -L -m 20 -o /tmp/tz53/body/r09 -D /tmp/tz53/hdr/r09 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=BTCUSDT&period=1h&limit=2'
     -> 200 241 application/json;charset=UTF-8 https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=BTCUSDT&period=1h&limit=2 | curl exit 0 | hops 200 | 2026-10-01T08:07:05Z .. 2026-10-01T08:07:05Z (0.28 s)
C6 globalLongShortAccountRatio: status 200; rows 2; key set ['longAccount', 'longShortRatio', 'shortAccount', 'symbol', 'timestamp']
READ r10 [C6] curl -sS -L -m 20 -o /tmp/tz53/body/r10 -D /tmp/tz53/hdr/r10 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/futures/data/takerlongshortRatio?symbol=BTCUSDT&period=1h&limit=2'
     -> 200 191 application/json;charset=UTF-8 https://fapi.binance.com/futures/data/takerlongshortRatio?symbol=BTCUSDT&period=1h&limit=2 | curl exit 0 | hops 200 | 2026-10-01T08:07:06Z .. 2026-10-01T08:07:07Z (0.29 s)
C6 takerlongshortRatio: status 200; rows 2; key set ['buySellRatio', 'buyVol', 'sellVol', 'timestamp']
READ r11 [C6] curl -sS -L -m 20 -o /tmp/tz53/body/r11 -D /tmp/tz53/hdr/r11 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=2'
     -> 200 341 application/json;charset=UTF-8 https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=2 | curl exit 0 | hops 200 | 2026-10-01T08:07:08Z .. 2026-10-01T08:07:08Z (0.28 s)
C6 openInterestHist: status 200; rows 2; key set ['CMCCirculatingSupply', 'sumOpenInterest', 'sumOpenInterestValue', 'symbol', 'timestamp']
COUNT [C6] attempted 4, answered 4
=== C7
READ r12 [C7] curl -sS -L -m 20 -o /tmp/tz53/body/r12 -D /tmp/tz53/hdr/r12 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.binance.com/api/v3/ping'
     -> 200 2 application/json;charset=UTF-8 https://api.binance.com/api/v3/ping | curl exit 0 | hops 200 | 2026-10-01T08:07:08Z .. 2026-10-01T08:07:08Z (0.28 s)
C7 status 200; body {}
COUNT [C7] attempted 1, answered 1
```

```
=== C8
READ r13 [C8] curl -sS -L -m 20 -o /tmp/tz53/body/r13 -D /tmp/tz53/hdr/r13 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/robots.txt'
     -> 200 6722 text/plain; charset=UTF-8 https://www.binance.com/robots.txt | curl exit 0 | hops 200 | 2026-10-01T08:07:15Z .. 2026-10-01T08:07:15Z (0.28 s)
     robots https://www.binance.com: parsed: 3 group(s); governing group *; 28 rule line(s); 15 Sitemap line(s)
     robots decision for /bapi/composite/v1/public/cms/article/list/query (group *, from r13): DISALLOWED; matching lines: ['Allow: /', 'Disallow: */bapi/']; deciding line: Disallow: */bapi/
     robots decision for /sitemap_output/ (group *, from r13): allowed; matching lines: ['Allow: /', 'Allow: */sitemap_output/']; deciding line: Allow: */sitemap_output/
C8 robots.txt Sitemap lines: 15
C8 Sitemap lines ending sitemap_SupportAndAnnouncement_index.xml: ['https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_index.xml']
     robots decision for /sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_index.xml (group *, from r13): allowed; matching lines: ['Allow: /', 'Allow: */sitemap_output/']; deciding line: Allow: */sitemap_output/
READ r14 [C8] curl -sS -L -m 20 -o /tmp/tz53/body/r14 -D /tmp/tz53/hdr/r14 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_index.xml'
     -> 200 13536 application/xml https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_index.xml | curl exit 0 | hops 200 | 2026-10-01T08:07:16Z .. 2026-10-01T08:07:17Z (0.78 s)
C8 index: 75 child sitemap(s); children ending _en_0.xml: ['https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_en_0.xml']
     robots decision for /sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_en_0.xml (group *, from r13): allowed; matching lines: ['Allow: /', 'Allow: */sitemap_output/']; deciding line: Allow: */sitemap_output/
READ r15 [C8] curl -sS -L -m 20 -o /tmp/tz53/body/r15 -D /tmp/tz53/hdr/r15 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_en_0.xml'
     -> 200 754121 application/xml https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_en_0.xml | curl exit 0 | hops 200 | 2026-10-01T08:07:18Z .. 2026-10-01T08:07:18Z (0.07 s)
C8 child: URLs 4973; URLs with lastmod 4973; distinct lastmod values 1; distinct lastmod dates (UTC day) 1; unparsed lastmod 0
C8 child: newest lastmod 2026-09-30T00:00:00+00:00; hours between it and the read (2026-10-01T08:07:18Z): 32.12
C8 child: oldest lastmod date 2026-09-30; newest lastmod date 2026-09-30
C8 child: <loc> values containing /support/announcement/: 4971; the first: https://www.binance.com/en/support/announcement/detail/0001cb4538b2445581d4e5c35bfbd63a
     robots decision for /en/support/announcement/detail/0001cb4538b2445581d4e5c35bfbd63a (group *, from r13): allowed; matching lines: ['Allow: /']; deciding line: Allow: /
READ r16 [C8] curl -sS -L -m 20 -o /tmp/tz53/body/r16 -D /tmp/tz53/hdr/r16 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/en/support/announcement/detail/0001cb4538b2445581d4e5c35bfbd63a'
     -> 405 2225 text/html; charset=UTF-8 https://www.binance.com/en/support/announcement/detail/0001cb4538b2445581d4e5c35bfbd63a | curl exit 0 | hops 405 | 2026-10-01T08:07:19Z .. 2026-10-01T08:07:19Z (0.04 s)
C8 announcement page: status 405; bytes 2225; content type text/html; charset=UTF-8
COUNT [C8] attempted 4, answered 4
```

The C8 page's refusal, as served:

```
$ grep --ignore-case --extended-regexp '^(HTTP/|server:|x-amzn-waf-action:|x-cache:)' /tmp/tz53/hdr/r16
HTTP/2 405 
server: CloudFront
x-amzn-waf-action: captcha
x-cache: Error from cloudfront
[exit 0]
$ grep --only-matching '<title>[^<]*</title>' /tmp/tz53/body/r16
<title>Human Verification</title>
[exit 0]
```

**Offline extras over the saved C2 and C5 bodies and A2's payload.** These are counts, dates and
symbols only, and they made no request:

```
$ python3 /tmp/tz53/extra.py
C5+ PERPETUAL rows with deliveryDate 2100-12-25: 569; before the read: 131 (status {'SETTLING': 131}); after the read and not 2100-12-25: 3
C5+ the future deliveryDate values among PERPETUAL rows (date, status, count): [(('2026-10-05', 'TRADING'), 3)]
C5+ status per contractType: {'CURRENT_QUARTER': {'TRADING': 2}, 'NEXT_QUARTER': {'TRADING': 2}, 'PERPETUAL': {'TRADING': 571, 'SETTLING': 131, 'PENDING_TRADING': 1}, 'TRADIFI_PERPETUAL': {'TRADING': 213}}
C2+ ticker symbols 788, by exchangeInfo contractType {'CURRENT_QUARTER': 2, 'NEXT_QUARTER': 2, 'PERPETUAL': 571, 'TRADIFI_PERPETUAL': 213}, absent from exchangeInfo 0
C2+ A2 x symbols 787; in both 787; only in A2 x 0; only in C2 1
C2+ A2 c symbols 31; of them in C2 31
C5+ symbols of the future non-2100 deliveryDate rows: [('2026-10-05', '1000000BOBUSDT'), ('2026-10-05', 'PROMPTUSDT'), ('2026-10-05', 'PUMPBTCUSDT')]
C2+ the symbol only in C2: ['CTUSDT'], onboardDate ['2026-10-01T07:45Z']
C5+ PENDING_TRADING row: [('GAIBUSDT', 'PERPETUAL', '2025-11-20T09:00Z')]
[exit 0]
```

### Stage D — Telegram, with no token

| Reading | Result |
|---|---|
| D1 `https://api.telegram.org/` | **302 → 200**, landing `https://core.telegram.org/bots`; first `Location:` `https://core.telegram.org/bots` |
| D2 `bot0:invalid/getMe` | **401**, body `{"ok":false,"error_code":401,"description":"Unauthorized: invalid token specified"}` |

```
=== D1
READ r17 [D1] curl -sS -L -m 20 -o /tmp/tz53/body/r17 -D /tmp/tz53/hdr/r17 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.telegram.org/'
     -> 200 24953 text/html; charset=utf-8 https://core.telegram.org/bots | curl exit 0 | hops 302>200 | 2026-10-01T08:07:43Z .. 2026-10-01T08:07:43Z (0.20 s)
D1 status 200; hops 302>200; landing https://core.telegram.org/bots; first Location header: https://core.telegram.org/bots
COUNT [D1] attempted 1, answered 1
=== D2
READ r18 [D2] curl -sS -L -m 20 -o /tmp/tz53/body/r18 -D /tmp/tz53/hdr/r18 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.telegram.org/bot0:invalid/getMe'
     -> 401 83 application/json https://api.telegram.org/bot0:invalid/getMe | curl exit 0 | hops 401 | 2026-10-01T08:07:44Z .. 2026-10-01T08:07:44Z (0.07 s)
D2 status 401; body verbatim: {"ok":false,"error_code":401,"description":"Unauthorized: invalid token specified"}
COUNT [D2] attempted 1, answered 1
```

### Stage E — The hunter's candidate lanes

| Reading | Result |
|---|---|
| E1 FRED `robots.txt` | 200; governing group `*`, 6 `Disallow` lines, none matching `/graph/fredgraph.csv`; `Crawl-delay: 1` |
| E1 `WALCL` · `WTREGEN` · `RRPONTSYD` · `WRESBAL` | 200 · 200 · 200 · 200; header `observation_date,<ID>`; last observation 2026-09-23 · 2026-09-23 · 2026-09-30 · 2026-09-23; 1 242 · 1 242 · 6 170 · 1 242 lines; gaps between FRED reads 1.05 s each |
| E2 Fed `robots.txt` | **404** → no restriction (RFC 9309 §2.3.1.3) |
| E2 `fomccalendars.htm` | 200; **8** meetings under «2026 FOMC Meetings»: January 27-28 · March 17-18* · April 28-29 · June 16-17* · July 28-29 · September 15-16* · October 27-28 · December 8-9* |
| E2 `h41.htm` | 200, 702 175 bytes; first date after `Release Date:` **September 24, 2026** |
| E3 Fiscal Data DTS | 200; 2 rows; newest `record_date` **2026-09-29**; 16-key row set in the log |
| E4 `stablecoins` | 200, 556 615 bytes; `peggedAssets` **429**; the first's 14 keys in the log |
| E4 `stablecoincharts/all` | 200; **3 229** rows; newest `date` **2026-10-01T00:00:00Z** |
| E5 `robots.txt` | iShares 200 (`*`, 8 lines, none matching) · Bitwise 200 (`Allow: /`) · Grayscale **429** (Vercel challenge) → no restriction by rule 3 |
| E5 iShares IBIT | 200, 1 548 584 bytes; `keyFundFacts-sharesOutstanding` datapoint present; as of **Sep 30, 2026** |
| E5 iShares ETHA | 200, 1 544 729 bytes; datapoint present; as of **Sep 30, 2026** |
| E5 `bitbetf.com` | 200, 241 444 bytes; «Shares Outstanding» present with a number; the block's «Data as of **09/29/2026**» |
| E5 Grayscale GBTC | **429**, 33 943 bytes; `x-vercel-mitigated: challenge`; «Shares Outstanding» absent |
| E6 Farside `robots.txt` | 200; one group, for `Twitterbot`, with an empty `Disallow` → no rule binds this client |
| E6 `/btc/` · `/eth/` | **403** · **403**; `cf-mitigated: challenge` on both; `<table` absent on both |
| E7 Coinbase `BTC-USD` · `ETH-USD` | 200 · 200; 8 keys; body `time` **0.368 s** · **0.691 s** before the read |

```
=== E1
READ r19 [E1] curl -sS -L -m 20 -o /tmp/tz53/body/r19 -D /tmp/tz53/hdr/r19 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fred.stlouisfed.org/robots.txt'
     -> 200 960 text/plain https://fred.stlouisfed.org/robots.txt | curl exit 0 | hops 200 | 2026-10-01T08:07:48Z .. 2026-10-01T08:07:48Z (0.20 s)
     robots https://fred.stlouisfed.org: parsed: 4 group(s); governing group *; 6 rule line(s); 0 Sitemap line(s)
E1 robots Crawl-delay in the * group: 1
     robots decision for /graph/fredgraph.csv?id=WALCL (group *, from r19): allowed; matching lines: none; deciding line: none (no match)
READ r20 [E1] curl -sS -L -m 20 -o /tmp/tz53/body/r20 -D /tmp/tz53/hdr/r20 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=WALCL'
     -> 200 23301 application/csv https://fred.stlouisfed.org/graph/fredgraph.csv?id=WALCL | curl exit 0 | hops 200 | 2026-10-01T08:07:49Z .. 2026-10-01T08:07:49Z (0.23 s)
E1 WALCL: status 200; rows 1242 (data rows 1241); header line observation_date,WALCL; date of the last observation 2026-09-23
     robots decision for /graph/fredgraph.csv?id=WTREGEN (group *, from r19): allowed; matching lines: none; deciding line: none (no match)
READ r21 [E1] curl -sS -L -m 20 -o /tmp/tz53/body/r21 -D /tmp/tz53/hdr/r21 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=WTREGEN'
     -> 200 21494 application/csv https://fred.stlouisfed.org/graph/fredgraph.csv?id=WTREGEN | curl exit 0 | hops 200 | 2026-10-01T08:07:50Z .. 2026-10-01T08:07:50Z (0.23 s)
E1 WTREGEN: status 200; rows 1242 (data rows 1241); header line observation_date,WTREGEN; date of the last observation 2026-09-23
     robots decision for /graph/fredgraph.csv?id=RRPONTSYD (group *, from r19): allowed; matching lines: none; deciding line: none (no match)
READ r22 [E1] curl -sS -L -m 20 -o /tmp/tz53/body/r22 -D /tmp/tz53/hdr/r22 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=RRPONTSYD'
     -> 200 95323 application/csv https://fred.stlouisfed.org/graph/fredgraph.csv?id=RRPONTSYD | curl exit 0 | hops 200 | 2026-10-01T08:07:51Z .. 2026-10-01T08:07:52Z (0.20 s)
E1 RRPONTSYD: status 200; rows 6170 (data rows 6169); header line observation_date,RRPONTSYD; date of the last observation 2026-09-30
     robots decision for /graph/fredgraph.csv?id=WRESBAL (group *, from r19): allowed; matching lines: none; deciding line: none (no match)
READ r23 [E1] curl -sS -L -m 20 -o /tmp/tz53/body/r23 -D /tmp/tz53/hdr/r23 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=WRESBAL'
     -> 200 22803 application/csv https://fred.stlouisfed.org/graph/fredgraph.csv?id=WRESBAL | curl exit 0 | hops 200 | 2026-10-01T08:07:53Z .. 2026-10-01T08:07:53Z (0.14 s)
E1 WRESBAL: status 200; rows 1242 (data rows 1241); header line observation_date,WRESBAL; date of the last observation 2026-09-23
E1 gaps between consecutive FRED reads (end of one to start of the next), s: [1.05, 1.05, 1.05, 1.05]
COUNT [E1] attempted 5, answered 5
=== E2
READ r24 [E2] curl -sS -L -m 20 -o /tmp/tz53/body/r24 -D /tmp/tz53/hdr/r24 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.federalreserve.gov/robots.txt'
     -> 404 81196 text/html https://www.federalreserve.gov/robots.txt | curl exit 0 | hops 404 | 2026-10-01T08:07:53Z .. 2026-10-01T08:07:53Z (0.19 s)
     robots https://www.federalreserve.gov: robots.txt HTTP 404: unavailable, no restriction (RFC 9309 2.3.1.3)
     robots decision for /monetarypolicy/fomccalendars.htm (group None, from r24): allowed; matching lines: none; deciding line: none (no match)
READ r25 [E2] curl -sS -L -m 20 -o /tmp/tz53/body/r25 -D /tmp/tz53/hdr/r25 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm'
     -> 200 165460 text/html https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm | curl exit 0 | hops 200 | 2026-10-01T08:07:54Z .. 2026-10-01T08:07:54Z (0.19 s)
E2 fomccalendars: status 200; section under "2026 FOMC Meetings" 10639 chars; meetings parsed 8
E2 meetings as read (month | date): [('January', '27-28'), ('March', '17-18*'), ('April', '28-29'), ('June', '16-17*'), ('July', '28-29'), ('September', '15-16*'), ('October', '27-28'), ('December', '8-9*')]
     robots decision for /releases/h41/current/h41.htm (group None, from r24): allowed; matching lines: none; deciding line: none (no match)
READ r26 [E2] curl -sS -L -m 20 -o /tmp/tz53/body/r26 -D /tmp/tz53/hdr/r26 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.federalreserve.gov/releases/h41/current/h41.htm'
     -> 200 702175 text/html https://www.federalreserve.gov/releases/h41/current/h41.htm | curl exit 0 | hops 200 | 2026-10-01T08:07:55Z .. 2026-10-01T08:07:56Z (0.22 s)
E2 h41: status 200; bytes 702175; "Release Date:" found True; first date after it: September 24, 2026
COUNT [E2] attempted 3, answered 3
=== E3
READ r27 [E3] curl -sS -L -m 20 -o /tmp/tz53/body/r27 -D /tmp/tz53/hdr/r27 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance?sort=-record_date&page%5Bsize%5D=2'
     -> 200 2796 application/json https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance?sort=-record_date&page%5Bsize%5D=2 | curl exit 0 | hops 200 | 2026-10-01T08:07:56Z .. 2026-10-01T08:07:57Z (1.52 s)
E3 status 200; top-level key set ['data', 'links', 'meta']; rows 2; newest record_date 2026-09-29; row key set ['account_type', 'close_today_bal', 'open_fiscal_year_bal', 'open_month_bal', 'open_today_bal', 'record_calendar_day', 'record_calendar_month', 'record_calendar_quarter', 'record_calendar_year', 'record_date', 'record_fiscal_quarter', 'record_fiscal_year', 'src_line_nbr', 'sub_table_name', 'table_nbr', 'table_nm']
COUNT [E3] attempted 1, answered 1
=== E4
READ r28 [E4] curl -sS -L -m 20 -o /tmp/tz53/body/r28 -D /tmp/tz53/hdr/r28 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://stablecoins.llama.fi/stablecoins?includePrices=false'
     -> 200 556615 application/json https://stablecoins.llama.fi/stablecoins?includePrices=false | curl exit 0 | hops 200 | 2026-10-01T08:07:57Z .. 2026-10-01T08:07:57Z (0.06 s)
E4 stablecoins: status 200; bytes 556615; top-level key set ['chains', 'peggedAssets']; peggedAssets 429; key set of the first ['chainCirculating', 'chains', 'circulating', 'circulatingPrevDay', 'circulatingPrevMonth', 'circulatingPrevWeek', 'gecko_id', 'id', 'name', 'pegMechanism', 'pegType', 'price', 'priceSource', 'symbol']
READ r29 [E4] curl -sS -L -m 20 -o /tmp/tz53/body/r29 -D /tmp/tz53/hdr/r29 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://stablecoins.llama.fi/stablecoincharts/all'
     -> 200 1298576 application/json https://stablecoins.llama.fi/stablecoincharts/all | curl exit 0 | hops 200 | 2026-10-01T08:07:58Z .. 2026-10-01T08:07:58Z (0.06 s)
E4 stablecoincharts/all: status 200; rows 3229; row key set of the last ['date', 'totalBridgedToUSD', 'totalCirculating', 'totalCirculatingUSD', 'totalMintedUSD', 'totalUnreleased']; newest date 2026-10-01T00:00:00Z
COUNT [E4] attempted 2, answered 2
```

The E5–E7 reads as made, with the **first** E5 parser (Deviation 1):

```
=== E5
READ r30 [E5] curl -sS -L -m 20 -o /tmp/tz53/body/r30 -D /tmp/tz53/hdr/r30 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.ishares.com/robots.txt'
     -> 200 920 text/plain; charset=UTF-8 https://www.ishares.com/robots.txt | curl exit 0 | hops 200 | 2026-10-01T08:08:04Z .. 2026-10-01T08:08:04Z (0.27 s)
     robots https://www.ishares.com: parsed: 2 group(s); governing group *; 8 rule line(s); 13 Sitemap line(s)
READ r31 [E5] curl -sS -L -m 20 -o /tmp/tz53/body/r31 -D /tmp/tz53/hdr/r31 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://bitbetf.com/robots.txt'
     -> 200 114 text/plain; charset=utf-8 https://bitbetf.com/robots.txt | curl exit 0 | hops 200 | 2026-10-01T08:08:04Z .. 2026-10-01T08:08:04Z (0.15 s)
     robots https://bitbetf.com: parsed: 1 group(s); governing group *; 1 rule line(s); 1 Sitemap line(s)
READ r32 [E5] curl -sS -L -m 20 -o /tmp/tz53/body/r32 -D /tmp/tz53/hdr/r32 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.grayscale.com/robots.txt'
     -> 429 33944 text/html; charset=utf-8 https://www.grayscale.com/robots.txt | curl exit 0 | hops 429 | 2026-10-01T08:08:04Z .. 2026-10-01T08:08:04Z (0.11 s)
     robots https://www.grayscale.com: robots.txt HTTP 429: unavailable, no restriction (RFC 9309 2.3.1.3)
     robots decision for /us/products/333011/ishares-bitcoin-trust-etf (group *, from r30): allowed; matching lines: none; deciding line: none (no match)
READ r33 [E5] curl -sS -L -m 20 -o /tmp/tz53/body/r33 -D /tmp/tz53/hdr/r33 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.ishares.com/us/products/333011/ishares-bitcoin-trust-etf'
     -> 200 1548584 text/html;charset=UTF-8 https://www.ishares.com/us/products/333011/ishares-bitcoin-trust-etf | curl exit 0 | hops 200 | 2026-10-01T08:08:05Z .. 2026-10-01T08:08:05Z (0.41 s)
E5 https://www.ishares.com/us/products/333011/ishares-bitcoin-trust-etf: status 200; bytes 1548584; landing https://www.ishares.com/us/products/333011/ishares-bitcoin-trust-etf; marker "keyFundFacts-sharesOutstanding" occurrences 7; as-of date near the first: None
     robots decision for /us/products/337614/ishares-ethereum-trust-etf (group *, from r30): allowed; matching lines: none; deciding line: none (no match)
READ r34 [E5] curl -sS -L -m 20 -o /tmp/tz53/body/r34 -D /tmp/tz53/hdr/r34 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.ishares.com/us/products/337614/ishares-ethereum-trust-etf'
     -> 200 1544729 text/html;charset=UTF-8 https://www.ishares.com/us/products/337614/ishares-ethereum-trust-etf | curl exit 0 | hops 200 | 2026-10-01T08:08:06Z .. 2026-10-01T08:08:07Z (0.54 s)
E5 https://www.ishares.com/us/products/337614/ishares-ethereum-trust-etf: status 200; bytes 1544729; landing https://www.ishares.com/us/products/337614/ishares-ethereum-trust-etf; marker "keyFundFacts-sharesOutstanding" occurrences 7; as-of date near the first: None
     robots decision for / (group *, from r31): allowed; matching lines: ['Allow: /']; deciding line: Allow: /
READ r35 [E5] curl -sS -L -m 20 -o /tmp/tz53/body/r35 -D /tmp/tz53/hdr/r35 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://bitbetf.com/'
     -> 200 241444 text/html; charset=utf-8 https://bitbetf.com/ | curl exit 0 | hops 200 | 2026-10-01T08:08:07Z .. 2026-10-01T08:08:07Z (0.17 s)
E5 https://bitbetf.com/: status 200; bytes 241444; landing https://bitbetf.com/; marker "Shares Outstanding" occurrences 2; as-of date near the first: None
     robots decision for /funds/grayscale-bitcoin-trust (group None, from r32): allowed; matching lines: none; deciding line: none (no match)
READ r36 [E5] curl -sS -L -m 20 -o /tmp/tz53/body/r36 -D /tmp/tz53/hdr/r36 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.grayscale.com/funds/grayscale-bitcoin-trust'
     -> 429 33943 text/html; charset=utf-8 https://www.grayscale.com/funds/grayscale-bitcoin-trust | curl exit 0 | hops 429 | 2026-10-01T08:08:07Z .. 2026-10-01T08:08:07Z (0.09 s)
E5 https://www.grayscale.com/funds/grayscale-bitcoin-trust: status 429; bytes 33943; landing https://www.grayscale.com/funds/grayscale-bitcoin-trust; marker "Shares Outstanding" occurrences 0; as-of date near the first: None
COUNT [E5] attempted 7, answered 7
=== E6
READ r37 [E6] curl -sS -L -m 20 -o /tmp/tz53/body/r37 -D /tmp/tz53/hdr/r37 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://farside.co.uk/robots.txt'
     -> 200 33 text/plain https://farside.co.uk/robots.txt | curl exit 0 | hops 200 | 2026-10-01T08:08:07Z .. 2026-10-01T08:08:07Z (0.04 s)
     robots https://farside.co.uk: parsed: 1 group(s); governing group none; 0 rule line(s); 0 Sitemap line(s)
     robots decision for /btc/ (group None, from r37): allowed; matching lines: none; deciding line: none (no match)
READ r38 [E6] curl -sS -L -m 20 -o /tmp/tz53/body/r38 -D /tmp/tz53/hdr/r38 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://farside.co.uk/btc/'
     -> 403 5331 text/html; charset=UTF-8 https://farside.co.uk/btc/ | curl exit 0 | hops 403 | 2026-10-01T08:08:08Z .. 2026-10-01T08:08:08Z (0.04 s)
E6 https://farside.co.uk/btc/: status 403; cf-mitigated challenge; body contains <table: False
     robots decision for /eth/ (group None, from r37): allowed; matching lines: none; deciding line: none (no match)
READ r39 [E6] curl -sS -L -m 20 -o /tmp/tz53/body/r39 -D /tmp/tz53/hdr/r39 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://farside.co.uk/eth/'
     -> 403 5331 text/html; charset=UTF-8 https://farside.co.uk/eth/ | curl exit 0 | hops 403 | 2026-10-01T08:08:09Z .. 2026-10-01T08:08:09Z (0.04 s)
E6 https://farside.co.uk/eth/: status 403; cf-mitigated challenge; body contains <table: False
COUNT [E6] attempted 3, answered 3
=== E7
READ r40 [E7] curl -sS -L -m 20 -o /tmp/tz53/body/r40 -D /tmp/tz53/hdr/r40 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.exchange.coinbase.com/products/BTC-USD/ticker'
     -> 200 186 application/json; charset=utf-8 https://api.exchange.coinbase.com/products/BTC-USD/ticker | curl exit 0 | hops 200 | 2026-10-01T08:08:09Z .. 2026-10-01T08:08:09Z (0.04 s)
E7 BTC-USD: status 200; key set ['ask', 'bid', 'price', 'rfq_volume', 'size', 'time', 'trade_id', 'volume']; body time present True; seconds between body time and the read (2026-10-01T08:08:09Z): 0.368
READ r41 [E7] curl -sS -L -m 20 -o /tmp/tz53/body/r41 -D /tmp/tz53/hdr/r41 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.exchange.coinbase.com/products/ETH-USD/ticker'
     -> 200 184 application/json; charset=utf-8 https://api.exchange.coinbase.com/products/ETH-USD/ticker | curl exit 0 | hops 200 | 2026-10-01T08:08:11Z .. 2026-10-01T08:08:11Z (0.07 s)
E7 ETH-USD: status 200; key set ['ask', 'bid', 'price', 'rfq_volume', 'size', 'time', 'trade_id', 'volume']; body time present True; seconds between body time and the read (2026-10-01T08:08:11Z): 0.691
COUNT [E7] attempted 2, answered 2
```

E5 as classified by the final parser, from the saved bodies, offline (every line ends
`(from ledger, no request)`):

```
=== E5
READ r30 [E5] curl -sS -L -m 20 -o /tmp/tz53/body/r30 -D /tmp/tz53/hdr/r30 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.ishares.com/robots.txt' (from ledger, no request)
     -> 200 920 text/plain; charset=UTF-8 https://www.ishares.com/robots.txt | curl exit 0 | hops 200 | 2026-10-01T08:08:04Z .. 2026-10-01T08:08:04Z (0.27 s)
     robots https://www.ishares.com: parsed: 2 group(s); governing group *; 8 rule line(s); 13 Sitemap line(s)
READ r31 [E5] curl -sS -L -m 20 -o /tmp/tz53/body/r31 -D /tmp/tz53/hdr/r31 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://bitbetf.com/robots.txt' (from ledger, no request)
     -> 200 114 text/plain; charset=utf-8 https://bitbetf.com/robots.txt | curl exit 0 | hops 200 | 2026-10-01T08:08:04Z .. 2026-10-01T08:08:04Z (0.15 s)
     robots https://bitbetf.com: parsed: 1 group(s); governing group *; 1 rule line(s); 1 Sitemap line(s)
READ r32 [E5] curl -sS -L -m 20 -o /tmp/tz53/body/r32 -D /tmp/tz53/hdr/r32 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.grayscale.com/robots.txt' (from ledger, no request)
     -> 429 33944 text/html; charset=utf-8 https://www.grayscale.com/robots.txt | curl exit 0 | hops 429 | 2026-10-01T08:08:04Z .. 2026-10-01T08:08:04Z (0.11 s)
     robots https://www.grayscale.com: robots.txt HTTP 429: unavailable, no restriction (RFC 9309 2.3.1.3)
     robots decision for /us/products/333011/ishares-bitcoin-trust-etf (group *, from r30): allowed; matching lines: none; deciding line: none (no match)
READ r33 [E5] curl -sS -L -m 20 -o /tmp/tz53/body/r33 -D /tmp/tz53/hdr/r33 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.ishares.com/us/products/333011/ishares-bitcoin-trust-etf' (from ledger, no request)
     -> 200 1548584 text/html;charset=UTF-8 https://www.ishares.com/us/products/333011/ishares-bitcoin-trust-etf | curl exit 0 | hops 200 | 2026-10-01T08:08:05Z .. 2026-10-01T08:08:05Z (0.41 s)
E5 https://www.ishares.com/us/products/333011/ishares-bitcoin-trust-etf: status 200; bytes 1548584; landing https://www.ishares.com/us/products/333011/ishares-bitcoin-trust-etf; mitigation header None; "keyFundFacts-sharesOutstanding" occurrences 7; shares-outstanding datum in served HTML: True; as-of date as read: Sep 30, 2026 (datapoint attribute keyFundFacts-sharesOutstanding; as-of from its -asOf datapoint)
     robots decision for /us/products/337614/ishares-ethereum-trust-etf (group *, from r30): allowed; matching lines: none; deciding line: none (no match)
READ r34 [E5] curl -sS -L -m 20 -o /tmp/tz53/body/r34 -D /tmp/tz53/hdr/r34 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.ishares.com/us/products/337614/ishares-ethereum-trust-etf' (from ledger, no request)
     -> 200 1544729 text/html;charset=UTF-8 https://www.ishares.com/us/products/337614/ishares-ethereum-trust-etf | curl exit 0 | hops 200 | 2026-10-01T08:08:06Z .. 2026-10-01T08:08:07Z (0.54 s)
E5 https://www.ishares.com/us/products/337614/ishares-ethereum-trust-etf: status 200; bytes 1544729; landing https://www.ishares.com/us/products/337614/ishares-ethereum-trust-etf; mitigation header None; "keyFundFacts-sharesOutstanding" occurrences 7; shares-outstanding datum in served HTML: True; as-of date as read: Sep 30, 2026 (datapoint attribute keyFundFacts-sharesOutstanding; as-of from its -asOf datapoint)
     robots decision for / (group *, from r31): allowed; matching lines: ['Allow: /']; deciding line: Allow: /
READ r35 [E5] curl -sS -L -m 20 -o /tmp/tz53/body/r35 -D /tmp/tz53/hdr/r35 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://bitbetf.com/' (from ledger, no request)
     -> 200 241444 text/html; charset=utf-8 https://bitbetf.com/ | curl exit 0 | hops 200 | 2026-10-01T08:08:07Z .. 2026-10-01T08:08:07Z (0.17 s)
E5 https://bitbetf.com/: status 200; bytes 241444; landing https://bitbetf.com/; mitigation header None; "Shares Outstanding" occurrences 2; shares-outstanding datum in served HTML: True; as-of date as read: 09/29/2026 (nearest preceding as-of statement, 101 chars of served text before the label)
     robots decision for /funds/grayscale-bitcoin-trust (group None, from r32): allowed; matching lines: none; deciding line: none (no match)
READ r36 [E5] curl -sS -L -m 20 -o /tmp/tz53/body/r36 -D /tmp/tz53/hdr/r36 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.grayscale.com/funds/grayscale-bitcoin-trust' (from ledger, no request)
     -> 429 33943 text/html; charset=utf-8 https://www.grayscale.com/funds/grayscale-bitcoin-trust | curl exit 0 | hops 429 | 2026-10-01T08:08:07Z .. 2026-10-01T08:08:07Z (0.09 s)
E5 https://www.grayscale.com/funds/grayscale-bitcoin-trust: status 429; bytes 33943; landing https://www.grayscale.com/funds/grayscale-bitcoin-trust; mitigation header challenge; "Shares Outstanding" occurrences 0; shares-outstanding datum in served HTML: False; as-of date as read: None (label absent)
COUNT [E5] attempted 7, answered 7
```

The robots files that governed Stage E, as served:

```
$ awk '/^User-agent: \*/{f=1} f' /tmp/tz53/body/r19
User-agent: *
Crawl-delay: 1
Disallow: /graph/graph-landing.php
Disallow: /graph/image.php
Disallow: /graph/fredgraph.png
Disallow: /searchresults
Disallow: /fred-glance-widget.php
Disallow: /seriesBeta
[exit 0]
$ grep --invert-match --extended-regexp '^\s*$|^SITEMAP' /tmp/tz53/body/r30
User-agent: Brightbot 1.0
Disallow: /
User-agent: *
Disallow: /*?truepdf*
Disallow: /*?norepdf*
Disallow: /*.dl$
Disallow: /*sign-on.oauth
Disallow: /*sign-on.saml
Disallow: /*sign-on-popup.saml
Disallow: /search/
Disallow: /us/MYCATEGORYURL
[exit 0]
$ grep --invert-match --extended-regexp '^\s*$|^#' /tmp/tz53/body/r31
User-agent: *
Allow: /
Host: https://bitbetf.com
Sitemap: https://bitbetf.com/sitemap.xml
[exit 0]
$ cat --show-nonprinting /tmp/tz53/body/r37
User-agent: Twitterbot^M
Disallow:[exit 0]
$ grep --ignore-case --extended-regexp '^(HTTP/|server:|x-vercel-mitigated:)' /tmp/tz53/hdr/r32 /tmp/tz53/hdr/r36
/tmp/tz53/hdr/r32:HTTP/2 429 
/tmp/tz53/hdr/r32:server: Vercel
/tmp/tz53/hdr/r32:x-vercel-mitigated: challenge
/tmp/tz53/hdr/r36:HTTP/2 429 
/tmp/tz53/hdr/r36:server: Vercel
/tmp/tz53/hdr/r36:x-vercel-mitigated: challenge
[exit 0]
```

Farside's file ends without a newline, so the helper's `[exit 0]` follows `Disallow:` on its line.

### Findings for the Architect

These are readings, not admissions. Lane admission is an Architect edit to
`ANALYST-INSTRUCTIONS.md` (TZ «What this TZ does not decide»).

1. **A scheduler on this machine can run a headless session.** A transient system unit started a
   headless `claude -p` that returned exactly `HEADLESS-OK` in 1 turn and 2 792 ms. Every probe
   step exited 0.
   - The unit's environment held `HOME`, `PATH`, `CLAUDE_BIN` and `REPO` beside systemd's own
     variables. No API key is set in this session (B5), and none was passed. **Inference, not
     read:** the run authenticated from a file under `HOME`.
   - The dry-run push likewise authenticated over SSH with no agent socket passed, so its key is
     file-based too (also inference).
   - The headless run left a session record under `~/.claude/projects/-tmp-tz53-unit/`: 2
     entries, 180 846 bytes. `~/.claude.json`'s mtime moved to 08:03:48, inside the unit's window.
     Neither was read and both were left in place (`## Final Repository State`).
2. **`--max-turns` does not occur in `claude --help` for 2.1.282.** The other six named options do.
   A unit that relies on a turn limit cannot take it from this help text.
3. **Both schedulers are available and neither is in use.** systemd 255 runs as PID 1
   (`running`) and `cron` is `active`. Root's crontab is empty: exit 1, 0 lines.
4. **Headroom is thin.** At B1 the machine had 74 MB of its 955 MB available, with 1 543 MB of
   3 099 MB swap in use, on 1 CPU. The map's row on gate step 5 (`955 MB single-CPU host`) reads
   the same machine.
5. **The repository clone persists and the session worktree does not.** A3's checkout is a
   harness worktree created 01.10.2026 07:59:30. Its common directory `/root/crypto-auto/.git`
   was cloned 29.08.2026 and carries 68 registered worktrees. The machine has been up since
   02.08.2026.
6. **`fapi.binance.com` carries the payload's schema from this machine.**
   - C2's row key set is equal to A2's `x[0]`.
   - C3 carries `markPrice` and `lastFundingRate`, and C4 carries `openInterest`.
   - C2's 788 symbols cover all 787 of A2's `x` and all 31 of `c`. The one more is `CTUSDT`,
     onboarded 2026-10-01T07:45Z, after the payload's `ts`.
   - **Inference, not read:** the names of `c`'s keys (`mark`, `fr`, `oi`, `qv`, …) suggest C2–C4
     as their sources. The Shortcut's mapping was not read.
7. **`exchangeInfo` is a dated, keyless record of listing and delisting.** `onboardDate` named 15
   symbols listed in the 7 days before the read. `deliveryDate` names 3 trading perpetuals with
   2026-10-05, before that day arrives. 131 settling rows carry past dates, and 569 carry
   2100-12-25, which means none.
8. **The announcement site offers this client no dated, permitted lane.**
   - The list API is `refused on permission`.
   - The English child sitemap is permitted, but its 4 973 URLs carry one generation stamp in
     place of a publication date. It is ordered by article code, so «the first `<loc>`» is an
     arbitrary article.
   - That article answered an AWS WAF captcha.
   - See Pre-existing Issue 2 for the methodology's own read of the disallowed list.
9. **Telegram's Bot API host answers this machine** (D1, D2). This says nothing about delivery.
10. **The calendar and liquidity publishers answer.**
    - FRED: 4 of 4 series as CSV.
    - Federal Reserve: the 2026 calendar, 8 meetings, and H.4.1 dated September 24, 2026, both
      at 08:07Z on 01.10.
    - Fiscal Data: newest record 2026-09-29.
    - DefiLlama: current to 2026-10-01T00:00Z.
11. **ETF holdings: two issuers answer and one refuses; the aggregator refuses.**
    - iShares answered for both products. Its as-of date (Sep 30, 2026) is one day later than the
      Architect's reading earlier on 01.10 (Sep 29, 2026).
    - Bitwise answered, «Data as of 09/29/2026».
    - Grayscale's page **and its robots.txt** are behind a Vercel Security Checkpoint (429). So
      that host's permission is unknown rather than granted, and the page was read only because
      rule 3 maps any 4xx robots.txt to no restriction.
    - Farside's flow pages are behind a Cloudflare challenge (403). Its robots.txt names only
      `Twitterbot`.
12. **Coinbase Exchange answers with a sub-second body time.** It is a second venue's spot clock
    for BTC and ETH.
13. **The hosting lookup and the virtualisation probe name different parties.** ipinfo reads
    AS20473 The Constant Company, LLC, and `systemd-detect-virt` reads `microsoft`. Both are
    printed as read and neither is a contract.

### Reading ledger

All 41 requests, in order. Every one used rule 1's form exactly (V4); the command is printed in
full in each stage's log above. «same» means the landing URL equals the requested one.

| id | stage | start (UTC) | s | URL | status | hops | bytes | content type | landing |
|---|---|---|---:|---|---|---|---:|---|---|
| r01 | B2 | 08:06:55 | 0.19 | `https://ipinfo.io/org` | 200 | 200 | 34 | text/html; charset=utf-8 | same |
| r02 | C1 | 08:06:56 | 0.28 | `https://fapi.binance.com/fapi/v1/ping` | 200 | 200 | 2 | application/json | same |
| r03 | C1 | 08:06:57 | 0.28 | `https://fapi.binance.com/fapi/v1/time` | 200 | 200 | 28 | application/json | same |
| r04 | C2 | 08:06:58 | 0.28 | `https://fapi.binance.com/fapi/v1/ticker/24hr` | 200 | 200 | 292784 | application/json | same |
| r05 | C3 | 08:07:00 | 0.29 | `https://fapi.binance.com/fapi/v1/premiumIndex` | 200 | 200 | 204789 | application/json | same |
| r06 | C4 | 08:07:01 | 0.28 | `https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT` | 200 | 200 | 68 | application/json | same |
| r07 | C5 | 08:07:02 | 0.40 | `https://fapi.binance.com/fapi/v1/exchangeInfo` | 200 | 200 | 1142974 | application/json | same |
| r08 | C6 | 08:07:04 | 0.29 | `https://fapi.binance.com/futures/data/topLongShortPositionRatio?symbol=BTCUSDT&period=1h&limit=2` | 200 | 200 | 241 | application/json;charset=UTF-8 | same |
| r09 | C6 | 08:07:05 | 0.28 | `https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=BTCUSDT&period=1h&limit=2` | 200 | 200 | 241 | application/json;charset=UTF-8 | same |
| r10 | C6 | 08:07:06 | 0.29 | `https://fapi.binance.com/futures/data/takerlongshortRatio?symbol=BTCUSDT&period=1h&limit=2` | 200 | 200 | 191 | application/json;charset=UTF-8 | same |
| r11 | C6 | 08:07:08 | 0.28 | `https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=2` | 200 | 200 | 341 | application/json;charset=UTF-8 | same |
| r12 | C7 | 08:07:08 | 0.28 | `https://api.binance.com/api/v3/ping` | 200 | 200 | 2 | application/json;charset=UTF-8 | same |
| r13 | C8 | 08:07:15 | 0.28 | `https://www.binance.com/robots.txt` | 200 | 200 | 6722 | text/plain; charset=UTF-8 | same |
| r14 | C8 | 08:07:16 | 0.78 | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_index.xml` | 200 | 200 | 13536 | application/xml | same |
| r15 | C8 | 08:07:18 | 0.07 | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_en_0.xml` | 200 | 200 | 754121 | application/xml | same |
| r16 | C8 | 08:07:19 | 0.04 | `https://www.binance.com/en/support/announcement/detail/0001cb4538b2445581d4e5c35bfbd63a` | 405 | 405 | 2225 | text/html; charset=UTF-8 | same |
| r17 | D1 | 08:07:43 | 0.20 | `https://api.telegram.org/` | 200 | 302>200 | 24953 | text/html; charset=utf-8 | `https://core.telegram.org/bots` |
| r18 | D2 | 08:07:44 | 0.07 | `https://api.telegram.org/bot0:invalid/getMe` | 401 | 401 | 83 | application/json | same |
| r19 | E1 | 08:07:48 | 0.20 | `https://fred.stlouisfed.org/robots.txt` | 200 | 200 | 960 | text/plain | same |
| r20 | E1 | 08:07:49 | 0.23 | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=WALCL` | 200 | 200 | 23301 | application/csv | same |
| r21 | E1 | 08:07:50 | 0.23 | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=WTREGEN` | 200 | 200 | 21494 | application/csv | same |
| r22 | E1 | 08:07:51 | 0.20 | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=RRPONTSYD` | 200 | 200 | 95323 | application/csv | same |
| r23 | E1 | 08:07:53 | 0.14 | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=WRESBAL` | 200 | 200 | 22803 | application/csv | same |
| r24 | E2 | 08:07:53 | 0.19 | `https://www.federalreserve.gov/robots.txt` | 404 | 404 | 81196 | text/html | same |
| r25 | E2 | 08:07:54 | 0.19 | `https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm` | 200 | 200 | 165460 | text/html | same |
| r26 | E2 | 08:07:55 | 0.22 | `https://www.federalreserve.gov/releases/h41/current/h41.htm` | 200 | 200 | 702175 | text/html | same |
| r27 | E3 | 08:07:56 | 1.52 | `https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance?sort=-record_date&page%5Bsize%5D=2` | 200 | 200 | 2796 | application/json | same |
| r28 | E4 | 08:07:57 | 0.06 | `https://stablecoins.llama.fi/stablecoins?includePrices=false` | 200 | 200 | 556615 | application/json | same |
| r29 | E4 | 08:07:58 | 0.06 | `https://stablecoins.llama.fi/stablecoincharts/all` | 200 | 200 | 1298576 | application/json | same |
| r30 | E5 | 08:08:04 | 0.27 | `https://www.ishares.com/robots.txt` | 200 | 200 | 920 | text/plain; charset=UTF-8 | same |
| r31 | E5 | 08:08:04 | 0.15 | `https://bitbetf.com/robots.txt` | 200 | 200 | 114 | text/plain; charset=utf-8 | same |
| r32 | E5 | 08:08:04 | 0.11 | `https://www.grayscale.com/robots.txt` | 429 | 429 | 33944 | text/html; charset=utf-8 | same |
| r33 | E5 | 08:08:05 | 0.41 | `https://www.ishares.com/us/products/333011/ishares-bitcoin-trust-etf` | 200 | 200 | 1548584 | text/html;charset=UTF-8 | same |
| r34 | E5 | 08:08:06 | 0.54 | `https://www.ishares.com/us/products/337614/ishares-ethereum-trust-etf` | 200 | 200 | 1544729 | text/html;charset=UTF-8 | same |
| r35 | E5 | 08:08:07 | 0.17 | `https://bitbetf.com/` | 200 | 200 | 241444 | text/html; charset=utf-8 | same |
| r36 | E5 | 08:08:07 | 0.09 | `https://www.grayscale.com/funds/grayscale-bitcoin-trust` | 429 | 429 | 33943 | text/html; charset=utf-8 | same |
| r37 | E6 | 08:08:07 | 0.04 | `https://farside.co.uk/robots.txt` | 200 | 200 | 33 | text/plain | same |
| r38 | E6 | 08:08:08 | 0.04 | `https://farside.co.uk/btc/` | 403 | 403 | 5331 | text/html; charset=UTF-8 | same |
| r39 | E6 | 08:08:09 | 0.04 | `https://farside.co.uk/eth/` | 403 | 403 | 5331 | text/html; charset=UTF-8 | same |
| r40 | E7 | 08:08:09 | 0.04 | `https://api.exchange.coinbase.com/products/BTC-USD/ticker` | 200 | 200 | 186 | application/json; charset=utf-8 | same |
| r41 | E7 | 08:08:11 | 0.07 | `https://api.exchange.coinbase.com/products/ETH-USD/ticker` | 200 | 200 | 184 | application/json; charset=utf-8 | same |

### Instrument sources

`probe.py`, verbatim:

```python
#!/usr/bin/env python3
"""TZ-53 probe: B2 and Stages C-E. One request per URL, ever (ledger); robots.txt first on
site hosts; bodies kept so every reading can be recomputed offline with no request.
Usage: probe.py <stage> ...   (stages: B2 C1 C2 C3 C4 C5 C6 C7 C8 D1 D2 E1 E2 E3 E4 E5 E6 E7)
Every line this script prints is piped through /tmp/tz53/mask.sed by the caller."""
import collections, datetime as dt, gzip, html, json, os, re, subprocess, sys, time
from urllib.parse import urlparse, urljoin

ROOT = '/tmp/tz53'
LEDGER = ROOT + '/ledger.jsonl'
BODY, HDR, OUT = ROOT + '/body', ROOT + '/hdr', ROOT + '/out'
W = '%{http_code} %{size_download} %{content_type} %{url_effective}\\n'  # backslash-n, as typed
SAME_HOST_GAP = 1.0      # courtesy gap between consecutive reads to one host
FRED_GAP = 1.0           # rule 4: FRED's own Crawl-delay: 1
OFFLINE = os.environ.get('TZ53_OFFLINE') == '1'   # replay: any URL not in the ledger aborts
for d in (BODY, HDR, OUT):
    os.makedirs(d, exist_ok=True)

# ---------------------------------------------------------------- fetch layer

def utc(t):
    return dt.datetime.fromtimestamp(t, dt.timezone.utc)

def iso(t):
    return utc(t).strftime('%Y-%m-%dT%H:%M:%SZ')

def ledger():
    if not os.path.exists(LEDGER):
        return []
    return [json.loads(l) for l in open(LEDGER, encoding='utf-8') if l.strip()]

def qurl(u):
    return "'" + u.replace("'", "'\\''") + "'"

def fetch(url, stage, purpose):
    """One request per URL, ever. A URL already in the ledger is returned from it, no request."""
    led = ledger()
    for r in led:
        if r['url'] == url:
            r = dict(r); r['reused'] = True
            return r
    if OFFLINE:
        raise SystemExit('OFFLINE replay asked for a URL not in the ledger: ' + url)
    host = urlparse(url).hostname or ''
    same = [r for r in led if urlparse(r['url']).hostname == host]
    gap = FRED_GAP if host == 'fred.stlouisfed.org' else SAME_HOST_GAP
    if same:
        wait = gap - (time.time() - same[-1]['t_end'])
        if wait > 0:
            time.sleep(wait + 0.05)
    rid = 'r%02d' % (len(led) + 1)
    bp, hp = BODY + '/' + rid, HDR + '/' + rid
    argv = ['curl', '-sS', '-L', '-m', '20', '-o', bp, '-D', hp, '-w', W, url]
    disp = "curl -sS -L -m 20 -o %s -D %s -w '%s' %s" % (bp, hp, W, qurl(url))
    t0 = time.time()
    p = subprocess.run(argv, capture_output=True, text=True)
    t1 = time.time()
    line = p.stdout.rstrip('\n').split('\n')[-1] if p.stdout else ''
    code, size, rest = (line.split(' ', 2) + ['', '', ''])[:3]
    ctype, landing = (rest.rsplit(' ', 1) + [''])[:2] if ' ' in rest else ('', rest)
    rec = dict(id=rid, stage=stage, purpose=purpose, url=url, cmd=disp, t_start=t0, t_end=t1,
               ts=iso(t0), te=iso(t1), secs=round(t1 - t0, 2), exit=p.returncode, code=code,
               bytes=size, ctype=ctype.strip(), landing=landing.strip(),
               stderr=p.stderr.strip()[:300], hops=hops(hp), reused=False)
    with open(LEDGER, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    return rec

def hops(hp):
    try:
        return [l.split()[1] for l in open(hp, errors='replace') if l.startswith('HTTP/') and len(l.split()) > 1]
    except OSError:
        return []

def show(rec):
    """V4: command, status, bytes, content type, landing URL - one line per reading."""
    print('READ %s [%s] %s%s' % (rec['id'], rec['stage'], rec['cmd'], ' (from ledger, no request)' if rec.get('reused') else ''))
    print('     -> %s %s %s %s | curl exit %d | hops %s | %s .. %s (%.2f s)%s' % (
        rec['code'], rec['bytes'], rec['ctype'] or '-', rec['landing'], rec['exit'],
        '>'.join(rec['hops']) or '-', rec['ts'], rec['te'], rec['secs'],
        (' | stderr: ' + rec['stderr']) if rec['stderr'] else ''))

def body(rec):
    try:
        b = open(BODY + '/' + rec['id'], 'rb').read()
    except OSError:
        return b''
    if b[:2] == b'\x1f\x8b':
        try:
            b = gzip.decompress(b)
        except Exception:
            pass
    return b

def text(rec):
    return body(rec).decode('utf-8', 'replace')

def headers(rec):
    try:
        return open(HDR + '/' + rec['id'], errors='replace').read()
    except OSError:
        return ''

def last_header(rec, name):
    """Value of a header in the final response block (after redirects), or None."""
    blocks = re.split(r'\r?\n\r?\n', headers(rec).strip())
    blk = blocks[-1] if blocks else ''
    for l in blk.splitlines():
        if l.lower().startswith(name.lower() + ':'):
            return l.split(':', 1)[1].strip()
    return None

def jbody(rec):
    try:
        return json.loads(body(rec))
    except Exception:
        return None

def keyset(o):
    return sorted(o) if isinstance(o, dict) else '(not an object: %s)' % type(o).__name__

# ---------------------------------------------------------------- robots.txt (RFC 9309)

def robots_parse(txt):
    groups, cur, in_rules, sitemaps = [], None, False, []
    for raw in txt.replace('\r', '\n').split('\n'):
        line = raw.split('#', 1)[0].strip()
        if ':' not in line:
            continue
        k, v = line.split(':', 1)
        k, v = k.strip().lower(), v.strip()
        if k == 'sitemap':
            if v:
                sitemaps.append(v)
            continue
        if k in ('user-agent', 'useragent'):
            if cur is None or in_rules:
                cur = {'agents': [], 'rules': []}
                groups.append(cur)
                in_rules = False
            cur['agents'].append(v)
        elif k in ('allow', 'disallow') and cur is not None:
            cur['rules'].append((k, v, raw.strip()))
            in_rules = True
    return groups, sitemaps

def robots_group(groups, token='curl'):
    mine = [g for g in groups if any(a.lower().split('/')[0].strip() == token for a in g['agents'])]
    if mine:
        return token, [r for g in mine for r in g['rules']]
    star = [g for g in groups if any(a.strip() == '*' for a in g['agents'])]
    if star:
        return '*', [r for g in star for r in g['rules']]
    return None, []

def rule_match(pattern, path):
    if not pattern:
        return False
    anchored = pattern.endswith('$')
    pat = pattern[:-1] if anchored else pattern
    rx = ''.join('.*' if ch == '*' else re.escape(ch) for ch in pat)
    return re.match(rx + ('$' if anchored else ''), path) is not None

def robots_decide(rules, path):
    """Longest match wins, Allow wins a tie; /robots.txt is always allowed."""
    if path == '/robots.txt':
        return True, [], None
    hits = [(k, v, raw) for (k, v, raw) in rules if rule_match(v, path)]
    if not hits:
        return True, [], None
    best = max(hits, key=lambda h: (len(h[1]), h[0] == 'allow'))
    return best[0] == 'allow', [h[2] for h in hits], best[2]

ROBOTS = {}

def origin(url):
    u = urlparse(url)
    return '%s://%s' % (u.scheme.lower(), (u.netloc or '').lower())

def robots_for(org, stage):
    if org in ROBOTS:
        return ROBOTS[org]
    rec = fetch(org + '/robots.txt', stage, 'robots.txt of ' + org)
    show(rec)
    c = rec['code']
    ent = dict(origin=org, rec=rec['id'], code=c, group=None, rules=[], sitemaps=[], crawl_delay=None)
    if c.startswith('2'):
        txt = text(rec)
        groups, sm = robots_parse(txt)
        g, rules = robots_group(groups)
        ent.update(group=g, rules=rules, sitemaps=sm, ngroups=len(groups))
        # crawl-delay of the governing group, as written
        cd, cur_star = None, False
        for raw in txt.replace('\r', '\n').split('\n'):
            line = raw.split('#', 1)[0].strip()
            if ':' not in line:
                continue
            k, v = [s.strip() for s in line.split(':', 1)]
            if k.lower() == 'user-agent':
                cur_star = (v == '*')
            elif k.lower() == 'crawl-delay' and cur_star:
                cd = v
        ent['crawl_delay'] = cd
        ent['basis'] = 'parsed: %d group(s); governing group %s; %d rule line(s); %d Sitemap line(s)' % (
            len(groups), g or 'none', len(rules), len(sm))
    elif c.startswith('4'):
        ent['basis'] = 'robots.txt HTTP %s: unavailable, no restriction (RFC 9309 2.3.1.3)' % c
    else:
        ent['basis'] = 'robots.txt HTTP %s / exit %d: unreachable, complete disallow (RFC 9309 2.3.1.4)' % (c, rec['exit'])
        ent['rules'] = [('disallow', '/', '(unreachable robots.txt: complete disallow)')]
    print('     robots %s: %s' % (org, ent['basis']))
    ROBOTS[org] = ent
    return ent

def decide(url, stage):
    u = urlparse(url)
    ent = robots_for(origin(url), stage)
    path = (u.path or '/') + (('?' + u.query) if u.query else '')
    ok, lines, best = robots_decide(ent['rules'], path)
    print('     robots decision for %s (group %s, from %s): %s; matching lines: %s; deciding line: %s' % (
        path, ent['group'], ent['rec'], 'allowed' if ok else 'DISALLOWED', lines or 'none', best or 'none (no match)'))
    return ok, dict(path=path, group=ent['group'], robots=ent['rec'], matched=lines, deciding=best,
                    decision='allowed' if ok else 'disallowed')

def site_read(url, stage, purpose):
    """Rule 3: robots.txt first; a disallowed path is not requested."""
    ok, perm = decide(url, stage)
    if not ok:
        print('SKIP [%s] %s -> refused on permission' % (stage, url))
        return None, perm
    rec = fetch(url, stage, purpose)
    show(rec)
    lo = origin(rec['landing']) if rec['landing'] else None
    if lo and lo != origin(url):
        print('     NOTE landing origin %s differs from requested origin %s' % (lo, origin(url)))
    return rec, perm

def api_read(url, stage, purpose):
    rec = fetch(url, stage, purpose)
    show(rec)
    return rec

def save(stage, res):
    json.dump(res, open(OUT + '/' + stage + '.json', 'w'), indent=1, ensure_ascii=False, default=str)

def counts(stage, recs):
    att = len(recs)
    ans = sum(1 for r in recs if r is not None and r['code'] not in ('', '000'))
    print('COUNT [%s] attempted %d, answered %d' % (stage, att, ans))
    return att, ans

def isodate_ms(ms):
    return utc(ms / 1000).strftime('%Y-%m-%d')

# ---------------------------------------------------------------- stages

def B2():
    r = api_read('https://ipinfo.io/org', 'B2', 'hosting provider')
    print('B2 body line: %s' % text(r).strip().split('\n')[0])
    counts('B2', [r]); save('B2', dict(rec=r['id'], line=text(r).strip().split('\n')[0]))

def C1():
    a = api_read('https://fapi.binance.com/fapi/v1/ping', 'C1', 'ping')
    print('C1 ping body: %s' % text(a).strip()[:80])
    b = api_read('https://fapi.binance.com/fapi/v1/time', 'C1', 'server time')
    j = jbody(b) or {}
    local_ms = int(round(b['t_end'] * 1000))
    st = j.get('serverTime')
    skew = (st - local_ms) if isinstance(st, int) else None
    print('C1 time: key set %s; serverTime %s; local epoch ms at return %d; skew serverTime - local = %s ms' % (
        keyset(j), st, local_ms, skew))
    counts('C1', [a, b]); save('C1', dict(ping=a['id'], time=b['id'], serverTime=st, local_ms=local_ms, skew_ms=skew))

def a2_xkeys():
    d = json.load(open('/root/crypto-auto/.claude/worktrees/bridge-cse_01D6P1U4thNUnBuHuwmJe2eS/analyst/live.json'))
    return sorted(d['x'][0])

def C2():
    r = api_read('https://fapi.binance.com/fapi/v1/ticker/24hr', 'C2', '24h tickers')
    j = jbody(r)
    rows = len(j) if isinstance(j, list) else None
    ks = sorted(set(k for x in j for k in x)) if rows else []
    same = sum(1 for x in j if sorted(x) == ks) if rows else 0
    x0 = a2_xkeys()
    cmp_ = 'equal' if ks == x0 else 'differ: only in C2 %s; only in A2 x[0] %s' % (sorted(set(ks) - set(x0)), sorted(set(x0) - set(ks)))
    print('C2 rows %s; row key set (%d keys, %d rows carry exactly it): %s' % (rows, len(ks), same, ks))
    print('C2 row key set vs A2 x[0] key set: %s' % cmp_)
    counts('C2', [r]); save('C2', dict(rec=r['id'], rows=rows, keys=ks, rows_with_keys=same, vs_a2=cmp_))

def C3():
    r = api_read('https://fapi.binance.com/fapi/v1/premiumIndex', 'C3', 'premium index')
    j = jbody(r)
    rows = len(j) if isinstance(j, list) else None
    ks = sorted(set(k for x in j for k in x)) if rows else []
    same = sum(1 for x in j if sorted(x) == ks) if rows else 0
    print('C3 rows %s; row key set (%d keys, %d rows carry exactly it): %s' % (rows, len(ks), same, ks))
    print('C3 markPrice among keys: %s; lastFundingRate among keys: %s' % ('markPrice' in ks, 'lastFundingRate' in ks))
    counts('C3', [r]); save('C3', dict(rec=r['id'], rows=rows, keys=ks, rows_with_keys=same))

def C4():
    r = api_read('https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT', 'C4', 'open interest')
    print('C4 key set: %s' % keyset(jbody(r)))
    counts('C4', [r]); save('C4', dict(rec=r['id'], keys=keyset(jbody(r))))

def C5():
    r = api_read('https://fapi.binance.com/fapi/v1/exchangeInfo', 'C5', 'exchange info')
    j = jbody(r) or {}
    syms = j.get('symbols', [])
    read_ms = int(r['t_end'] * 1000)
    ct = collections.Counter(s.get('contractType') for s in syms)
    stt = collections.Counter(s.get('status') for s in syms)
    perp = [s for s in syms if s.get('contractType') == 'PERPETUAL']
    dd = collections.Counter(s.get('deliveryDate') for s in perp)
    top = [(isodate_ms(k) if isinstance(k, int) else k, n) for k, n in dd.most_common(5)]
    lo = read_ms - 7 * 86400 * 1000
    recent = sorted([(isodate_ms(s['onboardDate']) + 'T' + utc(s['onboardDate'] / 1000).strftime('%H:%MZ'), s['symbol'])
                     for s in syms if isinstance(s.get('onboardDate'), int) and lo <= s['onboardDate'] <= read_ms])
    print('C5 top-level key set: %s' % keyset(j))
    print('C5 symbols %d; per contractType %s; per status %s' % (len(syms), dict(ct.most_common()), dict(stt.most_common())))
    print('C5 PERPETUAL rows %d; distinct deliveryDate values %d; five most frequent (ISO UTC date, count): %s' % (len(perp), len(dd), top))
    print('C5 onboardDate within the 7 days before the read (%s .. %s): %d symbol(s): %s' % (
        iso(lo / 1000), iso(read_ms / 1000), len(recent), recent))
    counts('C5', [r]); save('C5', dict(rec=r['id'], n=len(syms), ct=dict(ct), status=dict(stt), perp=len(perp),
                                     dd_distinct=len(dd), dd_top=top, recent=recent))

def C6():
    recs, res = [], {}
    for ep in ('topLongShortPositionRatio', 'globalLongShortAccountRatio', 'takerlongshortRatio', 'openInterestHist'):
        r = api_read('https://fapi.binance.com/futures/data/%s?symbol=BTCUSDT&period=1h&limit=2' % ep, 'C6', ep)
        j = jbody(r)
        rows = len(j) if isinstance(j, list) else None
        ks = sorted(set(k for x in j for k in x)) if rows else keyset(j)
        print('C6 %s: status %s; rows %s; key set %s' % (ep, r['code'], rows, ks))
        recs.append(r); res[ep] = dict(rec=r['id'], code=r['code'], rows=rows, keys=ks)
    counts('C6', recs); save('C6', res)

def C7():
    r = api_read('https://api.binance.com/api/v3/ping', 'C7', 'spot ping')
    print('C7 status %s; body %s' % (r['code'], text(r).strip()[:80]))
    counts('C7', [r]); save('C7', dict(rec=r['id'], code=r['code']))

def locs_lastmods(xml):
    """(loc, lastmod or None) per <url>/<sitemap> element."""
    out = []
    for m in re.finditer(r'<(url|sitemap)>(.*?)</\1>', xml, re.S):
        blk = m.group(2)
        loc = re.search(r'<loc>\s*(.*?)\s*</loc>', blk, re.S)
        lm = re.search(r'<lastmod>\s*(.*?)\s*</lastmod>', blk, re.S)
        out.append((html.unescape(loc.group(1)) if loc else None, lm.group(1) if lm else None))
    return out

def parse_lastmod(s):
    s = s.strip()
    for fmt in ('%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%S.%f%z', '%Y-%m-%dT%H:%M%z', '%Y-%m-%d'):
        try:
            t = dt.datetime.strptime(s.replace('Z', '+0000'), fmt)
            if t.tzinfo is None:
                t = t.replace(tzinfo=dt.timezone.utc)
            return t
        except ValueError:
            pass
    return None

def C8():
    recs, res = [], {}
    org = 'https://www.binance.com'
    for p in ('/bapi/composite/v1/public/cms/article/list/query', '/sitemap_output/'):
        ok, perm = decide(org + p, 'C8')
        res[p] = perm
    ent = ROBOTS[org]
    recs.append(next(r for r in ledger() if r['id'] == ent['rec']))
    print('C8 robots.txt Sitemap lines: %d' % len(ent['sitemaps']))
    res['sitemaps_total'] = len(ent['sitemaps'])
    idx = [s for s in ent['sitemaps'] if s.endswith('sitemap_SupportAndAnnouncement_index.xml')]
    print('C8 Sitemap lines ending sitemap_SupportAndAnnouncement_index.xml: %s' % idx)
    res['index_declared'] = idx
    if not res['/sitemap_output/']['decision'] == 'allowed' or not idx:
        print('C8 index not read: %s' % ('/sitemap_output/ disallowed' if idx else 'not declared'))
        counts('C8', recs); save('C8', res); return
    ri, perm = site_read(idx[0], 'C8', 'support-and-announcement sitemap index')
    recs.append(ri)
    if ri is None:
        counts('C8', recs); save('C8', res); return
    kids = locs_lastmods(text(ri))
    en = [k for k, _ in kids if k and k.endswith('_en_0.xml')]
    print('C8 index: %d child sitemap(s); children ending _en_0.xml: %s' % (len(kids), en))
    res['index'] = dict(rec=ri['id'], children=len(kids), en=en)
    if not en:
        counts('C8', recs); save('C8', res); return
    rc, perm = site_read(en[0], 'C8', 'English announcement child sitemap')
    recs.append(rc)
    if rc is None:
        counts('C8', recs); save('C8', res); return
    urls = locs_lastmods(text(rc))
    lms = [lm for _, lm in urls if lm]
    parsed = [parse_lastmod(x) for x in lms]
    parsed_ok = [t for t in parsed if t]
    newest = max(parsed_ok) if parsed_ok else None
    hours = round((rc['t_end'] - newest.timestamp()) / 3600, 2) if newest else None
    days = sorted(set(t.astimezone(dt.timezone.utc).strftime('%Y-%m-%d') for t in parsed_ok))
    print('C8 child: URLs %d; URLs with lastmod %d; distinct lastmod values %d; distinct lastmod dates (UTC day) %d; '
          'unparsed lastmod %d' % (len(urls), len(lms), len(set(lms)), len(days), len(parsed) - len(parsed_ok)))
    print('C8 child: newest lastmod %s; hours between it and the read (%s): %s' % (
        newest.isoformat() if newest else None, rc['te'], hours))
    print('C8 child: oldest lastmod date %s; newest lastmod date %s' % (days[0] if days else None, days[-1] if days else None))
    ann = [u for u, _ in urls if u and '/support/announcement/' in u]
    print('C8 child: <loc> values containing /support/announcement/: %d; the first: %s' % (len(ann), ann[0] if ann else None))
    res['child'] = dict(rec=rc['id'], urls=len(urls), with_lastmod=len(lms), distinct_values=len(set(lms)),
                        distinct_days=len(days), newest=newest.isoformat() if newest else None, hours=hours,
                        first_ann=ann[0] if ann else None, n_ann=len(ann))
    if ann:
        ra, perm = site_read(ann[0], 'C8', 'first announcement page of the English child')
        recs.append(ra)
        if ra is not None:
            print('C8 announcement page: status %s; bytes %s; content type %s' % (ra['code'], ra['bytes'], ra['ctype']))
            res['announcement'] = dict(rec=ra['id'], code=ra['code'], bytes=ra['bytes'], ctype=ra['ctype'])
    counts('C8', recs); save('C8', res)

def D1():
    r = api_read('https://api.telegram.org/', 'D1', 'telegram root')
    print('D1 status %s; hops %s; landing %s; first Location header: %s' % (
        r['code'], '>'.join(r['hops']), r['landing'], first_location(r)))
    counts('D1', [r]); save('D1', dict(rec=r['id'], code=r['code'], hops=r['hops'], landing=r['landing']))

def first_location(rec):
    for l in headers(rec).splitlines():
        if l.lower().startswith('location:'):
            return l.split(':', 1)[1].strip()
    return None

def D2():
    r = api_read('https://api.telegram.org/bot0:invalid/getMe', 'D2', 'getMe with an invalid token')
    print('D2 status %s; body verbatim: %s' % (r['code'], text(r)))
    counts('D2', [r]); save('D2', dict(rec=r['id'], code=r['code'], body=text(r)))

def E1():
    recs, res = [], {}
    org = 'https://fred.stlouisfed.org'
    ent = robots_for(org, 'E1')
    recs.append(next(r for r in ledger() if r['id'] == ent['rec']))
    print('E1 robots Crawl-delay in the * group: %s' % ent['crawl_delay'])
    res['robots'] = dict(rec=ent['rec'], crawl_delay=ent['crawl_delay'], group=ent['group'])
    for sid in ('WALCL', 'WTREGEN', 'RRPONTSYD', 'WRESBAL'):
        r, perm = site_read('%s/graph/fredgraph.csv?id=%s' % (org, sid), 'E1', 'FRED series ' + sid)
        recs.append(r)
        if r is None:
            res[sid] = dict(perm=perm); continue
        lines = [l for l in text(r).splitlines() if l.strip()]
        hdr = lines[0] if lines else None
        last = lines[-1].split(',')[0] if len(lines) > 1 else None
        print('E1 %s: status %s; rows %d (data rows %d); header line %s; date of the last observation %s' % (
            sid, r['code'], len(lines), max(len(lines) - 1, 0), hdr, last))
        res[sid] = dict(rec=r['id'], code=r['code'], rows=len(lines), header=hdr, last=last, perm=perm)
    fred = [x for x in ledger() if urlparse(x['url']).hostname == 'fred.stlouisfed.org']
    gaps = [round(b['t_start'] - a['t_end'], 2) for a, b in zip(fred, fred[1:])]
    print('E1 gaps between consecutive FRED reads (end of one to start of the next), s: %s' % gaps)
    res['gaps'] = gaps
    counts('E1', recs); save('E1', res)

MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
          'October', 'November', 'December')

def fomc_parse(page):
    """Meetings under the '2026 FOMC Meetings' heading, from fomc-meeting__month / __date blocks."""
    i = page.find('2026 FOMC Meetings')
    if i < 0:
        return None, []
    j = page.find('FOMC Meetings', i + len('2026 FOMC Meetings'))
    sec = page[i:j if j > 0 else len(page)]
    def strip(s):
        return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()
    months = [strip(m) for m in re.findall(r'class="[^"]*fomc-meeting__month[^"]*"[^>]*>(.*?)</div>', sec, re.S)]
    dates = [strip(m) for m in re.findall(r'class="[^"]*fomc-meeting__date[^"]*"[^>]*>(.*?)</div>', sec, re.S)]
    return (len(sec), list(zip(months, dates)) if len(months) == len(dates) else dict(months=months, dates=dates))

def E2():
    recs, res = [], {}
    org = 'https://www.federalreserve.gov'
    r, perm = site_read(org + '/monetarypolicy/fomccalendars.htm', 'E2', 'FOMC calendars')
    recs.insert(0, next(x for x in ledger() if x['id'] == ROBOTS[org]['rec']))
    recs.append(r)
    if r is not None:
        n, meets = fomc_parse(text(r))
        cnt = len(meets) if isinstance(meets, list) else None
        print('E2 fomccalendars: status %s; section under "2026 FOMC Meetings" %s chars; meetings parsed %s' % (r['code'], n, cnt))
        print('E2 meetings as read (month | date): %s' % meets)
        res['fomc'] = dict(rec=r['id'], code=r['code'], count=cnt, meetings=meets)
    r2, perm2 = site_read(org + '/releases/h41/current/h41.htm', 'E2', 'H.4.1 current')
    recs.append(r2)
    if r2 is not None:
        t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', text(r2))))
        k = t.find('Release Date:')
        m = re.search(r'([A-Z][a-z]+\.? \d{1,2}, \d{4})', t[k:k + 200]) if k >= 0 else None
        print('E2 h41: status %s; bytes %s; "Release Date:" found %s; first date after it: %s' % (
            r2['code'], r2['bytes'], k >= 0, m.group(1) if m else None))
        res['h41'] = dict(rec=r2['id'], code=r2['code'], bytes=r2['bytes'], release=m.group(1) if m else None)
    counts('E2', recs); save('E2', res)

def E3():
    r = api_read('https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance?sort=-record_date&page%5Bsize%5D=2', 'E3', 'DTS operating cash balance')
    j = jbody(r) or {}
    data = j.get('data') or []
    ks = sorted(set(k for x in data for k in x))
    dates = sorted(set(x.get('record_date') for x in data))
    print('E3 status %s; top-level key set %s; rows %d; newest record_date %s; row key set %s' % (
        r['code'], keyset(j), len(data), dates[-1] if dates else None, ks))
    counts('E3', [r]); save('E3', dict(rec=r['id'], code=r['code'], rows=len(data), newest=dates[-1] if dates else None, keys=ks))

def E4():
    a = api_read('https://stablecoins.llama.fi/stablecoins?includePrices=false', 'E4', 'stablecoin list')
    j = jbody(a) or {}
    pa = j.get('peggedAssets') or []
    print('E4 stablecoins: status %s; bytes %s; top-level key set %s; peggedAssets %d; key set of the first %s' % (
        a['code'], a['bytes'], keyset(j), len(pa), keyset(pa[0]) if pa else None))
    b = api_read('https://stablecoins.llama.fi/stablecoincharts/all', 'E4', 'stablecoin supply chart')
    k = jbody(b)
    rows = len(k) if isinstance(k, list) else None
    ds = [int(x['date']) for x in k if isinstance(x, dict) and str(x.get('date', '')).isdigit()] if rows else []
    newest = iso(max(ds)) if ds else None
    print('E4 stablecoincharts/all: status %s; rows %s; row key set of the last %s; newest date %s' % (
        b['code'], rows, keyset(k[-1]) if rows else None, newest))
    counts('E4', [a, b]); save('E4', dict(a=a['id'], n=len(pa), b=b['id'], rows=rows, newest=newest))

def plain(s):
    """Tags and comments stripped, entities unescaped, whitespace collapsed."""
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<!--.*?-->', '', s, flags=re.S)))).strip()

DATE_RX = r'([A-Z][a-z]{2,8}\.? \d{1,2}, \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})'

def ishares_datum(t):
    """The keyFundFacts-sharesOutstanding datapoint and its -asOf sibling, by attribute."""
    dm = re.search(r'<[^>]*webqc-datapoint="keyFundFacts-sharesOutstanding"[^>]*>(.*?)</', t, re.S)
    am = re.search(r'<[^>]*webqc-datapoint="keyFundFacts-sharesOutstanding-asOf"[^>]*>(.*?)</div>', t, re.S)
    present = bool(dm and re.search(r'\d', plain(dm.group(1))))
    asof = None
    if am:
        m = re.search(r'[Aa]s of:?\s*' + DATE_RX, plain(am.group(1)))
        asof = m.group(1) if m else None
    return present, asof, 'datapoint attribute keyFundFacts-sharesOutstanding; as-of from its -asOf datapoint'

def label_datum(t, label='Shares Outstanding'):
    """Label in served HTML; datum = a number right after the label's element; as-of = the nearest
    'as of <date>' statement within 600 chars of served text before the label, else 300 after."""
    i = t.find(label)
    if i < 0:
        return False, None, 'label absent'
    after = plain(t[i + len(label):i + len(label) + 400])
    present = bool(re.match(r'[\$]?\d[\d,\.]*', after))
    before = plain(t[max(0, i - 1500):i])[-600:]
    mb = list(re.finditer(r'[Aa]s of:?\s*' + DATE_RX, before))
    if mb:
        return present, mb[-1].group(1), 'nearest preceding as-of statement, %d chars of served text before the label' % (len(before) - mb[-1].start())
    ma = re.search(r'[Aa]s of:?\s*' + DATE_RX, after[:300])
    if ma:
        return present, ma.group(1), 'as-of statement %d chars after the label' % ma.start()
    return present, None, 'no as-of statement within the window'

def E5():
    recs, res = [], {}
    pages = ['https://www.ishares.com/us/products/333011/ishares-bitcoin-trust-etf',
             'https://www.ishares.com/us/products/337614/ishares-ethereum-trust-etf',
             'https://bitbetf.com/',
             'https://www.grayscale.com/funds/grayscale-bitcoin-trust']
    for o in ('https://www.ishares.com', 'https://bitbetf.com', 'https://www.grayscale.com'):
        ent = robots_for(o, 'E5')
        recs.append(next(x for x in ledger() if x['id'] == ent['rec']))
    for u in pages:
        r, perm = site_read(u, 'E5', 'ETF issuer page')
        recs.append(r)
        if r is None:
            res[u] = dict(perm=perm); continue
        t = text(r)
        if 'ishares.com' in u:
            marker = 'keyFundFacts-sharesOutstanding'
            present, asof, how = ishares_datum(t)
        else:
            marker = 'Shares Outstanding'
            present, asof, how = label_datum(t)
        n = t.count(marker)
        mit = last_header(r, 'x-vercel-mitigated') or last_header(r, 'cf-mitigated') or last_header(r, 'x-amzn-waf-action')
        print('E5 %s: status %s; bytes %s; landing %s; mitigation header %s; "%s" occurrences %d; '
              'shares-outstanding datum in served HTML: %s; as-of date as read: %s (%s)' % (
              u, r['code'], r['bytes'], r['landing'], mit, marker, n, present, asof, how))
        res[u] = dict(rec=r['id'], code=r['code'], bytes=r['bytes'], landing=r['landing'], marker=marker,
                      occurrences=n, present=present, asof=asof, how=how, mitigation=mit)
    counts('E5', recs); save('E5', res)

def E6():
    recs, res = [], {}
    ent = robots_for('https://farside.co.uk', 'E6')
    recs.append(next(x for x in ledger() if x['id'] == ent['rec']))
    for u in ('https://farside.co.uk/btc/', 'https://farside.co.uk/eth/'):
        r, perm = site_read(u, 'E6', 'Farside flow page')
        recs.append(r)
        if r is None:
            res[u] = dict(perm=perm); continue
        cfm = last_header(r, 'cf-mitigated')
        has = '<table' in text(r)
        print('E6 %s: status %s; cf-mitigated %s; body contains <table: %s' % (u, r['code'], cfm, has))
        res[u] = dict(rec=r['id'], code=r['code'], cf_mitigated=cfm, table=has)
    counts('E6', recs); save('E6', res)

def E7():
    recs, res = [], {}
    for p in ('BTC-USD', 'ETH-USD'):
        r = api_read('https://api.exchange.coinbase.com/products/%s/ticker' % p, 'E7', 'Coinbase ticker ' + p)
        j = jbody(r) or {}
        tb = j.get('time') if isinstance(j, dict) else None
        sec = None
        if tb:
            t = parse_lastmod(re.sub(r'\.(\d{6})\d*', r'.\1', tb))
            sec = round(r['t_end'] - t.timestamp(), 3) if t else None
        print('E7 %s: status %s; key set %s; body time present %s; seconds between body time and the read (%s): %s' % (
            p, r['code'], keyset(j), bool(tb), r['te'], sec))
        recs.append(r); res[p] = dict(rec=r['id'], code=r['code'], keys=keyset(j), secs=sec)
    counts('E7', recs); save('E7', res)

if __name__ == '__main__':
    for st in sys.argv[1:]:
        print('=== %s' % st)
        globals()[st]()
        sys.stdout.flush()
```

`extra.py`, `v34.py`, `selftest.py`, `blocks.py` and `run.sh`, verbatim:

```python
# Offline extras from saved bodies r04 (C2), r07 (C5) and A2's payload: counts and dates only.
import json, collections, datetime as dt
L = {json.loads(l)['id']: json.loads(l) for l in open('/tmp/tz53/ledger.jsonl')}
ei = json.load(open('/tmp/tz53/body/r07')); tk = json.load(open('/tmp/tz53/body/r04'))
pl = json.load(open('/root/crypto-auto/.claude/worktrees/bridge-cse_01D6P1U4thNUnBuHuwmJe2eS/analyst/live.json'))
read_ms = int(L['r07']['t_end'] * 1000); NEVER = 4133404800000
d = lambda ms: dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).strftime('%Y-%m-%d')
by = {s['symbol']: s for s in ei['symbols']}
perp = [s for s in ei['symbols'] if s['contractType'] == 'PERPETUAL']
fut = sorted((d(s['deliveryDate']), s['status']) for s in perp if s['deliveryDate'] != NEVER and s['deliveryDate'] > read_ms)
past = [s for s in perp if s['deliveryDate'] != NEVER and s['deliveryDate'] <= read_ms]
print('C5+ PERPETUAL rows with deliveryDate 2100-12-25: %d; before the read: %d (status %s); after the read and not 2100-12-25: %d' % (
    sum(s['deliveryDate'] == NEVER for s in perp), len(past), dict(collections.Counter(s['status'] for s in past)), len(fut)))
print('C5+ the future deliveryDate values among PERPETUAL rows (date, status, count): %s' % sorted(collections.Counter(fut).items()))
print('C5+ status per contractType: %s' % {ct: dict(collections.Counter(s['status'] for s in ei['symbols'] if s['contractType'] == ct)) for ct in sorted(set(s['contractType'] for s in ei['symbols']))})
c2 = set(r['symbol'] for r in tk); x = set(r['symbol'] for r in pl['x']); c = set(r['s'] for r in pl['c'])
print('C2+ ticker symbols %d, by exchangeInfo contractType %s, absent from exchangeInfo %d' % (
    len(c2), dict(sorted(collections.Counter(by[s]['contractType'] if s in by else '(absent)' for s in c2).items())), len(c2 - set(by))))
print('C2+ A2 x symbols %d; in both %d; only in A2 x %d; only in C2 %d' % (len(x), len(x & c2), len(x - c2), len(c2 - x)))
print('C2+ A2 c symbols %d; of them in C2 %d' % (len(c), len(c & c2)))
print('C5+ symbols of the future non-2100 deliveryDate rows: %s' % sorted((d(s['deliveryDate']), s['symbol']) for s in perp if s['deliveryDate'] != NEVER and s['deliveryDate'] > read_ms))
print('C2+ the symbol only in C2: %s, onboardDate %s' % (sorted(c2 - x), [dt.datetime.fromtimestamp(by[s]['onboardDate'] / 1000, dt.timezone.utc).strftime('%Y-%m-%dT%H:%MZ') for s in sorted(c2 - x)]))
print('C5+ PENDING_TRADING row: %s' % [(s['symbol'], s['contractType'], dt.datetime.fromtimestamp(s['onboardDate'] / 1000, dt.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')) for s in ei['symbols'] if s['status'] == 'PENDING_TRADING'])
```

```python
# V3/V4 over the ledger: completeness, one form, one request per URL, sequential reads.
import json, re, collections
L = [json.loads(l) for l in open('/tmp/tz53/ledger.jsonl')]
form = re.compile(r"^curl -sS -L -m 20 -o /tmp/tz53/body/(r\d\d) -D /tmp/tz53/hdr/\1 -w '%\{http_code\} %\{size_download\} %\{content_type\} %\{url_effective\}\\n' '[^']+'$")
complete = sum(all(r[k] not in ('', None) for k in ('cmd', 'code', 'bytes', 'ctype', 'landing')) for r in L)
inform = sum(bool(form.match(r['cmd'])) for r in L)
dups = [u for u, n in collections.Counter(r['url'] for r in L).items() if n > 1]
overl = sum(1 for a, b in zip(L, L[1:]) if b['t_start'] < a['t_end'])
print('V4 ledger records %d; with command, status, bytes, content type and landing all non-empty: %d; in the rule-1 form exactly: %d' % (len(L), complete, inform))
print('V4 duplicate URLs: %d; overlapping reads: %d; first read %s; last read ends %s' % (len(dups), overl, L[0]['ts'], L[-1]['te']))
print('V4 curl exit codes: %s; statuses: %s' % (dict(collections.Counter(r['exit'] for r in L)), dict(sorted(collections.Counter(r['code'] for r in L).items()))))
per = collections.OrderedDict()
for r in L:
    s = per.setdefault(r['stage'], [0, 0]); s[0] += 1; s[1] += r['code'] not in ('', '000')
print('V3 per stage (attempted, answered): %s; total %d, %d' % (dict(per), sum(v[0] for v in per.values()), sum(v[1] for v in per.values())))
print('V3 stages with zero attempted: %d' % sum(1 for v in per.values() if v[0] == 0))
```

```python
# Offline self-test of probe.py's robots.txt decision (RFC 9309 longest match, Allow wins a tie).
import re, sys
exec(open('/tmp/tz53/probe.py').read().split("if __name__ == '__main__':")[0])
fixture = """User-agent: Googlebot
Disallow: /x/
User-agent: *
Disallow: */bapi/
Allow: */bapi/fe/
Allow: */sitemap_output/
Disallow: /en/private$
"""
groups, sitemaps = robots_parse(fixture)
group, rules = robots_group(groups)
cases = [('/bapi/composite/v1/public/cms/article/list/query', False), ('/bapi/fe/x', True), ('/sitemap_output/', True),
         ('/en/private', False), ('/en/private2', True), ('/x/', True), ('/robots.txt', True), ('/en/bapi/', False)]
passed = 0
for path, expected in cases:
    got = robots_decide(rules, path)[0]
    passed += got == expected
    print('%-52s expected %-5s got %-5s %s' % (path, expected, got, 'PASS' if got == expected else 'FAIL'))
print('governing group %s; %d of %d PASS' % (group, passed, len(cases)))
sys.exit(0 if passed == len(cases) else 1)
```

```python
# The four scratch files the TZ dictates, compared byte for byte with the TZ's own code blocks.
import re
tz = open('CryptoTZ/TZ-53-automation-and-hunter-lanes-vps-reading.md').read()
blocks = re.findall(r'^( *)```\n(.*?)^\1```', tz, re.M | re.S)
def get(i):
    ind, b = blocks[i]
    return '\n'.join(l[len(ind):] if l.startswith(ind) else l for l in b.rstrip('\n').split('\n')) + '\n'
for i, path in ((0, '/tmp/tz53/mask.sed'), (1, '/tmp/tz53/unit/probe.sh'), (3, '/tmp/tz53/leak.re'), (4, '/tmp/tz53/fixture.txt')):
    print('TZ code block %d of %d vs %s: %s' % (i + 1, len(blocks), path, 'identical' if open(path).read() == get(i) else 'DIFFERENT'))
```

```sh
# run "<cmd>": print the command, its combined output and exit code, all through the mask
run() { { printf '$ %s\n' "$1"; bash -c "$1" 2>&1; printf '[exit %d]\n' $?; } | sed -E -f /tmp/tz53/mask.sed; }
```

---

## Validation

### V1 — The mask, on a fixture, with its negative control

The pattern and the fixture are the TZ's own (V1's two blocks), cut by code and byte-identical
(Instrument); they are cited here and not reprinted.

```
$ grep -cE -f /tmp/tz53/leak.re /tmp/tz53/fixture.txt
4
[exit 0]
$ sed -E -f /tmp/tz53/mask.sed /tmp/tz53/fixture.txt | grep -cE -f /tmp/tz53/leak.re
0
[exit 1]
$ sed -E -f /tmp/tz53/mask.sed /tmp/tz53/fixture.txt | grep -cxF "$(sed -n 5p /tmp/tz53/fixture.txt)"
1
[exit 0]
$ md5sum /tmp/tz53/mask.sed /tmp/tz53/leak.re /tmp/tz53/fixture.txt /tmp/tz53/unit/probe.sh
ac6307fe15d7cb8ef1952891842d2735  /tmp/tz53/mask.sed
12b41c41721c44f094bd52e841c4290b  /tmp/tz53/leak.re
c8e03622727cbaf6f9db611db7fe4bba  /tmp/tz53/fixture.txt
b33d1ce0959d7c74058cf1e55302a544  /tmp/tz53/unit/probe.sh
[exit 0]
```

| Check | Expected | Read |
|---|---|---|
| leak scan over the fixture — the negative control | `4` | `4` |
| the same scan over the masked fixture | `0` | `0` |
| the fifth line survives the mask byte for byte | `1` | `1` |

(`grep --count` exits 1 when it counts zero matches; that is the second row's `[exit 1]`.)

### V2 — The report is clean

Run over this file in its final form, after every other block was filled and before the commit:

```
$ grep -cE -f /tmp/tz53/leak.re CryptoReports/TZ-53-automation-and-hunter-lanes-vps-reading-report.md
0
```

V1's first row is this check's negative control.

### V3 — Counts are counts

Network stages, from the ledger:

```
V4 ledger records 41; with command, status, bytes, content type and landing all non-empty: 41; in the rule-1 form exactly: 41
V4 duplicate URLs: 0; overlapping reads: 0; first read 2026-10-01T08:06:55Z; last read ends 2026-10-01T08:08:11Z
V4 curl exit codes: {0: 41}; statuses: {'200': 34, '401': 1, '403': 2, '404': 1, '405': 1, '429': 2}
V3 per stage (attempted, answered): {'B2': [1, 1], 'C1': [2, 2], 'C2': [1, 1], 'C3': [1, 1], 'C4': [1, 1], 'C5': [1, 1], 'C6': [4, 4], 'C7': [1, 1], 'C8': [4, 4], 'D1': [1, 1], 'D2': [1, 1], 'E1': [5, 5], 'E2': [3, 3], 'E3': [1, 1], 'E4': [2, 2], 'E5': [7, 7], 'E6': [3, 3], 'E7': [2, 2]}; total 41, 41
V3 stages with zero attempted: 0
```

| Stage | Attempted | Answered |
|---|---:|---:|
| A2 | 2 commands | 2 |
| A3 | 4 commands | 4 |
| B1 | 9 commands | 9 |
| B2 | 1 request | 1 |
| B3 | 2 commands, plus 1 and 4 extra | 2 (+5) |
| B4 | 4 commands; 3 user-manager reads not applicable to root | 4 |
| B5 | 14 commands, plus 4 extra | 14 (+4) |
| B6 | 1 unit; 6 reading commands, plus 15 more (5 before, 7 after and extra, 3 accounting) | 1 unit, 6 (+15) |
| C1–C8 | 15 requests (C1 2, C2–C5 1 each, C6 4, C7 1, C8 4) | 15 |
| D1–D2 | 2 requests | 2 |
| E1–E7 | 23 requests (E1 5, E2 3, E3 1, E4 2, E5 7, E6 3, E7 2) | 23 |

«Answered» for a local command means it completed and printed its reading. An exit code that is
itself the reading, such as `crontab -l` exiting 1, counts as answered. No stage attempted zero.

### V4 — Evidence

Every reading line carries command, status, bytes, content type and landing URL, through the mask:
41 of 41 ledger records are complete, 41 of 41 commands are in rule 1's form exactly, there are 0
duplicate URLs and 0 overlapping reads (V3 block above). Each stage's log prints the line itself
(`READ … -> <status> <bytes> <content type> <landing>`). Every local block was printed by
`run.sh`'s helper through the same mask.

**Replay on the final instrument text.** `probe.py` changed after the network stages, when E5's
parser was revised (Deviation 1). Every stage was then re-run with `TZ53_OFFLINE=1`, which aborts
on any URL not already in the ledger. The run exited 0, served 41 of 41 reads from the ledger, and
reproduced **18 of 18 result files byte for byte**. The ledger stayed at 41 lines.

### V5 — Known answers

| Reading | Expected | Read | |
|---|---|---|---|
| C1 ping | `200` | `200` | match |
| C8 `/bapi/composite/v1/public/cms/article/list/query` | disallowed — `Disallow: */bapi/`, `*/bapi/fe/` the only carve-out | disallowed — deciding `Disallow: */bapi/`; `Allow: */bapi/fe/` is the `*` group's only `Allow` under `/bapi/` | match |
| C8 `/sitemap_output/` | allowed — `Allow: */sitemap_output/` | allowed — deciding `Allow: */sitemap_output/` | match |
| D1 | `302` to `https://core.telegram.org/bots` | hops `302>200`, `Location: https://core.telegram.org/bots` | match |
| D2 | `401`, the body quoted | `401`, the body byte-identical (below) | match |
| E1 `robots.txt` | `/graph/fredgraph.csv` not disallowed for `*`; `Crawl-delay: 1` | no `*` line matches; `Crawl-delay: 1` | match |
| E2 meetings | `8` | `8` | match |
| E5 iShares pages | datapoint present, with an as-of date | present on both, as of Sep 30, 2026 | match — the date is one day later than the Architect's «Sep 29, 2026»; the page's date moved, not the host |

```
$ awk '/^User-agent: \*/{f=1} /^# Sitemaps/{f=0} f' /tmp/tz53/body/r13 | grep --extended-regexp '^User-agent|^Allow: /$|bapi|sitemap_output'
User-agent: *
Allow: /
Allow: */bapi/fe/
Allow: */sitemap_output/
Disallow: */bapi/
[exit 0]
$ python3 -c 'import sys; b = open("/tmp/tz53/body/r18").read(); e = "{\"ok\":false,\"error_code\":401,\"description\":\"Unauthorized: invalid token specified\"}"; print("D2 body equals the expected string:", b == e)'
D2 body equals the expected string: True
[exit 0]
```

### V6 — Nothing but the report, and nothing left behind

Run with this report in place and before the commit:

```
$ git status --porcelain
?? CryptoReports/TZ-53-automation-and-hunter-lanes-vps-reading-report.md
[exit 0]
$ systemctl list-units --all 'tz53-*' --no-legend | wc -l
0
[exit 0]
$ git ls-remote origin 'refs/heads/tz-53-*'
[exit 0]
$ git diff --stat HEAD
[exit 0]
```

A3's user is root, so the unit was a system unit, and the system manager's list is the one read.
The unit was also collected straight after B6 (B6-after block). No production file, bench or
workflow was touched, so no bench ran. The empty `git diff` against `HEAD` is the
no-regression evidence.

### V7 — Hygiene

Run after V2, as the last act before the commit:

```
$ rm -rf /tmp/tz53 && ls /tmp/tz53
ls: cannot access '/tmp/tz53': No such file or directory
```

Nothing but this report is committed (V6).

---

## Test Results

| Item | Result |
|---|---|
| V1 mask | **4 · 0 · 1**, as expected |
| V2 report clean | **0** hits |
| V3 counts | every stage attempted > 0; 41 requests, 41 answered |
| V4 evidence | 41 of 41 ledger records complete; 41 of 41 in rule 1's form; 0 duplicates; 0 overlaps |
| V5 known answers | **8 of 8 match**; no host changed; the iShares as-of date moved by one day |
| V6 nothing left | porcelain lists exactly the report; 0 `tz53-*` units; no `tz-53-*` ref; empty diff |
| V7 hygiene | `/tmp/tz53` removed |
| Self-test (extra) | 8 of 8 PASS |
| Replay (extra) | 18 of 18 result files identical; ledger unchanged at 41 |

---

## Deviations

1. **E5's as-of parser was revised after the reads, and the pages were reclassified from saved
   bodies with no request.** The first parser looked 1 500 characters past the first marker, and
   both issuers place their date outside that window:
   - iShares carries its date in a sibling datapoint, `keyFundFacts-sharesOutstanding-asOf`,
     behind an inline SVG.
   - Bitwise states it once for the block, «Data as of …», before the label.

   The first parser's lines are printed in the E5–E7 log, and they read `None` for all four as-of
   dates. The final rules, applied uniformly:
   - **iShares:** the datum is the element whose `webqc-datapoint` is exactly
     `keyFundFacts-sharesOutstanding` and which holds a digit. Its date is the
     `keyFundFacts-sharesOutstanding-asOf` datapoint.
   - **Other pages:** the label «Shares Outstanding» followed by a number. The date is the nearest
     «as of <date>» within 600 characters of served text before the label, else within 300
     after it.

   The replay (V4) reproduces the final classification.
2. **Readings beyond the TZ's list.** All are local and read-only, and each is marked «extra»
   where it appears:
   - B3: the common git directory, 3 commands, and the worktree count.
   - B5: the binary's type, 4 commands.
   - B6:
     - the whole-option count;
     - `push.err` in full;
     - before and after snapshots: unit count, `~/.claude.json`'s mtime, the projects directory
       count;
     - the cgroup accounting, 3 commands.
   - C2 and C5: the offline extras, with no request.
   - The client block (curl version, proxy variables, curlrc).
   - The fallback path check in B5 ran although `command -v claude` was non-empty.
3. **A2's command ran twice, both times locally and read-only**, at 08:02:39Z and 08:02:49Z. The
   second form adds the per-row key-set counts, and the record carries it. The first printed the
   union of `c`'s keys, the same nine.
4. **Where the TZ is silent, these readings were chosen**, so the Architect can overrule any one
   in a line:
   - **A2:** `c` is a list, so its «key set» is `c[0]`'s, with the count of rows sharing it.
   - **B3:** in a worktree, `.git` is a regular file, so its `stat` dates the worktree.
   - **B4:** the three user-manager reads were not run for root, as the TZ conditions them.
   - **B6:** «occurs» counts lines containing the option string.
   - **C1:** the local epoch ms is taken the instant `curl` returned, so the skew includes the
     response's transit (0.28 s request).
   - **C5:** «the seven days before the read» is `[t − 7 × 86 400 s, t]`, where `t` is when the
     response returned.
   - **C8:** «distinct `lastmod` dates» is printed both as raw values and as UTC days (1 and 1).
   - **E1:** «rows» is the CSV's lines including the header; data rows are printed beside.
   - **Robots:** the product token `curl` falls back to `*` («`*` for curl»). Under RFC 9309,
     Grayscale's challenged 429 robots.txt maps to no restriction because rule 3 says any 4xx
     does (Finding 11).
   - **Pacing:** a 1 s gap was kept between consecutive reads to every host, not only to FRED.

---

## Pre-existing Issues

1. **The map's row «Executor has no GitHub API access» no longer describes this machine.**
   `SYSTEM-MAP-CRYPTOCALCUL.md:2811` reads it **closed, deliberately**, on «`gh` is absent and no
   PAT exists». B5 reads gh 2.45.0 installed, and `gh auth status` exits 0. TZ-49's report (line
   904) and TZ-50's (line 631) already record `gh` authenticated and used to open a pull request.
   The row's conclusion, that the hosted gate is the audit's to read, does not rest on the tool's
   absence alone. Reported, not acted on.
2. **Methodology §6a reads a path this host's robots.txt disallows to `*`.**
   `ANALYST-INSTRUCTIONS.md:2575` reads
   `https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&pageNo=1&pageSize=50`
   «on EVERY run, first». C8 reads `Disallow: */bapi/` as the deciding line for that path in the
   `*` group, which is the Architect's own V5 row. Under this TZ's rule 3 the path is
   `refused on permission`, and §6a states no robots rule for that lane. Recorded, not acted on.
3. **No fingerprint difference.** The map's four files and the TZ's two added files all match
   (`## Fingerprints`), so no quote in the TZ has moved.

---

## Remaining Risks

- **The transient unit reproduces a scheduler's environment, not a finished service's.**
  - It ran as root, with `HOME` and `PATH` copied from this session.
  - It had no `User=`, `WorkingDirectory=`, `EnvironmentFile=` or restart policy.
  - It was started by `systemd-run --wait` from a live session.

  A timer-started service with its own environment can differ on any of these.
- **A dry-run push proves authentication, not permission to push to `main`.** It sent no objects.
  Its second line, `* [new branch] HEAD -> tz-53-push-probe`, is the client's plan and not the
  server's acceptance.
- **D proves the host answers, not that a message is delivered.** No token exists, and `getMe`
  refused the invalid one as expected.
- **The hosting line is a lookup, not a contract.** It also disagrees in kind with
  `systemd-detect-virt` (Finding 13).
- **A host answering today may refuse tomorrow** (inv. 52). Every reading here is one sample from
  08:06:55Z to 08:08:11Z on 01.10.2026, and the no-retry rule is also why no second sample exists.
- **The unit's `Memory peak: 512.0K` is not the headless run's footprint.** Memory accounting was
  on (cgroup v2), and the binary is a 238 MB executable whose run made a model call. Where its
  memory was charged is not established here. B1's 74 MB available with swap in use is the
  measured headroom.
- **The headless run left state outside the repository:** a session record under
  `~/.claude/projects/-tmp-tz53-unit/` and a new mtime on `~/.claude.json`. Neither file was read,
  since one may carry account data, and neither was removed, since no clause authorises deleting
  outside `/tmp/tz53`.
- **The ETF as-of dates lag the read by one to two days**: Sep 30 at iShares, 09/29 at Bitwise.
  The datum describes the prior day's book by iShares' own tooltip.
- **This machine is not a runner.** Every 200 here, `fapi` included, says nothing about what a
  GitHub-hosted runner receives (contract §7 item 9, inv. 24).

---

## Commit

A report commit, direct to `main` on the `CryptoReports/**` path (contract §8). Its contents are
this file only. The message is the TZ's `## Commit Message`, verbatim:

```
TZ-53: report — automation environment and hunter lanes read from the VPS

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

## Pull Request

None — report-only TZ; direct push on the CryptoReports/** path (§8).

## CI Execution

**No workflow ran for this TZ.** No branch was pushed and no code path moved. The five workflows'
triggers, read from the working tree in this session:

```
$ for f in .github/workflows/*.yml; do echo "== $f"; awk '/^on:/{f=1} /^(jobs|permissions|concurrency|env):/{f=0} f' $f | grep --invert-match --extended-regexp '^\s*#|^\s*$|description:|default:|type:|inputs:|years:|source:|regime_gate:'; done
== .github/workflows/backtest_bench.yml
on:
  workflow_dispatch:
== .github/workflows/bench.yml
on:
  push:
    branches: [ main, 'claude/**' ]
    paths-ignore:
      - 'journal/data/**'
      - 'journal/out/**'
      - 'journal/runs.jsonl'
      - 'analyst/state.json'
      - 'analyst/live.json'
      - 'analyst/log/**'
      - 'analyst/owner.json'
      - '**.md'
  pull_request:
== .github/workflows/calib.yml
on:
  workflow_dispatch:
  push:
    branches: [ 'claude/**' ]
    paths:
      - 'bench/exhaustion_calib.py'
      - '.github/workflows/calib.yml'
== .github/workflows/journal.yml
on:
  schedule:
    - cron: '0 13 * * *'
  workflow_dispatch:
== .github/workflows/main.yml
on:
  push:
    branches: [ main ]
    paths:
      - 'main.py'
      - '.github/workflows/main.yml'
  workflow_dispatch:
[exit 0]
```

A commit that changes one `.md` file under `CryptoReports/` matches none of these triggers.
`main.yml` names two paths, `bench.yml` ignores `'**.md'`, and `calib.yml` names two non-`.md`
paths on `claude/**` only. `journal.yml` and `backtest_bench.yml` take no push at all.

## Final Repository State

The fingerprints were taken against harness worktree branch
`worktree-bridge-cse_01D6P1U4thNUnBuHuwmJe2eS`, which has no upstream. It stood at
`97c837275ea578d7ff6d20ef8348172b0dd2692d`, the same commit as `origin/main` after the fetch. At
validation time its working tree differed from that commit only by this untracked report (V6).
The probe's scratch lived under `/tmp/tz53/`, outside the repository, and V7 removed it.
**Outside the repository**, the B6 headless run left `~/.claude/projects/-tmp-tz53-unit/` and a
new mtime on `~/.claude.json` (Remaining Risks). The transient unit was collected, and the remote
carries no `tz-53-*` ref (V6).

**Where each block came from.** `report.py` filled every fenced block from a file or a command:
- the stage logs, the local blocks, V1 and the V3/V4 block, from `/tmp/tz53/out/`, as printed when
  they ran;
- the ledger table, from the ledger;
- the instrument sources, verbatim;
- the Inbound Filing, client, quote, robots, header, offline-extras, V5, V6, CI and fingerprint
  blocks, by running each command from the repository root while the report was generated.

Two blocks were written by hand, because each is the result of a step that runs on the generated
file itself: V2's scan and V7's removal. Each was run after the report was generated, and its
output was confirmed to equal the block.

## Fingerprints

### `SYSTEM-MAP-CRYPTOCALCUL.md`

| | |
|---|---|
| Revision string in `## 0. Fingerprint` | `**Revision 2026-10-01-a.**` |
| Required by TZ-53's header | `**Revision 2026-10-01-a.**` — **match** |
| Lines | 3073 |
| MD5 | `c20d27ecf7b4627fec2de742b5ccbf0d` |

### Anchors

The list was cut from the map's own anchor table **by structure**: the `| Anchor |` header row,
its `|---|---|` separator, and every row up to the first non-table line. It was not cut by matching
anchor names. **The table carries 7 rows and 7 were compared.**
- Each row was confirmed present in the TZ header as an identical table row, with
  `grep --fixed-strings --line-regexp`.
- Each anchor was confirmed an exact, case-sensitive substring of the map with
  `grep --fixed-strings --only-matching`, which prints the text it matched.
- Each anchor occurs twice in the map: once as its own table row (lines 362–368) and once at its
  site.
- The TZ header carries no row the map's table lacks.

| Anchor | In TZ header | In map | Lines in map (site · table) | Text the match returned |
|---|---|---|---|---|
| revision | yes | yes | 17 · 362 | `**Revision 2026-10-01-a.**` |
| direction engine | yes | yes | 1332 · 363 | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | yes | yes | 1722 · 364 | `### 3.15 Catalyst registry` |
| exhaustion measure | yes | yes | 1819 · 365 | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | yes | yes | 2830 · 366 | `## 11. Analytical engine` |
| squeeze block | yes | yes | 1986 · 367 | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | yes | yes | 2528 · 368 | `72. **A write that fails leaves this run's product or nothing` |

The gate first ran before any work, from `/tmp/tz53/gate.sh`. The block below re-runs the same cut
and the same matches from the repository root, with each command printed with its anchor in
place:

```
$ bash <<'GATE'
cut_rows() { awk 'f==0 && /^\| Anchor \|/{f=1;next} f==1 && /^\|---/{f=2;next} f==2 && /^\|/{print;next} f==2{exit}' "$1"; }
MAP=SYSTEM-MAP-CRYPTOCALCUL.md; TZ=CryptoTZ/TZ-53-automation-and-hunter-lanes-vps-reading.md
echo "rows in the map's table: $(cut_rows $MAP | wc --lines); rows in the TZ header's table: $(cut_rows $TZ | wc --lines)"
echo "TZ header rows absent from the map's table: $(cut_rows $TZ | grep --fixed-strings --line-regexp --invert-match --count --file=<(cut_rows $MAP))"
cut_rows $MAP | while IFS= read -r row; do
  a=$(printf '%s' "$row" | sed -E 's/^\| [^|]+ \| `(.*)` \|$/\1/')
  echo "grep --fixed-strings --only-matching --max-count=1 -- \"$a\" $MAP"
  echo "  -> $(grep --fixed-strings --only-matching --max-count=1 -- "$a" $MAP | head --lines=1)"
  echo "  lines in the map: $(grep --fixed-strings --line-number -- "$a" $MAP | cut --delimiter=: --fields=1 | tr '\n' ' ')"
  echo "  identical row in the TZ header (grep --fixed-strings --line-regexp --count): $(grep --fixed-strings --line-regexp --count -- "$row" $TZ)"
done
GATE
rows in the map's table: 7; rows in the TZ header's table: 7
TZ header rows absent from the map's table: 0
grep --fixed-strings --only-matching --max-count=1 -- "**Revision 2026-10-01-a.**" SYSTEM-MAP-CRYPTOCALCUL.md
  -> **Revision 2026-10-01-a.**
  lines in the map: 17 362 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "### 3.12 Direction engine — veto cascade" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ### 3.12 Direction engine — veto cascade
  lines in the map: 363 1332 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "### 3.15 Catalyst registry" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ### 3.15 Catalyst registry
  lines in the map: 364 1722 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "### 3.16 List exhaustion — the day-range measure" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ### 3.16 List exhaustion — the day-range measure
  lines in the map: 365 1819 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "## 11. Analytical engine" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ## 11. Analytical engine
  lines in the map: 366 2830 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "### 3.17 «РИСК ВЫНОСА» — the day's own risk" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ### 3.17 «РИСК ВЫНОСА» — the day's own risk
  lines in the map: 367 1986 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "72. **A write that fails leaves this run's product or nothing" SYSTEM-MAP-CRYPTOCALCUL.md
  -> 72. **A write that fails leaves this run's product or nothing
  lines in the map: 368 2528 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
[exit 0]
```

### Files of the map's `## 0` table, and the two the TZ adds

```
$ for f in SYSTEM-MAP-CRYPTOCALCUL.md index.html main.py catalysts.json bench/exhaustion-calibration.txt ANALYST-INSTRUCTIONS.md EXECUTOR-INSTRUCTIONS.md; do echo "$f  $(wc --lines < $f) lines  $(md5sum $f | cut --delimiter=' ' --fields=1)"; done; grep --max-count=1 --only-matching --extended-regexp '\*\*Revision [0-9a-z-]+\.\*\*' SYSTEM-MAP-CRYPTOCALCUL.md ANALYST-INSTRUCTIONS.md; grep --max-count=1 --only-matching --extended-regexp '\*\*Version [0-9]+\.\*\*' EXECUTOR-INSTRUCTIONS.md
SYSTEM-MAP-CRYPTOCALCUL.md  3073 lines  c20d27ecf7b4627fec2de742b5ccbf0d
index.html  3799 lines  4e71da9badca3ccae85b656fdc3773e8
main.py  518 lines  0e3ead8c300d2ee6783303c4bf2fb6b5
catalysts.json  17 lines  f9b2dd4a3594134b2b7b603de19075c3
bench/exhaustion-calibration.txt  175 lines  3b8730b254467c9df4c0a845a0f3cfb3
ANALYST-INSTRUCTIONS.md  3866 lines  feaaffc99f983b3441ce205bcf1b6466
EXECUTOR-INSTRUCTIONS.md  864 lines  02abb1969626d2af150a0d1f6e02f2a7
SYSTEM-MAP-CRYPTOCALCUL.md:**Revision 2026-10-01-a.**
ANALYST-INSTRUCTIONS.md:**Revision 2026-10-01-a.**
**Version 23.**
[exit 0]
```

| File | Lines (required) | Lines (measured) | MD5 (required) | MD5 (measured) | |
|---|---:|---:|---|---|---|
| `index.html` | 3799 | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | `4e71da9badca3ccae85b656fdc3773e8` | match |
| `main.py` | 518 | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | `0e3ead8c300d2ee6783303c4bf2fb6b5` | match |
| `catalysts.json` | 17 | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | `f9b2dd4a3594134b2b7b603de19075c3` | match |
| `bench/exhaustion-calibration.txt` | 175 | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | `3b8730b254467c9df4c0a845a0f3cfb3` | match |
| `ANALYST-INSTRUCTIONS.md` (TZ, reported) | 3866 | 3866 | `feaaffc99f983b3441ce205bcf1b6466` | `feaaffc99f983b3441ce205bcf1b6466` | match · `2026-10-01-a` |
| `EXECUTOR-INSTRUCTIONS.md` (TZ, reported) | 864 | 864 | `02abb1969626d2af150a0d1f6e02f2a7` | `02abb1969626d2af150a0d1f6e02f2a7` | match · `Version 23` |

No file outside `CryptoReports/` was written, so every row stands before and after the work.
