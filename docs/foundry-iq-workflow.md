# How Agents Use Foundry IQ

This document explains exactly how the agents query and use Foundry IQ enterprise knowledge.

---

## Overview

Two agents query Foundry IQ during the pipeline:

1. **Agent 2 (AR Ledger Builder)** — Queries customer master + invoice data
2. **Agent 4 (Mismatch Reasoning)** — Queries vendor profiles + compliance data

All other agents work without Foundry IQ.

---

## The Flow

```
Pipeline Starts
    │
    ├─→ FoundryIQClient initialized
    │   (demo mode with fixtures, or production mode with real API)
    │
    ├─→ Agent 1: Bank Statement Parser
    │   (no Foundry)
    │
    ├─→ Agent 2: AR Ledger Builder
    │   │
    │   ├─→ foundry.search_customer("*")
    │   │   Returns: All customers with aliases
    │   │
    │   ├─→ foundry.search_invoices("*")
    │   │   Returns: All open invoices
    │   │
    │   ├─→ format_context(foundry_results)
    │   │   Converts to readable text
    │   │
    │   └─→ Injects into agent's system prompt
    │
    ├─→ Agent 3: Reconciliation Engine
    │   (no Foundry, uses Agent 2 output)
    │
    ├─→ Agent 4: Mismatch Reasoning
    │   │
    │   ├─→ foundry.search_vendor_history("*")
    │   │   Returns: Vendor profiles
    │   │
    │   ├─→ foundry.search_compliance("*")
    │   │   Returns: Compliance holds and OFAC status
    │   │
    │   └─→ Uses context to ground reasoning
    │
    └─→ Agent 5: Cash Posting
        (no Foundry, final output)
```

---

## Agent 2: Customer & Invoice Data

### What Happens

**Code location:** `backend/agents/cash_app.py`, lines 332-336

```python
if agent_name == "ARLedgerAgent":
    # Query Foundry for customer + invoice data
    foundry_results = foundry.search_customer("*") + foundry.search_invoices("*")
    
    # Format results as readable text
    foundry_context = foundry.format_context(foundry_results)
    
    # Replace placeholder in system prompt
    system_prompt = system_prompt.replace("{foundry_context}", foundry_context)
```

### Step 1: Query Customers

```python
foundry.search_customer("*")
```

Returns a list of `SearchResult` objects:

```json
[
  {
    "document_id": "CUST-001",
    "source": "customer_master",
    "content": {
      "customer_id": "CUST-001",
      "name": "Greenfield Technology Solutions LLC",
      "aliases": ["GREENFIELD TECH SOLUT", "Greenfield Tech", "GTS"],
      "parent_customer_id": null,
      "factoring_agent": null,
      "credit_limit": 500000,
      "payment_terms": "NET 30",
      "total_open": 84250,
      "invoice_count": 3
    },
    "relevance_score": 1.0,
    "metadata": {"doc_type": "customer", "indexed_date": "2026-06-01"}
  },
  {
    "document_id": "CUST-003",
    "source": "customer_master",
    "content": {
      "customer_id": "CUST-003",
      "name": "Riverside Manufacturing Inc",
      "aliases": ["Riverside Mfg", "RMI"],
      "parent_customer_id": null,
      "factoring_agent": "ACE Capital Partners",
      "credit_limit": 250000,
      "total_open": 125000,
      "invoice_count": 4
    },
    "relevance_score": 1.0,
    "metadata": {"doc_type": "customer"}
  }
]
```

### Step 2: Query Invoices

```python
foundry.search_invoices("*")
```

Returns:

```json
[
  {
    "document_id": "INV-29500",
    "source": "invoice_history",
    "content": {
      "invoice_id": "INV-29500",
      "customer_id": "CUST-001",
      "amount": 29500,
      "open_amount": 29500,
      "date": "2026-05-01",
      "due_date": "2026-06-01",
      "status": "OPEN",
      "payment_terms": "NET 30"
    },
    "relevance_score": 0.95,
    "metadata": {"doc_type": "invoice", "indexed_date": "2026-06-01"}
  },
  {
    "document_id": "INV-27350",
    "source": "invoice_history",
    "content": {
      "invoice_id": "INV-27350",
      "customer_id": "CUST-001",
      "amount": 27350,
      "open_amount": 27350,
      "due_date": "2026-05-15",
      "status": "OPEN",
      "payment_terms": "NET 30"
    },
    "relevance_score": 0.95,
    "metadata": {"doc_type": "invoice"}
  }
]
```

### Step 3: Format as Text

```python
foundry_context = foundry.format_context(foundry_results)
```

Returns readable text:

```
## Foundry IQ Knowledge Retrieval (found 5 results)

### Result 1 (confidence: 100%)
**Source:** customer_master
**Document:** CUST-001

```json
{
  "customer_id": "CUST-001",
  "name": "Greenfield Technology Solutions LLC",
  "aliases": ["GREENFIELD TECH SOLUT", "Greenfield Tech", "GTS"],
  "parent_customer_id": null,
  "factoring_agent": null,
  "credit_limit": 500000,
  "payment_terms": "NET 30",
  "total_open": 84250,
  "invoice_count": 3
}
```

### Result 2 (confidence: 100%)
**Source:** customer_master
**Document:** CUST-003

```json
{
  "customer_id": "CUST-003",
  "name": "Riverside Manufacturing Inc",
  "aliases": ["Riverside Mfg", "RMI"],
  "parent_customer_id": null,
  "factoring_agent": "ACE Capital Partners",
  "credit_limit": 250000,
  "total_open": 125000
}
```

### Result 3 (confidence: 95%)
**Source:** invoice_history
**Document:** INV-29500

```json
{
  "invoice_id": "INV-29500",
  "customer_id": "CUST-001",
  "amount": 29500,
  "status": "OPEN",
  "due_date": "2026-06-01",
  "payment_terms": "NET 30"
}
```

[More results...]
```

### Step 4: Agent 2's System Prompt

Agent 2 receives this system prompt:

```
You are the AR Ledger Agent in a Cash Application swarm...

## Foundry IQ Knowledge Base
You have access to live enterprise sources via Foundry IQ. Here's what was retrieved:

## Foundry IQ Knowledge Retrieval (found 5 results)
...
[All the Foundry data from Step 3]
...

Use this Foundry IQ data to:
1. Enrich customer names and aliases
2. Identify parent-subsidiary relationships
3. Detect factoring agents
4. Flag compliance holds

For each invoice:
- Calculate aging bucket
- Parse payment terms
- Build customer index using Foundry aliases
...
```

### Step 5: Agent 2 Uses the Context

When Agent 2 sees bank payer "GREENFIELD TECH SOLUT":
- Foundry shows that's an alias for CUST-001
- Agent can match with high confidence
- Outputs enriched customer index with Foundry data

---

## Agent 4: Vendor & Compliance Data

### What Happens

**Code location:** `backend/agents/cash_app.py`, lines 338-345

```python
if agent_name == "MismatchReasoningAgent":
    # Query Foundry for vendor profiles + compliance
    foundry_vendors = foundry.search_vendor_history("*")
    foundry_compliance = foundry.search_compliance("*")
    foundry_context = foundry.format_context(foundry_vendors + foundry_compliance)
```

### Step 1: Query Vendor History

```python
foundry.search_vendor_history("*")
```

Returns vendor profiles:

```json
[
  {
    "document_id": "Greenfield Technology Solutions",
    "source": "vendor_profile",
    "content": {
      "vendor_name": "Greenfield Technology Solutions",
      "customer_id": "CUST-001",
      "risk_level": "low",
      "dispute_history_count": 0,
      "typical_deduction_pct": 0.5,
      "deduction_patterns": ["freight_claims"],
      "payment_reliability": "excellent"
    },
    "relevance_score": 0.95,
    "metadata": {"doc_type": "vendor_profile"}
  },
  {
    "document_id": "Alpine Manufacturing Corp",
    "source": "vendor_profile",
    "content": {
      "vendor_name": "Alpine Manufacturing Corp",
      "customer_id": "CUST-002",
      "risk_level": "medium",
      "dispute_history_count": 2,
      "typical_deduction_pct": 1.8,
      "deduction_patterns": ["freight_claims", "damage_claims"],
      "payment_reliability": "good"
    },
    "relevance_score": 0.95,
    "metadata": {"doc_type": "vendor_profile"}
  }
]
```

### Step 2: Query Compliance

```python
foundry.search_compliance("*")
```

Returns compliance flags:

```json
[
  {
    "document_id": "INV-29500_compliance",
    "source": "compliance",
    "content": {
      "invoice_id": "INV-29500",
      "holds": [],
      "ofac_status": "clear",
      "payment_blocked": false,
      "legal_dispute": null
    },
    "relevance_score": 1.0,
    "metadata": {"doc_type": "compliance"}
  }
]
```

### Step 3: Agent 4 Uses the Context

When analyzing an exception:

```
Transaction: $29,250 received
Invoice: INV-29500 for $29,500
Difference: -$250 (short by 2%)

Foundry data shows:
- Vendor "Greenfield" typical deduction: 0.5%
- This transaction: 0.85% deduction
- Contract allows: 1.5% freight deduction
- No compliance holds

Agent 4 reasons:
"0.85% is within the 1.5% contract limit and close to vendor's 
typical 0.5%. Vendor has low risk. No compliance issues. 
Likely legitimate freight deduction."

Output includes:
- Recommended action: AUTO_APPLY
- Foundry sources cited: vendor_profile, contract, compliance
```

---

## Code: The FoundryIQClient

### Search Methods

**Location:** `backend/agents/foundry_client.py`

```python
class FoundryIQClient:
    def search_customer(self, query: str, customer_id: Optional[str] = None):
        """Search for customer master data and aliases"""
        
    def search_invoices(self, customer_id: str, status: str = "OPEN"):
        """Search for open invoices by customer"""
        
    def search_contracts(self, customer_id: str):
        """Search for contract terms and deduction policies"""
        
    def search_vendor_history(self, vendor_name: str):
        """Search for vendor dispute history and deduction patterns"""
        
    def search_compliance(self, invoice_id: str):
        """Search for compliance holds, OFAC flags, legal disputes"""
        
    def format_context(self, results: list[SearchResult]) -> str:
        """Format search results as context string for agent prompts"""
```

### Demo vs Production

**Demo mode (current):**
```python
foundry = FoundryIQClient(use_fixtures=True)
# Uses in-memory fixtures (no credentials needed)
```

**Production mode (future):**
```python
foundry = FoundryIQClient(
    endpoint=os.environ.get("FOUNDRY_ENDPOINT"),
    api_key=os.environ.get("FOUNDRY_API_KEY"),
    use_fixtures=False
)
# Connects to real Foundry IQ API
```

The agent code stays exactly the same. Just the knowledge base source changes.

---

## Key Points

✓ **Agents don't know the difference** between demo fixtures and real Foundry IQ  
✓ **All queries happen upfront** before agent processing starts  
✓ **Results are injected as text** into agent system prompts  
✓ **Every decision can cite sources** from Foundry data  
✓ **Switching to real Foundry is a 1-line change** in the orchestrator  

---

## What Agents Get to See

Agent 2 sees:
- All customers with aliases and relationships
- All open invoices
- Payment terms and credit information

Agent 4 sees:
- Vendor profiles with historical patterns
- Compliance holds and legal status
- Contract terms for deductions

All formatted as readable context in their system prompts.
