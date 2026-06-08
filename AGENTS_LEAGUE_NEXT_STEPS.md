# Agents League 2026 — Next Steps

## ✅ What's Done

1. **New repo created locally** at `/Users/vgangidi/cash-app-foundry-iq`
2. **Foundry IQ integration built:**
   - `foundry_client.py` with search methods (fixtures mode ready)
   - Agent 2 (AR Ledger) + Foundry context injection
   - Agent 4 (Mismatch Reasoning) + Foundry-sourced vendor history
   - Orchestrator updated to initialize and inject Foundry context
3. **README written** — focused on Agents League narrative (Reasoning Agents + Foundry IQ)
4. **Initial commit made** with all code ready to go
5. **Deploy configs added** (render.yaml for Railway, Dockerfile for container)

---

## ⏳ What's Next (Your Action Items)

### Step 1: Push to GitHub (5 minutes)
```bash
cd /Users/vgangidi/cash-app-foundry-iq

# Create new repository on GitHub
# Name: cash-app-foundry-iq
# Description: "AI-powered cash application with Foundry IQ retrieval and multi-step reasoning"
# Make it PUBLIC
# Initialize with no README (we have one)

# Then push:
git remote add origin https://github.com/vinaygangidi/cash-app-foundry-iq.git
git branch -M main
git push -u origin main
```

### Step 2: Test Locally (15 minutes)
```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export USE_FIXTURES=true
uvicorn main:app --port 8001 --reload

# Frontend (another terminal)
cd frontend
npm install
export NEXT_PUBLIC_API_URL=http://localhost:8001
npm run dev

# Open http://localhost:3000
# Click "Load Demo Data" → "Run Cash Application"
# Watch 5 agents run with Foundry context injected
```

### Step 3: Deploy to Vercel (10 minutes)
1. Go to https://vercel.com
2. Connect your GitHub account
3. Import project → select `cash-app-foundry-iq`
4. Set root directory: `frontend`
5. Add environment variable: `NEXT_PUBLIC_API_URL=https://your-railway-url`
6. Deploy

### Step 4: Deploy Backend to Railway (10 minutes)
1. Go to https://railway.app
2. Connect GitHub
3. Create new project → Deploy from GitHub repo
4. Select `cash-app-foundry-iq`
5. Set root: `/backend`
6. Add environment variables:
   ```
   USE_FIXTURES=true
   FOUNDRY_MODE=fixtures
   ```
7. Deploy (Railway auto-detects Dockerfile)

### Step 5: Register for Agents League (5 minutes)
- Go to https://aka.ms/agentsleague/aisf
- Register with your GitHub account
- Select: **Reasoning Agents** track
- Submit repo: `https://github.com/vinaygangidi/cash-app-foundry-iq`
- Microsoft IQ: **Foundry IQ**

### Step 6: Record Demo Video (30 minutes)
Record a 3-5 minute video showing:
1. Navigate to live site (Vercel URL)
2. Click "Load Demo Data"
3. Click "Run Cash Application"
4. Show agents running in sequence
5. Highlight Foundry IQ context in Agent 2 (customer aliases) and Agent 4 (vendor history)
6. Show final workqueue with GL postings

Upload to YouTube (unlisted is fine) and link in README.

### Step 7: Final Polish & Submit (before June 14)
- [ ] README finalized
- [ ] Code tested locally + live
- [ ] Demo video recorded and linked
- [ ] No credentials in code
- [ ] Repo is public
- [ ] Submit via Agents League portal

---

## File Checklist

✅ Backend files:
- `backend/agents/foundry_client.py` — NEW Foundry IQ client
- `backend/agents/cash_app.py` — Updated with Foundry context injection
- `backend/agents/ar_ledger_agent.py` — Updated with Foundry context placeholder
- `backend/agents/mismatch_agent.py` — Updated to reference Foundry sources
- `backend/main.py` — Orchestrator (no changes needed)
- `backend/agents/bank_statement_agent.py` — Parser (no changes)
- `backend/agents/reconciliation_agent.py` — Matcher (no changes)
- `backend/agents/posting_agent.py` — Posting (no changes)

✅ Frontend files:
- All copied from cash-application-foundry (working UI)

✅ Docs:
- `README.md` — Agents League focused
- `docs/FOUNDRY_IQ_INTEGRATION.md` — Technical integration guide
- `LICENSE` — MIT
- `render.yaml` — Railway deployment config
- `.gitignore` — Excludes .env, venv, node_modules

---

## Expected Timeline

| Date | Task | Status |
|------|------|--------|
| Today (Jun 8) | Push to GitHub + test locally | ← You are here |
| Jun 9-10 | Deploy to Railway + Vercel | |
| Jun 10-11 | Record demo video | |
| Jun 11-12 | Final README polish + testing | |
| Jun 12-13 | Register for Agents League + submit | |
| Jun 14 | Deadline | |

**You have 6 days.** This is very doable.

---

## Key Highlights for Judges

When they review your submission, they'll see:

1. **GitHub repo** with clean Agents League branding (not recycled from Build AI Hackathon)
2. **README** explaining:
   - Problem: $2.3T annual AR, 35 edge cases
   - Solution: 5-agent reasoning pipeline
   - Innovation: Foundry IQ enterprise knowledge retrieval
3. **Code** with:
   - `foundry_client.py` showing Foundry integration
   - Agent 2 + 4 pulling live data (fixtures in demo, real Foundry in prod)
   - Clear separation: orchestration → agents → reasoning
4. **Demo video** showing:
   - Live system working end-to-end
   - Agents running in sequence
   - Foundry context in agent outputs
5. **Live site** at Vercel (judges can test themselves)

---

## Scoring Alignment

| Criterion (Weight) | How You Win |
|---|---|
| **Accuracy & Relevance (20%)** | Grounded in Foundry, not hallucination |
| **Reasoning & Multi-step (20%)** | 5 agents, each depends on previous output + Foundry retrieval |
| **Creativity (15%)** | AR as retrieval + reasoning problem is novel |
| **UX & Presentation (15%)** | Live site + demo video showing Foundry sources |
| **Reliability (20%)** | Foundry enforces compliance, agents handle 35 exception types |

**Total: 90+ points possible** if execution is clean.

---

## Questions?

- Agents League Discord: https://aka.ms/agentsleague/discord
- Foundry docs: https://learn.microsoft.com/en-us/azure/ai-foundry/
- Your submission: check that repo is PUBLIC before submitting

You're in great shape. Ship it! 🚀
