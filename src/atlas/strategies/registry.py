from atlas.strategies.base import InvestmentStrategy
from atlas.strategies.quality_strategy import QualityStrategy


class StrategyRegistry:
    """
    Registry of all available investment strategies.
    """

    _strategies: dict[str, type[InvestmentStrategy]] = {
        "quality": QualityStrategy,
    }

    @classmethod
    def create(
        cls,
        name: str,
    ) -> InvestmentStrategy:

        strategy = cls._strategies.get(
            name.lower(),
        )

        if strategy is None:
            supported = ", ".join(
                sorted(cls._strategies.keys())
            )
            raise ValueError(
                f"Unknown strategy '{name}'. Supported: {supported}"
            )

        return strategy()

    @classmethod
    def available_strategies(
        cls,
    ) -> list[str]:
        return sorted(cls._strategies.keys())
