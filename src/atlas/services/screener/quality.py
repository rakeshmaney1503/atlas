from __future__ import annotations

from decimal import Decimal

from atlas.schemas.financial_metrics import FinancialMetrics
from atlas.schemas.scorecard import ScoreCard
from atlas.schemas.screening_result import ScreeningResult

class QualityRules:
    """
    Quality-related screening rules.

    Each rule is deterministic and independent.
    """

    MAX_SCORE = Decimal("30")

    @staticmethod
    def _evaluate_threshold(
        *,
        rule: str,
        value: Decimal,
        threshold: Decimal,
        higher_is_better: bool,
        success_message: str,
        failure_message: str,
    ) -> ScreeningResult:

        passed = value >= threshold if higher_is_better else value <= threshold

        return ScreeningResult(
            rule=rule,
            passed=passed,
            value=value,
            threshold=threshold,
            message=success_message if passed else failure_message,
        )

    @staticmethod
    def evaluate_roe(
        metrics: FinancialMetrics,
    ) -> ScreeningResult:

        return QualityRules._evaluate_threshold(
            rule="Return on Equity",
            value=metrics.roe,
            threshold=Decimal("15"),
            higher_is_better=True,
            success_message="ROE meets Atlas quality threshold.",
            failure_message="ROE below preferred threshold.",
        )

    @staticmethod
    def evaluate_roce(
        metrics: FinancialMetrics,
    ) -> ScreeningResult:

        return QualityRules._evaluate_threshold(
            rule="Return on Capital Employed",
            value=metrics.roce,
            threshold=Decimal("15"),
            higher_is_better=True,
            success_message="ROCE meets Atlas quality threshold.",
            failure_message="ROCE below preferred threshold.",
        )

    @staticmethod
    def evaluate_roa(
        metrics: FinancialMetrics,
    ) -> ScreeningResult:

        return QualityRules._evaluate_threshold(
            rule="Return on Assets",
            value=metrics.roa,
            threshold=Decimal("8"),
            higher_is_better=True,
            success_message="ROA is healthy.",
            failure_message="ROA is below Atlas threshold.",
        )

    @staticmethod
    def evaluate(
        metrics: FinancialMetrics,
    ) -> ScoreCard:

        results = [
            QualityRules.evaluate_roe(metrics),
            QualityRules.evaluate_roce(metrics),
            QualityRules.evaluate_roa(metrics),
        ]

        score = Decimal("0")

        for result in results:
            if result.passed:
                score += Decimal("10")

        percentage = Decimal("0")

        if QualityRules.MAX_SCORE > Decimal("0"):
            percentage = (
                score
                / QualityRules.MAX_SCORE
                * Decimal("100")
            )

        return ScoreCard(
            category="Quality",
            score=score,
            max_score=QualityRules.MAX_SCORE,
            percentage=percentage,
            results=results,
        )

    @staticmethod
    def calculate_score(
        metrics: FinancialMetrics,
    ) -> tuple[Decimal, list[ScreeningResult]]:
        """
        Legacy API.

        This exists temporarily so that existing code and tests
        continue to work while the rest of the screener is migrated
        to ScoreCard.
        """

        card = QualityRules.evaluate(metrics)

        return (
            card.score,
            card.results,
        )
