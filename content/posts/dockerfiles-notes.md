---
title: Notes on writing Dockerfiles I'm not embarrassed by
date: 2026-06-30
tags: infra
read_time: 5 min read
excerpt: None of this is clever.
---
Multi-stage builds, pinned base image digests (not just tags), and a non-root user by default.

None of this is clever. All of it has saved a production incident at least once.

```dockerfile
FROM python:3.12-slim@sha256:REPLACE_WITH_DIGEST AS base
RUN useradd --create-home appuser
USER appuser
WORKDIR /app
COPY --chown=appuser:appuser . .
```

Pin the digest, not the tag. Tags move. Digests don't.
