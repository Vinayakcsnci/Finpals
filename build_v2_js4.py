"""Part 6: JS - Tab render functions"""

JS_TABS = r"""
function renderOverviewTab(app, dscrColor, dscrLabel, pdColor, gradeColor) {
  return `<div class="panel active" id="tab-overview">
    <div class="grid-5" style="margin-bottom:14px">
      <div class="card"><div class="card-title">PD</div><div class="card-value ${pdColor}">${(app.pd*100).toFixed(1)}%</div><div class="card-sub">Probability of Default</div></div>
      <div class="card"><div class="card-title">Risk Grade</div><div class="card-value ${gradeColor}">${app.riskGrade}</div><div class="card-sub">Internal rating</div></div>
      <div class="card"><div class="card-title">DSCR</div><div class="card-value ${dscrColor}">${app.dscr}\u00D7</div><div class="card-sub">${dscrLabel}</div></div>
      <div class="card"><div class="card-title">APR</div><div class="card-value">${app.apr}%</div><div class="card-sub">Risk-based pricing</div></div>
      <div class="card"><div class="card-title">Affordability</div><div class="card-value ${app.affordability>=0.6?'teal':'red'}">${(app.affordability*100).toFixed(0)}%</div><div class="card-sub">Capacity to repay</div></div>
    </div>
    <div class="grid-4" style="margin-bottom:14px">
      <div class="card"><div class="card-title">Declared Revenue</div><div class="card-value">${app.revenue||'\u2014'}</div><div class="card-sub">Management accounts</div></div>
      <div class="card"><div class="card-title">Actual Lodgements</div><div class="card-value ${app.discrepancy?'gold':'teal'}">${app.revenueActual||'\u2014'}</div><div class="card-sub">${app.discrepancy?'\u2691 Variance detected':'\u2713 Reconciled'}</div></div>
      <div class="card"><div class="card-title">Free Cash Flow</div><div class="card-value teal">${app.cashflow||'\u2014'}</div><div class="card-sub">After debt service p.a.</div></div>
      <div class="card"><div class="card-title">ECL (12-month)</div><div class="card-value">\u20AC${app.ecl12m?app.ecl12m.toLocaleString():'\u2014'}</div><div class="card-sub">IFRS 9 Stage ${app.eclStage||'\u2014'}</div></div>
    </div>
    <div class="grid-2">
      <div>
        <div class="section-header"><div class="section-title">Submitted Documents</div></div>
        ${['Management Accounts 2024','Management Accounts 2023','Tax Clearance Certificate','Director ID Docs','6 Months Bank Statements','GDPR Consent Form'].map((d,i)=>`
        <div class="doc-item">
          <div class="doc-icon">\uD83D\uDCC4</div>
          <div style="flex:1"><div class="doc-name">${d}</div><div class="doc-meta">${['PDF','PDF','PDF','JPEG','PDF','PDF'][i]} \u00B7 ${['2.1MB','1.9MB','148KB','1.6MB','4.2MB','89KB'][i]}</div></div>
          <div class="doc-status"><span style="color:var(--teal);font-size:13px">\u2713</span><span style="color:var(--muted);font-size:11px;font-family:var(--font-mono)">Processed</span></div>
        </div>`).join('')}
      </div>
      <div>
        <div class="section-header"><div class="section-title">Monthly Revenue Trend</div></div>
        <div class="card" style="padding-bottom:20px">
          <div class="card-title">Open Banking Lodgements \u2014 12 Months <span style="color:var(--teal)">${app.revenue||''}</span></div>
          <div class="bar-chart" id="revenue-chart"></div>
          <div style="display:flex;justify-content:space-between;margin-top:6px"><span style="font-size:10px;color:var(--muted);font-family:var(--font-mono)">Mar 24</span><span style="font-size:10px;color:var(--muted);font-family:var(--font-mono)">Feb 25</span></div>
        </div>
        ${app.discrepancy ? `<div class="flag-box" style="margin-top:12px"><div class="flag-title">\u2691 Revenue Discrepancy Detected</div><div class="flag-body">${app.discrepancyDetail}</div></div>` : `<div class="flag-box green" style="margin-top:12px"><div class="flag-title">\u2713 Revenue Reconciled</div><div class="flag-body">Declared revenue closely matches actual open banking lodgements. Variance within 2% tolerance.</div></div>`}
        ${app.status==='decided'?`<div class="decision-submitted" style="margin-top:12px"><div class="decision-submitted-icon">${app.decision==='approved'?'\u2705':'\u274C'}</div><div><div class="decision-submitted-text">${app.decision==='approved'?'Application Approved':'Application Declined'}</div><div class="decision-submitted-sub">Decision recorded \u00B7 Audit trail updated</div></div></div>`:''}
      </div>
    </div>
  </div>`;
}

function renderRiskXaiTab(app) {
  const maxShap = Math.max(...(app.shapValues||[]).map(s=>Math.abs(s.value)),0.01);
  return `<div class="panel" id="tab-riskxai">
    <div class="section-header"><div class="section-title">Credit Risk Scoring</div><span class="tag tag-complete">Model: PD v3.2 / LGD v2.1 / EAD v1.8</span></div>
    <div class="grid-3" style="margin-bottom:16px">
      <div class="card"><div class="card-title">PD (Probability of Default)</div>
        <div class="card-value ${app.pd<0.05?'teal':app.pd<0.10?'gold':'red'}">${(app.pd*100).toFixed(1)}%</div>
        <div class="card-sub">Application PD model v3.2</div></div>
      <div class="card"><div class="card-title">LGD (Loss Given Default)</div>
        <div class="card-value">${(app.lgd*100).toFixed(0)}%</div>
        <div class="card-sub">LGD model v2.1</div></div>
      <div class="card"><div class="card-title">EAD (Exposure at Default)</div>
        <div class="card-value">\u20AC${app.ead?app.ead.toLocaleString():'\u2014'}</div>
        <div class="card-sub">EAD model v1.8</div></div>
    </div>
    <div class="grid-2" style="margin-bottom:16px">
      <div class="card"><div class="card-title">Affordability &amp; Capacity to Repay</div>
        <div class="card-value ${app.affordability>=0.6?'teal':'red'}">${(app.affordability*100).toFixed(0)}%</div>
        <div class="card-sub">Cash-flow based \u2014 Affordability model v2.0</div>
        <div class="progress-bar" style="margin-top:10px"><div class="progress-fill" style="width:${app.affordability*100}%;background:${app.affordability>=0.6?'var(--teal)':'var(--red)'}"></div></div>
      </div>
      <div class="card"><div class="card-title">Risk-Based Pricing (EBA LOM)</div>
        <div class="metric-row"><span class="metric-label">APR</span><span class="metric-value">${app.apr}%</span></div>
        <div class="metric-row"><span class="metric-label">Risk Grade</span><span class="metric-value">${app.riskGrade}</span></div>
        <div class="metric-row"><span class="metric-label">Pricing Framework</span><span class="metric-value">EBA LOM aligned</span></div>
        <div class="metric-row"><span class="metric-label">Collateral</span><span class="metric-value">${app.loanType==='Asset Finance'?'Asset-backed':'Unsecured'}</span></div>
      </div>
    </div>
    <div class="section-header"><div class="section-title">SHAP Explainability \u2014 Top Decision Factors</div><span class="tag tag-complete">EU AI Act Art.13</span></div>
    <div class="card" style="margin-bottom:16px">
      <div class="card-title">Local Explanation (Per-Decision) <span style="font-size:10px;color:var(--muted)">SHAP v3.2 \u00B7 GPU-accelerated</span></div>
      ${(app.shapValues||[]).map(s => {
        const w = Math.round((Math.abs(s.value)/maxShap)*100);
        return `<div class="shap-bar-row">
          <div class="shap-feature">${s.feature}</div>
          <div class="shap-bar-container"><div class="shap-bar-fill ${s.direction}" style="width:${w}%"></div></div>
          <div class="shap-val" style="color:${s.direction==='positive'?'var(--teal)':'var(--red)'}">${s.direction==='positive'?'+':'−'}${s.value.toFixed(2)}</div>
        </div>`;
      }).join('')}
    </div>
    <div class="section-header"><div class="section-title">Fairness Metrics</div><span class="tag tag-complete">Bias Check Passed</span></div>
    <div class="grid-2">
      <div class="card">
        <div class="card-title">Disparate Impact Ratio</div>
        <div class="card-value ${app.fairnessMetrics&&app.fairnessMetrics.disparateImpact>=0.80?'green':'red'}">${app.fairnessMetrics?app.fairnessMetrics.disparateImpact.toFixed(2):'\u2014'}</div>
        <div class="card-sub">Threshold: &gt;0.80 ${app.fairnessMetrics&&app.fairnessMetrics.disparateImpact>=0.80?'\u2713 Pass':'\u2717 Fail'}</div>
      </div>
      <div class="card">
        <div class="card-title">Equal Opportunity Delta</div>
        <div class="card-value ${app.fairnessMetrics&&app.fairnessMetrics.equalOpportunity<=0.10?'green':'red'}">${app.fairnessMetrics?app.fairnessMetrics.equalOpportunity.toFixed(2):'\u2014'}</div>
        <div class="card-sub">Threshold: &lt;0.10 ${app.fairnessMetrics&&app.fairnessMetrics.equalOpportunity<=0.10?'\u2713 Pass':'\u2717 Fail'}</div>
      </div>
    </div>
  </div>`;
}

function renderBankingTab(app) {
  return `<div class="panel" id="tab-banking">
    <div class="grid-3" style="margin-bottom:16px">
      <div class="card"><div class="card-title">Bank Account</div><div style="font-size:15px;font-weight:600">AIB Business Current</div><div class="card-sub" style="font-family:var(--font-mono)">****4821 \u00B7 PSD2/AISP</div></div>
      <div class="card"><div class="card-title">Analysis Period</div><div style="font-size:15px;font-weight:600">24 Months</div><div class="card-sub">Feb 2023 \u2014 Feb 2025</div></div>
      <div class="card"><div class="card-title">Avg Monthly Revenue</div><div class="card-value teal" style="font-size:22px">${app.revenueActual ? '\u20AC' + (parseFloat(app.revenueActual.replace(/[\u20ACM]/g,''))*1000/12).toFixed(0)+'K' : '\u2014'}</div><div class="card-sub">From actual lodgements</div></div>
    </div>
    <div class="section-header"><div class="section-title">Recent Transactions</div></div>
    <div class="card" style="padding:0;overflow:hidden">
      <table class="tx-table"><thead><tr><th>Date</th><th>Description</th><th>Category</th><th style="text-align:right">Amount</th></tr></thead>
      <tbody>${(app.transactions||[]).map(t=>`<tr><td style="font-family:var(--font-mono);color:var(--muted)">${t.date}</td><td>${t.desc}</td><td><span class="tx-cat">${t.category}</span></td><td style="text-align:right" class="${t.amount.startsWith('+')?'amount-in':'amount-out'}">${t.amount}</td></tr>`).join('')}</tbody></table>
    </div>
    <div class="section-header" style="margin-top:20px"><div class="section-title">Financial Metrics</div></div>
    <div class="grid-2">
      <div class="card">${[['Annualised Actual Revenue',app.revenueActual||'\u2014'],['Declared Revenue',app.revenue||'\u2014'],['Monthly Debt Service','\u20AC12,800'],['Free Cash Flow p.a.',app.cashflow||'\u2014']].map(([l,v])=>`<div class="metric-row"><span class="metric-label">${l}</span><span class="metric-value">${v}</span></div>`).join('')}</div>
      <div class="card">${[['DSCR (Actual)',app.dscr?app.dscr+'\u00D7':'\u2014'],['Policy Min DSCR','1.20\u00D7'],['DSCR Status',app.dscr>=1.2?'\u2713 Pass':'\u2717 Fail'],['Affordability Score',app.affordability?(app.affordability*100).toFixed(0)+'%':'\u2014']].map(([l,v])=>`<div class="metric-row"><span class="metric-label">${l}</span><span class="metric-value" style="color:${l.includes('Status')?(app.dscr>=1.2?'var(--green)':'var(--red)'):'var(--white)'}">${v}</span></div>`).join('')}</div>
    </div>
  </div>`;
}

function renderIfrs9Tab(app) {
  const stageClass = 'ecl-stage-' + (app.eclStage||1);
  return `<div class="panel" id="tab-ifrs9">
    <div class="section-header"><div class="section-title">IFRS 9 Expected Credit Loss</div><span class="tag tag-complete">ECL Engine v2.4</span></div>
    <div class="grid-4" style="margin-bottom:16px">
      <div class="card" style="text-align:center">
        <div class="card-title" style="justify-content:center">ECL Stage</div>
        <div style="display:flex;justify-content:center;margin:10px 0"><div class="ecl-stage-badge ${stageClass}">${app.eclStage||'\u2014'}</div></div>
        <div class="card-sub">${app.eclStage===1?'Performing':app.eclStage===2?'SICR \u2014 Significant Increase':'Default'}</div>
      </div>
      <div class="card"><div class="card-title">12-Month ECL</div><div class="card-value">\u20AC${app.ecl12m?app.ecl12m.toLocaleString():'\u2014'}</div><div class="card-sub">Stage 1 provision</div></div>
      <div class="card"><div class="card-title">Lifetime ECL</div><div class="card-value ${app.eclStage>=2?'gold':''}">\u20AC${app.eclLifetime?app.eclLifetime.toLocaleString():'\u2014'}</div><div class="card-sub">${app.eclStage>=2?'Applied (Stage 2+)':'Reference only'}</div></div>
      <div class="card"><div class="card-title">EAD</div><div class="card-value">\u20AC${app.ead?app.ead.toLocaleString():'\u2014'}</div><div class="card-sub">Exposure at Default</div></div>
    </div>
    <div class="section-header"><div class="section-title">ECL Scenario Overlays</div></div>
    <div class="grid-3" style="margin-bottom:16px">
      <div class="card"><div class="card-title">Base Case (60%)</div><div class="card-value">\u20AC${app.ecl12m?Math.round(app.ecl12m*1.0).toLocaleString():'\u2014'}</div><div class="card-sub">Central economic forecast</div></div>
      <div class="card"><div class="card-title">Upside (20%)</div><div class="card-value green">\u20AC${app.ecl12m?Math.round(app.ecl12m*0.7).toLocaleString():'\u2014'}</div><div class="card-sub">Favorable conditions</div></div>
      <div class="card"><div class="card-title">Downside (20%)</div><div class="card-value gold">\u20AC${app.ecl12m?Math.round(app.ecl12m*1.8).toLocaleString():'\u2014'}</div><div class="card-sub">Stressed conditions</div></div>
    </div>
    <div class="section-header"><div class="section-title">PD/LGD/EAD Inputs (Point-in-Time)</div></div>
    <div class="card">
      ${[
        ['PD (12-month)',(app.pd*100).toFixed(2)+'%'],
        ['PD (Lifetime)',(app.pd*100*3.2).toFixed(2)+'%'],
        ['LGD',(app.lgd*100).toFixed(0)+'%'],
        ['EAD','\u20AC'+(app.ead?app.ead.toLocaleString():'\u2014')],
        ['Discount Rate','4.5% (EIR)'],
        ['Staging Trigger',app.eclStage===1?'No SICR detected':'SICR \u2014 significant deterioration'],
      ].map(([l,v])=>`<div class="metric-row"><span class="metric-label">${l}</span><span class="metric-value">${v}</span></div>`).join('')}
    </div>
    <div class="flag-box blue" style="margin-top:16px">
      <div class="flag-title">IFRS 9 Compliance Note</div>
      <div class="flag-body">ECL calculations follow IFRS 9 requirements with multi-scenario overlays (base/upside/downside). PD/LGD/EAD are refreshed point-in-time per EBA LOM expectations. Monthly provisioning runs with scenario sensitivity analysis. Disclosures prepared per IFRS 7/9.</div>
    </div>
  </div>`;
}

function renderChecksTab(app) {
  return `<div class="panel" id="tab-checks">
    <div class="section-header"><div class="section-title">Automated Compliance Checks</div></div>
    <div style="margin-bottom:16px">
      ${(app.checks||[]).map(c => {
        const icon = {pass:'\u2705',warn:'\u26A0\uFE0F',fail:'\u274C'}[c.status];
        const bc = {pass:'rgba(46,204,113,.2)',warn:'rgba(245,166,35,.2)',fail:'rgba(232,76,76,.25)'}[c.status];
        return `<div class="check-item" style="border-color:${bc}"><div class="check-status-icon">${icon}</div><div style="flex:1"><div class="check-name">${c.name}</div><div class="check-detail">${c.detail}</div></div><div class="check-timestamp">${c.time}</div></div>`;
      }).join('')}
    </div>
    ${app.consentLog && app.consentLog.length ? `
    <div class="section-header"><div class="section-title">GDPR Consent Ledger</div><span class="tag tag-complete">Art.22 Compliant</span></div>
    ${app.consentLog.map(c => `
      <div class="consent-row">
        <span style="color:var(--green);font-size:14px">\u2713</span>
        <div class="consent-type">${c.type}</div>
        <div class="consent-status" style="color:var(--green)">${c.status}</div>
        <div class="consent-time">${c.timestamp}</div>
      </div>`).join('')}
    <div style="margin-top:10px;display:flex;gap:8px">
      <button class="btn btn-outline" style="font-size:11px;padding:5px 12px">\u2139 Right to Explanation</button>
      <button class="btn btn-outline" style="font-size:11px;padding:5px 12px">\u270B Right to Object (Art.21)</button>
      <button class="btn btn-outline" style="font-size:11px;padding:5px 12px">\u2709 Data Subject Request</button>
    </div>` : ''}
    <div class="flag-box blue" style="margin-top:16px">
      <div class="flag-title">EU AI Act &amp; EBA LOM Compliance</div>
      <div class="flag-body">Credit scoring/creditworthiness assessment is classified as <strong>high-risk AI</strong> under EU AI Act 2024/1689. All checks above satisfy Art.9-15 requirements including risk management, data governance, transparency, logging, human oversight, and accuracy/robustness. EBA LOM (EBA/GL/2020/06) credit policy gates are applied. GDPR Art.22 safeguards (SCHUFA ruling) ensure meaningful human oversight for automated decisions.</div>
    </div>
  </div>`;
}
"""

with open(__file__.replace("_js4.py", "_js4.txt"), "w", encoding="utf-8") as f:
    f.write(JS_TABS)
print("Part 6 (JS tabs) ready")
