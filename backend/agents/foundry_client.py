"""
Foundry IQ Client for Cash Application

Provides semantic search and retrieval-augmented generation (RAG) over enterprise knowledge:
- Customer master data and aliases
- Open invoices and AR aging
- Contracts with payment terms and deduction policies
- Vendor profiles and dispute history
- Compliance holds and OFAC status

This client abstracts the Foundry IQ API so agents can query live enterprise sources
instead of working from static JSON fixtures.
"""

import os
import json
from typing import Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class SearchResult:
    """Single search result from Foundry IQ"""
    document_id: str
    source: str  # e.g., "customer_master", "invoice_history", "contract", "vendor_profile"
    content: dict
    relevance_score: float
    metadata: dict


class FoundryIQClient:
    """
    Client for Foundry IQ knowledge retrieval.

    In MVP (demo mode): Uses in-memory fixtures to simulate Foundry queries.
    In production: Connects to real Foundry IQ endpoint via Azure SDK.
    """

    def __init__(self, endpoint: str = "", api_key: str = "", use_fixtures: bool = True):
        """
        Initialize Foundry IQ client.

        Args:
            endpoint: Foundry IQ endpoint URL (e.g., https://project.services.ai.azure.com)
            api_key: API key for authentication
            use_fixtures: If True, use in-memory demo data instead of real Foundry
        """
        self.endpoint = endpoint or os.environ.get("FOUNDRY_ENDPOINT", "")
        self.api_key = api_key or os.environ.get("FOUNDRY_API_KEY", "")
        self.use_fixtures = use_fixtures or (not self.endpoint)
        self.knowledge_base = self._load_fixtures() if self.use_fixtures else {}

    def _load_fixtures(self) -> dict:
        """Load demo knowledge base (for USE_FIXTURES mode)"""
        return {
            "customers": [
                {
                    "customer_id": "CUST-001",
                    "name": "Greenfield Technology Solutions LLC",
                    "aliases": ["GREENFIELD TECH SOLUT", "Greenfield Tech", "GTS"],
                    "parent_customer_id": None,
                    "factoring_agent": None,
                    "credit_limit": 500000,
                    "payment_terms": "NET 30",
                    "total_open": 84250,
                    "invoice_count": 3,
                },
                {
                    "customer_id": "CUST-002",
                    "name": "Alpine Manufacturing Corp",
                    "aliases": ["Alpine Mfg", "AMC"],
                    "parent_customer_id": None,
                    "factoring_agent": None,
                    "credit_limit": 300000,
                    "payment_terms": "2/10 NET 30",
                    "total_open": 45000,
                    "invoice_count": 2,
                },
                {
                    "customer_id": "CUST-003",
                    "name": "Riverside Manufacturing Inc",
                    "aliases": ["Riverside Mfg", "RMI"],
                    "parent_customer_id": None,
                    "factoring_agent": "ACE Capital Partners",
                    "credit_limit": 250000,
                    "payment_terms": "NET 45",
                    "total_open": 125000,
                    "invoice_count": 4,
                },
            ],
            "invoices": [
                {
                    "invoice_id": "INV-29500",
                    "customer_id": "CUST-001",
                    "amount": 29500,
                    "open_amount": 29500,
                    "date": "2026-05-01",
                    "due_date": "2026-06-01",
                    "status": "OPEN",
                    "payment_terms": "NET 30",
                },
                {
                    "invoice_id": "INV-27350",
                    "customer_id": "CUST-001",
                    "amount": 27350,
                    "open_amount": 27350,
                    "date": "2026-04-15",
                    "due_date": "2026-05-15",
                    "status": "OPEN",
                    "payment_terms": "NET 30",
                },
                {
                    "invoice_id": "INV-27400",
                    "customer_id": "CUST-001",
                    "amount": 27400,
                    "open_amount": 27400,
                    "date": "2026-04-10",
                    "due_date": "2026-05-10",
                    "status": "OPEN",
                    "payment_terms": "NET 30",
                },
            ],
            "contracts": [
                {
                    "contract_id": "CST-2024-001",
                    "customer_id": "CUST-001",
                    "freight_allowance_pct": 1.5,
                    "freight_allowance_cap": 500,
                    "early_pay_discount_pct": 0,
                    "damage_claim_process": "documented_with_carrier",
                    "dispute_resolution": "escalate_to_legal_if_over_1000",
                    "signed_date": "2024-01-01",
                    "renewal_date": "2025-01-01",
                },
                {
                    "contract_id": "CST-2024-002",
                    "customer_id": "CUST-002",
                    "freight_allowance_pct": 2.0,
                    "freight_allowance_cap": 600,
                    "early_pay_discount_pct": 2.0,
                    "early_pay_discount_days": 10,
                    "damage_claim_process": "pre_approved_up_to_250",
                    "dispute_resolution": "arbitration",
                    "signed_date": "2024-03-01",
                    "renewal_date": "2025-03-01",
                },
            ],
            "vendor_profiles": [
                {
                    "vendor_name": "Greenfield Technology Solutions",
                    "customer_id": "CUST-001",
                    "risk_level": "low",
                    "dispute_history_count": 0,
                    "typical_deduction_pct": 0.5,
                    "deduction_patterns": ["freight_claims"],
                    "payment_reliability": "excellent",
                },
                {
                    "vendor_name": "Alpine Manufacturing Corp",
                    "customer_id": "CUST-002",
                    "risk_level": "medium",
                    "dispute_history_count": 2,
                    "typical_deduction_pct": 1.8,
                    "deduction_patterns": ["freight_claims", "damage_claims"],
                    "payment_reliability": "good",
                },
            ],
            "compliance": [
                {
                    "invoice_id": "INV-29500",
                    "holds": [],
                    "ofac_status": "clear",
                    "payment_blocked": False,
                    "legal_dispute": None,
                },
            ],
        }

    def search_customer(self, query: str, customer_id: Optional[str] = None) -> list[SearchResult]:
        """
        Search for customer master data and aliases.

        Args:
            query: Free-text search (e.g., "Greenfield Technology")
            customer_id: Optional exact customer ID match

        Returns:
            List of SearchResult objects with customer data
        """
        results = []

        if self.use_fixtures:
            for cust in self.knowledge_base.get("customers", []):
                score = 0.0
                if customer_id and cust["customer_id"] == customer_id:
                    score = 1.0
                elif query.lower() in cust["name"].lower():
                    score = 0.95
                elif any(q.lower() in alias.lower() for alias in cust.get("aliases", []) for q in query.split()):
                    score = 0.85

                if score > 0.5:
                    results.append(SearchResult(
                        document_id=cust["customer_id"],
                        source="customer_master",
                        content=cust,
                        relevance_score=score,
                        metadata={"doc_type": "customer", "indexed_date": "2026-06-01"}
                    ))

        return sorted(results, key=lambda r: r.relevance_score, reverse=True)[:10]

    def search_invoices(self, customer_id: str, status: str = "OPEN") -> list[SearchResult]:
        """
        Search for open invoices by customer.

        Args:
            customer_id: Customer ID to search
            status: Invoice status filter (OPEN, PARTIAL, CLOSED, DISPUTED, LEGAL_HOLD)

        Returns:
            List of SearchResult objects with invoice data
        """
        results = []

        if self.use_fixtures:
            for inv in self.knowledge_base.get("invoices", []):
                if inv["customer_id"] == customer_id and inv.get("status", "OPEN") == status:
                    results.append(SearchResult(
                        document_id=inv["invoice_id"],
                        source="invoice_history",
                        content=inv,
                        relevance_score=0.95,
                        metadata={"doc_type": "invoice", "indexed_date": "2026-06-01"}
                    ))

        return results

    def search_contracts(self, customer_id: str, invoice_id: Optional[str] = None) -> list[SearchResult]:
        """
        Search for contract terms and deduction policies.

        Args:
            customer_id: Customer ID to search
            invoice_id: Optional invoice ID for specific contract lookup

        Returns:
            List of SearchResult objects with contract terms
        """
        results = []

        if self.use_fixtures:
            for contract in self.knowledge_base.get("contracts", []):
                if contract["customer_id"] == customer_id:
                    results.append(SearchResult(
                        document_id=contract["contract_id"],
                        source="contract",
                        content=contract,
                        relevance_score=0.98,
                        metadata={"doc_type": "contract", "indexed_date": "2026-06-01"}
                    ))

        return results

    def search_vendor_history(self, vendor_name: str, customer_id: Optional[str] = None) -> list[SearchResult]:
        """
        Search for vendor dispute history and deduction patterns.

        Args:
            vendor_name: Vendor/customer name to search
            customer_id: Optional customer ID for exact match

        Returns:
            List of SearchResult objects with vendor profile data
        """
        results = []

        if self.use_fixtures:
            for profile in self.knowledge_base.get("vendor_profiles", []):
                score = 0.0
                if customer_id and profile["customer_id"] == customer_id:
                    score = 1.0
                elif vendor_name.lower() in profile["vendor_name"].lower():
                    score = 0.95

                if score > 0.5:
                    results.append(SearchResult(
                        document_id=profile["vendor_name"],
                        source="vendor_profile",
                        content=profile,
                        relevance_score=score,
                        metadata={"doc_type": "vendor_profile", "indexed_date": "2026-06-01"}
                    ))

        return results

    def search_compliance(self, invoice_id: str, transaction_id: Optional[str] = None) -> list[SearchResult]:
        """
        Search for compliance holds, OFAC flags, legal disputes.

        Args:
            invoice_id: Invoice ID to check
            transaction_id: Optional transaction ID for bank statement transaction

        Returns:
            List of SearchResult objects with compliance data
        """
        results = []

        if self.use_fixtures:
            for compliance in self.knowledge_base.get("compliance", []):
                if compliance["invoice_id"] == invoice_id:
                    results.append(SearchResult(
                        document_id=f"{invoice_id}_compliance",
                        source="compliance",
                        content=compliance,
                        relevance_score=1.0,
                        metadata={"doc_type": "compliance", "indexed_date": "2026-06-01"}
                    ))

        return results

    def format_context(self, results: list[SearchResult]) -> str:
        """
        Format search results as context string for agent prompts.

        Args:
            results: List of SearchResult objects from search methods

        Returns:
            Formatted string suitable for inclusion in agent system prompt
        """
        if not results:
            return "No Foundry IQ results found."

        context_lines = [f"## Foundry IQ Knowledge Retrieval (found {len(results)} results)\n"]

        for i, result in enumerate(results, 1):
            context_lines.append(f"### Result {i} (confidence: {result.relevance_score:.0%})")
            context_lines.append(f"**Source:** {result.source}")
            context_lines.append(f"**Document:** {result.document_id}\n")
            context_lines.append("```json")
            context_lines.append(json.dumps(result.content, indent=2))
            context_lines.append("```\n")

        return "\n".join(context_lines)
