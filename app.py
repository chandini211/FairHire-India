"""
FairHire India - Root Workspace Launcher
Directs execution into FairHire_India/app.py
"""
import sys
from pathlib import Path
import runpy

project_dir = Path(__file__).resolve().parent / "FairHire_India"
if str(project_dir) not in sys.path:
    sys.path.insert(0, str(project_dir))

runpy.run_path(str(project_dir / "app.py"), run_name="__main__")
