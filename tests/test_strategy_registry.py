import pytest

from atlas.strategies.quality_strategy import QualityStrategy
from atlas.strategies.registry import StrategyRegistry


def test_registry_returns_quality():

    strategy = StrategyRegistry.create(
        "quality",
    )

    assert isinstance(
        strategy,
        QualityStrategy,
    )


def test_registry_lists_quality():

    assert "quality" in StrategyRegistry.available_strategies()


def test_unknown_strategy():

    with pytest.raises(ValueError):
        StrategyRegistry.create(
            "buffett",
        )
