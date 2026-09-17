# Provider Handoff

A Planning provider checkpoints a semantic unit. A fresh compatible provider enters through `external.py acquire`. Work generation increments; the old generation is fenced. The new provider resumes from durable checkpoint/ticket without prior chat replay.
