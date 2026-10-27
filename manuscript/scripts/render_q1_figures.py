#!/usr/bin/env python3
"""Compatibility entry point for the maintained journal plot renderer."""
from pathlib import Path
import runpy
if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).resolve().parents[2]/'manuscript_q1/scripts/render_q1_figures.py'),run_name='__main__')
