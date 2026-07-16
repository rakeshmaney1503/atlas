from __future__ import annotations

from atlas.services.providers.market_data_provider import (
    CompanyProfile,
    MarketDataProvider,
)


class NSEProvider(MarketDataProvider):
    def provider_name(self) -> str:
        return "National Stock Exchange"

    def search_symbol(self, query: str) -> list[CompanyProfile]:
        raise NotImplementedError

    def get_company_profile(
        self,
        symbol: str,
    ) -> CompanyProfile | None:
        raise NotImplementedError

    def get_financial_statements(
        self,
        symbol: str,
    ) -> dict:
        raise NotImplementedError

    def get_ratios(
        self,
        symbol: str,
    ) -> dict:
        raise NotImplementedError

    def get_historical_prices(
        self,
        symbol: str,
        years: int = 10,
    ) -> dict:
        raise NotImplementedError
