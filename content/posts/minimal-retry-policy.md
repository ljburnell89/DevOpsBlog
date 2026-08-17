---
title: A minimal retry policy that has never bitten me
date: 2026-07-19
tags: systems
read_time: 4 min read
excerpt: Three knobs, no framework.
---
Exponential backoff with jitter, a hard cap on attempts, and — the part people skip — a circuit breaker that opens on error *rate*, not error count.

Three knobs, no framework, works the same in every language I've shipped it in:

- **Backoff**: base delay × 2^attempt, plus random jitter
- **Cap**: stop after 5 attempts, always
- **Circuit breaker**: open when >50% of the last 20 calls failed

That's it. No library needed for most services.
