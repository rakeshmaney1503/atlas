from __future__ import annotations

from decimal import Decimal

from atlas.schemas.financial_metrics import FinancialMetrics
from atlas.schemas.scorecard import ScoreCard
from atlas.schemas.screening_result import ScreeningResult


class ValuationRules:
    """
    Valuation screening rules.
    """

    MAX_SCORE = Decimal("50")

    @staticmethod
    def _evaluate(
        *,
        rule: str,
        value: Decimal,
        threshold: Decimal,
        higher_is_better: bool,
        success_message: str,
        failure_message: str,
    ) -> ScreeningResult:

        passed = (
            value >= threshold
            if higher_is_better
            else value <= threshold
        )

        return ScreeningResult(
            rule=rule,
            passed=passed,
            value=value,
            threshold=threshold,
            message=success_message if passed else failure_message,
        )

    @staticmethod
    def evaluate_pe_ratio(
        metrics: FinancialMetrics,
    ) -> ScreeningResult:

        return ValuationRules._evaluate(
            rule="Price to Earnings",
            value=metrics.pe_ratio,
            threshold=Decimal("25"),
            higher_is_better=False,
            success_message="PE is within preferred range.",
            failure_message="PE is above preferred range.",
        )

    @staticmethod
    def evaluate_pb_ratio(
        metrics: FinancialMetrics,
    ) -> ScreeningResult:

        return ValuationRules._evaluate(
            rule="Price to Book",
            value=metrics.pb_ratio,
            threshold=Decimal("5"),
            higher_is_better=False,
            success_message="PB is within preferred range.",
            failure_message="PB is above preferred range.",
        )

    @staticmethod
    def evaluate_peg_ratio(
        metrics: FinancialMetrics,
    ) -> ScreeningResult:

        return ValuationRules._evaluate(
            rule="PEG Ratio",
            value=metrics.peg_ratio,
            threshold=Decimal("1.5"),
            higher_is_better=False,
            success_message="PEG indicates reasonable valuation.",
            failure_message="PEG indicates expensive valuation.",
        )

    @staticmethod
    def evaluate_ev_ebitda(
        metrics: FinancialMetrics,
    ) -> ScreeningResult:

        return ValuationRules._evaluate(
            rule="EV / EBITDA",
            value=metrics.ev_ebitda,
            threshold=Decimal("15"),
            higher_is_better=False,
            success_message="EV/EBITDA is attractive.",
            failure_message="EV/EBITDA is expensive.",
        )

    @staticmethod
    def evaluate_price_to_sales(
        metrics: FinancialMetrics,
    ) -> ScreeningResult:

        return ValuationRules._evaluate(
            rule="Price / Sales",
            value=metrics.price_to_sales,
            threshold=Decimal("5"),
            higher_is_better=False,
            success_message="Price/Sales is attractive.",
            failure_message="Price/Sales is expensive.",
        )

    @staticmethod
    def evaluate(
        metrics: FinancialMetrics,
    ) -> ScoreCard:

        results = [
            ValuationRules.evaluate_pe_ratio(metrics),
            ValuationRules.evaluate_pb_ratio(metrics),
            ValuationRules.evaluate_peg_ratio(metrics),
            ValuationRules.evaluate_ev_ebitda(metrics),
            ValuationRules.evaluate_price_to_sales(metrics),
        ]

        score = Decimal("0")

        for result in results:
            if result.passed:
                score += Decimal("10")

        percentage = (
            score / ValuationRules.MAX_SCORE * Decimal("100")
        )

        return ScoreCard(
            category="Valuation",
            score=score,
            max_score=ValuationRules.MAX_SCORE,
            percentage=percentage,
            results=results,
        )
