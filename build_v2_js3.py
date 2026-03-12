"""Part 5: JS - renderAppList, loadApp, renderProcessing, renderFullApp"""

JS_APP = r"""
// ── Render sidebar app list ─────────────────────────────────
function renderAppList() {
  const el = document.getElementById('app-list');
  el.innerHTML = APPS.map(a => {
    const dot = {complete:'<span class="status-dot dot-green"></span>',processing:'<span class="status-dot dot-teal"></span>',flagged:'<span class="status-dot dot-yellow"></span>',decided:'<span class="status-dot dot-grey"></span>'}[a.status];
    const label = {complete:'Ready',processing:'Processing',flagged:'Flagged',decided:a.decision==='approved'?'Approved':'Decided'}[a.status];
    return `<div class="app-card ${currentAppId===a.id?'active':''}" onclick="switchView('apps');loadApp('${a.id}')">
      <div class="app-card-name">${a.company}</div>
      <div class="app-card-meta"><span>${dot}${label}</span><span>${a.amount}</span></div>
    </div>`;
  }).join('');
}

// ── Load application ────────────────────────────────────────
function loadApp(id) {
  currentAppId = id;
  renderAppList();
  const app = APPS.find(a => a.id === id);
  document.getElementById('topbar-title').textContent = app.company;
  document.getElementById('topbar-sub').textContent = `${app.id} \u00B7 ${app.loanType} \u00B7 Requested ${app.requested||'\u2014'}`;
  document.getElementById('topbar-actions').innerHTML = `<button class="btn btn-outline" onclick="showNewAppModal()">&#xFF0B; New Application</button>`;
  const content = document.getElementById('content');
  // hide side panels
  document.querySelectorAll('.side-panel').forEach(p=>{p.style.display='none';p.classList.remove('active');});
  const viewApps = document.getElementById('view-apps');
  viewApps.style.display=''; viewApps.classList.add('active');
  if (app.status === 'processing') { renderProcessing(app, viewApps); return; }
  renderFullApp(app, viewApps);
}

// ── Render processing ───────────────────────────────────────
function renderProcessing(app, container) {
  processingStep = 0;
  container.innerHTML = `
    <div style="flex:1;overflow-y:auto;padding:24px">
      <div style="display:flex;gap:14px;margin-bottom:20px">
        <div class="card" style="flex:1"><div class="card-title">Company</div><div style="font-family:var(--font-head);font-size:18px;font-weight:700">${app.company}</div><div class="chip chip-teal" style="display:inline-block;margin-top:6px">${app.sector}</div></div>
        <div class="card" style="flex:1"><div class="card-title">Loan Requested</div><div class="card-value teal">${app.amount}</div><div class="card-sub">${app.loanType}</div></div>
        <div class="card" style="flex:2"><div class="card-title">Assessment Status</div><div style="display:flex;align-items:center;gap:10px;margin-bottom:8px"><div class="tag tag-processing"><span class="status-dot dot-teal" style="width:7px;height:7px"></span> AI Assessment Running</div><div class="tag tag-danger">HIGH-RISK AI SYSTEM</div></div><div class="progress-bar"><div class="progress-fill" id="proc-bar" style="width:5%"></div></div></div>
      </div>
      <div class="processing-panel">
        <div class="spinner"></div>
        <div style="font-family:var(--font-head);font-size:18px;font-weight:700;color:var(--teal)" id="proc-headline">Initialising assessment\u2026</div>
        <div style="font-size:12px;color:var(--muted);margin-top:4px">FinPal is processing this application with EU AI Act compliant controls</div>
        <div class="step-list" id="proc-steps"></div>
      </div>
    </div>`;
  runProcessingAnimation(app);
}

function runProcessingAnimation(app) {
  clearInterval(processingTimer);
  const stepsEl = document.getElementById('proc-steps');
  const headline = document.getElementById('proc-headline');
  const bar = document.getElementById('proc-bar');
  processingTimer = setInterval(() => {
    processingStep++;
    const pct = Math.min(95, Math.round((processingStep / processingSteps.length) * 100));
    if (bar) bar.style.width = pct + '%';
    if (headline) headline.textContent = processingSteps[processingStep - 1] || 'Finalising\u2026';
    if (stepsEl) {
      stepsEl.innerHTML = processingSteps.slice(0, processingStep).map(s =>
        `<div class="step-item done"><span class="step-icon step-check">\u2713</span>${s}</div>`
      ).join('');
      stepsEl.scrollTop = stepsEl.scrollHeight;
    }
    if (processingStep >= processingSteps.length) {
      clearInterval(processingTimer);
      app.status = 'complete'; app.dscr = 1.65; app.revenue = '\u20AC3.2M'; app.revenueActual = '\u20AC3.18M';
      app.cashflow = '\u20AC210K'; app.discrepancy = false; app.requested = '19 Feb 2025';
      app.pd = 0.022; app.lgd = 0.38; app.ead = 185000; app.affordability = 0.87; app.riskGrade = 'A2'; app.apr = 7.2;
      app.eclStage = 1; app.ecl12m = 1549; app.eclLifetime = 4800;
      app.shapValues = [
        {feature:'DSCR (1.65\u00D7)',value:0.38,direction:'positive'},
        {feature:'Revenue Stability',value:0.30,direction:'positive'},
        {feature:'Contract Diversity',value:0.22,direction:'positive'},
        {feature:'Asset Backing',value:0.15,direction:'positive'},
        {feature:'Sector Cyclicality',value:0.08,direction:'negative'},
      ];
      app.fairnessMetrics = {disparateImpact:0.94,equalOpportunity:0.02};
      app.consentLog = [
        {type:'Open Banking (PSD2)',timestamp:'10:48:20',status:'granted'},
        {type:'Credit Bureau Pull',timestamp:'10:48:21',status:'granted'},
        {type:'Automated Processing (GDPR Art.22)',timestamp:'10:48:22',status:'granted'},
      ];
      app.narrative = `<strong>Clancy Logistics DAC</strong> is an established transport and logistics operator based in Athlone with 8 years of continuous trading.<br><br>Open banking analysis confirms <strong>consistent and growing revenue</strong> with annualised actual revenue of <strong>\u20AC3.18M</strong> closely aligned with declared \u20AC3.2M \u2014 variance of only <strong>0.6%</strong>.<br><br>PD model (v3.2) calculates <strong>probability of default at 2.2%</strong> with LGD of 38%, resulting in <strong>risk grade A2</strong>. Risk-based pricing: <strong>7.2% APR</strong>. DSCR of <strong>1.65\u00D7</strong> comfortably above 1.20\u00D7 policy threshold. IFRS 9: <strong>Stage 1</strong> with 12-month ECL of \u20AC1,549. All compliance checks passed. SHAP analysis identifies DSCR and revenue stability as primary positive drivers.`;
      app.checks = [
        {name:'GDPR Art.13/14 Notice',detail:'Data processing notice acknowledged. Consent obtained.',status:'pass',time:'10:48:22'},
        {name:'AML / PEP Screening',detail:'Patrick Clancy (Director) \u2014 Clear.',status:'pass',time:'10:48:33'},
        {name:'CRO Company History',detail:'Incorporated 14 Mar 2017. Status: Normal.',status:'pass',time:'10:48:35'},
        {name:'Tax Clearance (ROS)',detail:'Certificate valid. All tax headings current.',status:'pass',time:'10:48:36'},
        {name:'Fraud & Synthetic ID Check',detail:'Device fingerprint normal. No duplicates.',status:'pass',time:'10:48:37'},
        {name:'Revenue Reconciliation',detail:'Declared \u20AC3.2M vs actual \u20AC3.18M. Variance 0.6%. Within tolerance.',status:'pass',time:'10:48:38'},
        {name:'EBA LOM Credit Policy',detail:'DSCR 1.65\u00D7 exceeds 1.20\u00D7 minimum. All policy gates passed.',status:'pass',time:'10:48:40'},
        {name:'EU AI Act Compliance',detail:'High-risk controls active. SHAP explanations generated.',status:'pass',time:'10:48:41'},
        {name:'Fairness & Bias Check',detail:'DI: 0.94 (>0.80). EO delta: 0.02 (<0.10). No bias detected.',status:'pass',time:'10:48:42'},
      ];
      app.transactions = [
        {date:'Jan 25',desc:'LODGE - DPD CONTRACT',category:'Revenue',amount:'+\u20AC94,300'},
        {date:'Jan 25',desc:'LODGE - AMAZON FREIGHT',category:'Revenue',amount:'+\u20AC68,200'},
        {date:'Jan 25',desc:'DWT PAYROLL',category:'Payroll',amount:'-\u20AC38,400'},
        {date:'Jan 25',desc:'AIB LEASE REPAYMENT',category:'Debt Service',amount:'-\u20AC11,200'},
        {date:'Dec 24',desc:'LODGE - DPD CONTRACT',category:'Revenue',amount:'+\u20AC91,800'},
        {date:'Dec 24',desc:'DWT PAYROLL',category:'Payroll',amount:'-\u20AC38,400'},
        {date:'Nov 24',desc:'LODGE - AMAZON FREIGHT',category:'Revenue',amount:'+\u20AC72,100'},
      ];
      app.bars = [62,70,75,80,72,85,78,88,82,90,86,95];
      renderAppList();
      setTimeout(() => { if (currentAppId===app.id) { renderFullApp(app,document.getElementById('view-apps')); showToast('\u2713 Assessment complete \u2014 evidence pack ready'); } }, 800);
    }
  }, 700);
}

// ── Render full application ─────────────────────────────────
function renderFullApp(app, container) {
  const statusChip = {
    complete:'<span class="tag tag-complete">\u2713 Assessment Complete</span>',
    flagged:'<span class="tag tag-flagged">\u2691 Flagged \u2014 Review Required</span>',
    decided:`<span class="tag ${app.decision==='approved'?'tag-complete':'tag-flagged'}">${app.decision==='approved'?'\u2713 Approved':'\u2717 Declined'}</span>`,
  }[app.status] || '';
  const tabAlert = app.discrepancy ? ' tab-alert' : '';
  const dscrColor = app.dscr >= 1.2 ? 'teal' : 'red';
  const dscrLabel = app.dscr >= 1.2 ? '\u2713 Above Policy Min 1.20\u00D7' : '\u2717 Below Policy Min 1.20\u00D7';
  const pdColor = app.pd < 0.05 ? 'teal' : app.pd < 0.10 ? 'gold' : 'red';
  const gradeColor = app.riskGrade && app.riskGrade.startsWith('A') ? 'teal' : app.riskGrade && app.riskGrade.startsWith('B') ? 'green' : app.riskGrade && app.riskGrade.startsWith('C') ? 'gold' : 'red';

  container.innerHTML = `
    <div id="app-header">
      <div class="app-meta-row">
        <div style="flex:1">
          <div class="app-company">${app.company}</div>
          <div class="app-ref">${app.id} \u00B7 ${app.crn} \u00B7 ${app.sector}</div>
          <div class="meta-chips" style="margin-top:8px">
            ${statusChip}
            <span class="chip chip-red">EU AI Act: High-Risk</span>
            <span class="chip chip-teal">${app.loanType}</span>
            <span class="chip">${app.amount} requested</span>
            ${app.riskGrade ? `<span class="chip chip-${gradeColor==='teal'||gradeColor==='green'?'green':'gold'}">Grade: ${app.riskGrade}</span>` : ''}
          </div>
        </div>
        ${app.status !== 'decided' ? `
        <div style="display:flex;gap:8px">
          <button class="btn btn-outline" onclick="exportPack('${app.id}')">\u2193 Export Pack</button>
          ${app.status==='complete'||app.status==='flagged'?`<button class="btn btn-primary" onclick="openDecisionModal('${app.id}')">Make Decision \u2192</button>`:''}
        </div>` : ''}
      </div>
      <div class="tabs">
        <div class="tab active" data-tab="overview">Overview</div>
        <div class="tab" data-tab="riskxai">Risk &amp; XAI</div>
        <div class="tab" data-tab="banking">Open Banking</div>
        <div class="tab" data-tab="ifrs9">IFRS 9</div>
        <div class="tab${tabAlert}" data-tab="checks">Compliance</div>
        <div class="tab" data-tab="evidence">Evidence Pack</div>
        <div class="tab" data-tab="audit-log">Audit Log</div>
      </div>
    </div>
    <div style="flex:1;overflow:hidden;position:relative">
      ${renderOverviewTab(app, dscrColor, dscrLabel, pdColor, gradeColor)}
      ${renderRiskXaiTab(app)}
      ${renderBankingTab(app)}
      ${renderIfrs9Tab(app)}
      ${renderChecksTab(app)}
      ${renderEvidenceTab(app)}
      ${renderAuditTab(app)}
    </div>`;
  setTimeout(() => drawBarChart(app), 50);
  bindTabs(container);
}
"""

with open(__file__.replace("_js3.py", "_js3.txt"), "w", encoding="utf-8") as f:
    f.write(JS_APP)
print("Part 5 (JS app rendering) ready")
