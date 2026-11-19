#!/usr/bin/env python3
"""news-image-20261118 entry (Python 3.13, standard library only).

The entry image is entry.png beside this file: a newspaper front page
summing up the world's news of Wednesday 18 November 2026 -- the Gulf
strikes, the Kerch Bridge hit, Xi and Putin in Shenzhen, Peltola's
Alaska win, plus Ebola, Voyager 1 and measles in the ticker.

The program copies it to /output/entry.png (or
$MAKEFUN_OUTPUT_DIR/entry.png outside the grader's container).
Deterministic: the same bytes on every run, no network.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"),
                os.path.join(OUT, "entry.png"))
