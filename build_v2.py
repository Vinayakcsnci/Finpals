#!/usr/bin/env python3
"""Generate FinPal V2 index.html with all documentation changes."""

import os

OUT = r"C:\Users\lenovo\Downloads\NCI\CITI\feedback\finpalsme\index.html"

CSS = r"""
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --navy: #0B1F3A; --navy-mid: #0E2D52; --navy-dark: #061426;
  --teal: #00A896; --teal-dark: #007A6E; --teal-glow: rgba(0,168,150,.18);
  --ice: #F0F6FA; --white: #FFFFFF; --slate: #334E68; --muted: #7A94AC;
  --gold: #F5A623; --red: #E84C4C; --green: #2ECC71;
  --bg: #07182E; --panel: #0C2240; --border: rgba(0,168,150,.2);
  --font-head: 'Syne', sans-serif; --font-mono: 'DM Mono', monospace;
  --font-body: 'DM Sans', sans-serif; --r: 6px; --r-lg: 10px;
}
html, body { height:100%; background:var(--bg); color:var(--white); font-family:var(--font-body); font-size:14px; overflow:hidden; }
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:var(--navy-mid); border-radius:99px; }
#app { display:flex; height:100vh; overflow:hidden; }
#sidebar { width:230px; min-width:230px; background:var(--navy-dark); border-right:1px solid var(--border); display:flex; flex-direction:column; overflow:hidden; }
.logo { padding:22px 18px 16px; border-bottom:1px solid var(--border); display:flex; align-items:center; gap:10px; }
.logo-mark { width:32px; height:32px; background:var(--teal); border-radius:6px; display:flex; align-items:center; justify-content:center; font-family:var(--font-head); font-weight:800; font-size:16px; color:var(--navy-dark); flex-shrink:0; }
.logo-text { font-family:var(--font-head); font-weight:700; font-size:18px; color:var(--white); letter-spacing:-0.3px; }
.logo-tag { font-size:9px; color:var(--teal); font-family:var(--font-mono); letter-spacing:.5px; margin-top:1px; }
.nav-section { padding:10px 10px 4px; }
.nav-label { font-size:9px; color:var(--muted); font-family:var(--font-mono); letter-spacing:1px; text-transform:uppercase; padding:0 8px 6px; }
.nav-item { display:flex; align-items:center; gap:9px; padding:7px 10px; border-radius:var(--r); cursor:pointer; color:var(--muted); font-size:12.5px; transition:all .15s; user-select:none; }
.nav-item:hover { background:var(--teal-glow); color:var(--white); }
.nav-item.active { background:var(--teal-glow); color:var(--teal); }
.nav-item .icon { font-size:14px; width:18px; text-align:center; }
.nav-badge { margin-left:auto; background:var(--teal); color:var(--navy-dark); font-size:10px; font-weight:700; padding:1px 6px; border-radius:99px; font-family:var(--font-mono); }
.app-list { flex:1; overflow-y:auto; padding:10px; }
.app-card { padding:10px 10px 8px; border-radius:var(--r); border:1px solid transparent; margin-bottom:6px; cursor:pointer; transition:all .15s; position:relative; overflow:hidden; }
.app-card::before { content:''; position:absolute; left:0; top:0; bottom:0; width:3px; background:transparent; border-radius:99px 0 0 99px; transition:background .15s; }
.app-card:hover { background:var(--teal-glow); border-color:var(--border); }
.app-card:hover::before { background:var(--teal); }
.app-card.active { background:var(--navy-mid); border-color:var(--border); }
.app-card.active::before { background:var(--teal); }
.app-card-name { font-weight:500; font-size:13px; color:var(--white); margin-bottom:3px; }
.app-card-meta { font-size:11px; color:var(--muted); font-family:var(--font-mono); display:flex; justify-content:space-between; align-items:center; }
.status-dot { width:6px; height:6px; border-radius:50%; display:inline-block; margin-right:4px; }
.dot-green { background:var(--green); box-shadow:0 0 4px var(--green); }
.dot-yellow { background:var(--gold); }
.dot-teal { background:var(--teal); animation:pulse 1.5s ease-in-out infinite; }
.dot-grey { background:var(--muted); }
@keyframes pulse { 0%,100%{box-shadow:0 0 0 0 rgba(0,168,150,.4);} 50%{box-shadow:0 0 0 4px rgba(0,168,150,0);} }
#main { flex:1; display:flex; flex-direction:column; overflow:hidden; }
#topbar { height:56px; min-height:56px; background:var(--navy-dark); border-bottom:1px solid var(--border); display:flex; align-items:center; padding:0 24px; gap:16px; }
.topbar-title { font-family:var(--font-head); font-size:16px; font-weight:700; color:var(--white); flex:1; }
.topbar-subtitle { font-size:12px; color:var(--muted); font-family:var(--font-mono); }
.topbar-actions { display:flex; gap:8px; }
.btn { padding:7px 16px; border-radius:var(--r); border:none; font-family:var(--font-body); font-size:13px; font-weight:500; cursor:pointer; transition:all .15s; display:flex; align-items:center; gap:6px; }
.btn-outline { background:transparent; border:1px solid var(--border); color:var(--muted); }
.btn-outline:hover { border-color:var(--teal); color:var(--teal); }
.btn-primary { background:var(--teal); color:var(--navy-dark); font-weight:700; }
.btn-primary:hover { background:#00bfad; }
.btn-danger { background:transparent; border:1px solid rgba(232,76,76,.4); color:var(--red); }
.btn-danger:hover { background:rgba(232,76,76,.1); }
.btn:disabled { opacity:.4; pointer-events:none; }
#content { flex:1; overflow:hidden; display:flex; flex-direction:column; }
#app-header { padding:18px 24px 0; border-bottom:1px solid var(--border); }
.app-meta-row { display:flex; align-items:flex-start; gap:20px; margin-bottom:14px; }
.app-company { font-family:var(--font-head); font-size:24px; font-weight:700; }
.app-ref { font-family:var(--font-mono); font-size:11px; color:var(--muted); margin-top:2px; }
.meta-chips { display:flex; gap:8px; flex-wrap:wrap; margin-top:6px; }
.chip { padding:3px 10px; border-radius:99px; font-size:11px; font-family:var(--font-mono); border:1px solid var(--border); color:var(--muted); }
.chip-teal { background:var(--teal-glow); color:var(--teal); border-color:rgba(0,168,150,.3); }
.chip-gold { background:rgba(245,166,35,.1); color:var(--gold); border-color:rgba(245,166,35,.3); }
.chip-red { background:rgba(232,76,76,.1); color:var(--red); border-color:rgba(232,76,76,.3); }
.chip-green { background:rgba(46,204,113,.1); color:var(--green); border-color:rgba(46,204,113,.3); }
.tabs { display:flex; gap:0; margin-top:4px; overflow-x:auto; }
.tab { padding:10px 14px; font-size:12.5px; color:var(--muted); border-bottom:2px solid transparent; cursor:pointer; transition:all .15s; user-select:none; white-space:nowrap; }
.tab:hover { color:var(--white); }
.tab.active { color:var(--teal); border-bottom-color:var(--teal); }
.tab-alert { color:var(--gold) !important; }
.panel { display:none; flex:1; overflow-y:auto; padding:20px 24px 24px; }
.panel.active { display:block; }
.grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:14px; }
.grid-3 { display:grid; grid-template-columns:1fr 1fr 1fr; gap:14px; }
.grid-4 { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; }
.grid-5 { display:grid; grid-template-columns:repeat(5,1fr); gap:14px; }
.card { background:var(--panel); border:1px solid var(--border); border-radius:var(--r-lg); padding:16px; }
.card-title { font-size:11px; color:var(--muted); font-family:var(--font-mono); letter-spacing:.6px; text-transform:uppercase; margin-bottom:10px; display:flex; align-items:center; justify-content:space-between; }
.card-value { font-family:var(--font-mono); font-size:28px; font-weight:500; color:var(--white); }
.card-value.teal { color:var(--teal); } .card-value.gold { color:var(--gold); } .card-value.red { color:var(--red); } .card-value.green { color:var(--green); }
.card-sub { font-size:11px; color:var(--muted); margin-top:4px; }
.section-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; margin-top:20px; }
.section-header:first-child { margin-top:0; }
.section-title { font-family:var(--font-head); font-size:14px; font-weight:600; color:var(--white); display:flex; align-items:center; gap:8px; }
.section-title::before { content:''; width:3px; height:14px; background:var(--teal); border-radius:99px; }
.doc-item { display:flex; align-items:center; gap:12px; padding:12px 14px; background:var(--panel); border:1px solid var(--border); border-radius:var(--r); margin-bottom:8px; }
.doc-icon { width:36px; height:36px; border-radius:6px; background:var(--navy-mid); display:flex; align-items:center; justify-content:center; font-size:16px; flex-shrink:0; }
.doc-name { font-size:13px; font-weight:500; color:var(--white); }
.doc-meta { font-size:11px; color:var(--muted); font-family:var(--font-mono); margin-top:2px; }
.doc-status { margin-left:auto; display:flex; align-items:center; gap:6px; font-size:12px; }
.progress-bar { height:4px; background:var(--navy-mid); border-radius:99px; overflow:hidden; margin-top:6px; }
.progress-fill { height:100%; background:var(--teal); border-radius:99px; transition:width 1s ease; }
.processing-panel { display:flex; flex-direction:column; align-items:center; justify-content:center; padding:40px; text-align:center; min-height:300px; }
.spinner { width:52px; height:52px; border-radius:50%; border:3px solid var(--teal-glow); border-top-color:var(--teal); animation:spin .8s linear infinite; margin-bottom:20px; }
@keyframes spin { to { transform:rotate(360deg); } }
.step-list { text-align:left; margin-top:16px; width:100%; max-width:420px; }
.step-item { display:flex; align-items:center; gap:10px; padding:8px 0; font-size:13px; color:var(--muted); border-bottom:1px solid rgba(255,255,255,.05); transition:color .3s; }
.step-item.done { color:var(--white); } .step-item.active-step { color:var(--teal); }
.step-item .step-icon { font-size:14px; width:20px; text-align:center; }
.step-check { color:var(--teal); }
.tx-table { width:100%; border-collapse:collapse; font-size:12.5px; }
.tx-table th { text-align:left; padding:8px 10px; color:var(--muted); font-family:var(--font-mono); font-size:10px; letter-spacing:.5px; text-transform:uppercase; border-bottom:1px solid var(--border); font-weight:500; }
.tx-table td { padding:9px 10px; border-bottom:1px solid rgba(255,255,255,.04); color:var(--white); }
.tx-table tr:last-child td { border-bottom:none; }
.tx-table tr:hover td { background:rgba(255,255,255,.02); }
.amount-in { color:var(--green); font-family:var(--font-mono); }
.amount-out { color:var(--red); font-family:var(--font-mono); }
.tx-cat { padding:2px 8px; border-radius:99px; font-size:10px; font-family:var(--font-mono); background:var(--navy-mid); color:var(--muted); }
.metric-row { display:flex; align-items:center; justify-content:space-between; padding:10px 0; border-bottom:1px solid rgba(255,255,255,.05); }
.metric-row:last-child { border-bottom:none; }
.metric-label { font-size:13px; color:var(--muted); }
.metric-value { font-family:var(--font-mono); font-size:14px; font-weight:500; color:var(--white); }
.flag-box { background:rgba(245,166,35,.08); border:1px solid rgba(245,166,35,.35); border-radius:var(--r); padding:14px 16px; margin-top:12px; }
.flag-box.red { background:rgba(232,76,76,.08); border-color:rgba(232,76,76,.35); }
.flag-box.green { background:rgba(46,204,113,.08); border-color:rgba(46,204,113,.35); }
.flag-box.blue { background:rgba(0,168,150,.06); border-color:rgba(0,168,150,.3); }
.flag-title { font-size:13px; font-weight:600; color:var(--gold); margin-bottom:5px; display:flex; gap:8px; align-items:center; }
.flag-box.red .flag-title { color:var(--red); } .flag-box.green .flag-title { color:var(--green); } .flag-box.blue .flag-title { color:var(--teal); }
.flag-body { font-size:12px; color:var(--muted); line-height:1.6; }
.check-item { display:flex; align-items:flex-start; gap:12px; padding:14px; background:var(--panel); border:1px solid var(--border); border-radius:var(--r); margin-bottom:8px; transition:border-color .2s; }
.check-item:hover { border-color:rgba(0,168,150,.3); }
.check-status-icon { font-size:18px; margin-top:1px; flex-shrink:0; width:24px; text-align:center; }
.check-name { font-size:13px; font-weight:500; color:var(--white); margin-bottom:3px; }
.check-detail { font-size:12px; color:var(--muted); line-height:1.5; }
.check-timestamp { margin-left:auto; font-size:10px; color:var(--muted); font-family:var(--font-mono); white-space:nowrap; }
.evidence-header { background:linear-gradient(135deg, var(--navy-mid) 0%, #0a2040 100%); border:1px solid var(--border); border-radius:var(--r-lg); padding:20px 24px; margin-bottom:16px; }
.evidence-company { font-family:var(--font-head); font-size:22px; font-weight:700; }
.evidence-meta { display:flex; gap:20px; margin-top:10px; flex-wrap:wrap; }
.evidence-meta-item { font-family:var(--font-mono); font-size:11px; }
.evidence-meta-label { color:var(--muted); } .evidence-meta-value { color:var(--white); }
.narrative-box { background:var(--panel); border:1px solid var(--border); border-radius:var(--r); padding:16px; margin-bottom:14px; position:relative; }
.narrative-box::before { content:'XAI-GENERATED SUMMARY (SHAP v3.2)'; position:absolute; top:-8px; left:14px; background:var(--teal); color:var(--navy-dark); font-family:var(--font-mono); font-size:9px; font-weight:500; padding:2px 8px; border-radius:99px; letter-spacing:.5px; }
.narrative-text { font-size:13px; line-height:1.7; color:var(--muted); }
.narrative-text strong { color:var(--white); font-weight:500; }
.finding-row { display:flex; align-items:baseline; gap:10px; padding:9px 0; border-bottom:1px solid rgba(255,255,255,.04); }
.finding-row:last-child { border-bottom:none; }
.finding-label { font-size:12px; color:var(--muted); flex:1; }
.finding-value { font-family:var(--font-mono); font-size:13px; color:var(--white); text-align:right; min-width:80px; }
.finding-flag { font-size:11px; padding:1px 8px; border-radius:99px; margin-left:8px; }
.flag-amber { background:rgba(245,166,35,.15); color:var(--gold); }
.flag-green { background:rgba(46,204,113,.12); color:var(--green); }
.flag-red { background:rgba(232,76,76,.12); color:var(--red); }
.decision-gate { background:var(--navy-dark); border:2px solid var(--border); border-radius:var(--r-lg); padding:20px 24px; margin-top:20px; }
.decision-gate-title { font-family:var(--font-head); font-size:16px; font-weight:700; margin-bottom:6px; display:flex; align-items:center; gap:8px; }
.decision-gate-sub { font-size:12px; color:var(--muted); margin-bottom:16px; }
.decision-buttons { display:flex; gap:10px; margin-top:14px; }
.decision-textarea { width:100%; background:var(--panel); border:1px solid var(--border); border-radius:var(--r); color:var(--white); font-family:var(--font-body); font-size:13px; padding:10px 12px; resize:vertical; min-height:72px; transition:border-color .15s; }
.decision-textarea:focus { outline:none; border-color:var(--teal); }
.decision-textarea::placeholder { color:var(--muted); }
.audit-item { display:flex; gap:12px; padding:12px 0; border-bottom:1px solid rgba(255,255,255,.04); }
.audit-time { font-family:var(--font-mono); font-size:10px; color:var(--muted); min-width:80px; margin-top:2px; }
.audit-dot { width:8px; height:8px; border-radius:50%; background:var(--teal); margin-top:4px; flex-shrink:0; }
.audit-dot.gold { background:var(--gold); } .audit-dot.red { background:var(--red); } .audit-dot.green { background:var(--green); }
.audit-event { font-size:13px; color:var(--white); }
.audit-detail { font-size:11px; color:var(--muted); margin-top:2px; font-family:var(--font-mono); }
.bar-chart { display:flex; align-items:flex-end; gap:8px; height:80px; padding-top:10px; }
.bar-col { display:flex; flex-direction:column; align-items:center; flex:1; height:100%; justify-content:flex-end; }
.bar-fill { width:100%; border-radius:3px 3px 0 0; transition:height 1s ease; min-height:2px; }
.bar-label { font-size:9px; color:var(--muted); font-family:var(--font-mono); margin-top:4px; }
.modal-overlay { display:none; position:fixed; inset:0; background:rgba(6,20,38,.85); z-index:100; align-items:center; justify-content:center; backdrop-filter:blur(3px); }
.modal-overlay.open { display:flex; }
.modal { background:var(--panel); border:1px solid var(--border); border-radius:12px; padding:28px 28px 24px; max-width:480px; width:90%; animation:modalIn .2s ease; }
@keyframes modalIn { from{opacity:0;transform:translateY(12px) scale(.97);} to{opacity:1;transform:none;} }
.modal-title { font-family:var(--font-head); font-size:18px; font-weight:700; margin-bottom:8px; }
.modal-body { font-size:13px; color:var(--muted); line-height:1.6; margin-bottom:18px; }
.modal-actions { display:flex; gap:10px; justify-content:flex-end; }
.toast { position:fixed; bottom:24px; right:24px; z-index:200; background:var(--teal); color:var(--navy-dark); padding:12px 20px; border-radius:8px; font-weight:600; font-size:13px; animation:toastIn .3s ease; pointer-events:none; max-width:340px; }
@keyframes toastIn { from{opacity:0;transform:translateY(8px);} to{opacity:1;} }
.toast.hide { animation:toastOut .3s ease forwards; }
@keyframes toastOut { to{opacity:0;transform:translateY(8px);} }
svg.sparkline { display:block; }
.empty-state { display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; color:var(--muted); gap:12px; }
.empty-icon { font-size:40px; opacity:.4; } .empty-text { font-size:14px; }
@media(max-width:900px) { #sidebar{width:180px;min-width:180px;} .grid-4,.grid-5{grid-template-columns:repeat(2,1fr);} }
.teal-glow-text { color:var(--teal); text-shadow:0 0 12px rgba(0,168,150,.5); }
.tag { display:inline-flex; align-items:center; gap:4px; padding:3px 9px; border-radius:99px; font-size:11px; font-family:var(--font-mono); font-weight:500; }
.tag-processing { background:var(--teal-glow); color:var(--teal); border:1px solid rgba(0,168,150,.3); }
.tag-complete { background:rgba(46,204,113,.1); color:var(--green); border:1px solid rgba(46,204,113,.3); }
.tag-pending { background:rgba(122,148,172,.1); color:var(--muted); border:1px solid rgba(122,148,172,.2); }
.tag-flagged { background:rgba(245,166,35,.1); color:var(--gold); border:1px solid rgba(245,166,35,.3); }
.tag-danger { background:rgba(232,76,76,.1); color:var(--red); border:1px solid rgba(232,76,76,.3); }
.decision-submitted { display:flex; align-items:center; gap:12px; padding:16px; background:rgba(46,204,113,.08); border:1px solid rgba(46,204,113,.3); border-radius:var(--r); }
.decision-submitted-icon { font-size:24px; }
.decision-submitted-text { font-size:13px; color:var(--green); font-weight:500; }
.decision-submitted-sub { font-size:11px; color:var(--muted); font-family:var(--font-mono); margin-top:2px; }
/* V2: SHAP bars */
.shap-bar-row { display:flex; align-items:center; gap:10px; padding:8px 0; border-bottom:1px solid rgba(255,255,255,.04); }
.shap-bar-row:last-child { border-bottom:none; }
.shap-feature { font-size:12px; color:var(--muted); width:140px; flex-shrink:0; }
.shap-bar-container { flex:1; height:16px; background:var(--navy-mid); border-radius:3px; position:relative; overflow:hidden; }
.shap-bar-fill { height:100%; border-radius:3px; transition:width .8s ease; }
.shap-bar-fill.positive { background:var(--teal); }
.shap-bar-fill.negative { background:var(--red); }
.shap-val { font-family:var(--font-mono); font-size:11px; width:50px; text-align:right; flex-shrink:0; }
/* V2: ECL gauge */
.ecl-stage-badge { display:inline-flex; align-items:center; justify-content:center; width:40px; height:40px; border-radius:50%; font-family:var(--font-mono); font-size:16px; font-weight:700; }
.ecl-stage-1 { background:rgba(46,204,113,.15); color:var(--green); border:2px solid var(--green); }
.ecl-stage-2 { background:rgba(245,166,35,.15); color:var(--gold); border:2px solid var(--gold); }
.ecl-stage-3 { background:rgba(232,76,76,.15); color:var(--red); border:2px solid var(--red); }
/* V2: Consent row */
.consent-row { display:flex; align-items:center; gap:12px; padding:10px 14px; background:var(--panel); border:1px solid var(--border); border-radius:var(--r); margin-bottom:6px; }
.consent-type { font-size:13px; color:var(--white); flex:1; }
.consent-status { font-family:var(--font-mono); font-size:11px; }
.consent-time { font-family:var(--font-mono); font-size:10px; color:var(--muted); }
/* V2: Side panel views */
.side-panel { display:none; flex:1; overflow-y:auto; padding:24px; }
.side-panel.active { display:block; }
"""

# Write part 1 marker
with open(OUT + ".part1", "w", encoding="utf-8") as f:
    f.write("OK")
print("Part 1 (CSS) ready")
