from __future__ import annotations

from decimal import Decimal

from atlas.schemas.financial_metrics import FinancialMetrics
from atlas.schemas.screener import CompanyScore
from atlas.services.screener.financial_strength import FinancialStrengthRules
from atlas.services.screener.quality import QualityRules


class ScreenerService:
    """
    Atlas Screening Engine.

    Orchestrates all screening modules and produces
    a unified CompanyScore.
    """

    @staticmethod
    def build_company_score(
        metrics: FinancialMetrics,
    ) -> CompanyScore:

        quality_score, quality_results = (
            QualityRules.calculate_score(metrics)
        )

        (
            financial_strength_score,
            financial_strength_results,
        ) = FinancialStrengthRules.calculate_score(metrics)

        valuation_score = Decimal("0")
        growth_score = Decimal("0")
        risk_score = Decimal("0")

        total_score = (
            quality_score
            + financial_strength_score
            + valuation_score
            + growth_score
            + risk_score
        )

        # ==========================================================
        # Recommendation
        # ==========================================================

        if total_score >= Decimal("90"):
            recommendation = "Strong Buy"
        elif total_score >= Decimal("75"):
            recommendation = "Buy"
        elif total_score >= Decimal("60"):
            recommendation = "Candidate"
        else:
            recommendation = "Watch"

        # ==========================================================
        # Confidence
        # ==========================================================

        if total_score >= Decimal("75"):
            confidence = "High"
        elif total_score >= Decimal("50"):
            confidence = "Medium"
        else:
            confidence = "Low"

        return CompanyScore(
            symbol=metrics.symbol,
            company_name=metrics.company_name,
            quality_score=quality_score,
            financial_strength_score=financial_strength_score,
            valuation_score=valuation_score,
            growth_score=growth_score,
            risk_score=risk_score,
            total_score=total_score,
            recommendation=recommendation,
            confidence=confidence,
            screening_results=[
                *quality_results,
                *financial_strength_results,
            ],
        )
