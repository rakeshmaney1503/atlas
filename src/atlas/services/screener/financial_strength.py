from __future__ import annotations

from decimal import Decimal

from atlas.schemas.financial_metrics import FinancialMetrics
from atlas.schemas.screener import ScreeningResult


class FinancialStrengthRules:
    """
    Financial Strength screening rules.

    These rules evaluate the balance sheet and cash-flow quality
    of a company. Every passing rule contributes equally to the
    Financial Strength Score.
    """

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

        if higher_is_better:
            passed = value >= threshold
        else:
            passed = value <= threshold

        return ScreeningResult(
            rule=rule,
            passed=passed,
            value=value,
            threshold=threshold,
            message=success_message if passed else failure_message,
        )

    @staticmethod
    def evaluate_debt_to_equity(
        metrics: FinancialMetrics,
    ) -> ScreeningResult:

        return FinancialStrengthRules._evaluate(
            rule="Debt to Equity",
            value=metrics.debt_to_equity,
            threshold=Decimal("1.00"),
            higher_is_better=False,
            success_message="Debt level is acceptable.",
            failure_message="Debt level is higher than preferred.",
        )

    @staticmethod
    def evaluate_current_ratio(
        metrics: FinancialMetrics,
    ) -> ScreeningResult:

        return FinancialStrengthRules._evaluate(
            rule="Current Ratio",
            value=metrics.current_ratio,
            threshold=Decimal("1.50"),
            higher_is_better=True,
            success_message="Liquidity position is healthy.",
            failure_message="Current ratio is below preferred level.",
        )

    @staticmethod
    def evaluate_interest_coverage(
        metrics: FinancialMetrics,
    ) -> ScreeningResult:

        return FinancialStrengthRules._evaluate(
            rule="Interest Coverage",
            value=metrics.interest_coverage,
            threshold=Decimal("3.00"),
            higher_is_better=True,
            success_message="Interest obligations are comfortably covered.",
            failure_message="Interest coverage is weak.",
        )

    @staticmethod
    def evaluate_free_cash_flow(
        metrics: FinancialMetrics,
    ) -> ScreeningResult:

        return FinancialStrengthRules._evaluate(
            rule="Free Cash Flow",
            value=metrics.free_cash_flow,
            threshold=Decimal("0"),
            higher_is_better=True,
            success_message="Company generates positive free cash flow.",
            failure_message="Company generates negative free cash flow.",
        )

    @staticmethod
    def evaluate_operating_cash_flow(
        metrics: FinancialMetrics,
    ) -> ScreeningResult:

        return FinancialStrengthRules._evaluate(
            rule="Operating Cash Flow",
            value=metrics.operating_cash_flow,
            threshold=Decimal("0"),
            higher_is_better=True,
            success_message="Operating cash flow is positive.",
            failure_message="Operating cash flow is negative.",
        )

    @staticmethod
    def calculate_score(
        metrics: FinancialMetrics,
    ) -> tuple[Decimal, list[ScreeningResult]]:

        results = [
            FinancialStrengthRules.evaluate_debt_to_equity(metrics),
            FinancialStrengthRules.evaluate_current_ratio(metrics),
            FinancialStrengthRules.evaluate_interest_coverage(metrics),
            FinancialStrengthRules.evaluate_free_cash_flow(metrics),
            FinancialStrengthRules.evaluate_operating_cash_flow(metrics),
        ]

        score = Decimal("0")

        for result in results:
            if result.passed:
                score += Decimal("10")

        return score, results
