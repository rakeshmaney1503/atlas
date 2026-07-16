from atlas.services.providers.alpha_vantage_provider import AlphaVantageProvider
from atlas.services.providers.factory import ProviderFactory
from atlas.services.providers.fmp_provider import FMPProvider
from atlas.services.providers.market_data_provider import MarketDataProvider
from atlas.services.providers.nse_provider import NSEProvider


def test_provider_factory_returns_fmp_provider() -> None:
    provider = ProviderFactory.create("fmp")

    assert isinstance(provider, FMPProvider)
    assert isinstance(provider, MarketDataProvider)


def test_provider_factory_returns_alpha_vantage_provider() -> None:
    provider = ProviderFactory.create("alpha_vantage")

    assert isinstance(provider, AlphaVantageProvider)
    assert isinstance(provider, MarketDataProvider)


def test_provider_factory_returns_nse_provider() -> None:
    provider = ProviderFactory.create("nse")

    assert isinstance(provider, NSEProvider)
    assert isinstance(provider, MarketDataProvider)


def test_provider_factory_rejects_unsupported_provider() -> None:
    try:
        ProviderFactory.create("unsupported_provider")
    except ValueError as exc:
        assert "Unsupported provider" in str(exc)
    else:
        raise AssertionError("Expected ValueError for unsupported provider")


def test_all_providers_inherit_from_market_data_provider() -> None:
    assert issubclass(FMPProvider, MarketDataProvider)
    assert issubclass(AlphaVantageProvider, MarketDataProvider)
    assert issubclass(NSEProvider, MarketDataProvider)
