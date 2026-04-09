# BO7 Scraping Challenge – Solution

## Overview

This project solves all 8 puzzles on bo7.online, a challenge site that simulates real-world anti-bot protections. Each puzzle represents a different type of blocking mechanism that scrapers encounter in production environments.

The solution uses Python with async/await and curl_cffi for Chrome browser impersonation. All 8 puzzles run concurrently using asyncio.gather.

---

## Results

All 8 puzzles solved successfully:

| Puzzle | Category | Status |
|---|---|---|
| The Door of Echoed Steps | Mysterious Passages | Solved |
| The Clockwork Door | Mysterious Passages | Solved |
| The Exiled Door | Mysterious Passages | Solved |
| The Fractured Mirror | Curious Reflections | Solved |
| The Silver Veil | Curious Reflections | Solved |
| The Mirrored Gaze | Curious Reflections | Solved |
| The Sleeping Vault | Shattered Thresholds | Solved |
| The Verity Gate | Shattered Thresholds | Solved |

Each result is saved as an HTML file in test_results/.

---

## How It Works

### Session and Cookies

The site uses a session cookie called wormhole_token (value: galactic-cookie-42) to gate access to most puzzles. This cookie is set by the server on the first homepage visit, and it's also seeded directly into the session so that solvers can be run independently.

A single AsyncSession from curl_cffi is shared across all puzzle solvers. It's configured with impersonate="chrome" which replicates Chrome's TLS handshake (JA3 fingerprint) at the network level. This matters for puzzles that inspect the TLS signature of the incoming connection.

### Header Factory

All browser headers are centralised in core/headers.py. Three functions cover the three types of requests a browser makes:

- nav_headers() — full navigation headers for page loads (sec-fetch-dest: document)
- resource_headers() — sub-resource headers for script files (sec-fetch-dest: script)
- fetch_headers() — XHR/fetch headers for background API calls (sec-fetch-dest: empty)

This avoids duplication and ensures headers are consistent across all puzzles.

### Concurrency

The main entry point visits the homepage once to establish the session, then launches all 8 puzzle solvers concurrently with asyncio.gather. Because curl_cffi.AsyncSession is fully async, the solvers run in parallel without blocking each other.

---

## Puzzle Breakdown

### Pattern 1 — Single GET

These puzzles open with one request. The server checks the wormhole_token cookie and the Referer header to confirm the request came from within the site.

- The Door of Echoed Steps — Referer: bo7.online/
- The Clockwork Door — Referer: bo7.online/
- The Silver Veil — Referer: bo7.online/ with a consistent full header set

### Pattern 2 — Two-step with /resources/open.html

These puzzles follow the same flow a real browser takes when executing the page's JavaScript. The page JS performs some checks and then calls fetch("/resources/open.html"). The server validates the Referer header on that second request to confirm the fetch came from the correct puzzle page.

The strategy is to replicate exactly what the browser does:

1. GET /puzzle_page — loads the page, records server-side state
2. GET /resources/open.html with Referer: /puzzle_page — triggers the unlock

Puzzles using this pattern:

- The Sleeping Vault
- The Fractured Mirror
- The Mirrored Gaze

### Pattern 3 — Three-step with JS preload

Same as Pattern 2, but the page also loads a JavaScript file as a script tag before making the fetch call. The script load has to be replicated to satisfy the server's request-sequence check.

1. GET /the_verity_gate — page load
2. GET /resources/the_verity_gate.js?v=1 — script load (sec-fetch-dest: script)
3. GET /resources/open.html with Referer: /the_verity_gate

Puzzles using this pattern:

- The Verity Gate

### The Exiled Door — Special Case

This puzzle requires the request to look like it comes from a visitor who has never been on the site before — no cookie, no referer, sec-fetch-site: none. A fresh AsyncSession (no wormhole_token cookie) is used for both steps of this puzzle.

1. GET /the_exiled_door with sec-fetch-site: none and no Referer — fresh session, no cookie
2. GET /resources/open.html with Referer: /the_exiled_door — still within the fresh session

---

## Project Structure

```
oxylabs-assignment/
|
+-- core/
|   +-- session.py        # Shared AsyncSession with cookie + proxy config
|   +-- homepage.py       # Homepage visit to establish session
|   +-- headers.py        # Centralised browser header factories
|   +-- thumbmark.py      # Thumbmark POST helper (retained)
|
+-- mysterious_passages/
|   +-- the_door_echoed_steps.py
|   +-- the_clockwork_door.py
|   +-- the_exiled_doors.py
|
+-- curious_reflections/
|   +-- the_fractured_mirror.py
|   +-- the_silver_veil.py
|   +-- the_mirror_gaze.py
|
+-- shattered_thresholds/
|   +-- the_sleeping_vault.py
|   +-- the_verity_gate.py
|
+-- test_results/          # Saved HTML from each solved puzzle
+-- main.py                # Entry point — runs all solvers concurrently
+-- requirements.txt
+-- README.md
```

---

## Running the Solver

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables by creating a .env file:

```
PROXY_USER=your_user
PROXY_PASS=your_password
PROXY_HOST=your_host
PROXY_PORT=your_port
```

Run with defaults (10 req/s, all 8 solvers concurrent):

```bash
python main.py
```

Control request rate and concurrency:

```bash
python main.py --rps 5 --concurrency 4
```

| Flag | Default | Description |
|---|---|---|
| --rps | 10 | Maximum requests per second across all solvers |
| --concurrency | 8 | Maximum number of puzzle solvers running at once |

Lowering --concurrency or --rps is useful when testing against rate-limited environments. Raising them stress-tests the solution at scale.

---

## Key Technical Decisions

**curl_cffi over requests or httpx** — curl_cffi wraps libcurl and lets you specify a browser to impersonate. This replicates the TLS fingerprint (JA3 hash) and HTTP/2 settings at the socket level, which plain Python HTTP libraries cannot do. Puzzles that inspect the TLS handshake will reject requests from standard libraries regardless of what headers you set.

**No headless browser** — Playwright or Puppeteer would work but they add significant overhead and complexity. Analysing the JS on each page and replicating the request flow directly in Python is faster, lighter, and easier to scale.

**No ThumbmarkJS replication** — The initial approach tried to replicate the ThumbmarkJS fingerprint payload and POST it to /api/thumbmark before each puzzle. After analysis, that endpoint is passive analytics only — the server collects the data but does not use it as an access gate. The actual gate is the Referer header on the /resources/open.html fetch. Removing it simplified the code significantly.

**Async concurrency** — All 8 solvers run in parallel via asyncio.gather. The total runtime is roughly the time of the slowest single puzzle rather than the sum of all eight.
