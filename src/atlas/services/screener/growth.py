from __future__ import annotations

from decimal import Decimal

from atlas.schemas.financial_metrics import FinancialMetrics
from atlas.schemas.scorecard import ScoreCard
from atlas.schemas.screening_result import ScreeningResult


class GrowthRules:
    """
    Growth-related screening rules.
    """

    MAX_SCORE = Decimal("50")

    @staticmethod
    def _evaluate(
        *,
        rule: str,
        value: Decimal,
        threshold: Decimal,
        success_message: str,
        failure_message: str,
    ) -> ScreeningResult:

        passed = value >= threshold

        return ScreeningResult(
            rule=rule,
            passed=passed,
            value=value,
            threshold=threshold,
            message=success_message if passed else failure_message,
        )

    @staticmethod
    def evaluate_revenue_growth(
        metrics: FinancialMetrics,
    ) -> ScreeningResult:

        return GrowthRules._evaluate(
            rule="Revenue Growth",
            value=metrics.revenue_growth,
            threshold=Decimal("10"),
            success_message="Revenue growth is healthy.",
            failure_message="Revenue growth is below threshold.",
        )

    @staticmethod
    def evaluate_eps_growth(
        metrics: FinancialMetrics,
    ) -> ScreeningResult:

        return GrowthRules._evaluate(
            rule="EPS Growth",
            value=metrics.eps_growth,
            threshold=Decimal("10"),
            success_message="EPS growth is healthy.",
            failure_message="EPS growth is below threshold.",
        )

    @staticmethod
    def evaluate_fcf_growth(
        metrics: FinancialMetrics,
    ) -> ScreeningResult:

        return GrowthRules._evaluate(
            rule="Free Cash Flow Growth",
            value=metrics.free_cash_flow_growth,
            threshold=Decimal("10"),
            success_message="FCF growth is healthy.",
            failure_message="FCF growth is below threshold.",
        )

    @staticmethod
    def evaluate(
        metrics: FinancialMetrics,
    ) -> ScoreCard:

        results = [
            GrowthRules.evaluate_revenue_growth(metrics),
            GrowthRules.evaluate_eps_growth(metrics),
            GrowthRules.evaluate_fcf_growth(metrics),
        ]

        score = Decimal("0")

        for result in results:
            if result.passed:
                score += Decimal("10")

        max_score = Decimal("30")

        percentage = (
            score / max_score * Decimal("100")
            if max_score > 0
            else Decimal("0")
        )

        return ScoreCard(
            category="Growth",
            score=score,
            max_score=max_score,
            percentage=percentage,
            results=results,
        )
