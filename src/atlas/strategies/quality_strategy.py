from __future__ import annotations

from atlas.schemas.financial_metrics import FinancialMetrics
from atlas.services.screener_service import ScreenerService
from atlas.strategies.base import InvestmentStrategy
from atlas.schemas.company_score import CompanyScore

class QualityStrategy(InvestmentStrategy):
    """
    Default Atlas strategy.

    This simply delegates to the ScreenerService.
    Future strategies will apply additional filters before
    returning a recommendation.
    """

    name = "Quality"

    def evaluate(
        self,
        metrics: FinancialMetrics,
    ) -> CompanyScore:
        return ScreenerService.build_company_score(metrics)
