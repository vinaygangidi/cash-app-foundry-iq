# Quick Start

Get the system running locally in 15 minutes.

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- Git

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/vinaygangidi/cash-app-foundry-iq.git
cd cash-app-foundry-iq
```

---

## Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Step 3: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and set:
```
USE_FIXTURES=true
```

That's it. No Azure credentials needed for demo mode.

---

## Step 4: Start Backend

```bash
export USE_FIXTURES=true
uvicorn main:app --port 8001 --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8001
```

---

## Step 5: Frontend Setup (New Terminal)

```bash
cd frontend
npm install
```

---

## Step 6: Start Frontend

```bash
export NEXT_PUBLIC_API_URL=http://localhost:8001
npm run dev
```

You should see:
```
> ready - started server on 0.0.0.0:3000
```

---

## Step 7: Open Browser

Navigate to **http://localhost:3000**

You should see the Cash Application UI with:
- "Load Demo Data" button
- "Run Cash Application" button

---

## Step 8: Run the Demo

1. Click **"Load Demo Data"**
   - Wait for data to load (1-2 seconds)
   
2. Click **"Run Cash Application"**
   - Watch 5 agents run in sequence
   - See real-time streaming output
   - Agent 2 & 4 show Foundry IQ context

Expected runtime: 30-60 seconds in demo mode

---

## What You Should See

### Agent 1: Bank Statement Parser
```
Normalizing 35 bank transactions...
Flagging truncated names, foreign currency, compliance red flags...
```

### Agent 2: AR Ledger Builder
```
Foundry IQ context showing:
- GREENFIELD TECH SOLUT → CUST-001 (via alias)
- Open invoices by customer
- Payment terms and credit limits
Building customer index...
```

### Agent 3: Reconciliation Engine
```
Running 8-tier matching strategy...
Executing Python for verified arithmetic...
Matched 32 transactions, 3 exceptions flagged
```

### Agent 4: Mismatch Reasoning
```
Foundry IQ context showing:
- Vendor profiles (deduction patterns, risk level)
- Compliance holds and OFAC status
- Contract terms for authorized deductions
Analyzing exceptions with Foundry-sourced reasoning...
```

### Agent 5: Cash Posting
```
Generating GL posting instructions...
Creating workqueue items sorted by urgency...
```

### Final Output
```
✓ 35 transactions processed
✓ 32 auto-applied
✓ 3 escalated with risk tier and recommended action
✓ Full audit trail with Foundry sources
```

---

## Troubleshooting

### Backend won't start
```bash
# Make sure port 8001 is free
lsof -i :8001

# Or use a different port
uvicorn main:app --port 8002
```

### Frontend can't reach backend
```bash
# Verify backend is running
curl http://localhost:8001/health

# Check NEXT_PUBLIC_API_URL is set
echo $NEXT_PUBLIC_API_URL
```

### Dependencies not installing
```bash
# Clear pip cache and reinstall
pip install --no-cache-dir -r requirements.txt

# Or create fresh venv
rm -rf .venv
python -m venv .venv
pip install -r requirements.txt
```

---

## Next Steps

- **Deploy locally:** See [docs](.) for full deployment guide
- **Live deployment:** Deploy to Vercel (frontend) + Railway (backend)
- **Customize agents:** Edit `backend/agents/*.py`
- **Understand Foundry integration:** Read [foundry-iq-workflow.md](foundry-iq-workflow.md)

---

## Demo Data

The system includes 10 realistic demo scenarios in `backend/data/samples/`:
- Cloud vendor overage claims
- License true-up disputes
- Factoring agent payments
- OFAC-flagged transactions
- And 6 more...

Each has bank statement, open AR, and expected results.

---

## Key Features to Try

✓ **Real-time streaming** — Watch tokens appear as agents think  
✓ **Foundry IQ context** — See enterprise knowledge in Agent 2 & 4 output  
✓ **Risk tiering** — Exceptions escalated by severity  
✓ **GL entries** — Final posting instructions  
✓ **Full audit trail** — Every decision documented  

---

## Getting Help

- **GitHub issues:** [vinaygangidi/cash-app-foundry-iq/issues](https://github.com/vinaygangidi/cash-app-foundry-iq/issues)
- **Documentation:** See [docs/](.) for complete guides
- **Email:** vinay.gangidi@gmail.com
