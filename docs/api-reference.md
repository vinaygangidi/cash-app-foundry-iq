# API Reference

Agent input/output specifications for the 5-agent pipeline.

---

## Agent 1: Bank Statement Parser

### Input

```json
{
  "task": "Parse and normalize this bank statement...",
  "bank_statement": [
    {
      "transaction_id": "TXN-001",
      "date": "2026-06-01",
      "payer": "GREENFIELD TECH SOLUT",
      "amount": 29250,
      "remittance_text": "Invoice 29500",
      "transaction_type": "ACH"
    },
    ...
  ]
}
```

### Output

```json
{
  "agent": "BankStatementIntelligenceAgent",
  "transactions": [
    {
      "txn_id": "TXN-001",
      "original_payer": "GREENFIELD TECH SOLUT",
      "normalized_payer": "GREENFIELD TECHNOLOGY SOLUTIONS",
      "payer_confidence": 0.87,
      "amount": 29250,
      "currency": "USD",
      "date": "2026-06-01",
      "remittance_references": ["INV-29500"],
      "unusual_flags": [],
      "foreign_currency": false,
      "potential_compliance_issue": false
    },
    ...
  ],
  "summary": {
    "total_transactions": 35,
    "total_amount": 987654.32,
    "unusual_flags_count": 2,
    "foreign_currency_count": 0,
    "compliance_flags_count": 0
  }
}
```

---

## Agent 2: AR Ledger Builder

### Input

```json
{
  "task": "Structure this open AR ledger...",
  "open_ar": [
    {
      "invoice_id": "INV-29500",
      "customer_id": "CUST-001",
      "amount": 29500,
      "due_date": "2026-06-01",
      "payment_terms": "NET 30"
    },
    ...
  ]
}
```

### Foundry IQ Context Injected

Agent 2's system prompt includes:

```
## Foundry IQ Knowledge Retrieval

### Result 1 (confidence: 100%)
**Source:** customer_master

{
  "customer_id": "CUST-001",
  "name": "Greenfield Technology Solutions LLC",
  "aliases": ["GREENFIELD TECH SOLUT", "Greenfield Tech"],
  ...
}

[More results...]
```

### Output

```json
{
  "agent": "ARLedgerAgent",
  "invoices": [
    {
      "invoice_id": "INV-29500",
      "customer_id": "CUST-001",
      "customer_name": "Greenfield Technology Solutions LLC",
      "amount": 29500,
      "open_amount": 29500,
      "status": "OPEN",
      "aging_bucket": "CURRENT",
      "aging_days": 0,
      "payment_terms": "NET 30",
      "discount_pct": 0,
      "due_date": "2026-06-01"
    },
    ...
  ],
  "customer_index": {
    "CUST-001": {
      "name": "Greenfield Technology Solutions LLC",
      "aliases": ["GREENFIELD TECH SOLUT", "Greenfield Tech"],
      "parent_customer_id": null,
      "factoring_agent": null,
      "total_open": 84250,
      "invoice_count": 3
    },
    ...
  },
  "foundry_iq_sources": [
    "Foundry: customer_master (for aliases and parent relationships)",
    "Foundry: compliance registry (for holds and legal disputes)"
  ]
}
```

---

## Agent 3: Reconciliation Engine

### Input

```json
{
  "task": "Match every bank transaction to open AR invoices...",
  "normalized_transactions": [Agent 1 output],
  "invoices": [Agent 2 invoices],
  "customer_index": [Agent 2 customer_index]
}
```

### Output

```json
{
  "agent": "ReconciliationAgent",
  "matches": [
    {
      "txn_id": "TXN-001",
      "invoice_id": "INV-29500",
      "match_strategy": "EXACT_AMOUNT_MATCH",
      "confidence": 0.95,
      "exception": null,
      "matched_amount": 29500,
      "amount_diff": 0
    },
    {
      "txn_id": "TXN-002",
      "invoice_id": "INV-27350",
      "match_strategy": "AMOUNT_PLUS_SMALL_DELTA",
      "confidence": 0.87,
      "exception": "AMOUNT_MISMATCH",
      "matched_amount": 29250,
      "amount_diff": -250
    },
    ...
  ],
  "reconciliation_summary": {
    "total_transactions": 35,
    "matched": 32,
    "exceptions": 3,
    "match_rate": 0.914
  }
}
```

---

## Agent 4: Mismatch Reasoning

### Input

```json
{
  "task": "Analyze each exception...",
  "exception_matches": [
    {
      "txn_id": "TXN-002",
      "invoice_id": "INV-27350",
      "amount_diff": -250,
      "exception": "AMOUNT_MISMATCH"
    },
    ...
  ]
}
```

### Foundry IQ Context Injected

Agent 4's system prompt includes:

```
## Foundry IQ Knowledge Retrieval

### Result 1 (confidence: 95%)
**Source:** vendor_profile

{
  "vendor_name": "Greenfield Technology Solutions",
  "risk_level": "low",
  "typical_deduction_pct": 0.5,
  "deduction_patterns": ["freight_claims"]
}

### Result 2 (confidence: 100%)
**Source:** compliance

{
  "invoice_id": "INV-29500",
  "holds": [],
  "ofac_status": "clear",
  "payment_blocked": false
}

[More results...]
```

### Output

```json
{
  "agent": "MismatchReasoningAgent",
  "exception_analysis": [
    {
      "txn_id": "TXN-002",
      "exception_type": "FREIGHT_DEDUCTION",
      "exception_category_group": "AMOUNT_MISMATCH",
      "risk_tier": "LOW",
      "reasoning": "Payment is $250 short (0.85% deduction). Contract allows 1.5% freight deduction. Vendor has historical pattern of freight claims. No compliance holds.",
      "confidence_pct": 92,
      "recommended_action": "AUTO_APPLY",
      "sla_hours": 24,
      "escalation_contact": "NONE",
      "foundry_sources": [
        "Foundry: vendor_profile (deduction patterns)",
        "Foundry: contract_CUST-001 (authorized deductions)",
        "Foundry: compliance registry (no holds)"
      ]
    },
    ...
  ],
  "exception_summary": {
    "total_exceptions": 3,
    "by_risk_tier": {
      "LOW": 2,
      "MEDIUM": 1,
      "HIGH": 0,
      "CRITICAL": 0
    }
  }
}
```

---

## Agent 5: Cash Posting

### Input

```json
{
  "task": "Generate final GL posting instructions...",
  "all_matches": [Agent 3 matches],
  "exception_analysis": [Agent 4 analysis]
}
```

### Output

```json
{
  "agent": "CashPostingAgent",
  "workqueue": [
    {
      "work_item_id": "WQ-001",
      "txn_id": "TXN-001",
      "type": "AUTO_APPLY",
      "priority": "LOW",
      "gl_entries": [
        {
          "account": "1010",
          "account_name": "Cash Clearing",
          "debit": 29500,
          "credit": 0,
          "description": "Cash receipt from CUST-001"
        },
        {
          "account": "1200",
          "account_name": "Accounts Receivable",
          "debit": 0,
          "credit": 29500,
          "description": "Apply to INV-29500"
        }
      ],
      "confidence": 0.99,
      "sla_minutes": 15
    },
    {
      "work_item_id": "WQ-002",
      "txn_id": "TXN-002",
      "type": "DEDUCTION_WORKITEM",
      "priority": "MEDIUM",
      "gl_entries": [
        {
          "account": "1010",
          "account_name": "Cash Clearing",
          "debit": 29250,
          "credit": 0
        },
        {
          "account": "1200",
          "account_name": "Accounts Receivable",
          "debit": 0,
          "credit": 29250
        },
        {
          "account": "8020",
          "account_name": "Freight Deductions",
          "debit": 250,
          "credit": 0
        }
      ],
      "ar_analyst_note": "Likely freight deduction - vendor pattern matches. See exception analysis.",
      "sla_minutes": 240
    },
    ...
  ],
  "summary": {
    "total_work_items": 35,
    "auto_apply": 32,
    "manual_review": 2,
    "escalation": 1,
    "total_gl_entries": 105
  }
}
```

---

## Backend API Endpoints

### POST /analyze

Run the full 5-agent pipeline.

**Request:**
```json
{
  "bank_statement": [...],
  "open_ar": [...]
}
```

**Response:** Server-Sent Events (streaming)

```
event: agent_start
data: {"agent": "BankStatementIntelligenceAgent", ...}

event: agent_token
data: {"agent": "BankStatementIntelligenceAgent", "token": "Normalizing..."}

event: agent_complete
data: {"agent": "BankStatementIntelligenceAgent", "output": {...}}

[continues for each agent...]

event: swarm_complete
data: {"results": {...}, "final": {...}}
```

---

## Foundry IQ Client API

### Methods

**`search_customer(query: str) -> list[SearchResult]`**
- Search customer master data
- Returns: Customer names, aliases, parent relationships, credit limits

**`search_invoices(customer_id: str, status: str = "OPEN") -> list[SearchResult]`**
- Search open invoices by customer
- Returns: Invoice amounts, due dates, payment terms, aging

**`search_contracts(customer_id: str) -> list[SearchResult]`**
- Search contract terms
- Returns: Authorized deductions, freight allowances, early-pay discounts

**`search_vendor_history(vendor_name: str) -> list[SearchResult]`**
- Search vendor profiles and dispute history
- Returns: Risk level, deduction patterns, past disputes

**`search_compliance(invoice_id: str) -> list[SearchResult]`**
- Search compliance holds and OFAC status
- Returns: Legal holds, OFAC flags, payment blocks

**`format_context(results: list[SearchResult]) -> str`**
- Format search results as readable text
- Used to inject into agent system prompts

---

## Data Types

### SearchResult

```python
@dataclass
class SearchResult:
    document_id: str          # Unique ID (CUST-001, INV-29500, etc.)
    source: str               # "customer_master", "invoice_history", "contract", etc.
    content: dict             # The actual document content
    relevance_score: float    # 0.0 to 1.0 (1.0 = exact match)
    metadata: dict            # Additional metadata (doc_type, indexed_date, etc.)
```

---

## Error Handling

All agents return structured output, even on errors.

If an agent fails:
```json
{
  "agent": "AgentName",
  "error": "Error message",
  "output": null,
  "status": "FAILED"
}
```

The pipeline continues with Agent N+1, using available partial results.

---

## Specifications

- **Model:** GPT-4o-mini (agents 1, 2, 5), GPT-4o (agent 3, 4)
- **Max tokens:** 4096-8192 per agent
- **Timeout:** 300 seconds per agent
- **Streaming:** Real-time token output (Server-Sent Events)
- **Code execution:** Agent 3 uses Python in Azure Assistants API
