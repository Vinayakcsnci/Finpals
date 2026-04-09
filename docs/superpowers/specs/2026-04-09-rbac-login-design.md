# FinPal v5.0 — RBAC Login System Design

**Date:** 2026-04-09
**Author:** Claude (based on PRD v1.1, BRD v1.1, User Stories)
**Status:** Approved

---

## 1. Overview

Add a full-screen login page and role-based access control (RBAC) to `index.html`. Each of the 8 platform personas defined in the PRD/BRD gets dedicated credentials. After login, the sidebar navigation renders only the views permitted for that role. All 17 user story feature files are mapped to the roles and views they exercise.

The implementation stays within the single `index.html` file — no new files, no server required — so the app continues to work on GitHub Pages and via local file-open.

---

## 2. Architecture

### 2.1 Login Screen

- Full-screen overlay rendered **before** `#app` (which starts hidden)
- Contains: FinPal logo, username + password fields, "Sign In" button, inline error message div
- On submit: look up credentials in a hardcoded `USERS` map; on match set `currentUser` and transition to app; on mismatch show "Invalid credentials" error
- No cookies or localStorage — credentials live in-memory for the session only (appropriate for a prototype demo)

### 2.2 RBAC Data Structure

```js
const USERS = {
  'credit.officer':      { password: 'FinPal@CO1',  role: 'Credit Officer',      ... },
  'risk.manager':        { password: 'FinPal@RM2',  role: 'Risk Manager',         ... },
  'compliance.officer':  { password: 'FinPal@CMP3', role: 'Compliance Officer',   ... },
  'ops.manager':         { password: 'FinPal@OPS4', role: 'Operations Manager',   ... },
  'it.admin':            { password: 'FinPal@ITA5', role: 'IT Administrator',      ... },
  'mrm.analyst':         { password: 'FinPal@MRM6', role: 'MRM Analyst',           ... },
  'collections.officer': { password: 'FinPal@COL7', role: 'Collections Officer',  ... },
  'borrower.sme':        { password: 'FinPal@SME8', role: 'Borrower (SME)',        ... },
}
```

Each user entry also contains:
- `allowedViews: string[]` — list of view IDs the role may access
- `defaultView: string` — first view shown after login
- `displayName: string` — shown in topbar user-chip
- `avatarInitials: string` — two-letter avatar

### 2.3 Post-Login Rendering

1. `#login-screen` gets `display:none`; `#app` gets `display:flex`
2. Sidebar nav items are iterated; any item whose `data-view` is **not** in `allowedViews` is hidden (`display:none`)
3. Topbar user-chip `name` and `role` text nodes are updated
4. `switchView(currentUser.defaultView)` is called to activate the correct panel
5. A "Log Out" button is added to the topbar; clicking it reloads the page

---

## 3. Role → Views → User Stories

### Credit Officer
**Credentials:** `credit.officer` / `FinPal@CO1`
**Allowed views:** `apps`, `intake`, `audit`
**Default view:** `apps`

| User Story | Feature File | Key Scenarios |
|---|---|---|
| US 6.1 — Loan Assessment | `2_sme_underwriting_decisioning` | HITL queue, SHAP explanations, approve/decline/override with audit trail |
| US 6.2 — CCR Check | `2_sme_underwriting_decisioning` | Real-time CCR enquiry in underwriting workflow |
| Collateral Valuation | `6_collateral_valuation_ltv` | AVM/desktop/independent valuation selection, LTV haircut recording |

---

### Risk Manager
**Credentials:** `risk.manager` / `FinPal@RM2`
**Allowed views:** `models`, `portfolio`, `audit`
**Default view:** `models`

| User Story | Feature File | Key Scenarios |
|---|---|---|
| US 6.6 — Model Drift Alert | `12_model_lifecycle_drift` | PSI ≥ 0.10 or Gini breach triggers drift alert + remediation case |
| EBA Origination & Monitoring | `5_eba_loan_origination_monitoring` | Creditworthiness assessment, pricing auditability, EWI escalation |
| Stress Testing | `13_stress_testing` | Quarterly EBA/ECB scenario runs, ICAAP-format portfolio output |

---

### Compliance Officer
**Credentials:** `compliance.officer` / `FinPal@CMP3`
**Allowed views:** `compliance`, `audit`, `bureau`, `trustworthy`
**Default view:** `compliance`

| User Story | Feature File | Key Scenarios |
|---|---|---|
| US 6.3 — Audit Evidence | `14_audit_evidence_catalogue` | Immutable evidence retrieval: inputs, reason codes, model version, approver |
| EU AI Act Compliance | `4_eu_ai_act_compliance` | Conformity & registration readiness, accuracy/robustness/cybersecurity testing |
| CCR / AnaCredit Reporting | `11_ccr_anacredit_reporting` | Schema validation, <1% error rate, ECB 2016/867 compliance |

---

### Operations Manager
**Credentials:** `ops.manager` / `FinPal@OPS4`
**Allowed views:** `intake`, `apps`, `collections`, `bureau`, `compliance`, `audit`, `architecture`
**Default view:** `intake`

| User Story | Feature File | Key Scenarios |
|---|---|---|
| US 6.4 — Fund Disbursement | `9_psd2_open_banking` | PIS disbursement with SCA consent/audit trail |
| SEPA Instant Payouts | `10_sepa_payments` | SCT Inst ≤ 10s, 24/7/365 availability; SDD mandate lifecycle |
| Observability / SLAs / KPIs | `16_observability_slas_kpis` | Uptime ≥ 99.9%, SCT Inst ≥ 99.5%, SDD R-tx < 5%, NPS ≥ 45 |

---

### IT Administrator
**Credentials:** `it.admin` / `FinPal@ITA5`
**Allowed views:** `architecture`, `audit`, `models`
**Default view:** `architecture`

| User Story | Feature File | Key Scenarios |
|---|---|---|
| Identity & Access / SSO | `1_identity_access_sso` | JIT provisioning via SAML/OIDC, RBAC roles, access revocation + audit log |
| DORA Operational Resilience | `8_dora_operational_resilience`, `dora_resilience` | Major incident reporting, DR invocation (RTO ≤ 4h, RPO ≤ 1h) |
| Security / Residency | `17_security_residency_immutability` | AES-256 at rest, TLS 1.3 in transit, immutable reason codes |
| API-first Platform | `15_data_model_apis` | OAuth 2.0 token, OpenAPI 3.1 compliance, correlation IDs |

---

### MRM Analyst
**Credentials:** `mrm.analyst` / `FinPal@MRM6`
**Allowed views:** `models`, `portfolio`
**Default view:** `models`

| User Story | Feature File | Key Scenarios |
|---|---|---|
| Model Lifecycle & Drift | `12_model_lifecycle_drift` | Release gating, validation sign-off, champion-challenger runs |
| IFRS 9 / ECL Staging | `7_ifrs9_ecl_staging` | Automated Stage 1/2/3 classification, scenario-weighted ECL |

---

### Collections Officer
**Credentials:** `collections.officer` / `FinPal@COL7`
**Allowed views:** `collections`, `bureau`
**Default view:** `collections`

| User Story | Feature File | Key Scenarios |
|---|---|---|
| US 6.7 — SDD Mandate | `10_sepa_payments` | Digital SDD mandate lifecycle, R-transaction handling (R01–R35), retry per SEPA policy |

---

### Borrower (SME)
**Credentials:** `borrower.sme` / `FinPal@SME8`
**Allowed views:** `intake`
**Default view:** `intake`

| User Story | Feature File | Key Scenarios |
|---|---|---|
| US 6.5 — Explanation & Appeal | `3_gdpr_article22_transparency`, `gdpr_article22` | Intelligible explanation on demand, human review within 30 days, appeal path |

---

## 4. Login Screen UI

- Background: `var(--bg)` (#07182E) — matches app dark theme
- Centered card: `var(--panel)` with teal border, max-width 400px
- Header: FinPal logo-mark + "FinPal" wordmark + "v5.0 · TRUSTWORTHY AI" tag (reuse existing `.logo` styles)
- Fields: username (type=text), password (type=password) — styled to match existing `input` styles in new-app modal
- Button: `.btn.btn-primary` "Sign In"
- Error: inline `<div>` in red below button, hidden until bad credentials
- Keyboard: Enter on either field triggers submit

---

## 5. Logout

- A "Log Out" button (`.btn.btn-outline`) is added to the topbar right side after login
- Clicking it calls `window.location.reload()` — returns to login screen
- No session persistence — full page reload clears all state

---

## 6. Credentials Reference (Demo)

| Username | Password | Role | Default View |
|---|---|---|---|
| `credit.officer` | `FinPal@CO1` | Credit Officer | Applications |
| `risk.manager` | `FinPal@RM2` | Risk Manager | Model Governance |
| `compliance.officer` | `FinPal@CMP3` | Compliance Officer | Compliance Dashboard |
| `ops.manager` | `FinPal@OPS4` | Operations Manager | Intake Pipeline |
| `it.admin` | `FinPal@ITA5` | IT Administrator | Architecture & Security |
| `mrm.analyst` | `FinPal@MRM6` | MRM Analyst | Model Governance |
| `collections.officer` | `FinPal@COL7` | Collections Officer | Collections |
| `borrower.sme` | `FinPal@SME8` | Borrower (SME) | Intake Portal |

---

## 7. Out of Scope

- Real authentication (OAuth, SAML, sessions) — this is a prototype demo
- Password hashing — credentials are plaintext in source, acceptable for demo
- Persistent sessions (localStorage/cookies)
- Role management UI — roles are hardcoded
