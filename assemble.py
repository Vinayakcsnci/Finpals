#!/usr/bin/env python3
"""Assemble all parts into final index.html"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

# Import CSS
from build_v2 import CSS
# Import HTML body
from build_v2_html import BODY
# Import JS parts
from build_v2_js1 import JS_DATA
from build_v2_js2 import JS_FUNCS
from build_v2_js3 import JS_APP
from build_v2_js4 import JS_TABS
from build_v2_js5 import JS_UTILS

OUT = os.path.join(os.path.dirname(__file__), "index.html")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FinPal v2.0 — AI-Powered Loan Intake &amp; Assessment Platform</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>
{BODY}
<script>
{JS_DATA}
{JS_FUNCS}
{JS_APP}
{JS_TABS}
{JS_UTILS}
</script>
</body>
</html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

size = os.path.getsize(OUT)
print(f"index.html assembled: {size:,} bytes")
print(f"Written to: {OUT}")
