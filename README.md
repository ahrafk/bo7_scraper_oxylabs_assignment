BO7 Scraping Challenge – Solution

This repository contains my solutions for the BO7 scraping challenge.
The goal of the challenge is to build scrapers capable of bypassing various blocking mechanisms implemented on bo7.online.

Each puzzle represents a different type of protection that scrapers commonly encounter in real-world environments such as fingerprinting, request validation, header checks, and request flow verification.

My focus during the challenge was to understand how the website verifies clients and then reproduce the same behavior programmatically.

Overview

The website contains puzzles grouped into different categories:

Mysterious Passages

Curious Reflections

Shattered Thresholds

Each puzzle behaves like a “door” that remains closed until the scraper successfully mimics the expected browser behavior.

A puzzle is considered solved when the response contains the message:

The door slides open. 🚪
Cool breeze. Dim light. You step inside.

Whatever you’re doing — keep it weird, but quiet.
Puzzles Solved

The following puzzles were successfully solved:

Sleeping Vault

Verity Gate

Mirrored Gaze

(add the other solved puzzles here)

(add the other solved puzzles here)

For each puzzle the repository contains:

The scraping script

The saved HTML response confirming the door opened

Logs demonstrating the request flow

Approach
1. Understanding the Browser Flow

For each puzzle I started by reproducing the exact browser behavior using DevTools.

This involved analyzing:

Network requests

Headers and cookies

Request order

JavaScript logic executed on page load

In most cases the puzzle followed a pattern similar to:

Homepage request
↓
Fingerprint generation (ThumbmarkJS)
↓
POST /api/thumbmark
↓
Guarded page request
↓
Second fingerprint submission
↓
Final page unlock

The challenge was therefore less about parsing HTML and more about replicating the correct interaction flow with the server.

Fingerprinting (ThumbmarkJS)

Several puzzles rely on a browser fingerprint generated using ThumbmarkJS.

The JavaScript collects various browser characteristics such as:

Canvas fingerprint

WebGL fingerprint

Audio fingerprint

Installed fonts

Hardware information

Math function precision

Plugin list

The browser sends this fingerprint to:

POST /api/thumbmark

along with a header:

x-mysterious-value

To replicate this behavior without a browser I created a function that generates a consistent fingerprint payload, which is then reused across requests.

Handling Intentional 403 Responses

Some puzzles intentionally return HTTP 403 on the first request.

This is expected behavior and part of the verification process.

Even though the page is blocked, it still contains important information such as:

the next x-mysterious-value

additional scripts required for the challenge

The scraper therefore continues processing the response instead of treating it as a failure.

Request Flow Replication

Another key aspect of the challenge is that requests must occur in the correct order.

For example:

1. GET /
2. GET /resources/thumbmark.js
3. POST /api/thumbmark

4. GET /puzzle_page   (returns 403)

5. GET /resources/thumbmark.js
6. POST /api/thumbmark (new mysterious value)

7. GET /puzzle_page   (returns 200)

If any of these steps are skipped or executed too quickly, the server rejects the request.

For this reason small delays were introduced to simulate the time required for fingerprint generation in the browser.

Anti-Bot Considerations

The scripts also account for several anti-bot mechanisms:

Header validation

Requests replicate realistic browser headers such as:

sec-ch-ua

sec-fetch-*

upgrade-insecure-requests

referer

Cookie handling

The site relies on a session cookie (wormhole_token) which is preserved across requests using a shared session.

Browser impersonation

Requests are sent using curl_cffi with Chrome impersonation to match the TLS and HTTP fingerprint of a real browser.

Proxy usage

Some puzzles perform IP-based checks, so a proxy can be configured when needed.

Project Structure
oxylabs-assignment
│
├── core
│   ├── session.py
│   ├── homepage.py
│   ├── thumbmark.py
│
├── puzzles
│   ├── mirrored_gaze.py
│   ├── sleeping_vault.py
│   ├── verity_gate.py
│
├── test_results
│   ├── mirrored_gaze_result.html
│   ├── sleeping_vault_result.html
│   ├── verity_gate_result.html
│
├── main.py
└── README.md
Running the Solver

Install dependencies:

pip install -r requirements.txt

Run the main script:

python -m main

Each puzzle script will execute and save the resulting HTML confirming that the door was opened.

Notes

The challenge was a great exercise in understanding how modern websites verify clients and detect automated traffic.

Rather than relying on a headless browser, the focus of this solution was to analyze the verification logic and reproduce it using a lightweight HTTP client.

This approach makes the scrapers faster, simpler, and easier to scale.

Final Thoughts

This challenge was enjoyable and required careful analysis of both JavaScript behavior and network interactions.

It highlights how many anti-bot systems rely not just on headers or cookies, but on the complete interaction pattern between client and server.

Thank you for the opportunity to work on this challenge.