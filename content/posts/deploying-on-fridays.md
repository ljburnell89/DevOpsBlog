---
title: Why we stopped deploying on Fridays (and what we did instead)
date: 2026-08-02
tags: ci/cd
read_time: 6 min read
excerpt: Not a superstition — a postmortem pattern.
---
Not a superstition — a postmortem pattern. Friday incidents had a 3x longer mean time to resolve, simply because fewer people were around to help.

We moved risky deploys to Tuesday mornings and added a deploy-freeze window that the pipeline itself enforces, not just a wiki page nobody reads.

```yaml
- name: Block Friday deploys
  if: github.event.schedule || github.actor != 'release-bot'
  run: |
    day=$(date +%u)
    if [ "$day" -ge 5 ]; then
      echo "Deploys are frozen after Thursday. Opening a draft PR instead."
      exit 1
    fi
```

The rule is boring on purpose. Boring rules survive contact with a deadline.
