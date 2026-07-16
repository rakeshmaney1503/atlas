from __future__ import annotations

from decimal import Decimal

from atlas.schemas.company_score import CompanyScore
from atlas.schemas.financial_metrics import FinancialMetrics
from atlas.services.screener.financial_strength import FinancialStrengthRules
from atlas.services.screener.growth import GrowthRules
from atlas.services.screener.quality import QualityRules
from atlas.services.screener.valuation import ValuationRules


class ScreenerService:
    """
    Atlas Screening Engine.

    Orchestrates all screening modules.
    Each module returns a ScoreCard.
    """

    @staticmethod
    def build_company_score(
        metrics: FinancialMetrics,
    ) -> CompanyScore:

        scorecards = [
            QualityRules.evaluate(metrics),
            FinancialStrengthRules.evaluate(metrics),
            GrowthRules.evaluate(metrics),
            ValuationRules.evaluate(metrics),
        ]

        quality_score = Decimal("0")
        financial_strength_score = Decimal("0")
        growth_score = Decimal("0")
        valuation_score = Decimal("0")
        risk_score = Decimal("0")

        screening_results = []

        total_score = Decimal("0")

        for card in scorecards:

            total_score += card.score

            screening_results.extend(card.results)

            if card.category == "Quality":
                quality_score = card.score

            elif card.category == "Financial Strength":
                financial_strength_score = card.score

            elif card.category == "Growth":
                growth_score = card.score

            elif card.category == "Valuation":
                valuation_score = card.score

        # ----------------------------------------------------
        # Recommendation
        # ----------------------------------------------------

        if total_score >= Decimal("140"):
            recommendation = "Strong Buy"
        elif total_score >= Decimal("110"):
            recommendation = "Buy"
        elif total_score >= Decimal("80"):
            recommendation = "Candidate"
        else:
            recommendation = "Watch"

        # ----------------------------------------------------
        # Confidence
        # ----------------------------------------------------

        if total_score >= Decimal("140"):
            confidence = "High"
        elif total_score >= Decimal("100"):
            confidence = "Medium"
        else:
            confidence = "Low"

        return CompanyScore(
            symbol=metrics.symbol,
            company_name=metrics.company_name,

            quality_score=quality_score,
            financial_strength_score=financial_strength_score,
            growth_score=growth_score,
            valuation_score=valuation_score,
            risk_score=risk_score,

            total_score=total_score,

            recommendation=recommendation,
            confidence=confidence,

            scorecards=scorecards,

            screening_results=screening_results,
        )
