from atlas.schemas.financial_metrics import FinancialMetrics
from atlas.strategies.registry import StrategyRegistry
from atlas.schemas.company_score import CompanyScore

class StrategyService:
    """
    Executes Atlas investment strategies.
    """

    @staticmethod
    def evaluate(
        strategy: str,
        metrics: FinancialMetrics,
    ) -> CompanyScore:

        return StrategyRegistry.create(
            strategy,
        ).evaluate(metrics)
