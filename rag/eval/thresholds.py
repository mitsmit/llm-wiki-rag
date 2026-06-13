"""Threshold constants used by `run_eval.py --strict`.

These are starting points, not validated targets. Run the harness without
--strict first, look at rag/eval/results/summary.md, and tighten or relax
these based on real numbers before using --strict as a CI gate.
"""

MIN_HIT_AT_3 = 0.5
MIN_HIT_AT_5 = 0.6
MIN_HIT_AT_8 = 0.7
MIN_MRR = 0.4
MIN_CITATION_VALIDITY = 0.8
MIN_GROUNDEDNESS = 3.5
MIN_RELEVANCE = 3.5
