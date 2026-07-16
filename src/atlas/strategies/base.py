from __future__ import annotations

from abc import ABC, abstractmethod

from atlas.schemas.financial_metrics import FinancialMetrics
from atlas.schemas.company_score import CompanyScore

class InvestmentStrategy(ABC):
    """
    Base class for every Atlas investment strategy.

    Examples:
        - Quality Strategy
        - Buffett Strategy
        - Coffee Can Strategy
        - CANSLIM Strategy
        - Magic Formula Strategy
    """

    name: str = "Base Strategy"

    @abstractmethod
    def evaluate(
        self,
        metrics: FinancialMetrics,
    ) -> CompanyScore:
        """
        Evaluate a company and return a CompanyScore.
        """
        raise NotImplementedError
