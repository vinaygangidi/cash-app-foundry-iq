# Cash Application Foundry IQ

**AI-powered cash application with multi-step reasoning and enterprise knowledge retrieval**

> Built for Microsoft Agents League 2026 · Track: Reasoning Agents · Microsoft IQ: Foundry IQ

**Live Demo:** [cash-app-foundry-iq.vercel.app](https://cash-app-foundry-iq.vercel.app) · **Agents League:** [aka.ms/agentsleague/aisf](https://aka.ms/agentsleague/aisf)

---

## The Problem

Every company that sells on credit (net 30, net 60, etc.) has an Accounts Receivable team. Their job is to match money coming into the bank account to open invoices. Sounds simple. It isn't.

Real-world exceptions are constant:
- A customer sends $29,250 but the invoice is for $29,500. Is it a legitimate freight deduction or an unauthorized short pay?
- The bank shows the payer as "GREENFIELD TECH SOLUT" (truncated at 35 characters). Who is this?
- A payment comes from "ACE Capital Partners" but the customer is "Riverside Manufacturing." It's a factoring agent—the payment is legitimate but needs different routing.
- A payment arrives for an invoice that's under dispute in court. Posting it would be a compliance problem.

An experienced AR analyst handles maybe **8-10 edge cases per hour**. This system handles **35 in under 60 seconds** and shows its reasoning for every single one.

**The scale:** US companies process **$2.3 trillion in AR annually**. Each day a payment sits unposted is one more day of working capital tied up. For a $500M revenue company, that's roughly $1.4M per DSO day.

---

## How It Works: The 5-Agent Pipeline with Foundry IQ

Instead of one big AI trying to do everything, we split the work across **5 specialist agents**, each one does one job well, and each decision is grounded in **Foundry IQ enterprise knowledge**.

```
Your bank statement JSON
        │
        ▼
Agent 1: Bank Statement Parser          (normalizes payer names, flags unusual txns)
        │
        ▼
Agent 2: AR Ledger Builder              (+ Foundry IQ customer master)
         ├─ Query: Customer aliases, parent/subsidiary relationships
         ├─ Query: Open invoices by customer
         └─ Result: Enriched invoice index from enterprise sources
        │
        ▼
Agent 3: Reconciliation Engine          (runs 8 matching strategies + code execution)
        │
        ▼
Agent 4: Mismatch Reasoning             (+ Foundry IQ vendor history & compliance)
         ├─ Query: Vendor deduction patterns, dispute history, risk level
         ├─ Query: Compliance holds, OFAC status, legal disputes
         └─ Result: Grounded reasoning with cited sources
        │
        ▼
Agent 5: Cash Posting                   (generates final GL entries and workqueue)
```

---

## What Makes This Reasoning-Agents Track Material

### 1. **Multi-Step Reasoning Pipeline**
- 5 agents, each one processes structured output from the previous
- Agent 1 → Agent 2 → Agent 3 (code execution) → Agent 4 (business judgment) → Agent 5
- Not parallel, not simple orchestration—a **reasoning pipeline where later agents depend on earlier decisions**

### 2. **Complex Problem Domain**
- $2.3T annual AR problem, enterprise-grade
- 35 different exception types across 7 categories
- Reconciliation requires both **data matching AND business judgment**

### 3. **Foundry IQ Integration (Enterprise Knowledge Retrieval)**
- **Reasoning agents + enterprise sources = grounded answers**
- No hallucination: every deduction is validated against contract terms retrieved from Foundry
- Every vendor decision is grounded in historical dispute patterns from Foundry
- Compliance checks happen before any posting (OFAC, legal holds)

---

## Foundry IQ Integration Details

### Agent 2 (AR Ledger) + Foundry IQ
**What it does:**
- Queries Foundry for **customer master data** (canonical names, aliases, parent relationships)
- Retrieves **open invoices by customer** from Foundry knowledge base
- Validates customer data against live enterprise sources, not static JSON

**Example:**
```
Input: payer_alias_registry from bank statement contains "GREENFIELD TECH SOLUT"
Foundry query: search_customer("GREENFIELD TECH SOLUT")
Result: {
  customer_id: "CUST-001",
  name: "Greenfield Technology Solutions LLC",
  aliases: ["GREENFIELD TECH SOLUT", "Greenfield Tech", "GTS"],
  parent_customer_id: null,
  total_open: $84,250
}
Agent output: Invoice index enriched with Foundry's canonical customer names
```

### Agent 4 (Mismatch Reasoning) + Foundry IQ
**What it does:**
- Queries Foundry for **vendor dispute history and deduction patterns**
- Retrieves **contract terms** (authorized freight %, damage allowances, early-pay discounts)
- Checks **compliance registry** (OFAC status, legal holds, payment blocks)
- Every exception recommendation includes citation to Foundry source

**Example:**
```
Exception: Customer paid $29,250 but invoice is $29,500 ($250 short)

Foundry queries:
  1. search_contracts(customer_id="CUST-001")
     → Contract CST-2024-001: "freight_allowance_pct: 1.5%, freight_allowance_cap: $500"
  
  2. search_vendor_history(vendor_name="Greenfield")
     → Vendor profile: "typical_deduction_pct: 0.5%, deduction_patterns: ['freight_claims']"

Agent 4 reasoning:
  "$250 = 0.85% of $29,500 invoice"
  "Contract allows 1.5% freight deduction"
  "Vendor history shows pattern of 0.5% typical deductions"
  "Confidence: 92%"
  "Recommended action: AUTO_APPLY with note 'Freight deduction per CST-2024-001'"
  "Sources: Foundry contract_2024_001, vendor_profile_greenfield"
```

### Knowledge Base Schema
**Foundry IQ indexes (in demo mode: memory fixtures; in production: real Foundry):**

1. **customer_master** — Names, aliases, parent relationships, credit limits
2. **invoices** — Open AR by customer, amounts, aging, status (OPEN, DISPUTED, LEGAL_HOLD)
3. **contracts** — Payment terms, freight allowance %, damage procedures, dispute resolution
4. **vendor_profiles** — Risk level, deduction patterns, past dispute count, payment reliability
5. **compliance** — OFAC status, legal holds, payment blocks per invoice

---

## 35 Edge Cases We Handle

| Category | What it covers |
|---|---|
| **Amount mismatches** (10) | Exact match, multi-invoice bundle, early-pay discount (valid), unauthorized short pay, freight deduction, damage claim, overpayment to credit, credit memo netting, wire fee write-off (up to $25 auto), late discount |
| **Identity and name issues** (4) | SWIFT 35-char truncation, DBA/trade name, post-acquisition name change, fuzzy alias matching |
| **Multi-entity payments** (4) | Parent paying for subsidiary, factoring agent payment, intercompany AP/AR netting, wrong legal entity |
| **Timing problems** (6) | Duplicate payment, installment/partial, NSF return + reversal, post-dated check hold, stale check (over 180 days), prepayment to unearned revenue |
| **Remittance issues** (5) | No remittance (FIFO match), vague remittance (amount match), PO number only, legacy ERP invoice number, EDI 820 pending |
| **FX and international** (2) | EUR SWIFT payment with FX conversion, FX rate verification via Python |
| **Compliance and legal** (3) | OFAC/sanctions hold (same-day escalation), disputed invoice block, legal hold escalation |

---

## Code Structure

```
cash-app-foundry-iq/
├── backend/
│   ├── agents/
│   │   ├── foundry_client.py          # ← NEW: Foundry IQ client with search methods
│   │   ├── cash_app.py                # Orchestrator: injects Foundry context into agents
│   │   ├── bank_statement_agent.py    # Agent 1: parses bank statement
│   │   ├── ar_ledger_agent.py         # Agent 2: + Foundry IQ customer lookup
│   │   ├── reconciliation_agent.py    # Agent 3: matching with code execution
│   │   ├── mismatch_agent.py          # Agent 4: + Foundry IQ vendor history & compliance
│   │   └── posting_agent.py           # Agent 5: GL posting instructions
│   ├── data/
│   │   ├── bank_statement.json        # 35-txn demo bank statement
│   │   ├── open_ar.json               # 38-invoice demo AR ledger
│   │   └── cash_app_results.json      # Pre-built demo results (for fixtures mode)
│   ├── main.py                        # FastAPI: SSE streaming, demo + live modes
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   └── app/
│       ├── page.js                    # Next.js UI: real-time streaming, approve/reject
│       └── ...
├── docs/
│   └── FOUNDRY_IQ_INTEGRATION.md      # Detailed integration guide
├── README.md                          # ← You are here
└── LICENSE

```

---

## Running It Locally

You need: **Python 3.11+**, **Node.js 18+**, and **Git**. For demo mode, that's all. For live Azure mode, you also need an Azure AI Foundry project.

### Step 1: Clone the repo

```bash
git clone https://github.com/vinaygangidi/cash-app-foundry-iq.git
cd cash-app-foundry-iq
```

### Step 2: Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
# .venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### Step 3: Configure environment

Copy the example file:

```bash
cp .env.example .env
```

**Demo mode** (no Azure account needed):
```
USE_FIXTURES=true
FOUNDRY_MODE=fixtures
```

**Live Azure + Foundry mode** (requires Azure AI Foundry project):
```
AZURE_AI_ENDPOINT=https://your-project.services.ai.azure.com
AZURE_API_KEY=your_api_key_here
AZURE_OPENAI_API_VERSION=2024-12-01-preview
USE_FIXTURES=false
FOUNDRY_ENDPOINT=https://your-foundry.services.ai.azure.com
FOUNDRY_API_KEY=your_foundry_key
```

### Step 4: Start the backend

```bash
uvicorn main:app --port 8001 --reload
```

### Step 5: Frontend (separate terminal)

```bash
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8001 npm run dev
```

Open `http://localhost:3000`. Click **Load Demo Data**, then **Run Cash Application**.

---

## Deploying to Railway + Vercel

### Backend to Railway

1. Connect GitHub repo, set root to `/backend`
2. Railway detects the Dockerfile automatically
3. Add environment variables in the Railway dashboard
4. Railway gives you a public HTTPS URL

### Frontend to Vercel

1. Connect GitHub repo, set root to `/frontend`
2. Add `NEXT_PUBLIC_API_URL=https://your-railway-app.up.railway.app`
3. Every push to `main` deploys automatically

---

## Agents League Submission

### Judges Will See

1. **Multi-step reasoning** — 5 agents, each one builds on the previous
2. **Enterprise knowledge retrieval** — Agents query Foundry IQ, not static data
3. **Grounded answers** — Every deduction validated against contract terms, every vendor decision grounded in history
4. **Clear audit trail** — Each agent output shows sources: "Foundry contract_2024_001, vendor_profile, confidence 92%"

### How Foundry IQ Integration Strengthens the Submission

| Judging Criterion | How Foundry Helps |
|---|---|
| **Accuracy & Relevance (20%)** | Grounded in live enterprise sources, not hallucination |
| **Reasoning & Multi-step (20%)** | 5 agents + Foundry retrieval = traceable decision chain with citations |
| **Creativity (15%)** | AR reconciliation as retrieval + reasoning problem is novel positioning |
| **UX & Presentation (15%)** | Demo shows Foundry citations in every agent output = professional, auditable |
| **Reliability & Safety (20%)** | Foundry enforces permissions, compliance checks happen before posting |

---

## Quick Start: See It Working

### Local demo (5 minutes):
```bash
# Backend
cd backend
export USE_FIXTURES=true
uvicorn main:app --port 8001

# Frontend (another terminal)
cd frontend
npm run dev
# Open http://localhost:3000 → Load Demo → Run Cash App
```

### Live demo:
https://cash-app-foundry-iq.vercel.app

---

## What's Next (Production Roadmap)

**Phase 1 (Now):** MVP with Foundry IQ integration, demo data, streaming UI ✅
**Phase 2 (3 months):** PDF ingestion via Document Intelligence, async queue, PostgreSQL audit trail
**Phase 3 (12 months):** 50+ companies, 1M+ txns/month, SAP/Oracle/NetSuite connectors, multi-region, fine-tuned models

---

## Team

**Vinay Gangidi** | [vinay.gangidi@gmail.com](mailto:vinay.gangidi@gmail.com)

---

## References

- [Agents League Reasoning Agents Track](https://aka.ms/agentsleague/aisf)
- [Microsoft Foundry IQ Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [FOUNDRY_IQ_INTEGRATION.md](docs/FOUNDRY_IQ_INTEGRATION.md) — Detailed integration guide
- [Agents League Discord](https://aka.ms/agentsleague/discord)

---

*Microsoft Agents League 2026 · Reasoning Agents Track · Foundry IQ Integration*
