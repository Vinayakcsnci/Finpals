"""Part 4: JS functions - views, rendering"""

JS_FUNCS = r"""
// ── Sidebar view switching ──────────────────────────────────
function switchView(view) {
  currentView = view;
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.querySelector(`.nav-item[data-view="${view}"]`).classList.add('active');
  document.querySelectorAll('#content > div').forEach(p => { p.classList.remove('active'); p.style.display='none'; });

  if (view === 'apps') {
    const el = document.getElementById('view-apps');
    el.style.display=''; el.classList.add('active');
    if (currentAppId) loadApp(currentAppId);
    return;
  }
  const panel = document.getElementById('view-' + view);
  if (panel) { panel.style.display='block'; panel.classList.add('active'); }
  renderSideView(view);
}

function renderSideView(view) {
  const el = document.getElementById('view-' + view);
  if (!el) return;
  if (view === 'intake') el.innerHTML = renderIntakePipeline();
  else if (view === 'models') el.innerHTML = renderModelGovernance();
  else if (view === 'portfolio') el.innerHTML = renderPortfolioRisk();
  else if (view === 'compliance') el.innerHTML = renderComplianceDashboard();
  else if (view === 'collections') el.innerHTML = renderCollections();
  else if (view === 'bureau') el.innerHTML = renderBureauReporting();
  else if (view === 'audit') el.innerHTML = renderGlobalAudit();
  else if (view === 'architecture') el.innerHTML = renderArchitecture();
}

// ── Intake Pipeline ──────────────────────────────────────────
function renderIntakePipeline() {
  const steps = [
    {
      num:'1', label:'Borrower Application Submission', icon:'\u{1F4DD}', color:'var(--teal)',
      desc:'Borrower accesses the self-service intake portal and submits company details, loan amount, and loan purpose. GDPR Art.13/14 notice is presented automatically. Consent for automated processing (Art.22) is captured and timestamped before any data is processed.',
      items:['Company name, CRN, director details','Loan amount and purpose','GDPR consent capture (Art.13/14, Art.22)','Identity verification consent'],
    },
    {
      num:'2', label:'Document Upload', icon:'\u{1F4CE}', color:'var(--teal)',
      desc:'Borrower uploads supporting documents through the secure intake portal. All documents are encrypted in transit and at rest within the lender\'s dedicated tenant environment. No documents are accessible to FinPal or any external party.',
      items:['Passport / Director photo ID (JPEG/PDF)','Management accounts / financial statements (PDF)','Company registration documents (CRO)','Tax clearance certificate (ROS)','Bank statements (6-24 months)'],
    },
    {
      num:'3', label:'IDP \u2014 Intelligent Document Processing', icon:'\u{1F916}', color:'var(--teal)',
      desc:'FinPal\'s AI runs OCR and structured data extraction on all uploaded documents within the lender\'s isolated model instance. No raw document data leaves the lender\'s tenant environment. The AI model is dedicated per lender \u2014 it does not share compute or data with other lenders or external AI providers (OpenAI, AWS, etc.).',
      items:['OCR extraction of financial figures from PDFs','Named entity recognition (director names, company details)','Structured data output: revenue, P&L, balance sheet','Document authenticity signals (layout, font, metadata)','All processing inside dedicated tenant \u2014 no external AI calls'],
    },
    {
      num:'4', label:'Data Validation & External Checks', icon:'\u2705', color:'var(--gold)',
      desc:'Extracted data is cross-validated against authoritative external sources. This step confirms the accuracy of borrower-supplied information before the application enters the credit assessment pipeline.',
      items:['CRO company registry \u2014 directors, incorporation, filing history','Revenue reconciliation: declared vs actual open banking lodgements','AML/PEP screening on all directors','Tax clearance verification (ROS)','Identity verification against submitted documents','Fraud & synthetic identity detection'],
    },
    {
      num:'5', label:'Credit Assessment & CRM Entry', icon:'\u{1F4CA}', color:'var(--green)',
      desc:'Only after successful document processing and validation does the application enter the credit assessment pipeline. The CRM is the last step \u2014 it is the record of a clean, verified application. This is where FinPal runs PD/LGD/EAD models, SHAP explainability, IFRS 9 ECL, and risk-based pricing before presenting the evidence pack to the underwriter.',
      items:['PD / LGD / EAD credit scoring models','SHAP explainability \u2014 per-decision transparency (EU AI Act Art.13)','IFRS 9 ECL calculation and staging','Risk-based pricing (EBA LOM)','Fairness & bias checks','Evidence pack generation \u2014 human decision gate'],
    },
  ];
  return `
    <div class="section-header"><div class="section-title">AI-Powered Loan Application Intake Pipeline</div>
      <span class="tag tag-complete">IDP \u00B7 Document Processing \u00B7 Assessment</span></div>
    <div class="flag-box blue" style="margin-top:0;margin-bottom:20px">
      <div class="flag-title">\u{1F4A1} What FinPal Actually Does</div>
      <div class="flag-body">FinPal is not a CRM. The core product is an <strong>AI-powered loan application intake, document processing and credit assessment pipeline</strong>. The CRM is downstream infrastructure \u2014 it only receives clean, validated, assessed applications. The real value is in Steps 1\u20134: automating the slow, manual, error-prone intake process that costs lenders hours per application.</div>
    </div>
    ${steps.map(s => `
    <div class="card" style="margin-bottom:14px;border-left:3px solid ${s.color}">
      <div style="display:flex;align-items:flex-start;gap:16px">
        <div style="min-width:40px;height:40px;background:var(--navy-mid);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0">${s.icon}</div>
        <div style="flex:1">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
            <span style="background:var(--navy-mid);color:${s.color};font-family:var(--font-mono);font-size:10px;font-weight:700;padding:2px 8px;border-radius:99px">STEP ${s.num}</span>
            <span style="font-family:var(--font-head);font-size:14px;font-weight:600;color:var(--white)">${s.label}</span>
          </div>
          <p style="font-size:12.5px;color:var(--muted);line-height:1.6;margin-bottom:10px">${s.desc}</p>
          <div style="display:flex;flex-wrap:wrap;gap:6px">
            ${s.items.map(i => `<span style="background:var(--navy-mid);border:1px solid var(--border);color:var(--muted);font-size:11px;font-family:var(--font-mono);padding:3px 10px;border-radius:var(--r)">${i}</span>`).join('')}
          </div>
        </div>
      </div>
    </div>`).join('')}
    <div class="flag-box green" style="margin-top:4px">
      <div class="flag-title">\u2713 Key Differentiator: The Pain Point FinPal Solves</div>
      <div class="flag-body">The real pain point is <strong>loan application processing inefficiency</strong>: paper documents, email back-and-forth, missing documents, slow verification, and manual data extraction. FinPal eliminates this bottleneck with IDP + automated validation, reducing application processing time from days to minutes while maintaining full regulatory compliance.</div>
    </div>`;
}

// ── Architecture & Security ──────────────────────────────────
function renderArchitecture() {
  return `
    <div class="section-header"><div class="section-title">Architecture &amp; Data Security</div>
      <span class="tag tag-complete">Tenant-Isolated SaaS</span></div>
    <div class="flag-box blue" style="margin-top:0;margin-bottom:16px">
      <div class="flag-title">\u{1F512} How FinPal Addresses the SaaS Data Governance Challenge</div>
      <div class="flag-body">Investor concern: if FinPal is SaaS, how can lenders guarantee data control? Answer: <strong>tenant-isolated architecture</strong>. Each lender gets a completely separate infrastructure stack. FinPal's vendor team cannot access any lender's data. AI models run in isolated compute environments. No customer data is used to train shared models.</div>
    </div>
    <div class="section-header"><div class="section-title">Tenant Isolation Model</div></div>
    <div class="grid-3" style="margin-bottom:16px">
      <div class="card">
        <div class="card-title">Separate Database</div>
        <div style="font-size:22px;margin-bottom:8px">\u{1F5C4}</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.5">Each lender has a dedicated database instance. Lender A cannot access Lender B data. FinPal admin accounts have no read access to lender data stores.</div>
      </div>
      <div class="card">
        <div class="card-title">Separate AI Model Instance</div>
        <div style="font-size:22px;margin-bottom:8px">\u{1F916}</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.5">Credit models are instantiated per tenant. No shared model state. Lender data is never used to train or fine-tune models for another lender or for FinPal's shared infrastructure.</div>
      </div>
      <div class="card">
        <div class="card-title">Separate Infrastructure</div>
        <div style="font-size:22px;margin-bottom:8px">\u2601</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.5">Dedicated compute, networking, and storage per lender on Azure West EU. Logical and physical isolation prevents cross-tenant data leakage.</div>
      </div>
    </div>
    <div class="section-header"><div class="section-title">Private AI &amp; Data Sovereignty</div></div>
    <div class="card" style="margin-bottom:16px">
      ${[
        ['\u{1F512} No External AI Providers','Lender data is NEVER sent to OpenAI, AWS Bedrock, or any public AI API. All AI inference runs within the lender\'s isolated tenant environment.','green'],
        ['\u{1F512} No Training on Lender Data','Models are trained on anonymised, aggregated datasets only. No individual lender\'s application data is used for shared model training.','green'],
        ['\u{1F512} Data Anonymisation Pipeline','PII is stripped and anonymised before any model processing. The PII Vault stores raw data separately with strict access controls.','green'],
        ['\u2601 Private Cloud Option','Dedicated cloud instance per lender. All processing within lender\'s geographic boundary (Azure West EU for Irish/EU lenders).','teal'],
        ['\u{1F3E0} On-Premise Deployment Option','For lenders requiring maximum control, FinPal can be deployed inside the lender\'s own infrastructure. AI runs entirely within lender\'s network perimeter.','teal'],
        ['\u{1F50D} Vendor Cannot Access Data','FinPal vendor accounts have no access to lender application data, customer PII, or credit decisions. Access requires formal lender authorisation and is fully logged.','green'],
      ].map(([l,v,c])=>`<div class="metric-row"><span class="metric-label" style="font-size:12px;color:var(--white)">${l}</span><span style="font-size:11px;color:var(--${c});max-width:55%;text-align:right">${v}</span></div>`).join('')}
    </div>
    <div class="section-header"><div class="section-title">Security Controls</div></div>
    <div class="grid-2" style="margin-bottom:16px">
      <div class="card">
        <div class="card-title">Data Protection</div>
        ${[
          ['Encryption at rest','AES-256 &middot; per-tenant keys'],
          ['Encryption in transit','TLS 1.3 &middot; mutual auth'],
          ['PII Vault','Separate encrypted store'],
          ['Key Management','Azure Key Vault &middot; tenant-scoped'],
          ['Data Residency','Azure West EU &middot; GDPR compliant'],
        ].map(([l,v])=>`<div class="metric-row"><span class="metric-label">${l}</span><span class="metric-value" style="font-size:12px">${v}</span></div>`).join('')}
      </div>
      <div class="card">
        <div class="card-title">Access &amp; Monitoring</div>
        ${[
          ['Access Controls','RBAC &middot; least-privilege'],
          ['Audit Logging','All data access logged &middot; immutable'],
          ['Intrusion Detection','Real-time threat monitoring'],
          ['Vulnerability Mgmt','Continuous scanning &middot; patching SLA'],
          ['Incident Response','Documented IR plan &middot; 72h GDPR notify'],
        ].map(([l,v])=>`<div class="metric-row"><span class="metric-label">${l}</span><span class="metric-value" style="font-size:12px">${v}</span></div>`).join('')}
      </div>
    </div>
    <div class="section-header"><div class="section-title">EU AI Act &amp; CBI Compliance</div></div>
    <div class="card">
      ${[
        ['High-Risk AI Classification','Credit scoring is high-risk under EU AI Act 2024/1689 &middot; Central Bank of Ireland notified','green'],
        ['Risk Management (Art.9)','Documented risk management system &middot; risk-specific controls per use case','green'],
        ['Data Governance (Art.10)','Feature store with lineage &middot; PII anonymisation &middot; data quality controls','green'],
        ['Human Oversight (Art.14)','Mandatory underwriter decision gate &middot; no fully automated credit decisions','green'],
        ['Transparency (Art.13)','SHAP explanations per decision &middot; borrower right to explanation','green'],
        ['Record-Keeping (Art.12)','Cryptographically immutable audit trail &middot; CBI inspection-ready','green'],
      ].map(([l,v,c])=>`<div class="metric-row"><span class="metric-label">${l}</span><span class="metric-value" style="color:var(--${c});font-size:11px;max-width:55%;text-align:right">${v}</span></div>`).join('')}
    </div>
    <div class="flag-box" style="margin-top:16px">
      <div class="flag-title">\u26A0 Security Reality: No System is Completely Secure</div>
      <div class="flag-body">Even dedicated cloud infrastructure is subject to attack. AWS servers have been attacked within minutes of exposure. FinPal's approach is not to claim invulnerability but to implement defence-in-depth: tenant isolation, encryption, access controls, continuous monitoring, and a tested incident response plan \u2014 all aligned to DORA (Digital Operational Resilience Act) requirements.</div>
    </div>`;
}

// ── Model Governance (MRM) ──────────────────────────────────
function renderModelGovernance() {
  return `
    <div class="section-header"><div class="section-title">Model Registry &amp; Governance</div>
      <span class="tag tag-complete">SR 11-7 Aligned</span></div>
    <div class="flag-box blue" style="margin-bottom:16px;margin-top:0">
      <div class="flag-title">Model Risk Management Framework &mdash; Tenant-Isolated Private AI</div>
      <div class="flag-body">All models are governed under a documented MRM framework covering model inventory, conceptual soundness, validation, monitoring, and change control &mdash; aligned to SR 11-7 (Federal Reserve) and EU AI Act Article 9 requirements. <strong>Each lender runs a dedicated model instance</strong> in an isolated environment. Models are never shared across tenants. No lender data is sent to external AI providers (OpenAI, AWS, etc.) for inference or training. On-premise deployment is available for lenders requiring full infrastructure control.</div>
    </div>
    <div class="grid-2" style="margin-bottom:16px">
      ${[
        {name:'PD Model (Application)',ver:'v3.2',status:'Active',validated:'15 Jan 2025',auc:'0.84',challenger:'v3.3-beta'},
        {name:'PD Model (Behavioral)',ver:'v2.8',status:'Active',validated:'20 Dec 2024',auc:'0.81',challenger:'v2.9-beta'},
        {name:'LGD Model',ver:'v2.1',status:'Active',validated:'10 Jan 2025',auc:'0.76',challenger:'v2.2-dev'},
        {name:'EAD Model',ver:'v1.8',status:'Active',validated:'05 Jan 2025',auc:'N/A',challenger:'v1.9-beta'},
        {name:'Affordability Model',ver:'v2.0',status:'Active',validated:'12 Jan 2025',auc:'0.88',challenger:'v2.1-dev'},
        {name:'Risk-Based Pricing',ver:'v1.5',status:'Active',validated:'18 Jan 2025',auc:'N/A',challenger:'None'},
      ].map(m => `
        <div class="card">
          <div class="card-title">${m.name} <span class="tag tag-complete">${m.status}</span></div>
          <div style="font-size:15px;font-weight:600;margin-bottom:8px">${m.ver}</div>
          ${[
            ['Last Validated', m.validated],
            ['AUC/Gini', m.auc],
            ['Challenger', m.challenger],
          ].map(([l,v]) => `<div class="metric-row"><span class="metric-label">${l}</span><span class="metric-value">${v}</span></div>`).join('')}
        </div>`).join('')}
    </div>
    <div class="section-header"><div class="section-title">Model Monitoring &mdash; Drift Indicators</div></div>
    <div class="grid-3">
      <div class="card"><div class="card-title">PSI (PD Model)</div><div class="card-value teal">0.08</div><div class="card-sub">Threshold: &lt;0.25 &#x2713;</div></div>
      <div class="card"><div class="card-title">CSI (Features)</div><div class="card-value teal">0.12</div><div class="card-sub">Threshold: &lt;0.25 &#x2713;</div></div>
      <div class="card"><div class="card-title">Calibration</div><div class="card-value teal">1.03</div><div class="card-sub">Predicted/Actual ratio</div></div>
    </div>`;
}

// ── Portfolio Risk ──────────────────────────────────────────
function renderPortfolioRisk() {
  return `
    <div class="section-header"><div class="section-title">Portfolio Risk Dashboard</div></div>
    <div class="grid-4" style="margin-bottom:16px">
      <div class="card"><div class="card-title">Total Exposure</div><div class="card-value teal">\u20AC1.005M</div><div class="card-sub">4 active applications</div></div>
      <div class="card"><div class="card-title">Wtd Avg PD</div><div class="card-value">4.2%</div><div class="card-sub">Portfolio weighted</div></div>
      <div class="card"><div class="card-title">PAR30 / NPL</div><div class="card-value green">0.0%</div><div class="card-sub">No delinquencies</div></div>
      <div class="card"><div class="card-title">ECL Coverage</div><div class="card-value">\u20AC28.2K</div><div class="card-sub">Total provisions</div></div>
    </div>
    <div class="section-header"><div class="section-title">IFRS 9 Staging Distribution</div></div>
    <div class="grid-3" style="margin-bottom:16px">
      <div class="card"><div class="card-title">Stage 1</div><div class="card-value green">75%</div><div class="card-sub">3 exposures &middot; Performing</div></div>
      <div class="card"><div class="card-title">Stage 2</div><div class="card-value gold">25%</div><div class="card-sub">1 exposure &middot; SICR</div></div>
      <div class="card"><div class="card-title">Stage 3</div><div class="card-value teal">0%</div><div class="card-sub">No defaults</div></div>
    </div>
    <div class="section-header"><div class="section-title">Concentration Risk</div></div>
    <div class="card">
      ${[
        ['Construction','42% (\u20AC420K)','Standard weight'],
        ['Transport & Logistics','18% (\u20AC185K)','Standard weight'],
        ['Hospitality','31% (\u20AC310K)','Elevated \u2014 monitor'],
        ['Technology','9% (\u20AC90K)','Low weight'],
      ].map(([s,e,n])=>`<div class="metric-row"><span class="metric-label">${s}</span><span class="metric-value">${e} <span style="font-size:10px;color:var(--muted)">${n}</span></span></div>`).join('')}
    </div>`;
}

// ── Compliance Dashboard ────────────────────────────────────
function renderComplianceDashboard() {
  return `
    <div class="section-header"><div class="section-title">Regulatory Compliance Dashboard</div>
      <span class="tag tag-complete">All Systems Compliant</span></div>
    <div class="card" style="margin-bottom:16px;border-left:3px solid var(--teal)">
      <div class="card-title">Data Sovereignty &amp; Tenant Isolation <span class="tag tag-complete">SaaS Architecture</span></div>
      ${[
        ['Tenant Database Isolation','\u2713 Separate DB per lender &middot; no cross-tenant access','green'],
        ['AI Model Isolation','\u2713 Dedicated model instance per lender &middot; no shared state','green'],
        ['Infrastructure Isolation','\u2713 Separate compute &amp; networking per tenant &middot; Azure West EU','green'],
        ['Vendor Data Access','\u2713 FinPal vendor has zero access to lender application data','green'],
        ['No External AI Training','\u2713 Lender data never used to train shared or external models','green'],
        ['PII Anonymisation','\u2713 PII stripped before model processing &middot; PII Vault isolated','green'],
        ['CBI Regulatory Position','\u2713 Tenant isolation reduces high-risk AI classification burden','teal'],
      ].map(([l,v,c])=>`<div class="metric-row"><span class="metric-label">${l}</span><span class="metric-value" style="color:var(--${c})">${v}</span></div>`).join('')}
    </div>
    <div class="grid-2" style="margin-bottom:16px">
      <div class="card">
        <div class="card-title">EU AI Act (High-Risk) <span class="tag tag-danger">HIGH-RISK</span></div>
        ${[
          ['Art.9 Risk Management','&#x2713; Active','green'],
          ['Art.10 Data Governance','&#x2713; Feature store w/ lineage','green'],
          ['Art.11 Technical Docs','&#x2713; Complete','green'],
          ['Art.12 Record-Keeping','&#x2713; Immutable audit logs','green'],
          ['Art.13 Transparency','&#x2713; SHAP explanations','green'],
          ['Art.14 Human Oversight','&#x2713; HITL queues active','green'],
          ['Art.15 Accuracy/Robustness','&#x2713; Model validation current','green'],
        ].map(([l,v,c])=>`<div class="metric-row"><span class="metric-label">${l}</span><span class="metric-value" style="color:var(--${c})">${v}</span></div>`).join('')}
      </div>
      <div class="card">
        <div class="card-title">GDPR &amp; Data Protection</div>
        ${[
          ['Art.6 Lawful Basis','&#x2713; Consent + Legitimate Interest','green'],
          ['Art.13/14 Transparency','&#x2713; Notices at consent point','green'],
          ['Art.22 Automated Decisions','&#x2713; HITL + explanation + appeal','green'],
          ['Art.25 Privacy by Design','&#x2713; PII Vault + minimization','green'],
          ['Art.35 DPIA','&#x2713; Completed','green'],
          ['Data Subject Rights','&#x2713; Portal active','green'],
          ['SCHUFA Ruling Compliance','&#x2713; Meaningful human oversight','green'],
        ].map(([l,v,c])=>`<div class="metric-row"><span class="metric-label">${l}</span><span class="metric-value" style="color:var(--${c})">${v}</span></div>`).join('')}
      </div>
    </div>
    <div class="grid-2">
      <div class="card">
        <div class="card-title">EBA LOM (EBA/GL/2020/06)</div>
        ${[
          ['Credit Risk Policy','&#x2713; Documented','green'],
          ['Pricing Framework','&#x2713; Risk-based APR active','green'],
          ['Collateral Valuation','&#x2713; Independent valuation','green'],
          ['Monitoring/EWI','&#x2713; Behavioral triggers active','green'],
          ['Data Infrastructure','&#x2713; Quality controls active','green'],
        ].map(([l,v,c])=>`<div class="metric-row"><span class="metric-label">${l}</span><span class="metric-value" style="color:var(--${c})">${v}</span></div>`).join('')}
      </div>
      <div class="card">
        <div class="card-title">Additional Frameworks</div>
        ${[
          ['DORA (Operational Resilience)','&#x2713; Aligned','green'],
          ['MRM / SR 11-7','&#x2713; Framework active','green'],
          ['IFRS 9 Provisioning','&#x2713; ECL engine live','green'],
          ['Basel Credit Risk Principles','&#x2713; Policy/limits/controls','green'],
          ['CBI IAF (Ireland)','&#x2713; Audit trails active','green'],
        ].map(([l,v,c])=>`<div class="metric-row"><span class="metric-label">${l}</span><span class="metric-value" style="color:var(--${c})">${v}</span></div>`).join('')}
      </div>
    </div>`;
}

// ── Collections ─────────────────────────────────────────────
function renderCollections() {
  return `
    <div class="section-header"><div class="section-title">Collections &amp; Borrower Protection</div></div>
    <div class="flag-box blue" style="margin-top:0;margin-bottom:16px">
      <div class="flag-title">Responsible Digital Credit Framework</div>
      <div class="flag-body">Collections practices follow CGAP responsible digital credit guidelines. Borrower protection guardrails are active to prevent over-indebtedness, abusive practices, and data misuse. All treatment codes, hardship flags, and actions are logged to immutable audit trails.</div>
    </div>
    <div class="grid-3" style="margin-bottom:16px">
      <div class="card"><div class="card-title">Active Collections</div><div class="card-value teal">0</div><div class="card-sub">No delinquent accounts</div></div>
      <div class="card"><div class="card-title">Hardship Cases</div><div class="card-value">0</div><div class="card-sub">No active hardship</div></div>
      <div class="card"><div class="card-title">Over-Indebtedness Alerts</div><div class="card-value gold">1</div><div class="card-sub">Ferris Hospitality flagged</div></div>
    </div>
    <div class="section-header"><div class="section-title">Borrower Protection Controls</div></div>
    <div class="card">
      ${[
        ['Over-indebtedness screening','Active \u2014 DTI ratio checked at origination','green'],
        ['Hardship/rescheduling pathway','Available \u2014 champion/challenger strategy','green'],
        ['Contact channel optimization','Empathetic comms templates active','green'],
        ['Behavioral nudges','Enabled with guardrails','green'],
        ['Consumer protection checks','CGAP-aligned safeguards active','green'],
        ['Data misuse prevention','PII access controls + audit logging','green'],
      ].map(([l,v,c])=>`<div class="metric-row"><span class="metric-label">${l}</span><span class="metric-value" style="color:var(--${c})">${v}</span></div>`).join('')}
    </div>`;
}

// ── Bureau Reporting ────────────────────────────────────────
function renderBureauReporting() {
  return `
    <div class="section-header"><div class="section-title">Credit Bureau Reporting</div></div>
    <div class="flag-box blue" style="margin-top:0;margin-bottom:16px">
      <div class="flag-title">Jurisdictional Reporting Packs</div>
      <div class="flag-body">Bureau furnishing is configured per jurisdiction. Each market uses the appropriate schema (Metro 2&#x00AE;/CRRG&#x00AE; for U.S.; local schemas for EU/ROW). Automated cycles, dispute/intake workflows, reinvestigations, and correction &amp; re-reporting SLAs are enforced.</div>
    </div>
    <div class="grid-3" style="margin-bottom:16px">
      <div class="card"><div class="card-title">Furnishing Status</div><div class="card-value green">Current</div><div class="card-sub">Last cycle: 01 Mar 2025</div></div>
      <div class="card"><div class="card-title">Open Disputes</div><div class="card-value teal">0</div><div class="card-sub">All resolved</div></div>
      <div class="card"><div class="card-title">Error Rate</div><div class="card-value green">0.2%</div><div class="card-sub">Below 1% SLA &#x2713;</div></div>
    </div>
    <div class="section-header"><div class="section-title">Jurisdiction Configuration</div></div>
    <div class="card">
      ${[
        ['Ireland / EU','ICB (Irish Credit Bureau) \u2014 Local schema','Active'],
        ['United Kingdom','Experian/Equifax/TransUnion \u2014 CAIS format','Configured'],
        ['United States','Metro 2\u00AE / CRRG\u00AE schema','Configured'],
        ['Pan-African','Market-specific packs available','On demand'],
      ].map(([j,s,st])=>`<div class="metric-row"><span class="metric-label"><strong>${j}</strong><br><span style="font-size:11px">${s}</span></span><span class="metric-value"><span class="tag tag-complete">${st}</span></span></div>`).join('')}
    </div>
    <div class="section-header"><div class="section-title">Internal Rating System</div></div>
    <div class="card">
      ${[
        ['Borrower/Obligor Ratings','A1-D2 scale \u2014 Active'],
        ['Facility Grades','Mapped to external scales'],
        ['Migration Tracking','Quarterly transition matrices'],
        ['Override Governance','All overrides logged with reason'],
        ['Regulatory Reporting','AI Act/HRA docs + ECL disclosures (IFRS 7/9)'],
      ].map(([l,v])=>`<div class="metric-row"><span class="metric-label">${l}</span><span class="metric-value">${v}</span></div>`).join('')}
    </div>`;
}

// ── Global Audit ────────────────────────────────────────────
function renderGlobalAudit() {
  return `
    <div class="section-header"><div class="section-title">Global Audit Trail</div>
      <span class="tag tag-complete">CBI-Inspection Ready</span></div>
    <div class="flag-box green" style="margin-top:0;margin-bottom:16px">
      <div class="flag-title">&#x2713; EU AI Act Art.12 &amp; IAF Compliance</div>
      <div class="flag-body">This audit trail is cryptographically immutable and cannot be modified or deleted. Every entry is timestamped and attributed. Compliant with EU AI Act Article 12 (record-keeping), GDPR Article 30 (records of processing), and Ireland's Individual Accountability Framework.</div>
    </div>
    <div class="card" style="padding:4px 16px">
      ${APPS.filter(a=>a.status!=='processing').map(a => `
        <div class="audit-item">
          <div class="audit-time">${a.requested}</div>
          <div class="audit-dot ${a.status==='flagged'?'gold':a.status==='decided'?(a.decision==='approved'?'green':'red'):''}"></div>
          <div>
            <div class="audit-event">${a.company} \u2014 ${a.status==='decided'?(a.decision==='approved'?'Approved':'Declined'):(a.status==='flagged'?'Flagged':'Assessment Complete')}</div>
            <div class="audit-detail">${a.id} \u00B7 ${a.loanType} \u00B7 ${a.amount}</div>
          </div>
        </div>`).join('')}
    </div>`;
}
"""

with open(__file__.replace("_js2.py", "_js2.txt"), "w", encoding="utf-8") as f:
    f.write(JS_FUNCS)
print("Part 4 (JS views) ready")
