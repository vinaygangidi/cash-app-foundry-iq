# Cash Application Foundry IQ

**AI-powered accounts receivable reconciliation with enterprise knowledge retrieval**

Welcome to the documentation for Cash Application Foundry IQ. This system automates cash application using a 5-agent reasoning pipeline grounded in Foundry IQ enterprise knowledge.

---

## What This System Does

Handles **35 edge cases** in accounts receivable reconciliation in seconds:

- Customer name mismatches (SWIFT truncation, aliases, post-acquisition changes)
- Amount mismatches (freight deductions, damage claims, overpayments)
- Multi-entity payments (parent paying for subsidiary, factoring agents)
- Timing issues (duplicate payments, stale checks, NSF returns)
- Compliance holds (OFAC, legal disputes, payment blocks)

An experienced AR analyst handles 8-10 edge cases per hour. This system handles 35 in under 60 seconds.

---

## How It Works

### The 5-Agent Pipeline

Each agent is a specialist that does one job well:

1. **Bank Statement Parser** — Normalizes transactions, flags unusual activity
2. **AR Ledger Builder** — Structures invoices, builds lookup tables (+ Foundry IQ customer data)
3. **Reconciliation Engine** — Matches transactions to invoices using 8 strategies (with Python code execution)
4. **Mismatch Reasoning** — Analyzes exceptions, assigns risk, recommends action (+ Foundry IQ vendor history & compliance)
5. **Cash Posting** — Generates GL entries and workqueue items

### Foundry IQ Integration

**Agents 2 and 4 query Foundry IQ for enterprise knowledge:**

- **Customer master data** — Names, aliases, parent relationships, credit limits
- **Invoice history** — Open invoices, aging, payment terms
- **Contract data** — Authorized deductions, freight allowances, early-pay discounts
- **Vendor profiles** — Risk level, deduction patterns, historical disputes
- **Compliance registry** — OFAC status, legal holds, payment blocks

Every decision includes citations to its Foundry sources.

---

## Documentation

- **[How Agents Use Foundry IQ](foundry-iq-workflow.md)** — Step-by-step walkthrough with code examples
- **[Foundry IQ Integration Guide](FOUNDRY_IQ_INTEGRATION.md)** — Technical details and schema
- **[Quick Start](quick-start.md)** — Run locally in 15 minutes
- **[API Reference](api-reference.md)** — Agent inputs/outputs

---

## Quick Start

### Local Setup (5 minutes)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export USE_FIXTURES=true
uvicorn main:app --port 8001
```

In another terminal:
```bash
cd frontend
npm install
export NEXT_PUBLIC_API_URL=http://localhost:8001
npm run dev
```

Open http://localhost:3000 → Load Demo Data → Run Cash Application

---

## Key Features

✓ **Real-time streaming UI** — Watch agents reason in real-time  
✓ **Code execution** — Agent 3 verifies all arithmetic with Python  
✓ **Foundry IQ grounding** — Reasoning backed by enterprise data  
✓ **35+ edge cases** — Recognized and handled  
✓ **Risk-based routing** — Exceptions escalated by severity  
✓ **Full audit trail** — Every decision documented  
✓ **Demo + production** — Works with fixtures or real Azure  

---

## Architecture

```
Bank Statement JSON
    │
    ▼
Agent 1: Parser (normalizes)
    │
    ▼
Agent 2: AR Ledger (+ Foundry IQ)
    │
    ▼
Agent 3: Reconciliation (matches)
    │
    ▼
Agent 4: Mismatch Reasoning (+ Foundry IQ)
    │
    ▼
Agent 5: Posting (GL entries)
```

---

## Deployment

**Frontend:** Vercel  
**Backend:** Railway  
**Database:** Azure Blob Storage  
**Knowledge Base:** Foundry IQ (demo fixtures or real)

---

## Technologies

- **Backend:** Python 3.11, FastAPI, AsyncIO
- **Frontend:** Next.js 14, TypeScript, Tailwind CSS
- **AI:** Azure OpenAI (GPT-4o, GPT-4o-mini)
- **Knowledge:** Foundry IQ semantic search
- **Code Execution:** Azure Assistants API with Code Interpreter

---

## Repository

GitHub: [vinaygangidi/cash-app-foundry-iq](https://github.com/vinaygangidi/cash-app-foundry-iq)

---

## Contact

Built by Vinay Gangidi · [vinay.gangidi@gmail.com](mailto:vinay.gangidi@gmail.com)
