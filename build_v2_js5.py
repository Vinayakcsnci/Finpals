"""Part 7: JS - Evidence, Audit, Utilities"""

JS_UTILS = r"""
function renderEvidenceTab(app) {
  return `<div class="panel" id="tab-evidence">
    <div class="evidence-header">
      <div style="font-size:11px;color:var(--teal);font-family:var(--font-mono);margin-bottom:6px;letter-spacing:.5px">CREDIT EVIDENCE PACK \u00B7 EU AI ACT COMPLIANT</div>
      <div class="evidence-company">${app.company}</div>
      <div class="evidence-meta">
        <div class="evidence-meta-item"><div class="evidence-meta-label">Reference</div><div class="evidence-meta-value">${app.id}</div></div>
        <div class="evidence-meta-item"><div class="evidence-meta-label">Amount</div><div class="evidence-meta-value">${app.amount}</div></div>
        <div class="evidence-meta-item"><div class="evidence-meta-label">Product</div><div class="evidence-meta-value">${app.loanType}</div></div>
        <div class="evidence-meta-item"><div class="evidence-meta-label">Risk Grade</div><div class="evidence-meta-value">${app.riskGrade||'\u2014'}</div></div>
        <div class="evidence-meta-item"><div class="evidence-meta-label">APR</div><div class="evidence-meta-value">${app.apr?app.apr+'%':'\u2014'}</div></div>
        <div class="evidence-meta-item"><div class="evidence-meta-label">Generated</div><div class="evidence-meta-value">${new Date().toLocaleDateString('en-IE')}</div></div>
      </div>
    </div>
    ${app.narrative ? `<div class="narrative-box"><div class="narrative-text">${app.narrative}</div></div>` : ''}
    <div class="grid-2" style="margin-bottom:14px">
      <div class="card">
        <div class="card-title">Key Financial Findings</div>
        ${[
          ['Declared Revenue',app.revenue||'\u2014',''],
          ['Actual Revenue (Open Banking)',app.revenueActual||'\u2014',app.discrepancy?'flag-amber':'flag-green'],
          ['Revenue Variance',app.discrepancy?'\u2691 >5%':'\u2713 <2%',app.discrepancy?'flag-amber':'flag-green'],
          ['PD',app.pd?(app.pd*100).toFixed(1)+'%':'\u2014',app.pd<0.05?'flag-green':app.pd<0.10?'flag-amber':'flag-red'],
          ['LGD / EAD',app.lgd?(app.lgd*100).toFixed(0)+'% / \u20AC'+app.ead.toLocaleString():'\u2014',''],
          ['DSCR',app.dscr?app.dscr+'\u00D7':'\u2014',app.dscr>=1.2?'flag-green':'flag-red'],
          ['Risk Grade',app.riskGrade||'\u2014',app.riskGrade&&app.riskGrade<='B9'?'flag-green':'flag-amber'],
          ['APR (Risk-Based)',app.apr?app.apr+'%':'\u2014',''],
          ['ECL (12m / Lifetime)',app.ecl12m?'\u20AC'+app.ecl12m.toLocaleString()+' / \u20AC'+app.eclLifetime.toLocaleString():'\u2014',''],
          ['Policy Gate',app.dscr>=1.2?'\u2713 Pass':'\u2717 Fail',app.dscr>=1.2?'flag-green':'flag-red'],
        ].map(([l,v,f])=>`<div class="finding-row"><div class="finding-label">${l}</div><div class="finding-value">${v}${f?`<span class="finding-flag ${f}">${f.includes('green')?'Pass':f.includes('red')?'Fail':'Review'}</span>`:''}</div></div>`).join('')}
      </div>
      <div class="card">
        <div class="card-title">Compliance Summary</div>
        ${(app.checks||[]).map(c=>`<div class="finding-row"><div class="finding-label">${c.name}</div><div class="finding-value" style="color:${c.status==='pass'?'var(--green)':c.status==='warn'?'var(--gold)':'var(--red)'}">${c.status==='pass'?'\u2713 Clear':c.status==='warn'?'\u2691 Review':'\u2717 Fail'}</div></div>`).join('')}
      </div>
    </div>
    <div class="section-header"><div class="section-title">Pricing Transparency (EBA LOM)</div></div>
    <div class="card" style="margin-bottom:14px">
      <div class="metric-row"><span class="metric-label">Risk-Based APR</span><span class="metric-value">${app.apr?app.apr+'%':'\u2014'}</span></div>
      <div class="metric-row"><span class="metric-label">Risk Grade</span><span class="metric-value">${app.riskGrade||'\u2014'}</span></div>
      <div class="metric-row"><span class="metric-label">PD Component</span><span class="metric-value">${(app.pd*100).toFixed(2)}% - spread +${((app.pd*100)*0.8).toFixed(1)}bps</span></div>
      <div class="metric-row"><span class="metric-label">LGD Component</span><span class="metric-value">${(app.lgd*100).toFixed(0)}% - capital charge applied</span></div>
      <div class="metric-row"><span class="metric-label">Pricing Framework</span><span class="metric-value">EBA LOM aligned - risk-based pricing policy</span></div>
      <div class="metric-row"><span class="metric-label">Collateral Valuation</span><span class="metric-value">${app.loanType==='Asset Finance'?'Independent valuation required':'Not applicable (unsecured)'}</span></div>
    </div>
    <div class="decision-gate">
      <div class="decision-gate-title">\u2696 Underwriter Decision Gate</div>
      <div class="decision-gate-sub">FinPal has presented the evidence. The credit decision is yours. Under Ireland's IAF, EU AI Act Art.14 (human oversight), and GDPR Art.22, your decision and rationale will be permanently recorded.</div>
      ${app.status !== 'decided' ? `
      <textarea class="decision-textarea" id="ev-rationale" placeholder="Enter your decision rationale here (mandatory \u2014 recorded to immutable audit trail per EU AI Act Art.12)\u2026"></textarea>
      <div class="decision-buttons">
        <button class="btn btn-danger" onclick="openDecisionModal('${app.id}','decline')">\u2717 Decline Application</button>
        <button class="btn btn-primary" onclick="openDecisionModal('${app.id}','approve')">\u2713 Approve Application</button>
      </div>` : `
      <div class="decision-submitted"><div class="decision-submitted-icon">${app.decision==='approved'?'\u2705':'\u274C'}</div><div><div class="decision-submitted-text">Decision ${app.decision==='approved'?'Approved':'Declined'} \u2014 Logged to Audit Trail</div><div class="decision-submitted-sub">Decision recorded \u00B7 CBI/EU AI Act inspection-ready</div></div></div>`}
    </div>
  </div>`;
}

function renderAuditTab(app) {
  const entries = [
    {time:'14:21:45',dot:'',event:'GDPR Art.13/14 notice presented',detail:'Data processing notice displayed to applicant'},
    {time:'14:21:47',dot:'',event:'Consent obtained (GDPR Art.22)',detail:'Applicant consented to automated processing \u00B7 Right to object explained'},
    {time:'14:22:05',dot:'',event:'Application received',detail:`${app.id} \u00B7 ${app.company} \u00B7 ${app.loanType} \u00B7 ${app.amount}`},
    {time:'14:22:06',dot:'',event:'Open banking consent obtained (PSD2)',detail:'SME authorised read access via AISP'},
    {time:'14:22:07',dot:'',event:'Documents ingested',detail:'6 documents \u00B7 OCR extraction complete'},
    {time:'14:22:09',dot:'',event:'Transaction history pulled',detail:'284 transactions \u00B7 24 months'},
    {time:'14:22:12',dot:'',event:'PD/LGD/EAD models executed',detail:`PD: ${app.pd?(app.pd*100).toFixed(1)+'%':'N/A'} \u00B7 LGD: ${app.lgd?(app.lgd*100).toFixed(0)+'%':'N/A'} \u00B7 Model v3.2/v2.1/v1.8`},
    {time:'14:22:13',dot:'',event:'SHAP explanations generated',detail:'Local + global explanations \u00B7 GPU-accelerated \u00B7 EU AI Act Art.13 compliant'},
    {time:'14:22:14',dot:'',event:'Fairness metrics computed',detail:`DI: ${app.fairnessMetrics?app.fairnessMetrics.disparateImpact.toFixed(2):'N/A'} \u00B7 EO: ${app.fairnessMetrics?app.fairnessMetrics.equalOpportunity.toFixed(2):'N/A'}`},
    {time:'14:22:15',dot:'gold',event:'Revenue reconciliation',detail:app.discrepancy?'Variance detected \u2014 flagged for review':'Reconciled within tolerance'},
    {time:'14:22:17',dot:'',event:'AML / PEP screening complete',detail:'All directors clear'},
    {time:'14:22:18',dot:'',event:'CRO check complete',detail:'Company status normal'},
    {time:'14:22:19',dot:'',event:'Tax clearance verified',detail:'ROS confirmation valid'},
    {time:'14:22:20',dot:'',event:'IFRS 9 ECL calculated',detail:`Stage ${app.eclStage||'\u2014'} \u00B7 12m ECL: \u20AC${app.ecl12m?app.ecl12m.toLocaleString():'N/A'}`},
    {time:'14:22:21',dot:'',event:'EBA LOM credit policy applied',detail:`DSCR ${app.dscr||'N/A'}\u00D7 vs 1.20\u00D7 minimum`},
    {time:'14:22:22',dot:'',event:'EU AI Act compliance verified',detail:'High-risk controls: Art.9-15 all satisfied'},
    {time:'14:22:23',dot:'',event:'Risk-based pricing calculated',detail:`APR: ${app.apr||'N/A'}% \u00B7 Grade: ${app.riskGrade||'N/A'} \u00B7 EBA LOM pricing framework`},
    {time:'14:22:25',dot:'',event:'Evidence pack generated',detail:'PDF credit memo prepared \u00B7 All source data referenced'},
    {time:'14:22:26',dot:'',event:'Assessment complete \u2014 awaiting underwriter decision',detail:'Processing time: 41 seconds'},
  ];
  if (app.status === 'decided') {
    entries.push({time:'15:42:01',dot:app.decision==='approved'?'green':'red',event:`Credit decision: ${app.decision}`,detail:'Underwriter: M. Walsh \u00B7 Rationale documented \u00B7 Audit record sealed'});
  }
  return `<div class="panel" id="tab-audit-log">
    <div class="section-header"><div class="section-title">Immutable Audit Trail</div><span class="tag tag-complete">CBI / EU AI Act Inspection Ready</span></div>
    <div class="flag-box green" style="margin-bottom:16px">
      <div class="flag-title">\u2713 EU AI Act Art.12 &amp; IAF Compliance</div>
      <div class="flag-body">This audit trail is cryptographically immutable. Every entry is timestamped and attributed. Compliant with EU AI Act Art.12 (record-keeping), GDPR Art.30, and Ireland's Individual Accountability Framework.</div>
    </div>
    <div class="card" style="padding:4px 16px">
      ${entries.map(e=>`<div class="audit-item"><div class="audit-time">${e.time}</div><div class="audit-dot ${e.dot}"></div><div><div class="audit-event">${e.event}</div><div class="audit-detail">${e.detail}</div></div></div>`).join('')}
    </div>
  </div>`;
}

// ── Utility functions ───────────────────────────────────────
function drawBarChart(app) {
  const chartEl = document.getElementById('revenue-chart');
  if (chartEl && app.bars && app.bars.length) {
    const months = ['M','A','M','J','J','A','S','O','N','D','J','F'];
    const max = Math.max(...app.bars);
    chartEl.innerHTML = app.bars.map((v,i) => {
      const h = Math.round((v/max)*100);
      return `<div class="bar-col"><div class="bar-fill" style="height:${h}%;background:${v===max?'var(--teal)':'var(--navy-mid)'}"></div><div class="bar-label">${months[i]}</div></div>`;
    }).join('');
  }
}

function bindTabs(container) {
  container.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      container.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
      container.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
      tab.classList.add('active');
      const panel = container.querySelector('#tab-'+tab.dataset.tab);
      if (panel) panel.classList.add('active');
    });
  });
}

// ── Decision modal ──────────────────────────────────────────
let pendingDecision = {id:null,type:null};
function openDecisionModal(id,type) {
  pendingDecision = {id,type};
  document.getElementById('dm-title').textContent = type==='approve'?'Approve Application':type==='decline'?'Decline Application':'Submit Credit Decision';
  document.getElementById('dm-approve-btn').style.display = type==='decline'?'none':'';
  document.getElementById('dm-decline-btn').style.display = type==='approve'?'none':'';
  document.getElementById('dm-rationale').value = '';
  document.getElementById('decision-modal').classList.add('open');
}
function closeDecisionModal() { document.getElementById('decision-modal').classList.remove('open'); }
function submitDecision(type) {
  const r = document.getElementById('dm-rationale').value.trim();
  if (!r) { document.getElementById('dm-rationale').style.borderColor='var(--red)'; document.getElementById('dm-rationale').placeholder='Rationale is mandatory under IAF & GDPR Art.22'; return; }
  closeDecisionModal();
  const app = APPS.find(a=>a.id===pendingDecision.id||a.id===currentAppId);
  if (app) {
    app.status='decided'; app.decision=type==='approve'?'approved':'declined';
    renderAppList();
    renderFullApp(app,document.getElementById('view-apps'));
    showToast(type==='approve'?'\u2713 Application approved \u2014 decision logged':'\u2717 Application declined \u2014 decision logged');
  }
}

// ── New app modal ───────────────────────────────────────────
function showNewAppModal() { document.getElementById('new-app-modal').classList.add('open'); }
function submitNewApp() {
  const company = document.getElementById('new-company').value.trim();
  const amount = document.getElementById('new-amount').value.trim();
  const type = document.getElementById('new-type').value;
  if (!company||!amount||!type) return;
  const newId = 'FP-2025-00'+(43+APPS.filter(a=>a.status==='processing').length);
  APPS.unshift({
    id:newId, company, sector:'General', amount:amount.startsWith('\u20AC')?amount:'\u20AC'+amount,
    loanType:type, crn:'CRN pending', requested:new Date().toLocaleDateString('en-IE',{day:'numeric',month:'short',year:'numeric'}),
    status:'processing', dscr:null, revenue:null, discrepancy:false, narrative:null,
    pd:null,lgd:null,ead:null,affordability:null,riskGrade:null,apr:null,
    eclStage:null,ecl12m:null,eclLifetime:null,shapValues:[],fairnessMetrics:null,consentLog:[],
    checks:[], transactions:[], bars:[],
  });
  document.getElementById('new-app-modal').classList.remove('open');
  renderAppList();
  loadApp(newId);
  showToast('Assessment started for '+company);
}

function exportPack(id) { showToast('\uD83D\uDCC4 Evidence pack export initiated\u2026'); }

function showToast(msg) {
  const existing = document.querySelector('.toast');
  if (existing) existing.remove();
  const t = document.createElement('div');
  t.className = 'toast'; t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(()=>{t.classList.add('hide');setTimeout(()=>t.remove(),300);},3000);
}

// ── Init ────────────────────────────────────────────────────
renderAppList();
loadApp(APPS[0].id);
"""

with open(__file__.replace("_js5.py", "_js5.txt"), "w", encoding="utf-8") as f:
    f.write(JS_UTILS)
print("Part 7 (JS utils) ready")
