import sys
from pathlib import Path

# Put the plugin root (which contains the ``engine`` package) on the path so
# tests import it regardless of where pytest is invoked from.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
