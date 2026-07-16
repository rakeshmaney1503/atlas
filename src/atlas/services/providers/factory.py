from __future__ import annotations

from atlas.services.providers.alpha_vantage_provider import AlphaVantageProvider
from atlas.services.providers.fmp_provider import FMPProvider
from atlas.services.providers.market_data_provider import MarketDataProvider
from atlas.services.providers.nse_provider import NSEProvider


class ProviderFactory:
    _providers: dict[str, type[MarketDataProvider]] = {
        "fmp": FMPProvider,
        "alpha_vantage": AlphaVantageProvider,
        "nse": NSEProvider,
    }

    @staticmethod
    def create(provider_name: str) -> MarketDataProvider:
        if provider_name is None:
            raise ValueError("provider_name must be provided")

        normalized_name = provider_name.strip().lower()
        provider_class = ProviderFactory._providers.get(normalized_name)

        if provider_class is None:
            supported = ", ".join(sorted(ProviderFactory._providers.keys()))
            raise ValueError(
                f"Unsupported provider '{provider_name}'. Supported providers: {supported}"
            )

        return provider_class()
