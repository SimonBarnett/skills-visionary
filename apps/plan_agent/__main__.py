"""Entry: python apps/plan_agent/__main__.py  (or python -m apps.plan_agent)."""
from __future__ import annotations

import sys
from pathlib import Path

# Allow `python path/to/__main__.py` without installing the package.
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
