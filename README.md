# Cash Application Foundry IQ

**AI-powered cash application with multi-step reasoning and enterprise knowledge retrieval**

Handles accounts receivable reconciliation by splitting the work across 5 specialized AI agents. Each agent does one job well, and reasoning is grounded in enterprise data via Foundry IQ.

**Live Demo:** [cash-app-foundry-iq.vercel.app](https://cash-app-foundry-iq.vercel.app)

---

## The Problem

Every company that sells on credit (net 30, net 60, etc.) has an Accounts Receivable team. Their job is to match money coming into the bank account to open invoices.

Real-world exceptions are constant:
- A customer sends $29,250 but the invoice is for $29,500. Is it a legitimate freight deduction?
- The bank shows the payer as "GREENFIELD TECH SOLUT" (truncated). Who is this customer?
- A payment comes from a factoring agent, not the original customer. Payment is legitimate but needs different routing.
- A payment arrives for an invoice under dispute in court. Can't post it—compliance issue.

An experienced AR analyst handles **8-10 edge cases per hour**. This system handles **35 in under 60 seconds**.

---

## How It Works

The system runs 5 agents in sequence. Each one takes structured output from the previous and adds value:

```
Bank Statement JSON
        │
        ▼
Agent 1: Bank Statement Parser
         Normalizes payer names, flags unusual transactions
        │
        ▼
Agent 2: AR Ledger Builder
         Structures invoices, calculates aging
         + Queries Foundry IQ for customer master data
        │
        ▼
Agent 3: Reconciliation Engine
         Matches transactions to invoices using 8 strategies
         Executes Python for all arithmetic verification
        │
        ▼
Agent 4: Mismatch Reasoning
         Analyzes exceptions, assigns risk tier, recommends action
         + Queries Foundry IQ for vendor history & compliance
        │
        ▼
Agent 5: Cash Posting
         Generates GL entries and workqueue items
```

---

## Foundry IQ Integration

Instead of working from static data, agents query Foundry IQ for live enterprise sources:

**Agent 2 (AR Ledger)** retrieves:
- Customer master (names, aliases, parent relationships)
- Open invoices by customer
- Payment terms and credit limits

**Agent 4 (Mismatch Reasoning)** retrieves:
- Vendor profiles (deduction patterns, dispute history, risk level)
- Contract terms (authorized freight %, damage allowances)
- Compliance holds (OFAC status, legal disputes, payment blocks)

Every decision includes citations to its Foundry sources.

---

## Exceptions Handled

The system recognizes 35 edge case types across 7 categories:

| Category | Examples |
|---|---|
| **Amount mismatches** | Early-pay discount, freight deduction, damage claim, overpayment |
| **Identity & name** | SWIFT truncation, DBA mismatch, post-acquisition name change |
| **Multi-entity** | Parent paying for subsidiary, factoring agent, intercompany netting |
| **Timing** | Duplicate payment, installment, NSF return, stale check |
| **Remittance** | Missing remittance, vague reference, legacy invoice ID, PO number |
| **FX/International** | Foreign currency with conversion, FX rate mismatch |
| **Compliance** | OFAC hold, disputed invoice, legal hold |

---

## Getting Started

### Requirements
- Python 3.11+
- Node.js 18+
- Git

### Local Setup

**Backend:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

**Environment Configuration:**
```bash
cp .env.example .env
```

For demo mode (no Azure account needed):
```
USE_FIXTURES=true
```

For live Azure + Foundry mode:
```
AZURE_AI_ENDPOINT=https://your-project.services.ai.azure.com
AZURE_API_KEY=your_key
FOUNDRY_ENDPOINT=https://your-foundry.services.ai.azure.com
FOUNDRY_API_KEY=your_key
USE_FIXTURES=false
```

### Running Locally

**Terminal 1 - Backend:**
```bash
cd backend
export USE_FIXTURES=true
uvicorn main:app --port 8001 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
export NEXT_PUBLIC_API_URL=http://localhost:8001
npm run dev
```

Open http://localhost:3000 → Click "Load Demo Data" → "Run Cash Application"

---

## Deployment

### Frontend to Vercel
1. Connect GitHub repo to Vercel
2. Set root directory: `./frontend`
3. Deploy

### Backend to Railway
1. Connect GitHub repo to Railway
2. Set root directory: `/backend`
3. Add environment variables
4. Deploy (auto-detects Dockerfile)

---

## Project Structure

```
.
├── backend/
│   ├── agents/
│   │   ├── foundry_client.py          # Foundry IQ search client
│   │   ├── cash_app.py                # Orchestrator
│   │   ├── bank_statement_agent.py    # Agent 1
│   │   ├── ar_ledger_agent.py         # Agent 2 (+ Foundry)
│   │   ├── reconciliation_agent.py    # Agent 3
│   │   ├── mismatch_agent.py          # Agent 4 (+ Foundry)
│   │   └── posting_agent.py           # Agent 5
│   ├── data/
│   │   ├── bank_statement.json
│   │   ├── open_ar.json
│   │   └── cash_app_results.json      # Demo fixtures
│   ├── main.py                        # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
│   │   ├── page.js                    # Main UI
│   │   └── ...
│   └── package.json
├── docs/
│   ├── FOUNDRY_IQ_INTEGRATION.md
│   └── ...
└── README.md
```

---

## How Agents Reason

Each agent receives only the data it needs and outputs structured JSON:

**Agent 1 output:** Normalized transactions with flags
**Agent 2 output:** Structured invoices, customer index, aging buckets
**Agent 3 output:** Matches with confidence scores, exceptions flagged
**Agent 4 output:** Exception analysis with risk tier and recommended action
**Agent 5 output:** GL posting instructions and workqueue items

---

## Demo Data

The system includes 10 realistic demo scenarios (in `backend/data/samples/`):
- Cloud vendor overage claims
- License true-up disputes
- Scope creep billing conflicts
- Factoring agent payments
- OFAC-flagged transactions

Each scenario has:
- Bank statement JSON (normalized transactions)
- Open AR JSON (invoices with payment terms)
- Expected results (for validation)

---

## Key Features

✓ Real-time streaming UI (all tokens visible as they generate)  
✓ Code execution in Agent 3 (verified arithmetic, no hallucination on math)  
✓ Foundry IQ integration for grounded reasoning  
✓ 35+ edge case recognition  
✓ Risk-based escalation routing  
✓ Full audit trail (every decision documented)  
✓ Demo mode (no credentials needed) + production mode  

---

## License

MIT

---

## Contact

Built by Vinay Gangidi · [vinay.gangidi@gmail.com](mailto:vinay.gangidi@gmail.com)
