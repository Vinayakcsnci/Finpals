"""Part 2: HTML body"""

BODY = r"""
<div id="app">
  <nav id="sidebar">
    <div class="logo">
      <div class="logo-mark">F</div>
      <div>
        <div class="logo-text">FinPal</div>
        <div class="logo-tag">LOAN INTAKE &amp; ASSESSMENT</div>
      </div>
    </div>
    <div class="nav-section">
      <div class="nav-label">Platform</div>
      <div class="nav-item" data-view="intake" onclick="switchView('intake')">
        <span class="icon">&#x2B06;</span> Intake Pipeline
      </div>
      <div class="nav-item active" data-view="apps" onclick="switchView('apps')">
        <span class="icon">&#x2B1B;</span> Applications <span class="nav-badge">4</span>
      </div>
      <div class="nav-item" data-view="audit" onclick="switchView('audit')">
        <span class="icon">&#x25E7;</span> Audit Trail
      </div>
    </div>
    <div class="nav-section">
      <div class="nav-label">Risk &amp; Compliance</div>
      <div class="nav-item" data-view="models" onclick="switchView('models')">
        <span class="icon">&#x2699;</span> Model Governance
      </div>
      <div class="nav-item" data-view="portfolio" onclick="switchView('portfolio')">
        <span class="icon">&#x25A6;</span> Portfolio Risk
      </div>
      <div class="nav-item" data-view="compliance" onclick="switchView('compliance')">
        <span class="icon">&#x2696;</span> Compliance Dashboard
      </div>
    </div>
    <div class="nav-section">
      <div class="nav-label">Operations</div>
      <div class="nav-item" data-view="collections" onclick="switchView('collections')">
        <span class="icon">&#x21BA;</span> Collections
      </div>
      <div class="nav-item" data-view="bureau" onclick="switchView('bureau')">
        <span class="icon">&#x2709;</span> Bureau Reporting
      </div>
      <div class="nav-item" data-view="architecture" onclick="switchView('architecture')">
        <span class="icon">&#x1F512;</span> Architecture &amp; Security
      </div>
    </div>
    <div class="nav-section" style="flex:1;overflow:hidden;display:flex;flex-direction:column;">
      <div class="nav-label">Queue</div>
      <div class="app-list" id="app-list"></div>
    </div>
    <div style="padding:12px;border-top:1px solid var(--border)">
      <div style="font-size:11px;color:var(--muted);font-family:var(--font-mono)">
        <div style="display:flex;justify-content:space-between;margin-bottom:4px">
          <span>Jurisdiction</span><span style="color:var(--teal)" id="jurisdiction-label">EU / Ireland</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:4px">
          <span>Regulation</span><span style="color:var(--gold)">EU AI Act &middot; EBA LOM</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:4px">
          <span>Data residency</span><span style="color:var(--green)">&#x2713; Azure West EU</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:4px">
          <span>GDPR</span><span style="color:var(--green)">&#x2713; Art.22 Compliant</span>
        </div>
        <div style="display:flex;justify-content:space-between">
          <span>Tenant Isolation</span><span style="color:var(--teal)">&#x2713; Dedicated</span>
        </div>
      </div>
    </div>
  </nav>

  <div id="main">
    <div id="topbar">
      <div>
        <div class="topbar-title" id="topbar-title">Applications</div>
        <div class="topbar-subtitle" id="topbar-sub">FinPal AI-Powered Loan Intake &amp; Document Processing &middot; EU AI Act High-Risk Compliant &middot; Tenant-Isolated SaaS</div>
      </div>
      <div class="topbar-actions" id="topbar-actions">
        <button class="btn btn-outline" onclick="showNewAppModal()">&#xFF0B; New Application</button>
      </div>
    </div>
    <div id="content">
      <div id="view-apps" class="panel active">
        <div class="empty-state">
          <div class="empty-icon">&#x1F4C2;</div>
          <div class="empty-text">Select an application from the queue to begin</div>
        </div>
      </div>
      <!-- Side panel views -->
      <div id="view-intake" class="side-panel"></div>
      <div id="view-models" class="side-panel"></div>
      <div id="view-portfolio" class="side-panel"></div>
      <div id="view-compliance" class="side-panel"></div>
      <div id="view-collections" class="side-panel"></div>
      <div id="view-bureau" class="side-panel"></div>
      <div id="view-audit" class="side-panel"></div>
      <div id="view-architecture" class="side-panel"></div>
    </div>
  </div>
</div>

<!-- Decision modal -->
<div class="modal-overlay" id="decision-modal">
  <div class="modal">
    <div class="modal-title" id="dm-title">Submit Credit Decision</div>
    <div class="modal-body" id="dm-body">
      You are about to submit a formal credit decision. Under Ireland's Individual Accountability Framework and EU AI Act Article 14 (human oversight), this decision and your documented rationale will be permanently logged to the immutable audit trail.
    </div>
    <textarea class="decision-textarea" id="dm-rationale" placeholder="Enter your decision rationale (mandatory under IAF &amp; GDPR Art.22)..."></textarea>
    <div style="font-size:11px;color:var(--muted);font-family:var(--font-mono);margin-top:6px">
      &#x26A0; This action is irreversible. Your name and timestamp will be recorded per EU AI Act Art.12.
    </div>
    <div class="modal-actions" style="margin-top:14px">
      <button class="btn btn-outline" onclick="closeDecisionModal()">Cancel</button>
      <button class="btn btn-danger" id="dm-decline-btn" onclick="submitDecision('decline')">Decline</button>
      <button class="btn btn-primary" id="dm-approve-btn" onclick="submitDecision('approve')">Approve</button>
    </div>
  </div>
</div>

<!-- New App modal -->
<div class="modal-overlay" id="new-app-modal">
  <div class="modal" style="max-width:540px">
    <div class="modal-title">&#x2B06; Borrower Intake Portal</div>
    <div class="modal-body" style="margin-bottom:14px">
      <strong>Step 1 of 5 &mdash; Application Submission.</strong> The borrower submits basic details here. Documents will be uploaded next. GDPR Article 13/14 notice and consent for automated processing (Art.22) are captured automatically before assessment begins.
    </div>
    <div style="font-size:10px;color:var(--teal);font-family:var(--font-mono);letter-spacing:.5px;margin-bottom:10px;text-transform:uppercase">Borrower Details</div>
    <div style="display:flex;flex-direction:column;gap:10px">
      <input type="text" id="new-company" placeholder="Company / business name" style="background:var(--panel);border:1px solid var(--border);border-radius:var(--r);color:var(--white);font-family:var(--font-body);font-size:13px;padding:9px 12px;width:100%">
      <input type="text" id="new-amount" placeholder="Loan amount requested (EUR)" style="background:var(--panel);border:1px solid var(--border);border-radius:var(--r);color:var(--white);font-family:var(--font-body);font-size:13px;padding:9px 12px;width:100%">
      <select id="new-type" style="background:var(--panel);border:1px solid var(--border);border-radius:var(--r);color:var(--white);font-family:var(--font-body);font-size:13px;padding:9px 12px;width:100%">
        <option value="">Loan type...</option>
        <option>Working Capital</option>
        <option>Asset Finance</option>
        <option>Commercial Mortgage</option>
        <option>Invoice Finance</option>
      </select>
    </div>
    <div style="font-size:10px;color:var(--teal);font-family:var(--font-mono);letter-spacing:.5px;margin-top:14px;margin-bottom:10px;text-transform:uppercase">Document Upload (IDP)</div>
    <div style="display:flex;flex-direction:column;gap:8px">
      <div style="background:var(--panel);border:1px dashed var(--border);border-radius:var(--r);padding:10px 14px;font-size:12px;color:var(--muted)">
        <span style="color:var(--teal)">&#x1F4CB;</span> Passport / Director ID &mdash; <span style="font-family:var(--font-mono);font-size:11px">JPEG / PDF</span>
      </div>
      <div style="background:var(--panel);border:1px dashed var(--border);border-radius:var(--r);padding:10px 14px;font-size:12px;color:var(--muted)">
        <span style="color:var(--teal)">&#x1F4CB;</span> Financial Statements / Management Accounts &mdash; <span style="font-family:var(--font-mono);font-size:11px">PDF</span>
      </div>
      <div style="background:var(--panel);border:1px dashed var(--border);border-radius:var(--r);padding:10px 14px;font-size:12px;color:var(--muted)">
        <span style="color:var(--teal)">&#x1F4CB;</span> Company Registration / CRO Documents &mdash; <span style="font-family:var(--font-mono);font-size:11px">PDF</span>
      </div>
    </div>
    <div style="margin-top:12px;font-size:11px;color:var(--muted);font-family:var(--font-mono)">
      &#x1F512; All data remains within your dedicated tenant environment. IDP processing is performed in an isolated model instance. No data is shared with external AI providers.
    </div>
    <div class="modal-actions" style="margin-top:18px">
      <button class="btn btn-outline" onclick="document.getElementById('new-app-modal').classList.remove('open')">Cancel</button>
      <button class="btn btn-primary" onclick="submitNewApp()">&#x25B6; Begin IDP Assessment</button>
    </div>
  </div>
</div>
"""

with open(__file__.replace("_html.py", "_html.txt"), "w", encoding="utf-8") as f:
    f.write(BODY)
print("Part 2 (HTML body) ready")
