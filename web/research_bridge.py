"""Bridge for importing research-agent's modules from the main web app.

`research-agent/` isn't a Python package — its directory name has a hyphen
and its modules use bare imports (`from dedup import ...`), so it can't be
imported as `from research_agent.agent import research`. Instead, add its
directory to `sys.path` once here and import the modules directly.
"""

from __future__ import annotations

import sys
from pathlib import Path

RESEARCH_AGENT_DIR = Path(__file__).resolve().parent.parent / "research-agent"

if str(RESEARCH_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_AGENT_DIR))

import agent as research_agent  # noqa: E402
import dedup  # noqa: E402
import fetch  # noqa: E402
import parse  # noqa: E402

__all__ = ["research_agent", "dedup", "fetch", "parse"]
